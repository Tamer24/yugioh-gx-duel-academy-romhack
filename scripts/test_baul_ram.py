"""Prueba, en el emulador de verdad, que las cartas del baul ampliado (indice > 1200) sobreviven
arrancar, Continue, recorrer los menus, guardar y volver a arrancar.

Por que existe: test_ampliado.py corre la funcion de guardar y la de cargar sueltas, y no vio que el
juego pone en cero 0x0202B0C0-0x020350BF al arrancar y 0x0202B0C0-0x0203A8BF al elegir Continue
(donde estaba el bloque antes de 2026-10-13): las cartas ampliadas se perdian en cada sesion.

Uso: python3 scripts/test_baul_ram.py ROM.gba PARTIDA.sav
(no escribe el .sav; la SRAM vive en la memoria del emulador)

Teclas del menu principal: DOWN A abre Save y LEFT es "Yes" (UP o RIGHT cancelan).
"""
import ctypes as C
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(__file__))
import ampliar
from gba import GBA

EXT_SRAM = 0x6200
fallos = 0


def ok(nombre, cond, detalle=""):
    global fallos
    print(("  ok   " if cond else "  FALLA"), nombre, detalle)
    fallos += 0 if cond else 1


def arrancar(rom, sram):
    g = GBA(rom)
    n = g.lib.retro_get_memory_size(0)
    p = g.lib.retro_get_memory_data(0)
    C.memmove(p, bytes(sram) + bytes([255]) * (n - len(sram)), n)
    g.lib.retro_reset()
    return g


def sram_de(g):
    return C.string_at(g.lib.retro_get_memory_data(0), 0x8000)


def pulsar(g, *teclas, espera=40):
    for t in teclas:
        g.apretar(t)
        g.correr(espera)


def continuar(g):
    g.correr(300)
    for _ in range(6):                      # START / A hasta pasar el titulo
        g.apretar("START")
        g.correr(25)
        g.apretar("A")
        g.correr(60)
    g.apretar("A")
    g.correr(150)
    for _ in range(4):                      # el ultimo A abre el baul: B vuelve al menu principal
        g.apretar("B")
        g.correr(40)
    g.correr(60)


def bloque_ram(g):
    """{indice: (u16 +0, u16 +4, u32 +8)} de las cartas ampliadas que el juego tiene en memoria."""
    d = g.leer(ampliar.EXT, 12 * ampliar.EXTRA)
    return {1201 + k: (struct.unpack_from("<H", d, 12 * k)[0], struct.unpack_from("<H", d, 12 * k + 4)[0],
                       struct.unpack_from("<I", d, 12 * k + 8)[0]) for k in range(ampliar.EXTRA)}


def bloque_sram(sram):
    out = {}
    for k in range(ampliar.EXTRA):
        o = EXT_SRAM + 4 + 8 * k
        out[1201 + k] = (struct.unpack_from("<H", sram, o)[0], struct.unpack_from("<H", sram, o + 2)[0],
                         struct.unpack_from("<I", sram, o + 4)[0])
    return out


def main():
    rom, ruta = sys.argv[1], sys.argv[2]
    sav = open(ruta, "rb").read()
    esperado = bloque_sram(sav)
    con = sum(1 for v in esperado.values() if (v[1] >> 3) & 0xFF)
    print(f"partida: {con} cartas ampliadas con copias; bloque en RAM {ampliar.BLOQUE:#010x}")
    ok("la partida de prueba trae cartas ampliadas", con > 0)

    print("1. arrancar y Continue")
    g = arrancar(rom, sav)
    g.correr(300)
    ok("tras el titulo el bloque en RAM es el de la SRAM", bloque_ram(g) == esperado)
    continuar(g)
    ok("tras Continue sigue igual", bloque_ram(g) == esperado)

    print("2. sumar una copia en RAM, guardar (desde el menu principal) y volver a arrancar")
    k = next(i for i, v in esperado.items() if (v[1] >> 3) & 0xFF == 0)        # una carta que no tengo
    base = ampliar.EXT + 12 * (k - 1201)
    g.w16(base + 4, (2 << 3) | 2)
    g.w32(base + 8, 0x1234)
    pulsar(g, "DOWN", "A", "LEFT", "A")
    g.correr(400)
    sram = sram_de(g)
    nuevo = bloque_sram(sram)
    ok(f"la carta {k} quedo guardada con 2 copias", (nuevo[k][1] >> 3) & 0xFF == 2 and nuevo[k][2] == 0x1234, str(nuevo[k]))
    resto = {i: v for i, v in esperado.items() if i != k}
    ok("las demas cartas ampliadas siguen igual en la SRAM", all(nuevo[i] == v for i, v in resto.items()))
    g2 = arrancar(rom, sram)
    continuar(g2)
    ok("reiniciando con esa SRAM el bloque vuelve completo", bloque_ram(g2) == nuevo)

    esperado = nuevo
    print("3. recorrer los menus (el bloque guardado no cambia)")
    for ruta_icono in ("", "RIGHT", "DOWN", "DOWN LEFT", "LEFT", "UP", "UP RIGHT", "UP LEFT"):
        pulsar(g, *ruta_icono.split(), espera=25)
        g.correr(40)
        pulsar(g, "A", espera=200)
        pulsar(g, "A", "A", "A", espera=90)
        pulsar(g, "B", "B", "B", "B", "B", espera=60)
        ok(f"icono '{ruta_icono or 'centro'}': el bloque no cambia", bloque_ram(g) == esperado)

    print("\nFALLARON" if fallos else "\ntodo en orden", fallos or "")
    sys.exit(1 if fallos else 0)


main()
