"""Prueba automatica de Seal of the Ancients, sin ventana (nucleo libretro de mGBA).

Parte de estados/duelo-seal.st (duelo recien empezado, Seal en la mano), termina el
turno, deja jugar al rival y activa Seal. Comprueba que se pagan 1000 LP y que la
carta sale de la mano. Devuelve 0 si pasa y 1 si falla.

Uso: python3 prueba_seal.py rom.gba            (necesita nucleos/ y pillow)
"""
import os
import sys

from duelo_auto import Duelo

AQUI = os.path.dirname(os.path.abspath(__file__))
CARTA = "Seal of the Ancients"


def main():
    d = Duelo(sys.argv[1], estado=os.path.join(AQUI, "..", "estados", "duelo-seal.st"))
    d.g.correr(30)
    d.fin_turno(primero=True)                 # termina mi turno
    d.pasar_rival()                           # el rival juega y roba
    d.g.correr(120)
    rival = [n for s, n in d.zona(1, "05a")]  # cartas del rival en el campo
    assert rival, "el rival no puso ninguna carta: no hay nada que mirar"
    d.ir_mano(CARTA)
    d.tecla("A", 60)                          # menu: Activate Effect / Set / Detail Screen
    antes = d.lp()
    d.tecla("UP", 25)
    d.tecla("UP", 25)
    d.tecla("A", 40)
    d.g.correr(200)
    despues = d.lp()
    en_mano = CARTA in [n for s, n in d.mano()]
    pagado = antes[0] - despues[0]
    print(f"campo del rival: {rival}")
    print(f"LP del jugador: {antes[0]} -> {despues[0]} (pago {pagado})")
    print(f"{CARTA} sigue en la mano: {en_mano}")
    ok = pagado == 1000 and not en_mano
    print("PASA" if ok else "FALLA")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
