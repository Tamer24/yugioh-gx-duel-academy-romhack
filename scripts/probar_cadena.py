"""Corredor para Trampas que responden a una Magica del rival (Magic Drain, ...).

Coloca la trampa boca abajo, termina el turno y, SIN pulsar teclas durante el turno del rival
salvo una A espaciada para los dialogos, espera a que la IA juegue una Magica. El juego pregunta
"<carta> has activated. Will you chain? Yes / No" y espera sin limite: Yes (A), "Select
Spell/Trap Card to activate." (A), DOWN DOWN, LEFT x(4-zona), A, UP, A.

El evento NO aparece en 0x0202048C (la estructura del ataque declarado): por eso el corredor de
ataques no lo veia. Se detecta mirando que una carta nueva del rival quede en su fila de
magias/trampas (la IA juega Dian Keto en su 2.o turno, ~800 cuadros despues de terminar el mio).

Uso: python3 probar_cadena.py rom.gba [NOMBRE]    (por defecto Magic Drain)
"""
import os
import sys

import probar_trampas as pt
from duelo_auto import Duelo

AQUI = os.path.dirname(os.path.abspath(__file__))


def correr(ruta_rom, nombre="Magic Drain", fotos=None, maximo=2500):
    rom = pt.Rom(ruta_rom)
    d = Duelo(ruta_rom, estado=pt.estado_con(rom, nombre))
    d.g.correr(30)
    d.ir_mano(nombre)
    d.tecla("A", 60)
    d.tecla("UP", 25)
    d.tecla("A", 80)
    ranura = next((s for s, n in d.zona(0, "5") if n == nombre), None)
    if ranura is None:
        return "NO SE COLOCO", None, None
    antes_riv = {n for s, n in d.zona(1, "5a")}
    d.fin_turno(primero=True)
    for t in range(maximo):
        d.g.correr(6)
        if t % 15 == 14:
            d.tecla("A", 4)
        if {n for s, n in d.zona(1, "5a")} - antes_riv:
            break
    else:
        return "LA IA NO JUGO UNA MAGICA", None, None
    d.g.correr(200)                          # el aviso aparece y espera
    antes = {"LP": d.lp(), "cem_rival": sorted(n for s, n in d.zona(1, "d")),
             "campo_rival": sorted(n for s, n in d.zona(1, "5a"))}
    if fotos:
        d.foto(os.path.join(fotos, f"{nombre}_aviso.png"), escala=1)
    d.responder_con_trampa(ranura)
    d.g.correr(900)
    if fotos:
        d.foto(os.path.join(fotos, f"{nombre}_final.png"), escala=1)
    despues = {"LP": d.lp(), "cem_rival": sorted(n for s, n in d.zona(1, "d")),
               "campo_rival": sorted(n for s, n in d.zona(1, "5a")),
               "cem_mio": sorted(n for s, n in d.zona(0, "d"))}
    veredicto = "SE ACTIVO" if nombre in despues["cem_mio"] else "NO SE ACTIVO"
    return veredicto, antes, despues


if __name__ == "__main__":
    rom = sys.argv[1]
    v, a, b = correr(rom, *(sys.argv[2:3] or []), fotos=os.environ.get("FOTOS"))
    print(v)
    print("antes  ", a)
    print("despues", b)
