"""Vuelca a CSV lo que se sabe leer del ROM: cartas, tabla de efectos y mazos.

Uso: python3 volcar.py "Yu-Gi-Oh! GX - Duel Academy (USA).gba" [carpeta_salida]
     Si existe nombres_konami.csv (id,nombre) al lado del script, tambien
     nombra las cartas recortadas (las que tienen fila de efecto pero no estan
     en el juego).
"""
import csv
import os
import sys

from da_lib import *

rom = Rom(sys.argv[1])
out = sys.argv[2] if len(sys.argv) > 2 else "."
os.makedirs(out, exist_ok=True)
if rom.md5 != MD5_USA:
    print("AVISO: el MD5 no es el del ROM USA verificado; los offsets pueden no coincidir.")

aqui = os.path.dirname(os.path.abspath(__file__))
konami = {}
ruta_nombres = os.path.join(aqui, "nombres_konami.csv")
if os.path.exists(ruta_nombres):
    for fila in csv.DictReader(open(ruta_nombres, encoding="utf-8")):
        konami[int(fila["id"])] = fila

filas = rom.efectos()
por_id = {f["id"]: f for f in filas}
en_juego = {rom.id_de(i): i for i in range(1, N_CARTAS + 1)}


def nombre_id(cid):
    if cid in en_juego:
        return rom.nombre(en_juego[cid])
    return konami.get(cid, {}).get("nombre", f"<{cid}>")


def tiene_handlers(f):
    return f["fn_04"] not in (0, SIN_EFECTO) or any(f[k] for k in ("fn_c", "fn_10", "fn_14", "fn_18"))


with open(os.path.join(out, "cartas.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["indice", "id_konami", "nombre", "atk", "def", "nivel", "atributo", "tipo",
                "clase", "fila_efecto", "contrasena", "descripcion"])
    for i in range(1, N_CARTAS + 1):
        s, cid = rom.stats(i), rom.id_de(i)
        f = por_id.get(cid)
        estado = "no" if f is None else ("si" if tiene_handlers(f) else "vacia")
        monstruo = s["tipo"] <= 20
        w.writerow([i, cid, rom.nombre(i), s["atk"], s["def"], s["nivel"],
                    ATRIBUTOS[s["atributo"]] if monstruo else "", TIPOS[s["tipo"]],
                    CLASES[s["clase"]] if monstruo else f"sub{s['clase']}{s['sub17']}",
                    estado, rom.contrasena(i), rom.desc(i)])

with open(os.path.join(out, "efectos.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["fila", "id_konami", "nombre", "en_juego", "fn_04", "flags",
                "fn_0C", "fn_10", "fn_14", "fn_18"])
    for k, f in enumerate(filas):
        w.writerow([k, f["id"], nombre_id(f["id"]), "si" if f["id"] in en_juego else "NO",
                    "sin_efecto" if f["fn_04"] == SIN_EFECTO else f"{f['fn_04']:08X}",
                    f"{f['flags']:08X}"] + [f"{f[c]:08X}" if f[c] else "" for c in ("fn_c", "fn_10", "fn_14", "fn_18")])

with open(os.path.join(out, "cartas_recortadas.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["id_konami", "nombre", "tipo", "tiene_handlers", "hueco_vecino_indice", "hueco_vecino_nombre"])
    ids = [rom.id_de(i) for i in range(N_CARTAS + 1)]
    usados = set()
    for f in filas:
        cid = f["id"]
        if cid in en_juego:
            continue
        # hueco directo: un monstruo Normal vecino en el orden de IDs
        import bisect
        p = bisect.bisect_left(ids, cid, 1)
        hueco = ""
        for i in (p - 1, p):
            if not (1 <= i <= N_CARTAS) or i in usados:
                continue
            s = rom.stats(i)
            abajo = ids[i - 1] if i > 1 else 0
            arriba = ids[i + 1] if i < N_CARTAS else 0xFFFF
            if s["tipo"] <= 20 and s["clase"] == 0 and abajo < cid < arriba:
                hueco = i
                usados.add(i)
                break
        w.writerow([cid, nombre_id(cid), konami.get(cid, {}).get("tipo", ""),
                    "si" if tiene_handlers(f) else "vacia", hueco, rom.nombre(hueco) if hueco else ""])

with open(os.path.join(out, "mazos.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["mazo", "offset_renglon", "id_konami", "nombre", "copias"])
    for k, renglones in rom.mazos().items():
        for o, cid, copias in renglones:
            w.writerow([k, f"{o:07X}", cid, nombre_id(cid), copias])

print("listo:", ", ".join(sorted(os.listdir(out))))
