"""Donde trata el motor a una carta: todos los sitios del codigo que comparan con su ID de Konami.

El motor resuelve muchos efectos por ID, con arboles de comparacion. El ID no siempre esta como
literal: los arboles llegan a varios IDs con adds/subs desde un vecino (Kunai = Metalmorph - 7,
Necrofear = 0x1544 - 1 - 0xDD), asi que buscar el literal no alcanza. Este script sigue cada
`ldr rN, =literal` y las sumas y restas que le siguen sobre el mismo registro.

Sirve para dos cosas:
  - saber que hace ya el motor con una carta recortada antes de escribirle un efecto;
  - encontrar el molde: buscar una carta ORIGINAL que haga lo que se quiere y ver en que
    funciones aparece (despues: scripts/decompilar.py con esas direcciones).

Uso: python3 scripts/buscar_id.py ROM_ORIGINAL ID_O_NOMBRE [ID_O_NOMBRE ...]
  p. ej. python3 scripts/buscar_id.py USA.gba "Snatch Steal" 5222
Imprime, por sitio: direccion, si es literal o calculado, y la funcion que lo contiene (el inicio
se estima: ver funciones.inicio).
"""
import struct
import sys

import funciones
from da_lib import BASE, N_CARTAS, Rom

CODIGO = (0x8000, 0xF0000)        # donde hay codigo Thumb del juego


_MAPAS = {}


def mapa(rom):
    """{ID: [(direccion GBA, 'literal' | 'calculado')]} de todo el codigo, en una sola pasada."""
    if rom.md5 in _MAPAS:
        return _MAPAS[rom.md5]
    d = rom.d
    hallados = {}

    def u16(a):
        return struct.unpack_from("<H", d, a)[0]

    for ini in range(CODIGO[0], CODIGO[1], 2):
        w = u16(ini)
        if w & 0xF800 != 0x4800:                       # ldr rN, [pc, #x]
            continue
        reg = (w >> 8) & 7
        valor = struct.unpack_from("<I", d, ((ini + 4) & ~3) + (w & 0xFF) * 4)[0]
        if not 0xF00 <= valor <= 0x1B00:               # rango de los IDs de Konami del juego
            continue
        hallados.setdefault(valor, set()).add((BASE + ini, "literal"))
        a = ini + 2
        for _ in range(60):
            x = u16(a)
            mismo = (x >> 8) & 7 == reg
            if x & 0xF000 == 0x3000 and mismo:         # adds / subs rN, #imm
                valor += (x & 0xFF) if x & 0x0800 == 0 else -(x & 0xFF)
                hallados.setdefault(valor, set()).add((BASE + a, "calculado"))
            elif x & 0xF800 in (0x4800, 0x2000) and mismo:   # otro ldr o movs sobre el registro
                break
            elif x & 0xFF00 == 0xBD00 or x == 0x4770:  # pop {pc} / bx lr: fin de la funcion
                break
            a += 2
    _MAPAS[rom.md5] = {k: sorted(v) for k, v in hallados.items()}
    return _MAPAS[rom.md5]


def sitios(rom, id_konami):
    """[(direccion GBA, 'literal' | 'calculado')] de las comparaciones con ese ID."""
    return mapa(rom).get(id_konami, [])


def id_de(rom, texto):
    if texto.isdigit():
        return int(texto)
    for i in range(1, N_CARTAS + 1):
        if rom.nombre(i) == texto:
            return rom.id_de(i)
    raise SystemExit(f"no hay ninguna carta llamada {texto!r}")


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)
    rom = Rom(argv[0])
    for texto in argv[1:]:
        cid = id_de(rom, texto)
        print(f"== {texto} (ID {cid}, {cid:#06x})")
        por_funcion = {}
        for direccion, como in sitios(rom, cid):
            por_funcion.setdefault(funciones.inicio(rom.d, direccion), []).append(f"{direccion:08X} {como}")
        for f in sorted(por_funcion):
            print(f"  {funciones.nombre(f):<34} {', '.join(por_funcion[f])}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
