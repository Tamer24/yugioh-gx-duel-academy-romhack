"""Prueba con Unicorn de efectos/hiro_scout.s (fn_04 de Hiro's Shadow Scout, ID 4617).

Simula al motor: llama a fn_04 con el estado 0x80 y la vuelve a llamar con el estado que
devuelve, hasta que devuelve 0. Las funciones del motor que mueven la carta del tope del mazo
(al cementerio si es Magica, a la mano si no) se reemplazan por ganchos que la sacan del mazo.
Lo esperado sale del texto de la carta: el rival roba 3; las Magicas van al cementerio.

Uso: python3 test_hiro.py rom.gba            (pip install unicorn)
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R7,
                               UC_ARM_REG_LR, UC_ARM_REG_SP, UC_ARM_REG_PC)

from da_lib import *

J0, L = 0x02022250, 0x2B08
MAZO, ESTADO, CONTADOR = 0x28A4, 0x020204C6, 0x020204C7
A_CEMENTERIO, A_LA_MANO = 0x08018518, 0x08018570
AVISOS = (0x0801AAD4, 0x0801AB34)
MAGICA, MONSTRUO, TRAMPA = "Dian Keto the Cure Master", "Blue-Eyes White Dragon", "Call of the Haunted"


def correr(rom, mazo, lado=0, anulada=0, r7=0x55):
    """mazo: nombres de las cartas del mazo del rival, la primera es el tope.
    Devuelve (robadas, al cementerio, llamadas a fn_04)."""
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    rival = 1 - lado
    base = J0 + rival * L
    indices = {rom.nombre(i): i for i in range(1, N_CARTAS + 1)}
    ranuras = []
    for k, nombre in enumerate(mazo):
        s = 40 + k
        uc.mem_write(base + s * 0x50 + 0x24, struct.pack("<H", indices[nombre]))
        ranuras.append((rival << 7) | s)
    estado = {"mazo": list(ranuras)}

    def escribir_mazo():
        uc.mem_write(base + MAZO, bytes(estado["mazo"] + [0xFF] * (60 - len(estado["mazo"]))))
        uc.mem_write(base + 0x1C, struct.pack("<H", len(estado["mazo"]) << 6))

    escribir_mazo()
    carta = 0x02010000
    uc.mem_write(carta, struct.pack("<H", (38 << 1) | lado) + bytes([anulada, 0] + [0] * 12))
    robadas, cementerio = [], []

    def gancho(u, dir_, tam, _):
        if dir_ in (A_CEMENTERIO, A_LA_MANO):
            idc = u.reg_read(UC_ARM_REG_R1)
            (cementerio if dir_ == A_CEMENTERIO else robadas).append(mazo[ranuras.index(idc)])
            estado["mazo"].remove(idc)
            escribir_mazo()
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif dir_ in AVISOS:
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(rom.efectos_base + EFECTOS_FILA * filas[4617] + 4)
    siguiente, llamadas = 0x80, 0
    while siguiente and llamadas < 10:
        uc.mem_write(ESTADO, bytes([siguiente]))
        uc.reg_write(UC_ARM_REG_R0, carta)
        uc.reg_write(UC_ARM_REG_R7, r7)             # el motor no deja nada util en r7
        uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
        uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
        uc.emu_start(fn, 0x03007F00, count=50000)
        siguiente = uc.reg_read(UC_ARM_REG_R0) & 0xFF
        llamadas += 1
    return robadas, cementerio, llamadas


def main():
    rom = Rom(sys.argv[1])
    casos = [
        ("tres cartas sin Magicas: roba las 3",
         dict(mazo=[MONSTRUO, TRAMPA, MONSTRUO, MONSTRUO]), ([MONSTRUO, TRAMPA, MONSTRUO], [])),
        ("una Magica en el medio: roba 2 y la Magica va al cementerio",
         dict(mazo=[MONSTRUO, MAGICA, TRAMPA, MONSTRUO]), ([MONSTRUO, TRAMPA], [MAGICA])),
        ("tres Magicas: las 3 al cementerio",
         dict(mazo=[MAGICA, MAGICA, MAGICA, MONSTRUO]), ([], [MAGICA, MAGICA, MAGICA])),
        ("mazo con 2 cartas: procesa 2 y termina",
         dict(mazo=[TRAMPA, MAGICA]), ([TRAMPA], [MAGICA])),
        ("mazo vacio: nada", dict(mazo=[]), ([], [])),
        ("carta anulada: nada", dict(mazo=[MONSTRUO] * 4, anulada=8), ([], [])),
        ("la activa el rival (lado 1): roba el jugador",
         dict(mazo=[MAGICA, MONSTRUO, MONSTRUO, TRAMPA], lado=1), ([MONSTRUO, MONSTRUO], [MAGICA])),
    ]
    ok = True
    for nombre, kw, (robadas, cementerio) in casos:
        r, c, n = correr(rom, **kw)
        bien = (r, c) == (robadas, cementerio) and n < 10
        print(f"{'OK ' if bien else 'MAL'} {nombre}: roba={r} cementerio={c} llamadas={n}")
        ok = ok and bien
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
