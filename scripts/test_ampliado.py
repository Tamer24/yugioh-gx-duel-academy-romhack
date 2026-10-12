"""Prueba de logica del baul ampliado (scripts/ampliar.py), con Unicorn y sin emulador.

Llama a las rutinas del juego que tocan el baul con cartas de los dos lados del limite y mira que
bytes de la memoria cambian: una carta hasta la 1200 tiene que caer en el baul de siempre, una
posterior en su bloque aparte, y ninguna en la fecha, los DP ni los mazos (0x02003840 en adelante).

Uso: python3 scripts/test_ampliado.py "ROM (Ampliado).gba"
"""
import struct
import sys

from unicorn import UC_ARCH_ARM, UC_MODE_THUMB, Uc
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_SP

import ampliar
from da_lib import BASE, N_CARTAS, Rom

SUMAR, FALTA, CONTAR = 0x080E58B8, 0x080B7064, 0x080E57E0      # (indice, cuantas), (indice) -> 1 si no la tengo, (0)
EWRAM, IWRAM = 0x02000000, 0x03000000
fallos = 0


def ok(bien, texto):
    global fallos
    fallos += not bien
    print(("OK    " if bien else "FALLA ") + texto)


def maquina(rom):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(EWRAM, 0x40000)
    uc.mem_map(IWRAM, 0x8000)
    return uc


def llamar(uc, fn, *args):
    for k, v in enumerate(args):
        uc.reg_write(UC_ARM_REG_R0 + k, v)
    uc.reg_write(UC_ARM_REG_SP, IWRAM + 0x7E00)
    uc.reg_write(UC_ARM_REG_LR, (IWRAM + 0x7F00) | 1)
    uc.emu_start(fn | 1, IWRAM + 0x7F00, count=2000000)
    return uc.reg_read(UC_ARM_REG_R0)


def entrada(i):
    """Donde tiene que estar la carta 'i' (el inicio de sus 12 bytes)."""
    return ampliar.BAUL + 12 * (i - 1) if i <= N_CARTAS else ampliar.EXT + 12 * (i - N_CARTAS - 1)


def main(ruta):
    rom = Rom(ruta)
    assert rom.ampliado, "ese ROM no esta ampliado"
    uc = maquina(rom)
    print(f"{rom.n} cartas; baul aparte en {ampliar.EXT:08X}")
    ok(all(llamar(uc, FALTA, i) == 1 for i in (1, N_CARTAS, N_CARTAS + 1, rom.n)), "con el baul vacio no tengo ninguna")
    for i in (1, 600, N_CARTAS, N_CARTAS + 1, rom.n):
        antes = bytes(uc.mem_read(EWRAM, 0x40000))
        llamar(uc, SUMAR, i, 2)
        ahora = bytes(uc.mem_read(EWRAM, 0x40000))
        cambios = [EWRAM + k for k in range(0x40000) if antes[k] != ahora[k]]
        e = entrada(i)
        copias = (struct.unpack_from("<H", ahora, e + 4 - EWRAM)[0] >> 3) & 0xFF
        ok(bool(cambios) and all(e <= c < e + 12 for c in cambios) and copias == 2,
           f"sumar 2 copias de la carta {i} ({rom.nombre(i)}): cambia {[hex(c) for c in cambios]}, copias {copias}")
        ok(llamar(uc, FALTA, i) == 0, f"el juego ve que tengo la carta {i}")
    cola = bytes(uc.mem_read(ampliar.FIN_BAUL, 0x2950))
    ok(not any(cola), "nada escrito entre 0x02003840 y el final del bloque guardado (fecha, DP, mazos)")
    ok(llamar(uc, CONTAR, 0) == 5, "la cuenta de cartas distintas del baul ve las 5")
    print("TODO BIEN" if not fallos else f"{fallos} FALLAS")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
