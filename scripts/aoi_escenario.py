"""Escenario para observar a Spiritual Water Art - Aoi jugada por una persona.

Usa un ROM con el registrador (la fn_04 de Aoi anota estado y p[8..10]).
"""
import os

import probar_magicas as pm
from duelo_auto import Duelo, J0

HOVER = 0x02019F0C            # indice de la carta bajo el cursor


def bajo_cursor(d):
    return d.g.r16(HOVER) & 0x7FFF


def ir_a_carta(d, indice, y):
    """Mueve el cursor por la fila y hasta que la carta bajo el cursor sea 'indice'."""
    d.mover(y=y)
    for x in (3, 4, 5, 6, 7):
        d.mover(x=x, y=y)
        d.g.correr(10)
        if bajo_cursor(d) == indice:
            return True
    return False


def preparar(rom):
    d = Duelo(rom, estado=pm.estado_con(1191, {2: 450}))
    d.g.correr(30)
    d.g.w32(0x0203F000, 0)
    d.g.escribir(0x0203F010, bytes(256))
    d.ir_mano("Spiritual Water Art - Aoi")
    d.tecla("A", 60)
    n = pm.opciones_menu(d)
    for _ in range(n - 1):
        d.tecla("UP", 25)
    d.tecla("A", 60)
    d.g.correr(120)                              # Aoi colocada
    d.fin_turno(primero=True)
    d.pasar_rival()
    d.g.correr(200)
    pm.preparar(d, ["invocar:Mother Grizzly"])   # el WATER, en el turno 2
    return d
