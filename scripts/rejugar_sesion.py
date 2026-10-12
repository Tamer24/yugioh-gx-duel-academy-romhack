"""Vuelve a jugar una sesion de paso.py en una carpeta nueva, con las mismas ordenes.

A diferencia de repetir_sesion.py (que compara y no escribe), esta deja una sesion nueva con sus
capturas y su registro: sirve para rehacer la evidencia de una carta cuyo comportamiento cambio.

Uso (desde la raiz del proyecto):
  python3 scripts/rejugar_sesion.py ROM SESION_VIEJA SESION_NUEVA
Imprime el duelo al final del ultimo paso.
"""
import os
import subprocess
import sys

import repetir_sesion


def main(argv):
    if len(argv) != 3:
        raise SystemExit(__doc__)
    rom, vieja, nueva = argv
    if os.path.exists(nueva) and os.listdir(nueva):
        raise SystemExit(f"error: {nueva} ya existe y no esta vacia")
    aqui = os.path.dirname(os.path.abspath(__file__))
    ultimo = ""
    for numero, tipo, origen, ordenes, _ in repetir_sesion.leer_registro(vieja):
        if tipo == "estado":
            cmd = ["--desde", origen]
        else:
            if int(origen) != numero - 1:
                raise SystemExit(f"error: el paso {numero} sale del paso {origen}: la sesion tiene vueltas atras")
            cmd = [o.strip() for o in ordenes]
        r = subprocess.run([sys.executable, os.path.join(aqui, "paso.py"), rom, nueva] + cmd,
                           capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(f"error en el paso {numero}: {r.stderr.strip() or r.stdout.strip()}")
        ultimo = r.stdout
    print(ultimo.strip())


if __name__ == "__main__":
    main(sys.argv[1:])
