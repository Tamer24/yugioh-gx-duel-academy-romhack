"""Muda la tabla de recetas de fusion y la agranda, para que las cartas de Fusion nuevas se puedan
invocar con Polymerization.

La tabla original (0x17D9678) tiene 80 filas de 16 bytes: u16 ID de la fusion, u16 cantidad de
materiales (2 o 3; 5 para F.G.D.), y por cada material un u16 con su ID y un u16 en cero. Esta
ordenada por ID de la fusion y la busca `card_type_classifier` (0x0804FB3C) por biseccion, con el
tope `movs r4, #0x4F` (0x0804FB66). Termina pegada a otra tabla: no se puede estirar. Este script:
  1. copia las filas al espacio libre (FUSIONES_NUEVA), con las nuevas en su lugar por ID y una fila
     final en cero (como la original);
  2. cambia las 15 direcciones de la tabla que trae el codigo (literales de 4 bytes);
  3. cambia el tope de la biseccion por la cantidad nueva (a lo sumo 255).

Una receta nueva es {"resultado": ID o nombre, "materiales": [ID o nombre, ...]} (2 o 3). Solo
materiales con nombre propio: las que piden "1 monstruo de tipo X" no caben en este formato.

Uso: python3 scripts/ampliar_fusiones.py ROM_ENTRADA ROM_SALIDA recetas.json
"""
import json
import struct
import sys

from da_lib import BASE, EFECTOS_NUEVA, Rom

TABLA = 0x17D9678
FILAS = 80                              # contando la fila final en cero
TOPE_DIR = 0x0804FB66
FUSIONES_NUEVA = 0x1F1F000              # 4 KB al final de la zona de la tabla de efectos
MARCA = b"DA-FUSIONES-1\0\0\0"


def leer(rom):
    return [struct.unpack_from("<8H", rom.d, TABLA + 16 * k) for k in range(FILAS)]


def aplicar(rom, nuevas):
    """Agrega las recetas 'nuevas' (lista de {"resultado", "materiales"}) a la tabla de 'rom'."""
    # El espacio libre del ROM es relleno aleatorio: no se puede pedir que este en cero. Lo que si
    # hay que cuidar es no pisar la tabla de efectos (EFECTOS_NUEVA, a lo sumo 4000 filas).
    assert FUSIONES_NUEVA >= EFECTOS_NUEVA + 16 + 28 * 4000, "la tabla de fusiones pisaria la de efectos"
    assert bytes(rom.d[FUSIONES_NUEVA:FUSIONES_NUEVA + 16]) != MARCA, "la tabla de fusiones ya esta mudada"
    filas = [f for f in leer(rom) if f[0]]                   # sin la fila en cero
    existentes = {f[0] for f in filas}

    def a_id(x):
        if isinstance(x, int):
            return x
        i = next(i for i in range(1, rom.n + 1) if rom.nombre(i) == x)
        return rom.id_de(i)
    for r in nuevas:
        rid = a_id(r["resultado"])
        mats = [a_id(m) for m in r["materiales"]]
        assert rid not in existentes, f"la fusion {rid} ya tiene receta"
        assert rom.indice_de(rid), f"la fusion {rid} no esta en el ROM"
        assert 2 <= len(mats) <= 3, "una receta lleva 2 o 3 materiales"
        for m in mats:
            assert rom.indice_de(m), f"el material {m} no esta en el ROM"
        fila = [rid, len(mats)]
        for m in mats:
            fila += [m, 0]
        fila += [0] * (8 - len(fila))
        filas.append(tuple(fila))
        existentes.add(rid)
    filas.sort(key=lambda f: f[0])
    filas.append((0,) * 8)
    assert len(filas) <= 256, "el tope de la biseccion es un byte"
    cuerpo = b"".join(struct.pack("<8H", *f) for f in filas)
    assert len(cuerpo) <= 0x1000 - 16
    rom.d[FUSIONES_NUEVA:FUSIONES_NUEVA + 16] = MARCA
    destino = FUSIONES_NUEVA + 16
    rom.d[destino:destino + len(cuerpo)] = cuerpo
    # literales del codigo: la direccion de la tabla vieja
    viejo = struct.pack("<I", BASE + TABLA)
    nuevo = struct.pack("<I", BASE + destino)
    cambiados = 0
    o = 0
    while True:
        o = bytes(rom.d[:0x7A8000]).find(viejo, o)
        if o < 0:
            break
        rom.d[o:o + 4] = nuevo
        cambiados += 1
        o += 4
    assert cambiados == 15, f"se esperaban 15 literales de la tabla y hay {cambiados}"
    # tope de la biseccion: movs r4, #imm
    o = TOPE_DIR - BASE
    assert bytes(rom.d[o:o + 2]) == bytes([0x4F, 0x24]), "el tope de la biseccion no es el esperado"
    rom.d[o:o + 2] = bytes([len(filas) - 1, 0x24])
    return len(filas)


def main(entrada, salida, recetas):
    rom = Rom(entrada)
    n = aplicar(rom, json.load(open(recetas, encoding="utf-8")))
    open(salida, "wb").write(rom.d)
    print(f"{salida}: tabla de fusiones con {n} filas en {FUSIONES_NUEVA + 16:07X}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
