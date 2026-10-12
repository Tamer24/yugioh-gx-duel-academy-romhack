"""Vuelca EWRAM e IWRAM de un duelo en curso para ejecutar funciones sueltas del motor con
Unicorn (ver llamar_motor.py).

Uso: python3 volcar_ram.py rom.gba estado.st "Nombre de carta a invocar" salida_prefijo
Deja salida_prefijo.ewram y salida_prefijo.iwram. Requiere el nucleo de mGBA (nucleos/).
"""
import sys

import probar_magicas as pm
from duelo_auto import Duelo

rom, estado, nombre, salida = sys.argv[1:5]
d = Duelo(rom, estado=estado)
d.g.correr(30)
if nombre:
    pm.preparar(d, ["invocar:" + nombre])
d.g.correr(60)
open(salida + ".ewram", "wb").write(bytes(d.g.leer(0x02000000, 0x40000)))
open(salida + ".iwram", "wb").write(bytes(d.g.leer(0x03000000, 0x8000)))
print("campo", d.zona(0, "05a"))
