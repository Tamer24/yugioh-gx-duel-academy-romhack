"""Prueba con Unicorn de efectos/share_the_pain.s (fn_04 de Share the Pain, ID 4889).

El jugador (lado 0) activa la carta: el rival debe perder su monstruo de menor ATK
(FUN_08018518(0, id, ranura propia)). Si la activa la IA se delega en el original.

Uso: python3 test_share.py rom.gba            (pip install unicorn)
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                               UC_ARM_REG_LR, UC_ARM_REG_SP, UC_ARM_REG_PC)

from da_lib import *

J0, L = 0x02022250, 0x2B08
CEMENTERIO, ELEGIBLES, ORIGINAL = 0x08018518, 0x08010FA4, 0x0803F0D4


def correr(rom, rival=((26, 1000), (27, 1600)), lado=0, elegibles=1, estado=0x80):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    lista = J0 + 0x5610 + 11
    uc.mem_write(lista, bytes([0xFF] * 11))
    for k, (slot, atk) in enumerate(rival):
        uc.mem_write(lista + k, bytes([0x80 | slot]))
        uc.mem_write(J0 + L + slot * 0x50 + 0x28, struct.pack("<H", atk))
    uc.mem_write(0x020204C6, bytes([estado]))
    carta = 0x02010000
    uc.mem_write(carta, struct.pack("<H", (38 << 1) | lado) + bytes([0, 0] + [0] * 12))
    ev = {"cem": [], "orig": False}

    def gancho(u, dir_, tam, _):
        if dir_ == CEMENTERIO:
            ev["cem"].append(tuple(u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif dir_ == ELEGIBLES:
            u.reg_write(UC_ARM_REG_R0, elegibles)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif dir_ == ORIGINAL:
            ev["orig"] = True
            u.reg_write(UC_ARM_REG_R0, 0x1234)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(rom.efectos_base + EFECTOS_FILA * filas[4889] + 4)
    uc.reg_write(UC_ARM_REG_R0, carta)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
    uc.emu_start(fn, 0x03007F00, count=50000)
    return ev, uc.reg_read(UC_ARM_REG_R0)


def main():
    rom = Rom(sys.argv[1])
    casos = [
        ("jugador activa: pierde el de menor ATK", dict(), ([(0, 0x9A, 38)], False)),
        ("el de menor ATK es el 2.o", dict(rival=((26, 2000), (27, 500))), ([(0, 0x9B, 38)], False)),
        ("rival sin monstruos", dict(rival=()), ([], False)),
        ("rival sin monstruos tributables", dict(elegibles=0), ([], False)),
        ("la activa la IA: original", dict(lado=1), ([], True)),
        ("otro estado: original", dict(estado=0x7F), ([], True)),
    ]
    ok = True
    for nombre, kw, (cem, orig) in casos:
        ev, ret = correr(rom, **kw)
        bien = ev["cem"] == cem and ev["orig"] == orig
        print(f"{'OK ' if bien else 'MAL'} {nombre}: cementerio={ev['cem']} original={ev['orig']}")
        ok = ok and bien
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
