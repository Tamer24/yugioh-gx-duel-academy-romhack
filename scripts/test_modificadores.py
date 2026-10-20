"""Prueba con Unicorn de los modificadores de ATK de Goddess of Whim y Riryoku
(efectos/goddess_whim.s, efectos/riryoku.s, efectos/modificador_atk.s).

Usa un volcado de RAM de un duelo con Goddess en el campo (volcar_ram.py). Simula el evento
0x4B (FUN_0800E9B8) y comprueba el ATK que calcula el motor (FUN_08012460).

Uso: python3 test_modificadores.py rom.gba prefijo_volcado       (pip install unicorn)
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                               UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC)

from da_lib import *

J = 0x02022250
EVENTO, CONSUMIDOR, CALCULADOR = 0x0801A5BC, 0x0800E9B8, 0x08012460
ASK, AZAR = 0x08009744, 0x080E5740
SALIDA = 0x0203F000


def nuevo(rom, prefijo):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    e = open(prefijo + ".ewram", "rb").read()
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_write(0x02000000, e)
    uc.mem_map(0x03000000, 0x8000)
    uc.mem_write(0x03000000, open(prefijo + ".iwram", "rb").read())
    uc.mem_map(0x04000000, 0x1000)
    base32 = e[J - 0x02000000 + 32 * 0x50: J - 0x02000000 + 33 * 0x50]
    uc.mem_write(J + 8 * 0x50, base32)                       # ranura 8 = copia de la 32
    uc.mem_write(J + 8 * 0x50 + 0x24, struct.pack("<H", 979))   # indice 979 = Sand Gambler, ATK 300
    uc.mem_write(J + 0x5610, bytes([32, 8] + [0xFF] * 9))   # zonas de monstruo del lado 0
    uc.mem_write(J + 38 * 0x50 + 0x24, struct.pack("<H", rom.indice_de(5009)))  # ranura 38 = Riryoku
    return uc


def llamar(uc, direccion, *args):
    for i, a in enumerate(args):
        uc.reg_write((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)[i], a)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F01)
    uc.emu_start(direccion | 1, 0x03007F00, count=400000)
    return uc.reg_read(UC_ARM_REG_R0)


def atk(uc, ranura):
    uc.mem_write(SALIDA, bytes(32))
    llamar(uc, CALCULADOR, ranura, SALIDA, 3)
    return struct.unpack_from("<I", uc.mem_read(SALIDA + 4, 4))[0]


def con_eventos(uc, fn, p):
    ev = []

    def gancho(u, dir_, tam, _):
        if dir_ == EVENTO:
            ev.append(tuple(u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    h = uc.hook_add(UC_HOOK_CODE, gancho)
    llamar(uc, fn, p)
    uc.hook_del(h)
    for lado, origen, destino, tipo in ev:
        llamar(uc, CONSUMIDOR, lado, tipo, origen, destino)
    return ev


def main():
    rom = Rom(sys.argv[1])
    prefijo = sys.argv[2]
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = lambda cid: rom.u32(rom.efectos_base + EFECTOS_FILA * filas[cid] + 4) & ~1
    ok = True

    def chequear(nombre, obtenido, esperado):
        nonlocal ok
        bien = obtenido == esperado
        ok = ok and bien
        print(f"{'OK ' if bien else 'MAL'} {nombre}: {obtenido} (esperado {esperado})")

    p = 0x0203E000
    # Goddess acerto / erro (estado 0x7D, p[10] = acerto)
    for acerto, esperado in ((1, 1900), (0, 475)):
        uc = nuevo(rom, prefijo)
        uc.mem_write(0x020204C6, bytes([0x7D]))
        raw = bytearray(16)
        raw[0:2] = struct.pack("<H", 32 << 1)
        raw[10] = acerto
        uc.mem_write(p, bytes(raw))
        con_eventos(uc, fn(4435), p)
        chequear(f"Goddess {'acierta' if acerto else 'erra'}: ATK de la ranura 32", atk(uc, 32), esperado)
    # Goddess, estado 0x7F: p[10] = resultado de la moneda del menu (J + 0x5656), sin tirar otra
    for resultado, texto in ((1, b"You called it right"), (0, b"You called it wrong")):
        uc = nuevo(rom, prefijo)
        uc.mem_write(0x020204C6, bytes([0x7F]))
        uc.mem_write(J + 0x5656, bytes([resultado]))
        raw = bytearray(16)
        raw[0:2] = struct.pack("<H", 32 << 1)
        raw[10] = 1 - resultado
        uc.mem_write(p, bytes(raw))
        avisos, azar = [], []

        def gancho(u, dir_, tam, _):
            if dir_ in (ASK, AZAR):
                (avisos if dir_ == ASK else azar).append(u.reg_read(UC_ARM_REG_R0))
                u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

        h = uc.hook_add(UC_HOOK_CODE, gancho)
        ret = llamar(uc, fn(4435), p)
        uc.hook_del(h)
        dice = bytes(uc.mem_read(avisos[0], 19)) if avisos else b""
        chequear(f"Goddess 0x7F con moneda {resultado}: (estado, p[10], aviso, tiradas propias)",
                 (ret, uc.mem_read(p + 10, 1)[0], dice, len(azar)), (0x7D, resultado, texto, 0))
    # Riryoku: pierde la 32 (950 -> 475), gana la 8 (300 + 475)
    for pierde, gana, e32, e8 in ((32, 8, 475, 775), (8, 32, 1100, 150)):
        uc = nuevo(rom, prefijo)
        raw = bytearray(16)
        raw[0:2] = struct.pack("<H", 38 << 1)
        raw[8], raw[9], raw[10] = 2, pierde, gana
        uc.mem_write(p, bytes(raw))
        con_eventos(uc, fn(5009), p)
        chequear(f"Riryoku pierde {pierde}: ranura 32", atk(uc, 32), e32)
        chequear(f"Riryoku pierde {pierde}: ranura 8", atk(uc, 8), e8)
    # sin las dos elecciones no hace nada
    uc = nuevo(rom, prefijo)
    raw = bytearray(16)
    raw[0:2] = struct.pack("<H", 38 << 1)
    raw[8], raw[9], raw[10] = 1, 32, 8
    uc.mem_write(p, bytes(raw))
    chequear("Riryoku con 1 elegido: eventos", con_eventos(uc, fn(5009), p), [])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
