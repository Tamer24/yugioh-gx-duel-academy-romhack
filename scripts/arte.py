"""Arte de las cartas: del ROM a PNG y de PNG al formato del ROM.

Formato en el ROM (da_lib.ARTE y da_lib.PALETAS, una entrada por indice de carta):
  arte     6400 bytes: 80x80 pixeles de 8 bits, en 100 tiles de 8x8 (10 por fila); cada tile
           son sus 64 pixeles por filas. El valor es un indice de 0 a 63 en la paleta.
  paleta   64 colores de 16 bits, BGR555 (5 bits por canal, rojo en los bits bajos).
En las cartas del juego que no usan el indice 0, la paleta trae ahi 0x83E0 (verde marcador):
el conversor hace lo mismo y reparte la imagen en los indices 1 a 63.

Cada carta tiene ademas un dibujo chico (da_lib.MINI_ARTE y da_lib.MINI_PALETAS), el que se ve al
abrir un sobre: 32x32 en 16 tiles de 8x8 (1024 bytes) y 32 colores (64 bytes), todos utiles.
escribir() lo saca del dibujo grande: no hace falta otro PNG.

Uso (desde la raiz del proyecto):
  python3 scripts/arte.py extraer ROM CARTA salida.png [--escala 4]
  python3 scripts/arte.py mini ROM CARTA salida.png [--escala 4]      el dibujo chico
  python3 scripts/arte.py vista entrada.png salida.png [--escala 4]   como quedaria en el juego
CARTA es el nombre exacto o el indice (1..1200).

En una receta, la clave "arte" de una carta ("arte": "arte/kunai.png", relativa a la carpeta del
proyecto) hace que restaurar.py escriba ese dibujo en el hueco. Cualquier tamano sirve: se
recorta al centro en cuadrado y se lleva a 80x80.
"""
import struct
import sys

from PIL import Image

from da_lib import Rom

LADO, TILE, COLORES = 80, 8, 64
BYTES_ARTE, BYTES_PALETA = LADO * LADO, COLORES * 2
MARCADOR = 0x83E0             # lo que traen en el indice 0 las cartas del juego que no lo usan
MINI_LADO, MINI_COLORES = 32, 32
BYTES_MINI, BYTES_MINI_PALETA = MINI_LADO * MINI_LADO, MINI_COLORES * 2


class ErrorArte(Exception):
    pass


def decodificar(paleta, tiles, lado=LADO, n_colores=COLORES):
    """Bytes del ROM -> imagen RGB de 80x80 (o de 32x32 con lado y n_colores del dibujo chico)."""
    if len(paleta) != n_colores * 2 or len(tiles) != lado * lado:
        raise ErrorArte(f"la paleta tiene que medir {n_colores * 2} bytes y el arte {lado * lado}")
    colores = []
    for c in struct.unpack(f"<{n_colores}H", paleta):
        colores.append(tuple(((c >> d) & 0x1F) * 255 // 31 for d in (0, 5, 10)))
    img = Image.new("RGB", (lado, lado))
    px = img.load()
    por_fila = lado // TILE
    for t in range(por_fila * por_fila):
        x0, y0 = (t % por_fila) * TILE, (t // por_fila) * TILE
        for k in range(TILE * TILE):
            v = tiles[t * TILE * TILE + k]
            if v >= n_colores:
                raise ErrorArte(f"indice de color fuera de la paleta: {v}")
            px[x0 + k % TILE, y0 + k // TILE] = colores[v]
    return img


def leer(rom, indice):
    """Imagen de la carta 'indice' del ROM."""
    return decodificar(bytes(rom.d[rom.PALETAS + BYTES_PALETA * indice:rom.PALETAS + BYTES_PALETA * (indice + 1)]),
                       bytes(rom.d[rom.ARTE + BYTES_ARTE * indice:rom.ARTE + BYTES_ARTE * (indice + 1)]))


def leer_mini(rom, indice):
    """Dibujo chico (32x32) de la carta 'indice' del ROM."""
    return decodificar(bytes(rom.d[rom.MINI_PALETAS + BYTES_MINI_PALETA * indice:rom.MINI_PALETAS + BYTES_MINI_PALETA * (indice + 1)]),
                       bytes(rom.d[rom.MINI_ARTE + BYTES_MINI * indice:rom.MINI_ARTE + BYTES_MINI * (indice + 1)]),
                       MINI_LADO, MINI_COLORES)


def _a_bytes(q, lado, n_colores, primero):
    """Imagen ya reducida a una paleta -> (colores BGR555, tiles); 'primero' es el indice del primer color."""
    pal = q.getpalette()[:3 * n_colores]
    pal += [0] * (3 * n_colores - len(pal))
    colores = []
    for k in range(n_colores):
        r, g, b = ((pal[3 * k + c] * 31 + 127) // 255 for c in range(3))
        colores.append(r | (g << 5) | (b << 10))
    px = q.load()
    tiles = bytearray(lado * lado)
    por_fila = lado // TILE
    for t in range(por_fila * por_fila):
        x0, y0 = (t % por_fila) * TILE, (t // por_fila) * TILE
        for k in range(TILE * TILE):
            tiles[t * TILE * TILE + k] = px[x0 + k % TILE, y0 + k // TILE] + primero
    return colores, bytes(tiles)


def _a_consola(img):
    """A 5 bits por canal antes de elegir colores: es la precision que tiene la consola."""
    return img.point(lambda v: (v * 31 + 127) // 255 * 255 // 31)


def convertir_mini(grande):
    """Dibujo de 80x80 (PIL.Image) -> (paleta de 64 bytes, dibujo chico de 1024 bytes)."""
    img = _a_consola(grande.convert("RGB").resize((MINI_LADO, MINI_LADO), Image.LANCZOS))
    q = img.quantize(colors=MINI_COLORES, method=Image.MEDIANCUT, dither=Image.NONE)
    colores, tiles = _a_bytes(q, MINI_LADO, MINI_COLORES, 0)
    return struct.pack(f"<{MINI_COLORES}H", *colores), tiles


def convertir(imagen):
    """Imagen (ruta o PIL.Image) -> (paleta de 128 bytes, arte de 6400 bytes)."""
    img = Image.open(imagen) if isinstance(imagen, str) else imagen
    img = img.convert("RGB")
    ancho, alto = img.size
    if ancho < 8 or alto < 8:
        raise ErrorArte(f"la imagen es demasiado chica: {ancho}x{alto}")
    if ancho != alto:                                  # recorte cuadrado al centro
        lado = min(ancho, alto)
        x, y = (ancho - lado) // 2, (alto - lado) // 2
        img = img.crop((x, y, x + lado, y + lado))
    if img.size != (LADO, LADO):
        # un multiplo exacto (un dibujo de 80x80 ampliado) se reduce promediando cada bloque, que
        # devuelve el original; el resto, con Lanczos
        exacto = img.size[0] % LADO == 0
        img = img.resize((LADO, LADO), Image.BOX if exacto else Image.LANCZOS)
    q = _a_consola(img).quantize(colors=COLORES - 1, method=Image.MEDIANCUT, dither=Image.NONE)
    colores, tiles = _a_bytes(q, LADO, COLORES - 1, 1)
    return struct.pack(f"<{COLORES}H", MARCADOR, *colores), tiles


def escribir(rom, indice, imagen):
    """Pone 'imagen' como dibujo de la carta 'indice' del ROM (da_lib.Rom, se modifica): el grande
    y, sacado de el, el chico."""
    if not 1 <= indice <= rom.CAPACIDAD:
        raise ErrorArte(f"indice de carta fuera de rango: {indice}")
    paleta, tiles = convertir(imagen)
    rom.d[rom.PALETAS + BYTES_PALETA * indice:rom.PALETAS + BYTES_PALETA * (indice + 1)] = paleta
    rom.d[rom.ARTE + BYTES_ARTE * indice:rom.ARTE + BYTES_ARTE * (indice + 1)] = tiles
    paleta, tiles = convertir_mini(decodificar(paleta, tiles))
    rom.d[rom.MINI_PALETAS + BYTES_MINI_PALETA * indice:rom.MINI_PALETAS + BYTES_MINI_PALETA * (indice + 1)] = paleta
    rom.d[rom.MINI_ARTE + BYTES_MINI * indice:rom.MINI_ARTE + BYTES_MINI * (indice + 1)] = tiles


def _indice(rom, carta):
    if carta.isdigit():
        i = int(carta)
        if not 1 <= i <= rom.n:
            raise ErrorArte(f"indice de carta fuera de rango: {carta}")
        return i
    for i in range(1, rom.n + 1):
        if rom.nombre(i) == carta:
            return i
    raise ErrorArte(f"la carta {carta!r} no existe en el ROM")


def main(argv):
    escala = 1
    if "--escala" in argv:
        k = argv.index("--escala")
        escala = int(argv[k + 1])
        argv = argv[:k] + argv[k + 2:]
    if len(argv) == 4 and argv[0] in ("extraer", "mini"):
        rom = Rom(argv[1])
        img = (leer if argv[0] == "extraer" else leer_mini)(rom, _indice(rom, argv[2]))
    elif len(argv) == 3 and argv[0] == "vista":
        img = decodificar(*convertir(argv[1]))
    else:
        raise SystemExit(__doc__)
    if escala > 1:
        img = img.resize((img.size[0] * escala, img.size[1] * escala), Image.NEAREST)
    img.save(argv[-1])
    print(f"{argv[-1]}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except (ErrorArte, OSError) as err:
        raise SystemExit(f"error: {err}")
