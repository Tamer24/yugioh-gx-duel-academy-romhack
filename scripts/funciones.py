"""A que funcion del juego pertenece una direccion, y como se llama.

Los nombres salen de ghidra/nombres_yugiohgx-da.json (3862 direcciones, la mayoria FUN_...). Esa
lista no trae todas las funciones: 0x08030186 cae, segun ella, en FUN_0802F9C4, pero esta en otra
que empieza en 0x08030098. Por eso el inicio se busca en el codigo: el `push {..., lr}` mas cercano
hacia atras, sin pasar del inicio conocido anterior. Es una estimacion (una funcion hoja no guarda
lr); siempre se imprime para poder revisarla.
"""
import bisect
import json
import os
import struct

from da_lib import BASE

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_NOMBRES = None


def nombres():
    global _NOMBRES
    if _NOMBRES is None:
        ruta = os.path.join(RAIZ, "ghidra", "nombres_yugiohgx-da.json")
        _NOMBRES = {int(k, 16): v for k, v in json.load(open(ruta)).items()}
    return _NOMBRES


def registrar(direcciones, como="funcion de efecto"):
    """Agrega inicios de funcion conocidos (p. ej. las columnas de datos/efectos.csv), para que
    'inicio' no se pase de largo en una funcion hoja, que no guarda lr."""
    for d in direcciones:
        nombres().setdefault(d & ~1, f"FUN_{d & ~1:08x} ({como})")


def nombre(direccion):
    return nombres().get(direccion, f"FUN_{direccion:08X} (sin nombre)")


def inicio(d, direccion):
    """Inicio estimado de la funcion que contiene 'direccion' (GBA). 'd' = bytes del ROM."""
    conocidas = sorted(nombres())
    k = bisect.bisect_right(conocidas, direccion) - 1
    piso = conocidas[k] if k >= 0 else BASE
    a = (direccion & ~1) - BASE
    while BASE + a > piso:
        if struct.unpack_from("<H", d, a)[0] & 0xFF00 == 0xB500:        # push {..., lr}
            return BASE + a
        a -= 2
    return piso
