"""Prueba en duelo de una Fusion: Polymerization, la carta de Fusion y sus materiales en la mano.

Parte de estados/duelo-inicio.ss1 con Polymerization y los materiales en mi mano y, como ayuda de
prueba, convierte la carta de mi mazo de fusion (ranura 40) en la Fusion pedida. Activa
Polymerization, elige la Fusion en la lista "Fusion Deck", marca cada material en la lista "Hand"
(CHECK) y confirma (DECIDE). Pasa si la Fusion queda en mi campo.

Uso (desde la raiz del proyecto):
  python3 scripts/probar_fusion.py ROM "Fusion" "Material 1" "Material 2" ["Material 3"]
"""
import os
import sys

import probar_lote as P
from duelo_auto import J0


def probar(ruta_rom, fusion, materiales):
    estado = P.armar(ruta_rom, "fusion-prueba", yo={5: "Polymerization", **{4 - k: m for k, m in enumerate(materiales)}})
    d = P.abrir(ruta_rom, estado, 0)
    a = J0 + 40 * 0x50
    idx = next(i for i in range(1, d.rom.n + 1) if d.rom.nombre(i) == fusion)
    d.g.w16(a + 0x24, (d.g.r16(a + 0x24) & 0x8000) | idx)       # ayuda de prueba
    d.ir_mano("Polymerization")
    d.tecla("A", 60)
    d.tecla("UP", 30)
    d.tecla("UP", 30)                                              # Activate Effect
    d.tecla("A", 120)
    d.tecla("A", 90)
    ciclo = "A A A RIGHT RIGHT RIGHT A".split()                    # la Fusion en la lista
    n = 0
    while d.g.r8(0x020204C6) != 0x7D and n < 30:
        d.tecla(ciclo[n % 7], 60)
        n += 1
    if d.g.r8(0x020204C6) != 0x7D:
        return False, "no se pudo elegir la Fusion en la lista"
    for t in ("A", "A"):                                            # aviso y entrar a la lista de materiales
        d.tecla(t, 70)
    for k in range(len(materiales)):
        d.tecla("A", 70)                                            # iconos de la carta
        d.tecla("A", 70)                                            # CHECK
        if k < len(materiales) - 1:
            d.tecla("DOWN", 70)
    for t in ["A"] + ["RIGHT"] * 4 + ["A"]:                         # DECIDE
        d.tecla(t, 70)
    d.g.correr(400)
    for _ in range(4):
        d.tecla("A", 90)
    campo = [nombre for _, nombre in d.zona(0, "0")]
    return fusion in campo, f"campo {campo}, mano {[n for _, n in d.mano(0)]}"


def main(argv):
    if len(argv) < 4 or not os.path.exists(argv[0]):
        raise SystemExit(__doc__)
    ok, detalle = probar(argv[0], argv[1], argv[2:])
    print(("FUNCIONA: " if ok else "NO FUNCIONA: ") + f"{argv[1]} = {' + '.join(argv[2:])}; {detalle}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
