"""Juega un duelo de a pasos, sin ventana: cada llamada carga donde quedo la anterior, aprieta
botones, saca capturas y muestra el duelo leido de la memoria.

Sirve para revisar una carta "a ojo" por script: mirar la captura, decidir el paso siguiente.

Uso (desde la raiz del proyecto):
  python3 scripts/paso.py ROM SESION --desde ESTADO          # empieza (o reinicia) la sesion
  python3 scripts/paso.py ROM SESION ORDEN [ORDEN ...]       # sigue desde el ultimo paso
  python3 scripts/paso.py ROM SESION --volver N [ORDEN ...]  # retoma desde el paso N

SESION es una carpeta: guarda NNN.png (captura al final de cada paso), NNN-a.png, NNN-b.png...
(capturas pedidas con 'f' a mitad del paso), NNN.st.gz (estado) y registro.txt.

Cada ORDEN es un argumento entre comillas:
  "A w60 DOWN*2 f A"     botones (A B UP DOWN LEFT RIGHT L R START SELECT), esperas en cuadros
                         (w60 = 1 segundo), repeticiones (DOWN*2) y 'f' = captura en ese momento
  "mano:Nombre exacto"   lleva el cursor a esa carta de mi mano (sin menus abiertos)
  "cursor:X,Y"           lleva el cursor a la columna X de la fila Y (0 mano, 1 magias y trampas,
                         2 mis monstruos, 3 monstruos del rival, 4 magias y trampas del rival)
  "w8:DIR=VALOR"         ayuda de prueba: escribe un byte en memoria (hexadecimal); queda anotado

Nunca escribe sobre el ROM ni sobre el estado de partida.
"""
import gzip
import os
import sys
import tempfile

import escenario
from da_lib import Rom
from duelo_auto import CURSOR, Duelo, J0, J1
from gba import BOTONES, GBA

FILAS = {0: "mi mano", 1: "mis magias y trampas", 2: "mis monstruos", 3: "monstruos del rival",
         4: "magias y trampas del rival"}


class ErrorPaso(Exception):
    pass


def abrir(ruta_rom, datos):
    d = Duelo.__new__(Duelo)                 # sin el arranque de Duelo: el estado ya viene dado
    d.rom = Rom(ruta_rom)
    d.g = GBA(ruta_rom, dir_guardado=tempfile.mkdtemp(prefix="da_"))
    d.g.correr(2)
    d.g.cargar_estado(datos)
    d.g.correr(1)
    return d


def pasos(sesion):
    return sorted(int(f[:3]) for f in os.listdir(sesion) if f.endswith(".st.gz") and f[:3].isdigit())


def leer_paso(sesion, n):
    ruta = os.path.join(sesion, f"{n:03d}.st.gz")
    if not os.path.exists(ruta):
        raise ErrorPaso(f"no existe el paso {n} en {sesion}")
    with gzip.open(ruta, "rb") as f:
        return f.read()


def validar(orden):
    """Falla antes de tocar nada si la orden no se entiende."""
    if orden.startswith(("mano:", "cursor:", "w8:")):
        if orden.startswith("cursor:"):
            x, sep, y = orden[7:].partition(",")
            if not (sep and x.isdigit() and y.isdigit()):
                raise ErrorPaso(f"se esperaba cursor:X,Y y llego {orden!r}")
        if orden.startswith("w8:"):
            dire, sep, valor = orden[3:].partition("=")
            try:
                int(dire, 16), int(valor, 16)
            except ValueError:
                raise ErrorPaso(f"se esperaba w8:DIRECCION=VALOR en hexadecimal y llego {orden!r}")
        return
    for t in orden.split():
        boton, _, veces = t.partition("*")
        if t == "f" or (t[0] == "w" and t[1:].isdigit()):
            continue
        if boton not in BOTONES or (veces and not veces.isdigit()):
            raise ErrorPaso(f"no entiendo {t!r} en la orden {orden!r}")


def mano_en_orden(d, lado):
    base = J1 if lado else J0
    m = dict(d.mano(lado))
    return [m.get(s & 0x7F, "?") for s in d.g.leer(base + 0x2824, len(m))]     # bit 7 = lado


def describir(d):
    s = escenario.instantanea(d)
    x, y, i = d.cursor()
    out = [f"LP: yo {s['LP'][0]} | rival {s['LP'][1]}",
           f"cursor: columna {x}, fila {y} ({FILAS.get(y, '?')}), indice en la mano {i}"
           f" | carta bajo el cursor: {d.rom.nombre(d.g.r16(0x02019F0C)) if 0 < d.g.r16(0x02019F0C) <= 1200 else '-'}"
           f" | evento {d.tipo_evento():#x}"]
    for lado, quien in ((0, "yo"), (1, "rival")):
        monstruos = [f"{n} ({pos}, ATK {atk}, DEF {de})" for n, pos, atk, de in s[f"campo_{quien}"]]
        out.append(f"{quien}: mano {mano_en_orden(d, lado)}")
        out.append(f"    monstruos {monstruos} | magias y trampas {s[f'magias_{quien}']}")
        out.append(f"    cementerio {s[f'cementerio_{quien}']} | retiradas {s[f'retiradas_{quien}']}"
                   f" | mazo {s[f'mazo_{quien}']}")
    return "\n".join(out)


def ejecutar(d, orden, foto):
    if orden.startswith("mano:"):
        d.ir_mano(orden[5:])
    elif orden.startswith("cursor:"):
        x, y = (int(v) for v in orden[7:].split(","))
        if not (d.mover(y=y) and d.mover(x=x)):
            raise ErrorPaso(f"el cursor no llego a {x},{y}; quedo en {d.cursor()[:2]}")
    elif orden.startswith("w8:"):
        dire, valor = (int(v, 16) for v in orden[3:].split("="))
        d.g.w8(dire, valor)
    else:
        for t in orden.split():
            if t == "f":
                foto()
            elif t[0] == "w" and t[1:].isdigit():
                d.g.correr(int(t[1:]))
            else:
                boton, _, veces = t.partition("*")
                for _ in range(int(veces or 1)):
                    d.g.apretar(boton, mantener=4, soltar=20)


def jugar(ruta_rom, datos, ordenes, al_fotografiar=None):
    """Carga el estado 'datos', corre las ordenes y deja el duelo donde quedo. Devuelve (duelo, error).
    Lo usan este script y repetir_sesion.py, que tiene que contar los cuadros exactamente igual."""
    d = abrir(ruta_rom, datos)

    def foto():
        d.g.correr(2)
        if al_fotografiar:
            al_fotografiar(d)

    error = None
    try:
        for o in ordenes:
            ejecutar(d, o, foto)
    except (ErrorPaso, AssertionError, RuntimeError) as err:
        error = str(err)                     # se guarda igual donde quedo, para poder mirar
    d.g.correr(2)
    return d, error


def main(argv):
    if len(argv) < 3 or not os.path.exists(argv[0]):
        raise SystemExit(__doc__)
    ruta_rom, sesion, resto = argv[0], argv[1], argv[2:]
    os.makedirs(sesion, exist_ok=True)
    hechos = pasos(sesion)
    desde = None
    if resto[0] == "--desde":
        if len(resto) < 2 or not os.path.exists(resto[1]):
            raise ErrorPaso("--desde necesita un estado que exista")
        desde, ordenes = resto[1], resto[2:]
        datos, origen = open(desde, "rb").read(), f"estado {desde}"
    elif resto[0] == "--volver":
        if len(resto) < 2 or not resto[1].isdigit():
            raise ErrorPaso("--volver necesita el numero de paso")
        datos, origen, ordenes = leer_paso(sesion, int(resto[1])), f"paso {int(resto[1])}", resto[2:]
    else:
        if not hechos:
            raise ErrorPaso("la sesion esta vacia: empezala con --desde ESTADO")
        datos, origen, ordenes = leer_paso(sesion, hechos[-1]), f"paso {hechos[-1]}", resto
    for o in ordenes:
        validar(o)

    n = (hechos[-1] + 1) if hechos else 0
    fotos = []

    def guardar_foto(d):
        ruta = os.path.join(sesion, f"{n:03d}-{chr(ord('a') + len(fotos))}.png")
        d.g.imagen(2).save(ruta)
        fotos.append(ruta)

    d, error = jugar(ruta_rom, datos, ordenes, guardar_foto)
    final = os.path.join(sesion, f"{n:03d}.png")
    d.g.imagen(2).save(final)
    with gzip.open(os.path.join(sesion, f"{n:03d}.st.gz"), "wb", compresslevel=3) as f:
        f.write(d.g.guardar_estado())
    texto = describir(d)
    cabecera = f"paso {n} (desde {origen}): {' | '.join(ordenes) if ordenes else 'sin ordenes'}"
    with open(os.path.join(sesion, "registro.txt"), "a", encoding="utf-8") as f:
        f.write(f"{cabecera}\n{'ERROR: ' + error + chr(10) if error else ''}{texto}\n\n")
    print(cabecera)
    if error:
        print(f"ERROR en una orden (el paso se guardo donde quedo): {error}")
    print(texto)
    print("capturas: " + ", ".join(fotos + [final]))


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except (ErrorPaso, escenario.ErrorEscenario) as err:
        raise SystemExit(f"error: {err}")
