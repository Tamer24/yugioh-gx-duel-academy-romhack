"""Alta de un pack de cartas recortadas: de una lista de nombres a cartas listas para probar.

Dos pasos, cada uno un comando (desde la raiz del proyecto):

  python3 scripts/alta.py ROM_ORIGINAL preparar PACK "Carta" ["Carta" ...]
  python3 scripts/alta.py ROM_ORIGINAL preparar PACK --archivo lista.txt     (una carta por linea)
      Clasifica cada carta (scripts/triage.py), le asigna un hueco seguro libre (scripts/huecos.py)
      y escribe el borrador recetas/packs/PACK.json con sus datos (scripts/nombres_konami.csv).
      No toca nada mas. Lo unico que queda por completar a mano es la "descripcion" de cada carta
      (el texto que se lee en el juego), que no esta en el ROM.

  python3 scripts/alta.py ROM_ORIGINAL aplicar PACK [--simular]
      Valida el borrador entero y recien despues escribe: las filas de datos/huecos.csv, las
      cartas en recetas/lote.json y una fila por carta, sin veredicto, en datos/pruebas.csv.
      Con --simular valida y muestra lo que haria, sin escribir.

Despues de aplicar: sh scripts/construir_lote.sh ROM_ORIGINAL arma el ROM de trabajo con las cartas
nuevas (3 copias de cada una en el baul de una partida nueva). De ahi en mas cada carta sigue el
metodo de PLAN.md: probarla, escribirle lo que falte con ACCIONES.md y registrar el veredicto.

Solo acepta cartas recortadas (con fila de efecto en el ROM y fuera del juego). Los huecos seguros
son pocos: si no alcanzan, 'preparar' lo dice y no arma el borrador.
"""
import csv
import datetime
import json
import os
import re
import sys

import huecos
import registro
import triage
from da_lib import ATRIBUTOS, CLASES, TIPOS, Rom
from restaurar import SUBTIPOS

RAIZ = registro.RAIZ
PACKS = os.path.join(RAIZ, "recetas", "packs")
LOTE = os.path.join(RAIZ, "recetas", "lote.json")
PENDIENTE = ""                     # una descripcion vacia es un borrador sin terminar
MAGICAS = {"Spell Normal": "Spell", "Trap Normal": "Trap"}


def error(texto):
    raise SystemExit("error: " + texto)


def datos_konami():
    ruta = os.path.join(RAIZ, "scripts", "nombres_konami.csv")
    with open(ruta, newline="", encoding="utf-8") as f:
        return {int(x["id"]): x for x in csv.DictReader(f)}


def clase_de(tipo):
    """('tipo de monstruo', 'clase de la receta', aviso) a partir del texto de nombres_konami.csv."""
    if tipo in MAGICAS or tipo in SUBTIPOS:
        return "", MAGICAS.get(tipo, tipo), ""
    partes = [x.strip() for x in tipo.split("/")]
    if len(partes) < 2 or partes[0] not in TIPOS:
        return "", "", f"tipo desconocido: {tipo!r}"
    if "Fusion" in partes:
        return partes[0], "Fusion", "monstruo de Fusion: sus materiales no tienen receta todavia"
    return partes[0], "Effect", ""


def preparar(rom, pack, pedidas):
    destino = os.path.join(PACKS, pack + ".json")
    if os.path.exists(destino):
        error(f"ya existe {os.path.relpath(destino, RAIZ)}: borralo para rehacer el borrador, o usa otro nombre")
    t, konami = triage.Triage(rom), datos_konami()
    cartas, rechazadas, vistos = [], [], set()
    for texto in pedidas:
        r = t.carta(texto)
        if r["estado"] != "recortada":
            rechazadas.append(f"{texto}: {r['estado'] or 'no la reconozco'}")
            continue
        if r["id_konami"] in vistos:
            rechazadas.append(f"{texto}: repetida en la lista")
            continue
        vistos.add(r["id_konami"])
        cartas.append(r)
    if rechazadas:
        error("estas cartas no se pueden dar de alta:\n  " + "\n  ".join(rechazadas))
    if not cartas:
        error("la lista esta vacia")
    libres = huecos.libres(rom)
    if len(cartas) > len(libres):
        error(f"el pack tiene {len(cartas)} cartas y quedan {len(libres)} huecos seguros "
              f"(python3 scripts/huecos.py ROM_ORIGINAL). Achicar el pack o decidir que huecos se sacrifican.")
    salida, avisos = [], []
    for r, (indice, hueco_nombre) in zip(cartas, libres):
        k = konami.get(r["id_konami"])
        if not k or not k["tipo"]:
            error(f"{r['carta']}: no tengo sus datos en scripts/nombres_konami.csv")
        tipo, clase, aviso = clase_de(k["tipo"])
        if not clase:
            error(f"{r['carta']}: {aviso}")
        c = {"hueco": indice, "hueco_nombre": hueco_nombre, "id_konami": r["id_konami"], "nombre": k["nombre"]}
        if tipo:
            c.update(atk=int(k["atk"]), **{"def": int(k["def"])}, nivel=int(k["nivel"]), atributo=k["atributo"],
                     tipo=tipo)
        c.update(clase=clase, contrasena=k["contrasena"], descripcion=PENDIENTE)
        salida.append({"carta": c, "triage": {x: r[x] for x in ("diagnostico", "por_que", "fn_04", "otras_columnas",
                                                                 "motor", "avisos")}})
        if aviso:
            avisos.append(f"{k['nombre']}: {aviso}")
    os.makedirs(PACKS, exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        json.dump({"pack": pack, "estado": "borrador", "creado": datetime.date.today().isoformat(),
                   "nota": "Completar la \"descripcion\" de cada carta y correr: python3 scripts/alta.py ROM aplicar "
                           + pack, "cartas": salida}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"borrador: {os.path.relpath(destino, RAIZ)} ({len(salida)} cartas; quedan {len(libres) - len(salida)} huecos seguros)")
    for x in salida:
        c, g = x["carta"], x["triage"]
        print(f"  {g['diagnostico']}  {c['nombre']:<32} hueco {c['hueco']:>4} ({c['hueco_nombre']})  {g['por_que']}")
        if g["avisos"]:
            print(f"     AVISO: {g['avisos']}")
    for a in avisos:
        print("  AVISO: " + a)
    print('falta: la "descripcion" de cada carta en el borrador')


def validar_carta(c, rom, usados, contrasenas):
    """Errores de una carta del borrador. Lo que no detecta aca lo detecta restaurar.py al armar."""
    e, n = [], c.get("nombre", "?")
    for clave in ("hueco", "hueco_nombre", "id_konami", "nombre", "clase", "contrasena", "descripcion"):
        if clave not in c:
            e.append(f"{n}: falta la clave {clave}")
    if e:
        return e
    if not c["descripcion"].strip():
        e.append(f"{n}: falta la descripcion")
    else:
        try:
            c["descripcion"].encode("latin1")
        except UnicodeEncodeError:
            e.append(f"{n}: la descripcion tiene caracteres que el juego no puede mostrar")
    if not re.fullmatch(r"\d{8}", c["contrasena"]):
        e.append(f"{n}: la contrasena tiene que tener 8 digitos")
    elif c["contrasena"] in contrasenas:
        e.append(f"{n}: la contrasena {c['contrasena']} ya es de {contrasenas[c['contrasena']]}")
    if c["hueco"] in usados:
        e.append(f"{n}: el hueco {c['hueco']} ya es de {usados[c['hueco']]['carta']}")
    elif rom.nombre(c["hueco"]) != c["hueco_nombre"]:
        e.append(f"{n}: el hueco {c['hueco']} es {rom.nombre(c['hueco'])!r}, no {c['hueco_nombre']!r}")
    if rom.indice_de(c["id_konami"]):
        e.append(f"{n}: el ID {c['id_konami']} ya esta en el juego")
    if len(c["nombre"]) > 45:
        e.append(f"{n}: nombre demasiado largo")
    if c["clase"] in SUBTIPOS:
        pass
    elif c["clase"] not in CLASES:
        e.append(f"{n}: clase desconocida {c['clase']!r}")
    else:
        for clave in ("atk", "def", "nivel", "atributo", "tipo"):
            if clave not in c:
                e.append(f"{n}: es un monstruo y le falta {clave}")
        if c.get("atributo") not in ATRIBUTOS[1:] or c.get("tipo") not in TIPOS[1:21]:
            e.append(f"{n}: atributo o tipo desconocido")
    return e


def aplicar(rom, pack, simular):
    ruta = os.path.join(PACKS, pack + ".json")
    if not os.path.exists(ruta):
        error(f"no existe {os.path.relpath(ruta, RAIZ)}: primero 'preparar'")
    borrador = json.load(open(ruta, encoding="utf-8"))
    if borrador.get("estado") != "borrador":
        error(f"el pack {pack} ya fue aplicado ({borrador.get('estado')})")
    cartas = [x["carta"] for x in borrador["cartas"]]
    usados = huecos.usados()
    seguros = dict(huecos.libres(rom))
    contrasenas = {u["contrasena"]: u["carta"] for u in usados.values()}
    nombres = {u["carta"] for u in usados.values()}
    errores = []
    for c in cartas:
        errores += validar_carta(c, rom, usados, contrasenas)
        if c.get("nombre") in nombres:
            errores.append(f"{c['nombre']}: ya esta restaurada")
        if c.get("hueco") not in seguros and c.get("hueco") not in usados:
            errores.append(f"{c.get('nombre')}: el hueco {c.get('hueco')} no es un hueco seguro")
        contrasenas[c.get("contrasena")] = c.get("nombre")
        nombres.add(c.get("nombre"))
    if len({c.get("hueco") for c in cartas}) != len(cartas):
        errores.append("hay huecos repetidos dentro del pack")
    lote = json.load(open(LOTE, encoding="utf-8"))
    en_lote = {c["hueco"] for c in lote.get("cartas", [])}
    errores += [f"{c['nombre']}: el hueco {c['hueco']} ya esta en recetas/lote.json" for c in cartas
                if c.get("hueco") in en_lote]
    filas = registro.leer()
    if errores:
        error("el borrador no se puede aplicar:\n  " + "\n  ".join(errores))
    hoy = datetime.date.today().isoformat()
    print(f"pack {pack}: {len(cartas)} cartas")
    for c in cartas:
        print(f"  {c['nombre']:<32} hueco {c['hueco']:>4} ({c['hueco_nombre']})  contrasena {c['contrasena']}")
    if simular:
        print("simulacion: el borrador es valido; no se escribio nada")
        return
    # 1. registro de huecos
    with open(os.path.join(RAIZ, "datos", "huecos.csv"), "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        for c in cartas:
            w.writerow([c["hueco"], c["hueco_nombre"], c["id_konami"], c["nombre"], c["contrasena"], f"{pack} ({hoy})"])
    # 2. receta del ROM de trabajo
    lote.setdefault("cartas", []).extend({**c, "pack": pack} for c in cartas)
    with open(LOTE, "w", encoding="utf-8") as f:
        json.dump(lote, f, ensure_ascii=False, indent=2)
        f.write("\n")
    # 3. registro de pruebas: una fila por carta, sin veredicto
    por_carta = {x["carta"]["nombre"]: x["triage"] for x in borrador["cartas"]}
    for c in cartas:
        clase = {"Effect": "Monstruo de efecto", "Fusion": "Monstruo de Fusion"}.get(c["clase"], c["clase"])
        fila = dict.fromkeys(registro.COLUMNAS, "")
        fila.update(carta=c["nombre"], indice=str(c["hueco"]), id_konami=str(c["id_konami"]), clase=clase,
                    usa_piezas_nuevas="no", aparcada="no", ev_ojo="pendiente")
        filas.append(fila)
    registro.escribir(filas)
    borrador.update(estado=f"aplicado el {hoy}", nota="Aplicado: las cartas estan en recetas/lote.json, "
                    "datos/huecos.csv y datos/pruebas.csv. Este archivo queda como constancia del alta.")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(borrador, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("aplicado. Sigue:")
    print('  sh scripts/construir_lote.sh "ROM original.gba"        arma el ROM de trabajo con las cartas nuevas')
    print('  python3 scripts/registro.py tabla "build/...(Lote).gba"  regenera la tabla de PRUEBAS.md')
    print("  y para cada carta, el metodo de PLAN.md (probar, completar con ACCIONES.md, registrar). Orden sugerido:")
    for grupo in "ACED":
        del_grupo = [n for n, g in por_carta.items() if g["diagnostico"] == grupo]
        if del_grupo:
            print(f"    {grupo} ({triage.TEXTOS[grupo]}): {', '.join(del_grupo)}")


def main(argv):
    if len(argv) < 3 or argv[1] not in ("preparar", "aplicar"):
        raise SystemExit(__doc__)
    rom, orden, pack = Rom(argv[0]), argv[1], argv[2]
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", pack):
        error("el nombre del pack va en minusculas, numeros y guiones (p. ej. pack-2)")
    resto = argv[3:]
    if orden == "preparar":
        if resto[:1] == ["--archivo"]:
            pedidas = [l.strip() for l in open(resto[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
        else:
            pedidas = resto
        preparar(rom, pack, pedidas)
    else:
        aplicar(rom, pack, "--simular" in resto)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
