"""Reemplaza en un C decompilado por Ghidra los simbolos DAT_08xxxxxx por el valor que hay en el ROM.

Uso: python3 resolver_literales.py rom.gba entrada.c [salida.c]
Los DAT_ son literales de 32 bits del codigo: con el valor a la vista se reconocen IDs de carta
(4007..6467 se anotan con el nombre, de datos/efectos.csv y datos/cartas.csv), direcciones y mascaras.
"""
import csv
import os
import re
import struct
import sys

from da_lib import BASE


def main():
    rom = open(sys.argv[1], "rb").read()
    texto = open(sys.argv[2], encoding="utf-8").read()
    nombres = {}
    datos = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datos")
    for archivo in ("efectos.csv", "cartas.csv"):       # las 901 filas de efecto y las 1200 cartas
        ruta = os.path.join(datos, archivo)
        if os.path.exists(ruta):
            for fila in csv.DictReader(open(ruta, encoding="utf-8")):
                nombres[int(fila["id_konami"])] = fila["nombre"]

    def valor(m):
        d = int(m.group(1), 16)
        if not BASE <= d < BASE + len(rom) - 4:
            return m.group(0)
        v = struct.unpack_from("<I", rom, d - BASE)[0]
        if 4007 <= v <= 6467:
            return f"{v}/*{nombres.get(v, '?')}*/" if nombres else str(v)
        return f"0x{v:x}"

    salida = re.sub(r"\b[DS]U?[AB]T?_(0[89][0-9a-fA-F]{6})\b", valor, texto)
    if len(sys.argv) > 3:
        open(sys.argv[3], "w", encoding="utf-8").write(salida)
    else:
        sys.stdout.write(salida)


if __name__ == "__main__":
    main()
