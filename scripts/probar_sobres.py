"""Prueba en pantalla de un sobre de la tienda (sin ventana): lo compra y mira que cartas dio.

Parte de estados/tienda.ss1 (estado de mGBA de Oscar, parado en la tienda sobre el primer sobre,
con 3000 DP y los sobres 0 a 3 en venta). Elige el sobre, pide la cantidad, confirma, pasa la
apertura y sale de la lista. Despues compara la memoria con la de antes:
  - los DP bajan precio x cantidad y lo que queda en venta baja en la cantidad;
  - entran al baul cartas por sobre x cantidad cartas, ninguna otra cosa cambia de cantidad;
  - cada carta que entro esta en las listas de ese sobre (scripts/sobres.py).
En un ROM ampliado las cartas 1201 en adelante se leen de su pedazo de baul aparte.

Uso (desde la raiz del proyecto):
  python3 scripts/probar_sobres.py ROM [SOBRE] [--cuantos 5] [--espera 0] [--capturas PREFIJO]
SOBRE es el nombre o el numero (por defecto el 0) y tiene que estar en venta en ese estado.
--espera cambia cuantos cuadros pasan antes de la primera tecla: da otro sorteo.
--capturas deja PREFIJO-tienda.png y PREFIJO-lista.png.
"""
import os
import sys
import tempfile

import estado
import sobres
from da_lib import N_CARTAS, Rom
from gba import GBA

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ESTADO = os.path.join(RAIZ, "estados", "tienda.ss1")
import ampliar
BAUL, BAUL_APARTE = 0x02000000, ampliar.EXT
DP = 0x02003848
EN_VENTA = 0x02004C08                           # 4 bytes por sobre; la cantidad son los bits 1 a 7
OFRECIDOS = 0x0203B5A8                          # 64 bits: que sobres muestra la tienda


def copias(g, i):
    a = BAUL + 12 * (i - 1) if i <= N_CARTAS else BAUL_APARTE + 12 * (i - N_CARTAS - 1)
    return g.r16(a + 4) >> 3 & 0xFF


def probar(ruta_rom, sobre=0, cuantos=5, espera=0, capturas=None):
    """Devuelve (bien, renglones del informe)."""
    rom = Rom(ruta_rom)
    k = sobres.numero(rom, sobre)
    s = sobres.leer(rom, k)
    g = GBA(ruta_rom, dir_guardado=tempfile.mkdtemp(prefix="da_"))
    g.correr(2)
    g.cargar_estado(bytes(estado.abrir(ESTADO)))
    g.correr(1 + espera)

    def tecla(boton, despues):
        g.apretar(boton)
        g.correr(despues)

    ofrecidos = [j for j in range(sobres.N_SOBRES) if (g.r32(OFRECIDOS + 4 * (j // 32)) >> (j % 32)) & 1]
    if k not in ofrecidos:
        return False, [f"el sobre {k} ({s['nombre']}) no esta en venta en ese estado: estan {ofrecidos}"]
    antes = {i: copias(g, i) for i in range(1, rom.n + 1)}
    dp, en_venta = g.r32(DP), g.r8(EN_VENTA + 4 * k) >> 1
    if cuantos > en_venta or cuantos * s["precio"] > dp:
        return False, [f"no alcanza para {cuantos}: hay {en_venta} en venta y {dp} DP"]
    for _ in range(ofrecidos.index(k)):
        tecla("DOWN", 55)
    for _ in range(cuantos):
        tecla("RIGHT", 12)
    g.correr(20)
    if capturas:
        g.captura(capturas + "-tienda.png")
    tecla("A", 50)                              # "Are you sure?", con el cursor en Yes
    tecla("A", 100)
    for n_a in range(s["cartas_por_sobre"] + 3):  # la apertura; lo que falte lo saltea B
        tecla("A", 50)
        if capturas:
            g.captura(f"{capturas}-a{n_a}.png")
    g.correr(120)
    if capturas:
        g.captura(capturas + "-lista.png")
    for _ in range(4):                          # con un sobre grande la lista abre el filtro: otra B lo cierra
        tecla("B", 100)

    gano = {i: copias(g, i) - antes[i] for i in antes if copias(g, i) != antes[i]}
    en_listas = {c for v in s["listas"].values() for c in v}
    fuera = [rom.nombre(i) for i in gano if rom.id_de(i) not in en_listas]
    informe = [f"sobre {k} ({s['nombre']}) x {cuantos}: DP {dp} -> {g.r32(DP)}, en venta {en_venta} -> "
               f"{g.r8(EN_VENTA + 4 * k) >> 1}, {sum(gano.values())} cartas"]
    informe += [f"  +{n} {rom.nombre(i)} (indice {i})" for i, n in sorted(gano.items())]
    bien = True
    for cumple, queja in (
            (dp - g.r32(DP) == cuantos * s["precio"], "los DP no bajaron precio x cantidad"),
            (en_venta - (g.r8(EN_VENTA + 4 * k) >> 1) == cuantos, "lo que queda en venta no bajo en la cantidad"),
            (sum(gano.values()) == cuantos * s["cartas_por_sobre"] and min(gano.values(), default=0) > 0,
             f"no entraron {cuantos * s['cartas_por_sobre']} cartas al baul"),
            (k == sobres.REGALO or not fuera, f"salieron cartas que no son de ese sobre: {', '.join(fuera)}")):
        if not cumple:
            bien = False
            informe.append("  MAL: " + queja)
    return bien, informe


def main(argv):
    opciones = {"--cuantos": 5, "--espera": 0, "--capturas": None}
    for clave in opciones:
        if clave in argv:
            j = argv.index(clave)
            opciones[clave] = argv[j + 1] if clave == "--capturas" else int(argv[j + 1])
            argv = argv[:j] + argv[j + 2:]
    if not 1 <= len(argv) <= 2:
        raise SystemExit(__doc__)
    bien, informe = probar(argv[0], argv[1] if len(argv) == 2 else 0, opciones["--cuantos"],
                           opciones["--espera"], opciones["--capturas"])
    print("\n".join(informe))
    print("BIEN" if bien else "MAL")
    sys.exit(0 if bien else 1)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except (sobres.ErrorSobres, OSError) as err:
        raise SystemExit(f"error: {err}")
