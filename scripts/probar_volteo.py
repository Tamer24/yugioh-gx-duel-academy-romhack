"""Corredor para monstruos de volteo: coloca el monstruo boca abajo (Set), termina el turno y deja
que el rival ataque. Informa el campo de los dos lados antes y despues, y saca fotos.

Uso: ESTADO_BASE=estados/duelo-bagworm.ss1 python3 probar_volteo.py rom.gba "Electromagnetic Bagworm" [ciclos]
"""
import os
import sys

from da_lib import Rom
from duelo_auto import Duelo, J1
import probar_trampas as pt


def campo(d):
    """Monstruos por CONTROLADOR (listas de zonas), no por dueno: un monstruo robado sigue en el
    bloque de memoria de su dueno pero pasa a la lista de quien lo controla."""
    from duelo_auto import LISTA_ZONAS
    def lado(j):
        out = []
        for i in range(5):
            idc = d.g.r8(LISTA_ZONAS + 11 * j + i)
            if idc != 0xFF:
                base = J1 if idc & 0x80 else 0x02022250
                a = base + (idc & 0x7F) * 0x50
                out.append((idc, d.rom.nombre(d.g.r16(a + 0x24) & 0x7FFF), d.g.r8(a + 0x33)))
        return out
    return {"mio": lado(0), "rival": lado(1),
            "cem_mio": sorted(n for s, n in d.zona(0, "d")), "cem_rival": sorted(n for s, n in d.zona(1, "d")),
            "LP": d.lp()}


def parar_teclas(d):
    """True cuando mi monstruo ya se volteo: ahi aparecen avisos de seleccion y una A los contesta."""
    return any(d.g.r8(0x02022250 + s * 0x50 + 0x33) == 0x30 for s, n in d.zona(0, "0"))


def correr(ruta, nombre, ciclos=5, fotos=None):
    d = Duelo(ruta, estado=os.environ.get("ESTADO_BASE") or pt.BASE)
    d.g.correr(30)
    d.ir_mano(nombre)
    d.menu(1)                                   # Set
    d.g.correr(60)
    print("tras Set:", campo(d))
    if fotos:
        d.foto(os.path.join(fotos, "v_set.png"), escala=1)
    d.fin_turno(primero=True)
    for t in range(ciclos * 150):
        d.g.correr(6)
        if t % 15 == 14 and not parar_teclas(d):
            d.tecla("A", 4)
        if t % 100 == 99:
            print(t * 6, campo(d))
            if fotos:
                d.foto(os.path.join(fotos, f"v_{t:04d}.png"), escala=1)


if __name__ == "__main__":
    correr(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 5, os.environ.get("FOTOS"))
