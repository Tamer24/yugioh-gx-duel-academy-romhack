"""Huecos: que monstruos Normales se pueden reemplazar por una carta restaurada sin romper nada.

Una carta restaurada ocupa el indice de un monstruo Normal, que deja de existir. Un hueco es
"seguro" si ese monstruo no figura en ningun lado mas que en los sobres:
  - no esta en un mazo (rivales e iniciales);
  - el codigo no compara con su ID (ni literal ni calculado: scripts/buscar_id.py);
  - no aparece en ningun lugar de los datos del examen escrito (restaurar.py solo sabe corregir
    cuatro campos de cada pregunta);
  - no aparece en la zona de listas de cartas (fusiones, categorias de la IA, tableros), al lado
    de otro ID valido;
  - sale en algun sobre, para que la carta restaurada se pueda conseguir jugando.
El registro de los ya usados es datos/huecos.csv.

No se busca en el resto del ROM: en los datos graficos y de sonido hay rampas de numeros que
caen en el rango de los IDs y dan falsos positivos (probado: 0x05ECD6C, 0x11EA760).

Uso: python3 scripts/huecos.py ROM_ORIGINAL            lista los seguros libres
     python3 scripts/huecos.py ROM_ORIGINAL --todos    cada monstruo Normal y por que no sirve
"""
import csv
import os
import struct
import sys

import buscar_id
import funciones
from da_lib import EXAMEN, EXAMEN_N, EXAMEN_OFF, FIN_DATOS, LISTAS_INI, N_CARTAS, Rom

SOBRES = 0x17F0DCC          # desde aca hasta FIN_DATOS: listas de los sobres


def usados():
    ruta = os.path.join(funciones.RAIZ, "datos", "huecos.csv")
    with open(ruta, newline="", encoding="utf-8") as f:
        return {int(x["indice"]): x for x in csv.DictReader(f)}


def revisar(rom):
    """[(indice, nombre, [motivos por los que NO es seguro])] de todos los monstruos Normales."""
    d = bytes(rom.d)
    validos = {rom.id_de(i) for i in range(1, N_CARTAS + 1)}
    en_mazos = {rom.u32(o) for o in rom.renglones_u32()}
    en_codigo = buscar_id.mapa(rom)
    fin_examen = EXAMEN + max(rom.u32(EXAMEN_OFF + 4 * q) for q in range(EXAMEN_N)) + 0x40

    def es_id(o):
        return 0 <= o < len(d) - 1 and struct.unpack_from("<H", d, o)[0] in validos

    mazos = set(rom.renglones_u32())

    salida = []
    for i in range(1, N_CARTAS + 1):
        s = rom.stats(i)
        if not (s["tipo"] <= 20 and s["clase"] == 0):
            continue
        v = rom.id_de(i)
        patron, motivos, sobres, listas, examen = struct.pack("<H", v), [], 0, [], 0
        o = d.find(patron)
        while o != -1:
            if o % 2 == 0:
                if SOBRES <= o < FIN_DATOS:
                    sobres += 1
                elif EXAMEN_OFF <= o < fin_examen:
                    examen += 1
                elif LISTAS_INI <= o < SOBRES and o not in mazos and (es_id(o - 2) or es_id(o + 2)):
                    listas.append(o)
            o = d.find(patron, o + 1)
        if v in en_mazos:
            motivos.append("esta en un mazo")
        if v in en_codigo:
            motivos.append("el codigo compara con su ID")
        if examen:
            motivos.append("aparece en el examen")
        if listas:
            motivos.append("en una lista de cartas (" + ", ".join(f"{x:07X}" for x in listas[:3]) + ")")
        if not sobres:
            motivos.append("no sale en ningun sobre")
        salida.append((i, rom.nombre(i), motivos))
    return salida


def libres(rom):
    """[(indice, nombre)] de los huecos seguros que todavia no usa ninguna carta."""
    ya = usados()
    return [(i, n) for i, n, motivos in revisar(rom) if not motivos and i not in ya]


def main(argv):
    if not argv:
        raise SystemExit(__doc__)
    rom, ya = Rom(argv[0]), usados()
    todos = revisar(rom)
    if "--todos" in argv:
        for i, n, motivos in todos:
            estado = f"usado por {ya[i]['carta']}" if i in ya else ""
            print(f"{i:5d} {n:<34} {'SEGURO' if not motivos else '; '.join(motivos)} {estado}")
    seguros = [x for x in todos if not x[2]]
    quedan = [x for x in seguros if x[0] not in ya]
    print(f"{len(todos)} monstruos Normales | {len(seguros)} seguros | {len(ya)} huecos usados | {len(quedan)} seguros libres")
    for i, n, _ in quedan:
        print(f"  {i:5d} {n}")
    fuera = [(i, n, m) for i, n, m in todos if i in ya and m]
    if fuera:
        print("usados que hoy no pasarian el criterio:")
        for i, n, m in fuera:
            print(f"  {i:5d} {n} ({ya[i]['carta']}): {'; '.join(m)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
