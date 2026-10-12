"""Lista los BL de Thumb del codigo del ROM que llaman a una direccion dada.

Uso: python3 llamadores.py rom.gba DIRECCION [nombres.json]
Recorre los primeros 0x7A8000 bytes (el codigo) buscando pares BL cuyo destino sea DIRECCION.
Con nombres.json (ghidra/nombres_yugiohgx-da.json) dice en que funcion esta cada llamada.
"""
import bisect
import json
import struct
import sys

from da_lib import BASE

FIN_CODIGO = 0x7A8000


def llamadores(datos, destino):
    destino &= ~1
    out = []
    for o in range(0, FIN_CODIGO - 4, 2):
        a, b = struct.unpack_from("<HH", datos, o)
        if a & 0xF800 == 0xF000 and b & 0xF800 == 0xF800:
            off = ((a & 0x7FF) << 12) | ((b & 0x7FF) << 1)
            if off & 0x400000:
                off -= 0x800000
            if BASE + o + 4 + off == destino:
                out.append(BASE + o)
    return out


def main():
    datos = open(sys.argv[1], "rb").read()
    nombres, claves = {}, []
    if len(sys.argv) > 3:
        nombres = {int(k, 16): v for k, v in json.load(open(sys.argv[3])).items()}
        claves = sorted(nombres)
    for a in llamadores(datos, int(sys.argv[2], 16)):
        donde = ""
        if claves:
            f = claves[bisect.bisect_right(claves, a) - 1]
            donde = f"  en {nombres[f]} ({f:08X})"
        print(f"{a:08X}{donde}")


if __name__ == "__main__":
    main()
