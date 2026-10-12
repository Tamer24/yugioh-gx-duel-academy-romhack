"""Corredor de pruebas automaticas para Magicas (sin ventana).

Por cada carta: parte de estados/duelo-inicio.ss1, la pone en la mano (en la ranura
de una Magica), ejecuta una preparacion, abre su menu, la activa y observa el duelo
sin tocar nada hasta que se estabiliza. Clasifica el resultado:

  NO OFRECE ACTIVAR   el menu solo trae Set / Detail Screen (falla la condicion)
  NO HACE NADA        solo se mueve la propia carta (mano -> campo -> cementerio)
  QUEDA SIN RESOLVER  la carta sigue boca arriba en el campo: el efecto no termina
  CAMBIA              algo mas se modifico: LP, mazo, manos, campo, cementerios

Uso: python3 probar_magicas.py rom.gba [NOMBRE ...] [--fotos carpeta]
"""
import os
import struct
import sys
import tempfile

import estado
from duelo_auto import Duelo, J0, J1

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "..", "estados", "duelo-inicio.ss1")
POS_MAGICA = 5          # posicion de la mano que ocupa Monster Reincarnation (una Magica)
BORDE_MENU = (41, 40, 41)

# nombre -> (indice de carta, preparacion, monstruos propios que hacen falta en el campo)
# preparaciones: "invocar:Nombre" (Normal Summon), "turno" (termina turno, juega el rival)
# El rival ataca en su turno: se invoca primero el monstruo mas fuerte para que sobreviva.
# Condicion de Chosen One (fn_10): un monstruo invocable y 2 Magicas/Trampas en la mano.
MANO_EXTRA = {"Chosen One": {4: 1065}}      # pos. 4 pasa a ser Monster Reincarnation (Magica)
CARTAS = {
    "Chosen One": (70, [], 0),
    "Reasoning": (508, [], 0),
    "Monster Recovery": (227, ["invocar:Blazing Inpachi"], 1),
    "Riryoku": (487, ["invocar:Blazing Inpachi", "turno", "invocar:Needle Worm"], 2),
}


def estado_con(indice, extra=None):
    """Estado de duelo con la carta en la mano. 'extra': {posicion: indice} cambia otras
    cartas de la mano (por ejemplo, para cumplir la condicion de activacion)."""
    e = estado.abrir(BASE)
    estado.comprobar(e)
    struct.pack_into("<H", e, estado.ranura_mano(e, 0, POS_MAGICA) + 0x24, indice)
    for pos, idx in (extra or {}).items():
        struct.pack_into("<H", e, estado.ranura_mano(e, 0, pos) + 0x24, idx)
    struct.pack_into("<H", e, estado.WRAM + 0x19F0C, indice)         # carta bajo el cursor
    f = tempfile.NamedTemporaryFile(suffix=".st", delete=False)
    f.write(e)
    f.close()
    return f.name


def opciones_menu(d):
    """Cantidad de opciones del menu de carta abierto (3 = Activate/Set/Detail)."""
    im = d.g.imagen(1).convert("RGB")
    for y in range(36, 100):
        if im.getpixel((160, y)) == BORDE_MENU and im.getpixel((160, y + 4)) == (0, 0, 0):
            return round((100 - y) / 16)
    return 0


def mazo(d, lado):
    return (d.g.r16((J0, J1)[lado] + 0x1C) & 0x1FFF) >> 6


def instantanea(d):
    z = d.zona
    return {
        "LP": d.lp(),
        "mano": sorted(n for s, n in d.mano(0)),
        "mano_rival": len(d.mano(1)),
        "mazo": mazo(d, 0), "mazo_rival": mazo(d, 1),
        "campo": sorted(n for s, n in z(0, "05a")), "campo_rival": sorted(n for s, n in z(1, "05a")),
        "cementerio": sorted(n for s, n in z(0, "d")), "cementerio_rival": sorted(n for s, n in z(1, "d")),
        "retiradas": sorted(n for s, n in z(0, "e")), "retiradas_rival": sorted(n for s, n in z(1, "e")),
    }


def sin_la_carta(a, carta):
    """Instantanea sin contar el movimiento de la propia carta."""
    out = dict(a)
    for k in ("mano", "campo", "cementerio", "retiradas"):
        out[k] = [n for n in a[k] if n != carta]
    return out


def preparar(d, prep):
    primero = True
    for paso in prep:
        if paso.startswith("invocar:"):
            d.ir_mano(paso.split(":", 1)[1])
            d.menu(0)                       # 1a opcion: Summon
            d.g.correr(90)
            d.tecla("DOWN", 20)             # "You Summoned a monster. Activate...?": No
            d.tecla("A", 60)
        elif paso == "turno":
            d.fin_turno(primero=primero)
            primero = False
            d.pasar_rival()
            d.g.correr(150)


def correr(ruta_rom, nombre, indice, prep, requisito=0, fotos=None):
    d = Duelo(ruta_rom, estado=estado_con(indice, MANO_EXTRA.get(nombre)))
    d.g.correr(30)
    preparar(d, prep)
    antes = instantanea(d)
    if len(antes["campo"]) < requisito:
        return antes, antes, 0, f"PREPARACION FALLIDA (campo: {antes['campo']}, hacen falta {requisito})", 0
    d.ir_mano(nombre)
    d.tecla("A", 60)
    n = opciones_menu(d)
    if fotos:
        d.foto(os.path.join(fotos, f"{nombre}_menu.png"))
    if n < 3:
        d.tecla("B", 30)
        return antes, antes, n, "NO OFRECE ACTIVAR", 0
    for _ in range(n - 1):
        d.tecla("UP", 25)
    d.tecla("A", 10)
    # observar sin tocar; si queda quieto, se asume que espera una confirmacion
    quieto, pulsaciones, ultimo = 0, 0, None
    for k in range(60):
        d.g.correr(40)
        ahora = instantanea(d)
        quieto = quieto + 1 if ahora == ultimo else 0
        ultimo = ahora
        if quieto >= 8:
            if pulsaciones >= 6:
                break
            d.tecla("A", 20)
            pulsaciones += 1
            quieto = 0
    despues = instantanea(d)
    if fotos:
        d.foto(os.path.join(fotos, f"{nombre}_final.png"))
    cambio = sin_la_carta(antes, nombre) != sin_la_carta(despues, nombre)
    if nombre in despues["campo"] and nombre not in despues["cementerio"]:
        veredicto = "QUEDA SIN RESOLVER"
    else:
        veredicto = "CAMBIA" if cambio else "NO HACE NADA"
    return antes, despues, n, veredicto, pulsaciones


def main():
    args = sys.argv[1:]
    fotos = None
    if "--fotos" in args:
        i = args.index("--fotos")
        fotos = args[i + 1]
        os.makedirs(fotos, exist_ok=True)
        del args[i:i + 2]
    ruta_rom, nombres = args[0], args[1:] or list(CARTAS)
    resumen = []
    for nombre in nombres:
        indice, prep, requisito = CARTAS[nombre]
        print(f"=== {nombre} (indice {indice}); preparacion: {prep or 'ninguna'}")
        try:
            antes, despues, n, veredicto, pulsos = correr(ruta_rom, nombre, indice, prep, requisito, fotos)
        except Exception as e:
            print(f"   ERROR: {type(e).__name__}: {e}")
            resumen.append((nombre, "ERROR"))
            continue
        print(f"   opciones del menu: {n} | confirmaciones necesarias: {pulsos}")
        for k in antes:
            if antes[k] != despues[k] and k not in ("mano", "campo", "cementerio", "retiradas"):
                print(f"   {k}: {antes[k]} -> {despues[k]}")
        for k in ("mano", "campo", "cementerio", "retiradas"):
            a, b = sin_la_carta(antes, nombre)[k], sin_la_carta(despues, nombre)[k]
            if a != b:
                print(f"   {k}: {a} -> {b}")
        print(f"   => {veredicto}")
        resumen.append((nombre, veredicto))
    print("\nRESUMEN")
    for n, v in resumen:
        print(f"  {n:20} {v}")


if __name__ == "__main__":
    main()
