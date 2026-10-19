"""Arma una version de JUEGO del hack: solo las cartas aptas, sin ayudas de prueba.

Una carta es apta cuando el registro (datos/pruebas.csv) dice que funciona y tiene sus tres
evidencias: logica, duelo y la confirmacion (a ojo de Oscar o por capturas; scripts/registro.py aptas ROM).
La version lleva los parches que necesita el juego (busqueda de IDs y, si entra Dark Necrofear,
la invocacion por tipo) y las piezas de efectos/ de las cartas aptas; no lleva contrasenas gratis ni cartas
regaladas en el baul. Cada carta ocupa el hueco que le fija datos/huecos.csv.

Uso (desde la raiz del proyecto):
  python3 scripts/armar_version.py "ROM original.gba" VERSION [--rehacer]
VERSION es un numero como 0.1. Escribe:
  recetas/juego-vVERSION.json                              la receta (reproducible)
  build/Yu-Gi-Oh! GX - Duel Academy (Hack vVERSION).gba    el ROM (no se comparte)
  build/hack-vVERSION.bps                                  el parche (es lo que se comparte)
  build/hack-vVERSION.md                                   las notas: cartas, contrasenas y MD5
Sin --rehacer no pisa una version que ya existe.
"""
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

import registro
import restaurar
from da_lib import MD5_USA, Rom

RAIZ = registro.RAIZ
CON_INVOCACION_TIPO = {"Dark Necrofear": {"id_konami": 5222, "tipo": "Fiend", "cantidad": 3}}
# Ganchos que solo sirven a ciertas cartas (por ID de Konami): entran si alguna de ellas es apta.
# Los demas ganchos (G:, T:, B:) son del motor y van siempre.
GANCHOS_DE = {"efectos/gancho_atk_cuenta.s": {6773}, "efectos/gancho_batalla.s": {6770, 6771}}


def piezas_para(piezas, ids):
    """Las piezas de lote.json que necesitan las cartas de ids: las de una carta (ID:columna:fuente)
    solo si la carta entra; los ganchos de GANCHOS_DE solo si entra alguna de sus cartas."""
    out = []
    for p in piezas:
        cabeza = p.split(":")[0]
        if cabeza.isdigit():
            if int(cabeza) in ids:
                out.append(p)
        elif p.split(":")[-1] in GANCHOS_DE:
            if GANCHOS_DE[p.split(":")[-1]] & ids:
                out.append(p)
        else:
            out.append(p)
    return out


def main(argv):
    rehacer = "--rehacer" in argv
    argv = [a for a in argv if a != "--rehacer"]
    if len(argv) != 2 or not os.path.exists(argv[0]) or not re.fullmatch(r"\d+(\.\d+)*", argv[1]):
        raise SystemExit(__doc__)
    original, version = argv
    if Rom(original).md5 != MD5_USA:
        raise SystemExit("error: el primer archivo tiene que ser el ROM original USA")
    receta_ruta = os.path.join(RAIZ, "recetas", f"juego-v{version}.json")
    rom_ruta = os.path.join(RAIZ, "build", f"Yu-Gi-Oh! GX - Duel Academy (Hack v{version}).gba")
    bps_ruta = os.path.join(RAIZ, "build", f"hack-v{version}.bps")
    notas_ruta = os.path.join(RAIZ, "build", f"hack-v{version}.md")
    existentes = [r for r in (receta_ruta, rom_ruta, bps_ruta, notas_ruta) if os.path.exists(r)]
    if existentes and not rehacer:
        raise SystemExit(f"error: la version {version} ya existe ({os.path.relpath(existentes[0], RAIZ)}). "
                         "Usa otro numero, o --rehacer si todavia no se compartio.")

    filas = registro.leer()
    aptas = [f for f in filas if registro.apta(f)[0]]
    fuera = [(f["carta"], registro.apta(f)[1]) for f in filas if not registro.apta(f)[0]]
    if not aptas:
        raise SystemExit("error: el registro no tiene ninguna carta apta")
    prueba = json.load(open(os.path.join(RAIZ, "recetas", "test.json"), encoding="utf-8"))
    lote = json.load(open(os.path.join(RAIZ, "recetas", "lote.json"), encoding="utf-8"))
    nombres = {f["carta"] for f in aptas}
    # lote.json corrige cartas de test.json por hueco (texto y columnas de Dark Necrofear): la
    # version de juego tiene que llevar la carta corregida, igual que el ROM (Lote).
    # Las cartas dadas de alta despues (scripts/alta.py) estan solo en lote.json, enteras.
    corregidas = {c["hueco"]: c for c in lote.get("cartas", [])}
    heredadas = {c["hueco"] for c in prueba["cartas"]}
    todas = ([{**c, **corregidas.get(c["hueco"], {})} for c in prueba["cartas"]]
             + [c for c in lote.get("cartas", []) if c["hueco"] not in heredadas])
    cartas = [{k: v for k, v in c.items() if k != "pack"} for c in todas if c["nombre"] in nombres]
    faltan = nombres - {c["nombre"] for c in cartas}
    if faltan:
        raise SystemExit(f"error: cartas aptas que no estan en las recetas: {sorted(faltan)}")
    parches = {"busqueda_ids": True}
    tipo = [v for k, v in CON_INVOCACION_TIPO.items() if k in nombres]
    if tipo:
        parches["invocacion_tipo"] = tipo
    receta = {"nota": f"Version de JUEGO {version}: las {len(cartas)} cartas aptas del registro al "
                      f"{datetime.date.today().isoformat()}. Generada por scripts/armar_version.py; no editar a mano.",
              "parches": parches, "cartas": cartas,
              "piezas": piezas_para(lote["piezas"], {int(c["id_konami"]) for c in cartas})}
    # Las cartas que el juego nunca tuvo necesitan su fila nueva en la tabla de efectos.
    filas = [f for f in lote.get("filas_efecto", []) if int(f["id_konami"]) in {int(c["id_konami"]) for c in cartas}]
    if filas:
        receta["filas_efecto"] = filas
    with open(receta_ruta, "w", encoding="utf-8") as f:
        json.dump(receta, f, ensure_ascii=False, indent=2)
        f.write("\n")
    restaurar.main(original, receta_ruta, rom_ruta)
    subprocess.run([sys.executable, os.path.join(RAIZ, "scripts", "bps.py"), original, rom_ruta, bps_ruta], check=True)

    rom = Rom(rom_ruta)
    for c in cartas:                                # comprobacion sobre el resultado
        assert rom.nombre(c["hueco"]) == c["nombre"] and rom.id_de(c["hueco"]) == c["id_konami"], c["nombre"]
    md5_bps = hashlib.md5(open(bps_ruta, "rb").read()).hexdigest()
    lineas = [f"# Duel Academy Hack v{version}", "",
              f"Fecha: {datetime.date.today().isoformat()}. {len(cartas)} cartas restauradas, todas probadas en duelo "
              "y verificadas (a ojo o por capturas).", "",
              "## Cómo se usa", "",
              f"1. Hace falta el ROM original *Yu-Gi-Oh! GX - Duel Academy (USA)*, MD5 `{MD5_USA}`.",
              f"2. Aplicar el parche: `python3 scripts/bps.py --aplicar \"ROM original.gba\" build/hack-v{version}.bps "
              f"\"Yu-Gi-Oh! GX - Duel Academy (Hack v{version}).gba\"` (o cualquier programa que aplique `.bps`).",
              f"3. El ROM que sale tiene MD5 `{rom.md5}`. El parche tiene MD5 `{md5_bps}`.", "",
              "Las cartas nuevas ocupan el lugar de monstruos Normales y aparecen en los sobres donde salían "
              "ellos; también se pueden comprar con su contraseña. Todavía muestran el dibujo del monstruo que "
              "reemplazan.", "",
              "## Cartas", "",
              "| Carta | N.º | Reemplaza a | Clase | Contraseña |", "|---|---|---|---|---|"]
    for c in sorted(cartas, key=lambda c: c["nombre"]):
        clase = c["clase"] if c["clase"] not in ("Effect", "Normal") else f"{c['tipo']} / {c['clase']}"
        lineas.append(f"| {c['nombre']} | {c['hueco']} | {c['hueco_nombre']} | {clase} | {c.get('contrasena', '')} |")
    lineas += ["", "## Qué quedó afuera", "",
               "Cartas del lote que no entran en esta versión y qué les falta:", ""]
    lineas += [f"- {carta}: {motivo}" for carta, motivo in sorted(fuera)]
    with open(notas_ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    print(f"version {version}: {len(cartas)} cartas")
    for r in (receta_ruta, rom_ruta, bps_ruta, notas_ruta):
        print("  ", os.path.relpath(r, RAIZ))
    print("   MD5 del ROM:", rom.md5)


if __name__ == "__main__":
    main(sys.argv[1:])
