"""Lee y edita savestates de mGBA (RAM del juego) para armar bancos de prueba.

Acepta el estado crudo (libretro / .st) o el de mGBA Qt (PNG con el estado en el
fragmento gbAs). Siempre escribe estado crudo, que mGBA carga con
Archivo > Cargar estado desde archivo.

`duelo` y `mano` trabajan sobre un estado guardado DENTRO de un duelo.

AVISO: `resumen` es fiable. `baul` y `mazo` escriben los bytes pero el editor de
mazos del juego no los toma (usa listas y contadores propios); ver PRUEBAS.md.

Uso:
  python3 estado.py duelo estado.st
    Muestra LP y la mano de los dos lados (con los nombres del ROM si se da --rom).
  python3 estado.py mano estado.st salida.st LADO POSICION CARTA
    Cambia la carta que ocupa POSICION (0..n-1) de la mano de LADO (0 jugador,
    1 rival) por la carta de indice CARTA. Conviene reemplazar una carta del mismo
    tipo (Magica por Magica): solo se cambia el indice, no los campos derivados.
  python3 estado.py resumen estado.st
  python3 estado.py baul estado.st salida.st IDX:copias [IDX:copias ...]
    Fija las copias de cada carta (indice 1..1200) en el baul.
  python3 estado.py mazo estado.st salida.st SLOT "Nombre" IDX[:copias] [IDX[:copias] ...]
    SLOT 1..8: mazo del jugador. IDX: indice de carta del juego (1..1200).
    Rellena hasta 40 ciclando los IDX dados; no valida copias contra el baul.
"""
import struct
import sys
import zlib

from da_lib import Rom, MD5_USA

WRAM = 0x21000                 # inicio de la RAM del juego (0x02000000) en el estado crudo
DP = 0x3848
MAZOS = 0x3858                 # 8 mazos de 0xC6 bytes: u16 indices
MAZO_BYTES = 0xC6
CABECERAS = 0x4B08             # 8 de 36 bytes: u8 cantidad, u8 ?, 2 bytes, nombre[32]
CABECERA_BYTES = 36


def abrir(ruta):
    b = open(ruta, "rb").read()
    if b[:8] == b"\x89PNG\r\n\x1a\n":              # estado de mGBA Qt
        o = 8
        while o < len(b):
            n, tipo = struct.unpack_from(">I4s", b, o)
            if tipo == b"gbAs":
                return bytearray(zlib.decompress(b[o + 8:o + 8 + n]))
            o += 12 + n
        raise SystemExit("el PNG no trae un estado gbAs")
    return bytearray(b)


def comprobar(e):
    assert struct.unpack_from("<I", e, 0)[0] & 0xFFFFFF == 7, "version de estado no soportada"
    assert e[0x10:0x1A] == b"YUGIOHGXDA", "no es un estado de Duel Academy"


def u16(e, o): return struct.unpack_from("<H", e, WRAM + o)[0]


def resumen(e):
    print("DP:", struct.unpack_from("<I", e, WRAM + DP)[0])
    for s in range(8):
        h = WRAM + CABECERAS + CABECERA_BYTES * s
        cant, nombre = e[h], bytes(e[h + 4:h + 36]).split(b"\0")[0].decode("latin1")
        idx = [u16(e, MAZOS + MAZO_BYTES * s + 2 * i) for i in range(cant)]
        print(f"mazo {s + 1}: {cant:2} cartas  {nombre!r}  {idx[:12]}{'...' if cant > 12 else ''}")


def copias(e, i):
    return (u16(e, 12 * (i - 1) + 4) >> 3) & 0xFF


def fijar_copias(e, i, n):
    assert 1 <= i <= 1200 and 0 <= n <= 99
    o = WRAM + 12 * (i - 1) + 4
    v = struct.unpack_from("<H", e, o)[0]
    struct.pack_into("<H", e, o, (v & ~(0xFF << 3)) | (n << 3) | 2)     # bit 1: carta nueva


def fijar_mazo(e, slot, nombre, cartas):
    assert 1 <= slot <= 8 and len(cartas) <= 40
    cartas = list(cartas)
    resto = [c for c in cartas for _ in range(1)] or [1]
    while len(cartas) < 40:                      # relleno: ciclar los IDX dados
        cartas.append(resto[len(cartas) % len(resto)])
    base = WRAM + MAZOS + MAZO_BYTES * (slot - 1)
    e[base:base + MAZO_BYTES] = bytes(MAZO_BYTES)
    for i, c in enumerate(cartas):
        struct.pack_into("<H", e, base + 2 * i, c)
    h = WRAM + CABECERAS + CABECERA_BYTES * (slot - 1)
    e[h] = len(cartas)
    e[h + 4:h + 36] = nombre.encode("latin1")[:31].ljust(32, b"\0")


DUELO = 0x22250                # duelo (WRAM): jugador; el rival esta +0x2B08 mas adelante
LADO_BYTES = 0x2B08
MANO = 0x2824                  # lista de ranuras en la mano; byte: bit 7 = lado, 0..6 = ranura
RANURA = 0x50                  # bytes por carta en juego; +0x24 u16 = indice de carta


def cantidad_mano(e, lado):
    b = DUELO + lado * LADO_BYTES
    return ((e[WRAM + b + 0x1C] & 0x3F) << 1) | (e[WRAM + b + 0x1B] >> 7)


def ranura_mano(e, lado, pos):
    """Offset (en el archivo) de la ranura de la carta en la posicion 'pos' de la mano."""
    n = cantidad_mano(e, lado)
    assert 0 <= pos < n, f"la mano de {lado} tiene {n} cartas; posicion {pos} no existe"
    r = e[WRAM + DUELO + lado * LADO_BYTES + MANO + pos]
    return WRAM + DUELO + (r & 0x7F) * RANURA + (r >> 7) * LADO_BYTES


def mostrar_duelo(e, rom=None):
    for lado, nom in ((0, "jugador"), (1, "rival")):
        lp = struct.unpack_from("<I", e, WRAM + DUELO + lado * LADO_BYTES)[0]
        print(f"{nom}: LP={lp}, {cantidad_mano(e, lado)} cartas en mano")
        for pos in range(cantidad_mano(e, lado)):
            idx = struct.unpack_from("<H", e, ranura_mano(e, lado, pos) + 0x24)[0] & 0x7FFF
            print(f"   [{pos}] {idx:4} {rom.nombre(idx) if rom and 0 < idx <= 1200 else ''}")


def main():
    cmd = sys.argv[1]
    e = abrir(sys.argv[2])
    comprobar(e)
    if cmd == "resumen":
        resumen(e)
    elif cmd == "duelo":
        mostrar_duelo(e, Rom(sys.argv[3]) if len(sys.argv) > 3 else None)
    elif cmd == "mano":
        lado, pos, carta = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
        assert lado in (0, 1) and 1 <= carta <= 1200
        o = ranura_mano(e, lado, pos) + 0x24
        antes = struct.unpack_from("<H", e, o)[0]
        struct.pack_into("<H", e, o, (antes & 0x8000) | carta)      # conserva el bit alto
        print(f"mano[{pos}] del lado {lado}: carta {antes & 0x7FFF} -> {carta}")
        open(sys.argv[3], "wb").write(e)
    elif cmd == "baul":
        for a in sys.argv[4:]:
            i, n = a.split(":")
            fijar_copias(e, int(i), int(n))
            print(f"carta {i}: {copias(e, int(i))} copias")
        open(sys.argv[3], "wb").write(e)
    elif cmd == "mazo":
        slot, nombre = int(sys.argv[4]), sys.argv[5]
        cartas = []
        for a in sys.argv[6:]:
            i, _, n = a.partition(":")
            cartas += [int(i)] * int(n or 1)
        fijar_mazo(e, slot, nombre, cartas)
        open(sys.argv[3], "wb").write(e)
        resumen(e)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
