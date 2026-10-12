"""Decompila funciones del juego con Ghidra, dadas direcciones cualesquiera dentro de ellas.

Uso (desde la raiz del proyecto):
  python3 scripts/decompilar.py ROM_ORIGINAL NOMBRE DIRECCION [DIRECCION ...]
  p. ej. python3 scripts/decompilar.py USA.gba snatch 0803F2E8 0802F78E 08030186

Deja el C en ghidra/salida/NOMBRE.c y el registro de Ghidra en ghidra/salida/NOMBRE.c.log.
Cada direccion puede ser el inicio de una funcion (p. ej. una columna de datos/efectos.csv, con o
sin el bit Thumb) o un punto interior (p. ej. un sitio de scripts/buscar_id.py): el inicio se
estima con funciones.inicio y se imprime, porque a Ghidra hay que darle el inicio exacto.

Necesita Ghidra (brew install ghidra) y openjdk@21. El proyecto ya analizado esta en
ghidra/proyecto; para rehacerlo, ver NOTAS-REVERSE.md ("Regenerar").

Ojo al leer la salida: donde Ghidra pone `return FUN_xxx(...)` a mitad de una funcion, o "Subroutine
does not return", el flujo esta cortado y la funcion sigue. Para esos tramos, scripts/desensamblar.py.
"""
import glob
import os
import subprocess
import sys

import funciones
from da_lib import Rom

RAIZ = funciones.RAIZ


def analizador():
    hallados = sorted(glob.glob("/opt/homebrew/Cellar/ghidra/*/libexec/support/analyzeHeadless"))
    if not hallados:
        raise SystemExit("no encuentro analyzeHeadless (brew install ghidra)")
    return hallados[-1]


def main(argv):
    if len(argv) < 3:
        raise SystemExit(__doc__)
    rom, nombre = Rom(argv[0]), argv[1]
    inicios = []
    for texto in argv[2:]:
        direccion = int(texto, 16) & ~1
        f = funciones.inicio(rom.d, direccion)
        print(f"{direccion:08X} -> {funciones.nombre(f)} ({f:08X})")
        if f not in inicios:
            inicios.append(f)
    salida = os.path.join(RAIZ, "ghidra", "salida", nombre + ".c")
    entorno = dict(os.environ, JAVA_HOME=os.environ.get("JAVA_HOME") or "/opt/homebrew/opt/openjdk@21")
    orden = [analizador(), os.path.join(RAIZ, "ghidra", "proyecto"), "da", "-process", "codigo.bin", "-noanalysis",
             "-scriptPath", os.path.join(RAIZ, "ghidra", "scripts"), "-postScript", "Decompilar.java", salida]
    orden += [f"{f:08X}" for f in inicios]
    with open(salida + ".log", "w") as registro:
        r = subprocess.run(orden, stdout=registro, stderr=subprocess.STDOUT, env=entorno)
    if r.returncode != 0 or not os.path.exists(salida):
        raise SystemExit(f"Ghidra fallo: ver {salida}.log")
    print(f"{salida}: {sum(1 for _ in open(salida))} lineas")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
