"""Muda la tabla de efectos al espacio libre y la agranda, para que entren cartas nuevas CON efecto.

La tabla original (0x17D9BEC, 901 filas de 28 bytes, ordenada por ID de Konami) tiene su tamano
escrito en el codigo y termina pegada a otra tabla, asi que no se puede estirar. Este script:
  1. copia las filas al espacio libre (EFECTOS_NUEVA = 0x1F00000, tras una marca y la cantidad);
  2. suma las filas nuevas y mantiene el orden por ID (la busqueda es binaria);
  3. reemplaza la direccion de la tabla en los 13 lugares del codigo que la usan (literales);
  4. cambia el tope de la busqueda (FUN_0806162C, `movs r4,#0xE1; lsls r4,#2` = 900) por el nuevo.
     Solo se puede escribir como `a << k` (a <= 255): si la cantidad no es de esa forma, se rellena
     con filas de relleno (ID mayor que cualquier carta y funcion "sin efecto"): nunca se encuentran.
Las dos direcciones 0x097DFE78 que aparecen en el codigo NO son el fin de esta tabla: son el inicio
de la lista que le sigue. No se tocan.

Uso: python3 scripts/ampliar_efectos.py ROM_ENTRADA ROM_SALIDA [nuevas.json]
nuevas.json = lista de {"id_konami": N, "copiar_de": ID}   (columnas de otra carta)
           o {"id_konami": N, "fn_04": "0x...", "flags": "0xFFFFFFFF", "fn_0c": ..., "fn_10": ..., "fn_14": ..., "fn_18": ...}
"""
import json
import struct
import sys

from da_lib import (BASE, EFECTOS, EFECTOS_FILA, EFECTOS_FILAS, EFECTOS_MARCA, EFECTOS_NUEVA,
                    SIN_EFECTO, Rom)

LITERAL_VIEJO = BASE + EFECTOS
TOPE_INSTR = 0x61632                  # movs r4,#0xE1 ; lsls r4,r4,#2
RELLENO_ID = 20000                    # IDs de relleno: por encima de cualquier carta
MAX_FILAS = 4000                      # 112 KB: de sobra (la zona 0x1F00000 a 0x2000000 da para 37000)
COLUMNAS = {"fn_04": 4, "flags": 8, "fn_0c": 0xC, "fn_10": 0x10, "fn_14": 0x14, "fn_18": 0x18}


def forma_tope(maximo):
    """Menor (a, k) con a << k >= maximo y a <= 255."""
    for k in range(0, 8):
        a = -(-maximo // (1 << k))
        if a <= 255:
            return a, k
    raise ValueError("demasiadas filas")


def fila_bytes(f):
    return struct.pack("<HHIIIIII", f["id"], 0, f["fn_04"], f["flags"], f["fn_c"], f["fn_10"],
                       f["fn_14"], f["fn_18"])


def ampliar(rom, nuevas=()):
    assert not rom.efectos_mudada, "la tabla de efectos de ese ROM ya esta mudada"
    filas = [dict(f, id=f["id"]) for f in rom.efectos()]
    por_id = {f["id"]: f for f in filas}
    for n in nuevas:
        cid = n["id_konami"]
        assert cid not in por_id, f"el ID {cid} ya tiene fila de efecto"
        if "copiar_de" in n:
            base = por_id[n["copiar_de"]]
            f = {k: base[k] for k in ("fn_04", "flags", "fn_c", "fn_10", "fn_14", "fn_18")}
        else:
            f = {"fn_04": SIN_EFECTO, "flags": 0xFFFFFFFF, "fn_c": 0, "fn_10": 0, "fn_14": 0, "fn_18": 0}
            for k, v in n.items():
                if k in COLUMNAS:
                    f["fn_c" if k == "fn_0c" else k] = int(v, 0) if isinstance(v, str) else v
        f["id"] = cid
        filas.append(f)
        por_id[cid] = f
    filas.sort(key=lambda f: f["id"])
    assert filas[-1]["id"] < RELLENO_ID
    a, k = forma_tope(len(filas) - 1)
    total = (a << k) + 1
    relleno = {"fn_04": SIN_EFECTO, "flags": 0xFFFFFFFF, "fn_c": 0, "fn_10": 0, "fn_14": 0, "fn_18": 0}
    for j in range(total - len(filas)):
        filas.append(dict(relleno, id=RELLENO_ID + j))
    assert len(filas) == total <= MAX_FILAS
    ids = [f["id"] for f in filas]
    assert ids == sorted(set(ids)), "la tabla tiene que quedar ordenada y sin repetidos"

    zona = EFECTOS_NUEVA
    assert bytes(rom.d[zona:zona + 16]) != EFECTOS_MARCA
    datos = b"".join(fila_bytes(f) for f in filas)
    rom.d[zona:zona + 16] = EFECTOS_MARCA
    rom.w32(zona + 16, len(filas))
    rom.d[zona + 20:zona + 32] = b"\0" * 12
    rom.d[zona + 32:zona + 32 + len(datos)] = datos

    nuevo = BASE + zona + 32
    cambiados = []
    for o in range(0, 0x100000, 4):
        if rom.u32(o) == LITERAL_VIEJO:
            rom.w32(o, nuevo)
            cambiados.append(o)
    assert len(cambiados) == 13, f"se esperaban 13 referencias a la tabla y hay {len(cambiados)}"
    assert bytes(rom.d[TOPE_INSTR:TOPE_INSTR + 4]) == struct.pack("<HH", 0x24E1, 0x00A4), "el tope no es el esperado"
    rom.d[TOPE_INSTR:TOPE_INSTR + 4] = struct.pack("<HH", 0x2400 | a, (k << 6) | 0x24)
    return {"filas": len(filas), "tope": a << k, "a": a, "k": k, "literales": cambiados}


def main(argv):
    if len(argv) not in (2, 3):
        raise SystemExit(__doc__)
    rom = Rom(argv[0])
    nuevas = json.load(open(argv[2], encoding="utf-8")) if len(argv) == 3 else []
    info = ampliar(rom, nuevas)
    open(argv[1], "wb").write(rom.d)
    print(f"{argv[1]}: tabla de efectos mudada a {EFECTOS_NUEVA:07X} con {info['filas']} filas "
          f"(tope {info['tope']} = {info['a']} << {info['k']}; {len(info['literales'])} referencias)")


if __name__ == "__main__":
    main(sys.argv[1:])
