"""Vuelve a jugar sesiones de paso.py con las mismas teclas y compara el duelo paso a paso.

Sirve de regresion despues de rearmar el ROM: una sesion grabada en un ROM anterior se repite
en el nuevo y, si la lectura de memoria de cada paso (LP, manos, campo, cementerios, mazos) es
la misma que quedo en su registro.txt, el ROM nuevo se comporta igual en ese duelo.

Uso (desde la raiz del proyecto):
  python3 scripts/repetir_sesion.py ROM SESION [SESION ...]
  python3 scripts/repetir_sesion.py ROM $(cat scripts/sesiones_regresion.txt)   # las 30 de siempre

Si el estado de partida de una sesion ya no esta donde dice su registro.txt, se busca con el mismo
nombre en estados/regresion/.

Por cada sesion imprime IGUAL o DISTINTA (con el primer paso que difiere). No escribe nada.
Salida 0 si todas son iguales.
"""
import os
import re
import sys

import paso

CABECERA = re.compile(r"paso (\d+) \(desde (estado|paso) (.+?)\): (.*)")


def leer_registro(sesion):
    """[(numero, tipo de origen, origen, ordenes, texto esperado)] en el orden en que se jugaron."""
    ruta = os.path.join(sesion, "registro.txt")
    if not os.path.exists(ruta):
        raise paso.ErrorPaso(f"{sesion} no tiene registro.txt")
    entradas = []
    for bloque in open(ruta, encoding="utf-8").read().split("\n\n"):
        lineas = bloque.strip().split("\n")
        m = CABECERA.fullmatch(lineas[0]) if lineas[0] else None
        if not m:
            continue
        cuerpo = [l for l in lineas[1:] if not l.startswith("ERROR: ")]
        ordenes = [] if m.group(4) == "sin ordenes" else m.group(4).split(" | ")
        entradas.append((int(m.group(1)), m.group(2), m.group(3), ordenes, "\n".join(cuerpo)))
    return entradas


def repetir(ruta_rom, sesion):
    """(True, cantidad de pasos) o (False, descripcion del primer paso distinto)."""
    estados = {}
    entradas = leer_registro(sesion)
    for n, tipo, origen, ordenes, esperado in entradas:
        if tipo == "estado":
            if not os.path.exists(origen):
                # los estados de partida de las sesiones de regresion viven ahora en estados/regresion/
                otro = os.path.join("estados", "regresion", os.path.basename(origen))
                origen = otro if os.path.exists(otro) else origen
            if not os.path.exists(origen):
                return False, f"paso {n}: no existe el estado de partida {origen}"
            datos = open(origen, "rb").read()
        elif int(origen) in estados:
            datos = estados[int(origen)]
        else:
            return False, f"paso {n}: sale del paso {origen}, que no esta en el registro (no se puede repetir)"
        d, _ = paso.jugar(ruta_rom, datos, ordenes)
        estados[n] = d.g.guardar_estado()
        obtenido = paso.describir(d)
        if obtenido != esperado:
            distintas = [f"      antes: {a}\n      ahora: {b}" for a, b in zip(esperado.split("\n"), obtenido.split("\n"))
                         if a != b]
            return False, f"paso {n} ({' | '.join(ordenes)}):\n" + "\n".join(distintas[:4])
    return True, len(entradas)


def main(argv):
    if len(argv) < 2 or not os.path.exists(argv[0]):
        raise SystemExit(__doc__)
    ruta_rom, todas = argv[0], True
    for sesion in argv[1:]:
        if os.path.isdir(sesion) and not os.path.exists(os.path.join(sesion, "registro.txt")):
            print(f"OMITIDA  {sesion} (no es una sesion: no tiene registro.txt)")    # p. ej. ronda4/auto
            continue
        igual, detalle = repetir(ruta_rom, sesion.rstrip("/"))
        todas = todas and igual
        print(f"{'IGUAL   ' if igual else 'DISTINTA'} {sesion}" + (f" ({detalle} pasos)" if igual else f"\n   {detalle}"))
    return 0 if todas else 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except paso.ErrorPaso as err:
        raise SystemExit(f"error: {err}")
