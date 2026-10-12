"""Prueba con Unicorn la funcion nueva de The Inexperienced Spy (efectos/spy_mano.s).

Se llama a la fila de efecto del ROM (columna fn_04) con un duelo armado a mano y
las funciones del motor reemplazadas por espias. No sustituye jugar la carta.

Uso: python3 test_spy.py rom.gba            (pip install unicorn)
"""
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                               UC_ARM_REG_LR, UC_ARM_REG_SP, UC_ARM_REG_PC)

from da_lib import *

ID_SPY = 4848
BASE_DUELO, LADO = 0x02022250, 0x2B08
ESTADO = 0x020204C6
CARTA = 0x02010000
ESPIAS = {0x0800B89C: "clear_zone", 0x0800B640: "registrar", 0x080875F4: "dialogo", 0x08009094: "bloqueo"}
RETORNO = 0x03007F00


def correr(rom, estado=0x80, mano=(), propio=0, flags=0, bloqueo=0):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    rival = 1 - propio
    n = len(mano)
    est = BASE_DUELO + rival * LADO
    uc.mem_write(est + 0x1B, bytes([(n & 1) << 7, n >> 1]))
    uc.mem_write(est + 0x2824, bytes(mano) + bytes(11 - n))
    uc.mem_write(ESTADO, bytes([estado]))
    uc.mem_write(CARTA, bytes([propio, 0, flags, 0, 0, 0, 0, 0, 0, 0]))
    uc.mem_write(0x02019F1F, b"\xff")
    uc.mem_write(0x02019F20, b"\xff")
    uc.mem_write(0x02019F00, b"\xff")
    llamadas = []

    def gancho(u, dir_, tam, _):
        if dir_ in ESPIAS:
            llamadas.append((ESPIAS[dir_], u.reg_read(UC_ARM_REG_R0), u.reg_read(UC_ARM_REG_R1),
                             u.reg_read(UC_ARM_REG_R2), u.reg_read(UC_ARM_REG_R3)))
            u.reg_write(UC_ARM_REG_R0, bloqueo if ESPIAS[dir_] == "bloqueo" else 0)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(EFECTOS + EFECTOS_FILA * filas[ID_SPY] + 4)
    uc.reg_write(UC_ARM_REG_R0, CARTA)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, RETORNO | 1)
    uc.emu_start(fn, RETORNO, count=50000)
    post = tuple(uc.mem_read(a, 1)[0] for a in (0x02019F1F, 0x02019F20, 0x02019F00))
    return uc.reg_read(UC_ARM_REG_R0), llamadas, post


def main():
    rom = Rom(sys.argv[1])
    fallos = 0

    def comprobar(nombre, cond, detalle=""):
        nonlocal fallos
        print(("  ok  " if cond else "  FALLA"), nombre, detalle)
        fallos += 0 if cond else 1

    mano = (0x11, 0x22, 0x33, 0x44, 0x55)
    print("1. estado 0x80, rival con 5 cartas en mano")
    r, ll, post = correr(rom, 0x80, mano)
    reg = [x for x in ll if x[0] == "registrar"]
    dia = [x for x in ll if x[0] == "dialogo"]
    comprobar("devuelve 10", r == 10, f"(r0={r})")
    comprobar("registra las 5 cartas de la mano, en orden", [x[1] for x in reg] == list(mano))
    comprobar("vacia la zona 6 antes", ll[1] == ("clear_zone", 6, 0, ll[1][3], ll[1][4]) if len(ll) > 1 else False)
    comprobar("abre el dialogo con (0, 5, 0x02019F24, 0)", dia and dia[0][1:] == (0, 5, 0x02019F24, 0), str(dia))
    comprobar("ajusta los tres bytes como Telescope", post == (0x3F, 0xFC, 0xF2), str(tuple(hex(x) for x in post)))

    print("2. estado 0x80, mano vacia")
    r, ll, post = correr(rom, 0x80, ())
    comprobar("devuelve 0 y no registra nada", r == 0 and not [x for x in ll if x[0] in ("registrar", "dialogo")])

    print("3. otros estados: no hace nada (si devolviera 0x80 el motor reabriria la lista al cerrarla)")
    for estado in (0x7F, 0x0A, 0x00):
        r, ll, post = correr(rom, estado, mano)
        comprobar(f"estado {estado:#04x}: devuelve 0 sin mostrar nada",
                  r == 0 and not [x for x in ll if x[0] in ("registrar", "dialogo")], f"(r0={r:#x})")

    print("4. carta anulada (flag 8)")
    r, ll, post = correr(rom, 0x80, mano, flags=8)
    comprobar("devuelve 0", r == 0 and not [x for x in ll if x[0] in ("registrar", "dialogo")])

    print("5. el otro lado (el jugador es el rival)")
    r, ll, post = correr(rom, 0x80, (0xA1, 0xA2), propio=1)
    reg = [x[1] for x in ll if x[0] == "registrar"]
    comprobar("lee la mano del lado contrario", r == 10 and reg == [0xA1, 0xA2], str([hex(x) for x in reg]))

    print("6. bloqueo del motor (FUN_08009094 distinto de 0)")
    r, ll, post = correr(rom, 0x80, mano, bloqueo=1)
    comprobar("devuelve 0", r == 0 and not [x for x in ll if x[0] in ("registrar", "dialogo")])

    print("\nFALLARON" if fallos else "\ntodo en orden", fallos or "")
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
