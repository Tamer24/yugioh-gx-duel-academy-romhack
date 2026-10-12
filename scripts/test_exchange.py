"""Prueba con Unicorn de la rama de la IA de Exchange (efectos/exchange.s).

El rival (lado 1) activa Exchange en el estado 0x80: elige al azar una carta de la mano
del jugador y le da otra al azar de la suya. El azar se fija para comprobar el resultado.

Uso: python3 test_exchange.py rom.gba            (pip install unicorn)
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_LR, UC_ARM_REG_SP, UC_ARM_REG_PC

from da_lib import *

J0, L = 0x02022250, 0x2B08


def correr(rom, azar, mano_jug, mano_ia, estado=0x80, lado=1, anulada=0):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    ranuras = {}
    for lado_m, mano in ((0, mano_jug), (1, mano_ia)):
        n = len(mano)
        b = J0 + lado_m * L
        uc.mem_write(b + 0x1B, bytes([(n & 1) << 7, n >> 1]))
        for k, (slot, indice) in enumerate(mano):
            uc.mem_write(b + 0x2824 + k, bytes([slot | (lado_m << 7)]))
            a = J0 + slot * 0x50 + lado_m * L
            uc.mem_write(a + 0x24, struct.pack("<H", indice))
            uc.mem_write(a + 0x30, bytes([0xAA, 0xF2, 0x08 * lado_m, 0]))
            ranuras[(lado_m, slot)] = a
    uc.mem_write(0x020204C6, bytes([estado]))
    carta = 0x02010000
    uc.mem_write(carta, bytes([lado, 0, anulada, 0] + [0] * 12))
    cuenta = {"n": 0}

    def gancho(u, dir_, tam, _):
        if dir_ == 0x080E5740:                       # AZAR: valores fijos y consecutivos
            u.reg_write(UC_ARM_REG_R0, azar[min(cuenta["n"], len(azar) - 1)])
            cuenta["n"] += 1
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(EFECTOS + EFECTOS_FILA * filas[5218] + 4)
    uc.reg_write(UC_ARM_REG_R0, carta)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
    uc.emu_start(fn, 0x03007F00, count=50000)
    ret = uc.reg_read(UC_ARM_REG_R0)
    info = {k: (struct.unpack("<H", uc.mem_read(a + 0x24, 2))[0], uc.mem_read(a + 0x32, 1)[0] & 8)
            for k, a in ranuras.items()}
    return ret, info


def main():
    rom = Rom(sys.argv[1])
    fallos = 0

    def comprobar(nombre, cond, detalle=""):
        nonlocal fallos
        print(("  ok  " if cond else "  FALLA"), nombre, detalle)
        fallos += 0 if cond else 1

    jug = [(0x0B, 318), (0x08, 251), (0x20, 892)]
    ia = [(0x06, 448), (0x0B, 819)]
    print("1. la IA activa Exchange en 0x80 (azar: 1 y 0)")
    r, info = correr(rom, [1, 0], jug, ia)
    # azar 1 -> 2a carta del jugador (ranura 0x08, indice 251); azar 0 -> 1a carta de la IA (ranura 6, indice 448)
    comprobar("devuelve 0x64", r == 0x64, f"(r0={r:#x})")
    comprobar("la ranura 8 del jugador pasa a tener la carta de la IA (448, dueno 0)", info[(0, 0x08)] == (448, 0), str(info[(0, 8)]))
    comprobar("la ranura 6 de la IA pasa a tener la del jugador (251, dueno 1)", info[(1, 0x06)] == (251, 8), str(info[(1, 6)]))
    comprobar("las demas ranuras no cambian", info[(0, 0x0B)] == (318, 0) and info[(0, 0x20)] == (892, 0) and info[(1, 0x0B)] == (819, 8))

    print("2. carta anulada")
    r, info = correr(rom, [1, 0], jug, ia, anulada=8)
    comprobar("no cambia nada", info[(0, 0x08)] == (251, 0) and r == 0)

    print("3. la IA sin cartas en la mano")
    r, info = correr(rom, [0, 0], jug, [])
    comprobar("devuelve 0 y no cambia nada", r == 0 and info[(0, 0x0B)] == (318, 0))

    print("4. el jugador sin cartas en la mano")
    r, info = correr(rom, [0, 0], [], ia)
    comprobar("devuelve 0", r == 0)

    print("\\nFALLARON" if fallos else "\\ntodo en orden", fallos or "")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
