"""Arma un archivo de guardado (.sav) con cartas regaladas en el baul y mas DP, sin tocar el original.

Parte del .sav que se le pasa (el de Oscar) y escribe otro: el juego exige que las dos sumas de control
(0x3856 y 0x6184) cuadren, asi que se recalculan. Las cartas ampliadas (indice > 1200) van en el
bloque compacto de la SRAM 0x6200 (marca DAX1, 8 bytes por carta).

Uso:
  python3 scripts/dar_cartas.py ROM.gba ENTRADA.sav SALIDA.sav [--copias 3] [--dp 30000] [--lista]
         [--patron REGEX ...]

Sin --patron regala todas las Neo-Spacian, los Elemental Hero y Neos (lo que pidio Oscar).
--lista solo muestra que cartas tocaria.
"""
import argparse
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(__file__))
from da_lib import Rom

SEMILLA_1, FIN_1, POS_1 = 0x0573, 0x3856, 0x3856      # suma del encabezado, guardada en 0x3856
SEMILLA_2, FIN_2, POS_2 = 0x5847, 0x6184, 0x6184      # suma de todo el bloque, guardada en 0x6184
DP = 0x3848
EXT = 0x6200                                          # marca "DAX1" y despues 8 bytes por carta
MARCA = b"DAX1"
PATRON_DEFECTO = [r"^Neo-Spacian ", r"^Elemental Hero ", r"^Neo Space$", r"^Neos "]


def suma(d, semilla, fin):
    a = semilla
    for i in range(0, fin, 2):
        a = ((struct.unpack_from("<H", d, i)[0] + a) & 0xFFFF) ^ 0xFFFF
    return a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rom")
    ap.add_argument("entrada")
    ap.add_argument("salida")
    ap.add_argument("--copias", type=int, default=3)
    ap.add_argument("--dp", type=int)
    ap.add_argument("--patron", action="append")
    ap.add_argument("--lista", action="store_true")
    a = ap.parse_args()
    rom = Rom(a.rom)
    d = bytearray(open(a.entrada, "rb").read())
    assert len(d) == 0x8000, "no es una SRAM de 32 KB"
    assert suma(d, SEMILLA_1, FIN_1) == struct.unpack_from("<H", d, POS_1)[0], \
        "la suma de control 1 del guardado de entrada no cuadra: no es un guardado valido"
    assert suma(d, SEMILLA_2, FIN_2) == struct.unpack_from("<H", d, POS_2)[0], "la suma de control 2 no cuadra"
    patrones = [re.compile(p) for p in (a.patron or PATRON_DEFECTO)]
    flags_por_id = {f["id"]: f["flags"] for f in rom.efectos()}
    nuevas = 0
    nombres = []
    for i in range(1, rom.n + 1):
        n = rom.nombre(i)
        if not any(p.search(n) for p in patrones):
            continue
        if i <= 1200:
            o = (i - 1) * 12
            ox = 0
        else:
            if bytes(d[EXT:EXT + 4]) != MARCA:
                d[EXT:EXT + 4] = MARCA
            o = EXT + 4 + 8 * (i - 1201)
            ox = 1
        # campos: baul normal {u16 +0, u16 +4, u32 +8}; compacto {u16 +0, u16 +2, u32 +4}
        p_b, p_f = (o + 4, o + 8) if not ox else (o + 2, o + 4)
        b = struct.unpack_from("<H", d, p_b)[0]
        copias = (b >> 3) & 0xFF
        if copias >= a.copias:
            continue
        if copias == 0:                                   # como FUN_080E58B8: bit "nueva" y flags
            b |= 2
            struct.pack_into("<I", d, p_f, flags_por_id.get(rom.id_de(i), 0))
            nuevas += 1
        b = (b & 0xF807) | (a.copias << 3)
        struct.pack_into("<H", d, p_b, b)
        nombres.append(f"{i} {n}")
    print(f"{len(nombres)} cartas subidas a {a.copias} copias ({nuevas} eran nuevas):")
    print("  " + "\n  ".join(nombres))
    if a.lista:
        return
    if a.dp is not None:
        struct.pack_into("<I", d, DP, a.dp)
    struct.pack_into("<H", d, POS_1, suma(d, SEMILLA_1, FIN_1))
    struct.pack_into("<H", d, POS_2, suma(d, SEMILLA_2, FIN_2))
    assert a.salida != a.entrada
    open(a.salida, "wb").write(d)
    print("guardado ->", a.salida, "| DP", struct.unpack_from("<I", d, DP)[0])


main()
