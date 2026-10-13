"""Arma recetas/packs/pack-4.json: todos los Elemental Hero y Neo-Spacian que el juego nunca tuvo.

Los datos salen de la base de ygoprodeck (JSON ya bajado en la carpeta que se pasa) y los dibujos
de images.ygoprodeck.com (recortados, ya del tamano que lleva arte.py). Las cartas que ya estan en
el Lote (Neos y los 6 Neo-Spacian) y las del juego original se saltan. Las que tienen efecto entran
como monstruo Normal con un texto que lo dice: el efecto no esta hecho.

Uso: python3 scripts/hacer_pack4.py CARPETA_JSON
"""
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from da_lib import Rom, ATRIBUTOS, TIPOS

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGINAL = os.path.expanduser("~/Downloads/Yu-Gi-Oh! GX - Duel Academy (USA).gba")
YA_EN_LOTE = {6653, 6768, 6769, 6770, 6771, 6772, 6773}
# Los sobres de la tienda guardan el ID de la carta en 13 bits (FUN_080BD89C, mascara 0x1FFF): un ID
# de Konami desde 8192 no puede salir de un sobre. Esas cartas llevan un ID propio, libre, de
# 8191 para abajo ("id_real" guarda el de Konami). El ID solo es la llave que usa el juego.
TOPE_ID_SOBRE = 8191


def nombre_juego(n):
    return re.sub(r"^Elemental HERO", "Elemental Hero", n)


def main(carpeta):
    rom = Rom(ORIGINAL)
    en_juego = {rom.nombre(i).lower() for i in range(1, rom.n + 1)}
    vistas = {}
    for f in os.listdir(carpeta):
        if f.endswith(".json"):
            d = json.load(open(os.path.join(carpeta, f)))
            for c in (d.get("data", []) if isinstance(d, dict) else []):
                if "Monster" in c["type"] and re.match(r"(Elemental HERO|Neo-Spacian) ", c["name"]):
                    vistas[c["misc_info"][0]["konami_id"]] = c
    cartas = []
    libres = iter(i for i in range(TOPE_ID_SOBRE, 6467, -1)
                  if i not in vistas and i not in YA_EN_LOTE and rom.indice_de(i) == 0)
    for kid, c in sorted(vistas.items()):
        n = nombre_juego(c["name"])
        if kid in YA_EN_LOTE or n.lower() in en_juego:
            continue
        if c["type"] == "Fusion Monster":
            clase = "Fusion"
            materiales = c["desc"].split("\n")[0].replace('"', "").strip()
            desc = materiales if "+" in materiales and len(materiales) < 120 else \
                "A Fusion Monster of the Elemental Heroes."
        else:
            clase = "Normal"
            desc = (c["desc"] if c["type"] == "Normal Monster" else
                    f"A {c['attribute'].lower()} {'Neo-Spacian' if 'Neo-Spacian' in n else 'Elemental Hero'} "
                    f"with a special power. Its original effect is not in this version.")
        assert c["attribute"] in ATRIBUTOS and c["race"] in TIPOS, (n, c["attribute"], c["race"])
        ruta = f"arte/{re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')}.png"
        if not os.path.exists(os.path.join(RAIZ, ruta)):
            tmp = os.path.join(carpeta, f"{c['id']}.jpg")
            for _ in range(4):
                if subprocess.run(["curl", "-sf", "-m", "40", "-o", tmp,
                                   f"https://images.ygoprodeck.com/images/cards_cropped/{c['id']}.jpg"]).returncode == 0:
                    break
                time.sleep(3)
            else:
                raise SystemExit(f"no baja el dibujo de {n}")
            from PIL import Image
            Image.open(tmp).convert("RGB").save(os.path.join(RAIZ, ruta))
            time.sleep(0.3)
        real = kid
        if kid > TOPE_ID_SOBRE:
            kid = next(libres)
        cartas.append({"carta": {
            "id_konami": kid, "id_real": real, "nombre": n, "atk": c["atk"], "def": c["def"], "nivel": c["level"],
            "atributo": c["attribute"], "tipo": c["race"], "clase": clase,
            "contrasena": str(c["id"]), "descripcion": desc, "arte": ruta}})
    # recetas de fusion: solo las de materiales con nombre propio (2 o 3) que el juego tiene
    conocidos = set(en_juego) | {c["carta"]["nombre"].lower() for c in cartas}
    lote = json.load(open(os.path.join(RAIZ, "recetas/lote.json"), encoding="utf-8"))
    conocidos |= {c["nombre"].lower() for c in lote["cartas"] if "nombre" in c}
    fusiones, sin_receta = [], []
    for c in cartas:
        c = c["carta"]
        if c["clase"] != "Fusion":
            continue
        partes = [p.strip() for p in c["descripcion"].split(" + ")]
        nombres = [nombre_juego(p.strip('"').strip()) for p in partes]
        if 2 <= len(nombres) <= 3 and all(n.lower() in conocidos for n in nombres):
            fusiones.append({"resultado": c["nombre"], "materiales": nombres})
        else:
            sin_receta.append(c["nombre"])
    print(len(fusiones), "recetas de fusion;", len(sin_receta), "sin receta:", ", ".join(sin_receta))
    sal = os.path.join(RAIZ, "recetas/packs/pack-4.json")
    json.dump({"pack": "pack-4", "estado": "borrador", "fusiones": fusiones,
               "nota": "Elemental Hero y Neo-Spacian que el juego nunca tuvo; se aplica sobre el ROM ampliado con ampliar.py --cartas. Los que tenian efecto entran sin el (texto lo dice).",
               "cartas": cartas}, open(sal, "w"), indent=2, ensure_ascii=False)
    print(len(cartas), "cartas ->", sal)


main(sys.argv[1])
