"""Prueba con Unicorn de efectos/two_pronged_attack.s (fn_04 de Two-Pronged Attack, ID 4839).

Con las tres elecciones hechas (p[8] & 0xF = 3; p[9], p[10] propias y distintas; p[11] del
rival) debe mandar las tres al cementerio con FUN_08018518(lado, id, ranura propia). En
cualquier otro caso no debe destruir nada. Siempre devuelve 0.

Uso: python3 test_two_pronged.py rom.gba            (pip install unicorn)
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                               UC_ARM_REG_LR, UC_ARM_REG_SP, UC_ARM_REG_PC)

from da_lib import *

CEMENTERIO = 0x08018518
RANURA = 38                    # ranura de la propia Two-Pronged Attack


def correr(rom, elegidas=(0x05, 0x06, 0x9A), cantidad=3, lado=0, anulada=False):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    carta = 0x02010000
    p = bytearray(16)
    struct.pack_into("<H", p, 0, (RANURA << 1) | lado)
    p[2] = 8 if anulada else 0
    p[8] = cantidad
    p[9:12] = bytes(elegidas)
    uc.mem_write(carta, bytes(p))
    cem = []

    def gancho(u, dir_, tam, _):
        if dir_ == CEMENTERIO:
            cem.append(tuple(u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(EFECTOS + EFECTOS_FILA * filas[4839] + 4)
    uc.reg_write(UC_ARM_REG_R0, carta)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
    uc.emu_start(fn, 0x03007F00, count=50000)
    return cem, uc.reg_read(UC_ARM_REG_R0)


def main():
    rom = Rom(sys.argv[1])
    tres = lambda lado, ids: [(lado, i, RANURA) for i in ids]
    casos = [
        ("jugador: 2 propias y 1 del rival", dict(), tres(0, (0x05, 0x06, 0x9A))),
        ("la activa el rival (lado 1)", dict(lado=1, elegidas=(0x85, 0x86, 0x1A)), tres(1, (0x85, 0x86, 0x1A))),
        ("cantidad con bits altos (0x13)", dict(cantidad=0x13), tres(0, (0x05, 0x06, 0x9A))),
        ("solo 2 elegidas", dict(cantidad=2), []),
        ("las dos propias son la misma", dict(elegidas=(0x05, 0x05, 0x9A)), []),
        ("la primera es del rival", dict(elegidas=(0x85, 0x06, 0x9A)), []),
        ("la segunda es del rival", dict(elegidas=(0x05, 0x86, 0x9A)), []),
        ("la tercera es propia", dict(elegidas=(0x05, 0x06, 0x1A)), []),
        ("una eleccion vacia (0xFF)", dict(elegidas=(0x05, 0x06, 0xFF)), []),
        ("carta anulada", dict(anulada=True), []),
    ]
    ok = True
    for nombre, kw, esperado in casos:
        cem, ret = correr(rom, **kw)
        bien = cem == esperado and ret == 0
        print(f"{'OK ' if bien else 'MAL'} {nombre}: cementerio={cem} devuelve={ret:#x}")
        ok = ok and bien
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
