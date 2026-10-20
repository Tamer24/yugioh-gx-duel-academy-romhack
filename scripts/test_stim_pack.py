"""Prueba con Unicorn del gancho de Stim-Pack (efectos/gancho_cambio_turno.s, en FUN_0801D7DC).

Ejecuta, desde la direccion del gancho (0x0801D7DC) hasta 0x0801D7E4 (donde sigue la funcion
original), con la memoria del duelo armada a mano, y comprueba que:
  - suma 1 al contador (+0x3A) de cada Stim-Pack boca arriba en la zona de Magicas y Trampas del
    jugador que empieza turno (el que no es el del bit 15 de 0x020214E0);
  - no toca los Stim-Pack del jugador cuyo turno termina, ni uno boca abajo, ni uno en el
    cementerio, ni otras cartas con su +0x3A;
  - no pasa de 255;
  - deja r4-r7 como estaban y, en la pila, lo que dejaria el push original.
El contador lo usa el calculador de ATK del motor: 700 - 200 x contador.

Uso: python3 scripts/test_stim_pack.py ROM
"""
import struct
import sys

from unicorn import UC_ARCH_ARM, UC_MODE_THUMB, Uc
from unicorn.arm_const import (UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R8, UC_ARM_REG_PC, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
                               UC_ARM_REG_R7, UC_ARM_REG_SP)

from da_lib import BASE, Rom

J, LADO, TURNO = 0x02022250, 0x2B08, 0x020214E0
GANCHO, SIGUE = 0x0801D7DC, 0x0801D7E4
STIM = 4890


def ranura(lado, n):
    return J + lado * LADO + n * 0x50


def correr(rom, turno, cartas):
    """cartas: [(lado, n, indice, zona, posicion, contador)]. Devuelve {(lado, n): contador} y la maquina."""
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    uc.mem_write(TURNO, struct.pack("<H", turno << 15))
    for lado, n, indice, zona, pos, cont in cartas:
        a = ranura(lado, n)
        uc.mem_write(a + 0x24, struct.pack("<H", indice))
        uc.mem_write(a + 0x31, bytes([zona << 4]))
        uc.mem_write(a + 0x33, bytes([pos]))
        uc.mem_write(a + 0x3A, bytes([cont]))
    for reg, v in ((UC_ARM_REG_R4, 0x44), (UC_ARM_REG_R5, 0x55), (UC_ARM_REG_R6, 0x66), (UC_ARM_REG_R7, 0x77), (UC_ARM_REG_R8, 0x88)):
        uc.reg_write(reg, v)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x08001235)
    uc.emu_start(GANCHO | 1, SIGUE, count=200000)
    assert uc.reg_read(UC_ARM_REG_PC) == SIGUE, hex(uc.reg_read(UC_ARM_REG_PC))
    sp = uc.reg_read(UC_ARM_REG_SP)
    pila = struct.unpack("<5I", uc.mem_read(sp, 20))
    assert sp == 0x03007E00 - 20 and pila == (0x44, 0x55, 0x66, 0x77, 0x08001235), (hex(sp), pila)
    assert (uc.reg_read(UC_ARM_REG_R7), uc.reg_read(UC_ARM_REG_R5)) == (0, 0x88)   # mov r7, sl ; mov r5, r8
    res = {(lado, n): uc.mem_read(ranura(lado, n) + 0x3A, 1)[0] for lado, n, *_ in cartas}
    return res


def main(ruta):
    rom = Rom(ruta)
    stim = rom.indice_de(STIM)
    otra = 1 if stim != 1 else 2                  # una carta que no es Stim-Pack
    assert stim, "Stim-Pack no esta en el ROM"
    fallas = 0
    casos = [
        # termina el turno de 0: suma a los de 1
        (0, [(1, 3, stim, 5, 0x10, 0), (1, 4, stim, 5, 0x10, 2), (0, 3, stim, 5, 0x10, 0),
             (1, 5, stim, 5, 0x20, 0), (1, 6, stim, 0xD, 0x10, 0), (1, 7, otra, 5, 0x10, 0),
             (1, 8, stim, 5, 0x10, 255)],
         {(1, 3): 1, (1, 4): 3, (0, 3): 0, (1, 5): 0, (1, 6): 0, (1, 7): 0, (1, 8): 255}),
        # termina el turno de 1: suma a los de 0
        (1, [(0, 0, stim, 5, 0x10, 0), (1, 0, stim, 5, 0x10, 0), (0, 99, stim, 5, 0x10, 4)],
         {(0, 0): 1, (1, 0): 0, (0, 99): 5}),
        # sin cartas
        (0, [], {}),
    ]
    for turno, cartas, esperado in casos:
        visto = correr(rom, turno, cartas)
        ok = visto == esperado
        fallas += not ok
        print(("  ok   " if ok else "  FALLA"), f"termina el turno de {turno}: {visto}" + ("" if ok else f" esperado {esperado}"))
    print("RESULTADO:", "FUNCIONA" if not fallas else f"{fallas} FALLAS")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
