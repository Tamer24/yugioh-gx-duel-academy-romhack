"""Prueba de scripts/arte.py: el conversor de dibujos (PNG <-> formato del ROM).

Ida y vuelta con dibujos del propio juego: se lee el arte de una carta, se convierte como si
fuera un PNG nuevo y se vuelve a leer. Lo esperado sale del formato (80x80, 64 colores):
  - un dibujo que usa 63 colores o menos tiene que volver identico, pixel por pixel;
  - uno que usa los 64 pierde un color (el indice 0 se reserva): la diferencia tiene que ser chica;
  - el indice 0 no se usa y la paleta trae ahi el marcador 0x83E0;
  - una imagen de otro tamano o no cuadrada se acepta y sale de 80x80;
  - el dibujo chico (32x32, el de los sobres) sale del grande y se parece al del juego.
Tambien escribe un dibujo en una copia del ROM en memoria y comprueba que solo cambian los
bytes de esa carta.

Uso: python3 test_arte.py rom.gba
"""
import struct
import sys

from PIL import Image, ImageChops

import arte
from da_lib import ARTE, MINI_ARTE, MINI_PALETAS, PALETAS, Rom


def colores_usados(rom, i):
    return len(set(rom.d[ARTE + 6400 * i:ARTE + 6400 * (i + 1)]))


def main():
    rom = Rom(sys.argv[1])
    indices = {rom.nombre(i): i for i in range(1, 1201)}
    ok = True

    def caso(nombre, bien, detalle=""):
        nonlocal ok
        print(f"{'OK ' if bien else 'MAL'} {nombre}{': ' + detalle if detalle else ''}")
        ok = ok and bien

    for carta in ("Sangan", "Blue-Eyes White Dragon", "Mechanicalchaser", "Dian Keto the Cure Master"):
        i = indices[carta]
        original = arte.leer(rom, i)
        paleta, tiles = arte.convertir(original)
        vuelta = arte.decodificar(paleta, tiles)
        usados = colores_usados(rom, i)
        dif = ImageChops.difference(original, vuelta)
        maximo = max(v for banda in dif.getextrema() for v in banda)
        crudo = dif.tobytes()
        distintos = sum(1 for k in range(0, len(crudo), 3) if crudo[k:k + 3] != b"\0\0\0")
        if usados <= 63:
            caso(f"{carta} ({usados} colores): vuelve identico", maximo == 0, f"diferencia maxima {maximo}")
        else:
            caso(f"{carta} ({usados} colores): pierde un color, diferencia chica",
                 maximo <= 48 and distintos <= 640, f"diferencia maxima {maximo} en {distintos} de 6400 pixeles")
        caso(f"{carta}: no usa el indice 0 y deja ahi el marcador",
             0 not in set(tiles) and struct.unpack_from("<H", paleta)[0] == arte.MARCADOR and max(tiles) <= 63)

    grande = arte.leer(rom, indices["Sangan"]).resize((400, 400), Image.NEAREST)
    paleta, tiles = arte.convertir(grande)
    caso("imagen de 400x400: sale de 80x80 e identica a la original",
         ImageChops.difference(arte.decodificar(paleta, tiles), arte.leer(rom, indices["Sangan"])).getbbox() is None)
    rara = arte.decodificar(*arte.convertir(arte.leer(rom, indices["Sangan"]).resize((137, 137), Image.LANCZOS)))
    dif = ImageChops.difference(rara, arte.leer(rom, indices["Sangan"]))
    caso("imagen de 137x137 (no es multiplo): sale de 80x80 y parecida",
         rara.size == (80, 80) and sum(dif.convert("L").tobytes()) / 6400 < 24,
         f"diferencia media {sum(dif.convert('L').tobytes()) / 6400:.1f} sobre 255")
    ancha = Image.new("RGB", (200, 80), (255, 0, 0))
    ancha.paste(arte.leer(rom, indices["Sangan"]), (60, 0))
    paleta, tiles = arte.convertir(ancha)
    caso("imagen de 200x80: se recorta al centro",
         ImageChops.difference(arte.decodificar(paleta, tiles), arte.leer(rom, indices["Sangan"])).getbbox() is None)

    antes = bytes(rom.d)
    destino = indices["Mechanicalchaser"]
    arte.escribir(rom, destino, arte.leer(rom, indices["Sangan"]))
    cambiados = [k for k in range(len(antes)) if antes[k] != rom.d[k]]
    en_carta = all(PALETAS + 128 * destino <= k < PALETAS + 128 * (destino + 1)
                   or ARTE + 6400 * destino <= k < ARTE + 6400 * (destino + 1)
                   or MINI_PALETAS + 64 * destino <= k < MINI_PALETAS + 64 * (destino + 1)
                   or MINI_ARTE + 1024 * destino <= k < MINI_ARTE + 1024 * (destino + 1) for k in cambiados)
    caso("escribir en el ROM: solo cambian las paletas y los dibujos (grande y chico) de esa carta",
         bool(cambiados) and en_carta, f"{len(cambiados)} bytes")
    # el dibujo chico que arma el conversor tiene que parecerse al que trae el juego para ese dibujo
    dif = ImageChops.difference(arte.leer_mini(rom, destino), arte.leer_mini(rom, indices["Sangan"]))
    media = sum(dif.convert("L").tobytes()) / 1024
    caso("escribir en el ROM: el dibujo chico sale parecido al del juego", media < 24,
         f"diferencia media {media:.1f} sobre 255")
    caso("escribir en el ROM: la carta muestra el dibujo nuevo",
         ImageChops.difference(arte.leer(rom, destino), arte.leer(rom, indices["Sangan"])).getbbox() is None)
    try:
        arte.escribir(rom, 0, grande)
        caso("indice 0: se rechaza", False)
    except arte.ErrorArte:
        caso("indice 0: se rechaza", True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
