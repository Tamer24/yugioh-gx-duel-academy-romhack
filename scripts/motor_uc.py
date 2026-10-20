"""Arnes de Unicorn para probar piezas de efectos/ sin el juego.

Carga el ROM, deja la memoria del duelo en cero y reemplaza las funciones del motor que las piezas
llaman (todas las de parches.MOTOR, mas las que se agreguen) por registradores: anotan
(nombre, r0, r1, r2, r3) y vuelven con el valor pedido. Asi una prueba arma el campo a mano, llama
a la pieza y compara los llamados con lo que dice el texto de la carta.

Uso desde una prueba:
    m = Motor(rom)
    m.carta(0, 3, indice, zona=0, pos=0x10, atk=1000)
    m.zonas_monstruo(0, [3])
    r0 = m.fn_estados(m.fila(6769)["fn_04"], m.entrada(0, 3))
    m.llamadas -> [("GANAR_LP", 0, 1500, ...), ...]
"""
import struct

from unicorn import UC_ARCH_ARM, UC_HOOK_CODE, UC_MODE_THUMB, Uc
from unicorn.arm_const import (UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                               UC_ARM_REG_R3, UC_ARM_REG_SP)

import parches
from da_lib import BASE, EFECTOS_FILA

J0, LADO = 0x02022250, 0x2B08
ESTADO = 0x020204C6               # byte de estado de la resolucion
ELEGIDA = 0x02019F24              # eleccion de la lista: id de ranura en los bits 11-18
ZONAS = J0 + 0x5610               # listas de zonas: 11 por lado, las 5 primeras son monstruos
ENTRADA = 0x02010000              # donde se arma la entrada p
VUELTA = 0x03007F00
PILA = 0x03007E00


class Motor:
    def __init__(self, rom, falsas=None):
        self.rom = rom
        self.uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
        self.uc.mem_map(BASE, 0x2000000)
        self.uc.mem_write(BASE, bytes(rom.d))
        self.uc.mem_map(0x02000000, 0x40000)
        self.uc.mem_map(0x03000000, 0x8000)
        for lado in (0, 1):
            self.uc.mem_write(ZONAS + 11 * lado, b"\xff" * 11)
        self.llamadas = []
        self.falsas = {d & ~1: (n, 0) for n, d in parches.MOTOR.items()}
        self.falsas.update({d & ~1: v for d, v in (falsas or {}).items()})
        self.uc.hook_add(UC_HOOK_CODE, self._gancho)

    def _gancho(self, uc, dir_, tam, _):
        if dir_ in self.falsas:
            nombre, ret = self.falsas[dir_]
            args = tuple(uc.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3))
            self.llamadas.append((nombre,) + args)
            valor = ret(self, args) if callable(ret) else ret
            uc.reg_write(UC_ARM_REG_R0, valor & 0xFFFFFFFF)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    # --- el campo -------------------------------------------------------------
    @staticmethod
    def ranura(lado, n):
        return J0 + lado * LADO + n * 0x50

    def carta(self, lado, n, indice, zona=0, pos=0x10, atk=0, banderas=0):
        a = self.ranura(lado, n)
        self.uc.mem_write(a + 0x24, struct.pack("<H", indice))
        self.uc.mem_write(a + 0x28, struct.pack("<I", atk))
        self.uc.mem_write(a + 0x31, bytes([zona << 4]))
        self.uc.mem_write(a + 0x33, bytes([pos]))
        self.uc.mem_write(a + 0x60, struct.pack("<I", banderas))
        return (lado << 7) | n

    def zonas_monstruo(self, lado, ns):
        ids = [(lado << 7) | n for n in ns]
        self.uc.mem_write(ZONAS + 11 * lado, bytes(ids + [0xFF] * (5 - len(ids))))

    def mano(self, lado, ns):
        """La mano: lista de ids en +0x2824 y la cantidad en los bits 7-13 de u16(+0x1B)."""
        base = J0 + lado * LADO
        ids = [(lado << 7) | n for n in ns]
        self.uc.mem_write(base + 0x2824, bytes(ids + [0xFF] * (0x40 - len(ids))))
        b1b, b1c = self.uc.mem_read(base + 0x1B, 2)
        n = len(ids)
        self.uc.mem_write(base + 0x1B, bytes([(b1b & 0x7F) | (n & 1) << 7, (b1c & 0xC0) | (n >> 1)]))

    def leer_indice(self, lado, n):
        return struct.unpack("<H", self.uc.mem_read(self.ranura(lado, n) + 0x24, 2))[0]

    # --- llamar a una pieza ------------------------------------------------------
    def fila(self, id_konami):
        for k in range(self.rom.efectos_n):
            f = self.rom.fila_efecto(k)
            if f["id"] == id_konami:
                return f
        raise KeyError(id_konami)

    def entrada(self, lado, n, anulada=False, cabecera=0):
        """p: u32 de cabecera con el lado en el bit 0 y el id de ranura en los bits 1-8 (mas
        'cabecera', p. ej. tipo y momento del disparo), y la bandera anulada en el bit 3 de p[2]."""
        idr = (lado << 7) | n
        cab = (cabecera & ~0x1FF) | (idr << 1) | lado
        if anulada:
            cab |= 8 << 16
        self.uc.mem_write(ENTRADA, struct.pack("<I", cab) + bytes(12))
        return ENTRADA

    def elegir(self, idr):
        self.uc.mem_write(ELEGIDA, struct.pack("<I", (idr & 0xFF) << 11))

    def llamar(self, dir_, r0=0, r1=0, r2=0, r3=0, maximo=500000):
        uc = self.uc
        for reg, v in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), (r0, r1, r2, r3)):
            uc.reg_write(reg, v)
        uc.reg_write(UC_ARM_REG_SP, PILA)
        uc.reg_write(UC_ARM_REG_LR, VUELTA | 1)
        uc.emu_start(dir_ | 1, VUELTA, count=maximo)
        return uc.reg_read(UC_ARM_REG_R0)

    def fn_estado(self, dir_, p, estado):
        """Una llamada de la fn con el byte de estado dado. Devuelve el estado siguiente (r0)."""
        self.uc.mem_write(ESTADO, bytes([estado]))
        return self.llamar(dir_, p) & 0xFF

    def nombres(self):
        return [c[0] for c in self.llamadas]
