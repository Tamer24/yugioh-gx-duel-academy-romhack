"""Registro de resultados del lote de cartas restauradas (datos/pruebas.csv).

El CSV es la fuente unica. La tabla de PRUEBAS.md se genera desde el, entre las marcas
<!-- registro:inicio --> y <!-- registro:fin -->, para que no puedan divergir.

Uso (desde la raiz del proyecto):
  python3 scripts/registro.py verificar ROM
  python3 scripts/registro.py tabla ROM              regenera la tabla de PRUEBAS.md
  python3 scripts/registro.py aptas ROM              cartas que pueden ir a una receta de juego
  python3 scripts/registro.py pendientes ROM         cartas que Oscar tiene que mirar
  python3 scripts/registro.py ojo ROM "CARTA" si|no ["que vio"] [--veredicto "funciona en parte"]

Hay una fila por cada carta de datos/huecos.csv. Una carta recien dada de alta (scripts/alta.py)
no tiene veredicto todavia: es valido mientras no tenga evidencia registrada.

Reglas del CSV: specs/001-cerrar-pruebas-lote/contracts/registro-csv.md
"""
import csv
import datetime
import os
import re
import sys

from da_lib import Rom

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CSV = os.path.join(RAIZ, "datos", "pruebas.csv")
PRUEBAS = os.path.join(RAIZ, "PRUEBAS.md")
INICIO, FIN = "<!-- registro:inicio -->", "<!-- registro:fin -->"
COLUMNAS = ["carta", "indice", "id_konami", "clase", "usa_piezas_nuevas", "veredicto", "aparcada",
            "motivo_aparcada", "detalle", "falla", "ev_logica", "ev_auto", "ev_ojo", "nota_ojo",
            "rom_md5", "estado", "fecha"]
VEREDICTOS = ("funciona", "funciona en parte", "no funciona")
HUECOS = os.path.join(RAIZ, "datos", "huecos.csv")     # que cartas hay: una fila del registro por cada una
EN_CURSO = False            # --en-curso: se conserva por compatibilidad; ya no cambia ninguna regla
ROMS = {"c1b1289a1e0a3ca4c725272073c791db": "Lote",
        "6c667223c062b6a3aa6f602e55a904dc": "Lote (2026-10-11, Necrofear en version simplificada)",
        "d15bb70918d2d2e2ae218ea553f807f4": "Lote (2026-10-11, con el aviso de Necrofear al ser destruida en batalla)",
        "990aefb8bc7ff1cf159f52caeda97999": "Lote (2026-10-11, antes del -500 de Bagworm y la posesion de Necrofear)",
        "a9d3ee4019218b2ee3f642615b51a659": "Lote (2026-10-11, antes de completar)",
        "dbbbab32ccc659ae077cf12fcf4c15c6": "Lote (2026-10-10)", "4ed08c04c7c3f5256ed7597200def613": "Efectos", "d6fe444f169d3a1f92ec2c453b7ccc3a": "Test",
        "0122cad69328c075c66a6d0227a93f58": "Prueba3", "257d19a682dcd794f7cd44e929f11c28": "Spy"}


def leer(ruta=CSV):
    with open(ruta, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        if lector.fieldnames != COLUMNAS:
            raise SystemExit(f"error: las columnas de {ruta} no son las del contrato.\n"
                             f"  esperadas: {','.join(COLUMNAS)}\n  encontradas: {','.join(lector.fieldnames or [])}")
        return list(lector)


def escribir(filas, ruta=CSV):
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS, lineterminator="\n")
        w.writeheader()
        w.writerows(filas)


def _script(texto):
    """Ruta del script que nombra un comando ('python3 scripts/x.py ...') o una ruta suelta."""
    m = re.search(r"(scripts/[\w./-]+\.py)", texto)
    return m.group(1) if m else None


def errores(filas, rom):
    """Lista de incumplimientos de las reglas del contrato. Vacia si el registro es valido."""
    out = []
    with open(HUECOS, newline="", encoding="utf-8") as h:
        restauradas = {x["carta"]: x["indice"] for x in csv.DictReader(h)}
    registradas = {f["carta"]: f["indice"] for f in filas}
    for carta in sorted(set(restauradas) - set(registradas)):
        out.append(f"{carta}: esta en datos/huecos.csv y no tiene fila en el registro")
    for carta in sorted(set(registradas) - set(restauradas)):
        out.append(f"{carta}: tiene fila en el registro y no esta en datos/huecos.csv")
    for carta in sorted(set(registradas) & set(restauradas)):
        if registradas[carta] != restauradas[carta]:
            out.append(f"{carta}: indice {registradas[carta]} en el registro y {restauradas[carta]} en datos/huecos.csv")
    for col in ("carta", "indice", "id_konami"):
        vistos = set()
        for f in filas:
            if f[col] in vistos:
                out.append(f"{f['carta']}: {col} repetido ({f[col]})")
            vistos.add(f[col])
    for f in filas:
        c = f["carta"]

        def mal(col, msg):
            out.append(f"{c}: {col}: {msg}")

        if not f["indice"].isdigit() or not 1 <= int(f["indice"]) <= 1200:
            mal("indice", f"no es un numero de carta: {f['indice']!r}")
        else:
            i = int(f["indice"])
            if rom.nombre(i) != c:
                mal("carta", f"en el ROM el indice {i} es {rom.nombre(i)!r}")
            if str(rom.id_de(i)) != f["id_konami"]:
                mal("id_konami", f"en el ROM el indice {i} tiene el ID {rom.id_de(i)}")
        for col, validos in (("usa_piezas_nuevas", ("si", "no")), ("aparcada", ("si", "no")),
                             ("ev_ojo", ("si", "no", "pendiente")), ("veredicto", VEREDICTOS + ("",))):
            if f[col] not in validos:
                mal(col, f"valor no permitido: {f[col]!r}")
        # Sin veredicto es el estado de una carta recien dada de alta (scripts/alta.py). Lo que no
        # puede pasar es que haya evidencia y falte el veredicto.
        if not f["veredicto"] and f["aparcada"] != "si" and (f["ev_auto"] or f["ev_ojo"] == "si"):
            mal("veredicto", "hay evidencia y falta el veredicto")
        if f["aparcada"] == "si" and not f["motivo_aparcada"]:
            mal("motivo_aparcada", "la carta esta aparcada y no dice por que")
        if f["veredicto"] and not f["detalle"]:
            mal("detalle", "hay veredicto y no dice que se observo")
        if f["veredicto"] in VEREDICTOS[1:] and not f["falla"]:
            mal("falla", "el veredicto no es 'funciona' y no dice que difiere del texto")
        if (f["ev_ojo"] == "si" or f["ev_auto"]) and not f["rom_md5"]:
            mal("rom_md5", "hay evidencia y no dice en que ROM se obtuvo")
        if f["rom_md5"] and not re.fullmatch(r"[0-9a-f]{32}", f["rom_md5"]):
            mal("rom_md5", f"no es un MD5: {f['rom_md5']!r}")
        if f["fecha"] and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", f["fecha"]):
            mal("fecha", f"no tiene la forma AAAA-MM-DD: {f['fecha']!r}")
        if f["estado"] and not os.path.exists(os.path.join(RAIZ, f["estado"])):
            mal("estado", f"no existe el archivo {f['estado']}")
        for col in ("ev_logica", "ev_auto"):
            s = _script(f[col])
            if s and not os.path.exists(os.path.join(RAIZ, s)):
                mal(col, f"no existe el script {s}")
        if f["ev_ojo"] == "si" and f["nota_ojo"].startswith("discrepancia") and f["veredicto"] == "funciona":
            mal("nota_ojo", "Oscar vio algo distinto y el veredicto sigue en 'funciona'")
    return out


def apta(f):
    """Regla de aptitud de data-model.md. Devuelve (True, '') o (False, que le falta)."""
    falta = []
    if f["veredicto"] != "funciona":
        falta.append("veredicto " + (f["veredicto"] or "sin definir"))
    if f["aparcada"] == "si":
        falta.append("aparcada")
    if f["ev_ojo"] != "si":
        falta.append("confirmacion a ojo")
    if not f["ev_auto"]:
        falta.append("prueba en duelo registrada")
    if f["usa_piezas_nuevas"] == "si" and f["ev_logica"] in ("", "n/a"):
        falta.append("prueba de logica (Unicorn)")
    return (not falta, ", ".join(falta))


def _celda(texto):
    return texto.replace("|", "\\|").replace("\n", " ")


def tabla(filas):
    orden = {"funciona": 0, "funciona en parte": 1, "no funciona": 2, "": 3}
    out = ["| Carta | Nº | Veredicto | Lógica | Duelo | A ojo | Qué se observó | Cómo reproducir |",
           "|---|---|---|---|---|---|---|---|"]
    for f in sorted(filas, key=lambda f: (orden[f["veredicto"]], f["carta"])):
        ver = f["veredicto"] or "sin veredicto"
        if f["aparcada"] == "si":
            ver += " (aparcada: " + f["motivo_aparcada"] + ")"
        logica = "n/a" if f["usa_piezas_nuevas"] == "no" else ("sí" if f["ev_logica"] not in ("", "n/a") else "falta")
        duelo = "sí" if f["ev_auto"] else "falta"
        ojo = {"si": "sí", "no": "no hace falta", "pendiente": "**pendiente**"}[f["ev_ojo"]]
        detalle = f["detalle"] + (" **Falla:** " + f["falla"] if f["falla"] else "")
        if f["nota_ojo"]:
            detalle += " **Oscar:** " + f["nota_ojo"]
        como = []
        if f["rom_md5"]:
            como.append("ROM `" + ROMS.get(f["rom_md5"], f["rom_md5"][:8]) + "`")
        if f["estado"]:
            como.append("`" + f["estado"] + "`")
        if f["ev_auto"]:
            como.append("`" + f["ev_auto"] + "`" if "python3 " in f["ev_auto"] else f["ev_auto"])
        out.append("| " + " | ".join(_celda(x) for x in (
            f["carta"], "%04d" % int(f["indice"]), ver, logica, duelo, ojo, detalle, "; ".join(como))) + " |")
    return "\n".join(out)


def bloque_actual():
    texto = open(PRUEBAS, encoding="utf-8").read()
    if texto.count(INICIO) != 1 or texto.count(FIN) != 1 or texto.index(INICIO) > texto.index(FIN):
        raise SystemExit(f"error: PRUEBAS.md tiene que tener una vez {INICIO} y despues {FIN}")
    a, b = texto.index(INICIO) + len(INICIO), texto.index(FIN)
    return texto, a, b


def resumen(filas):
    cuenta = {v: sum(1 for f in filas if f["veredicto"] == v) for v in VEREDICTOS}
    sin = sum(1 for f in filas if not f["veredicto"])
    return (f"{len(filas)} cartas | funciona {cuenta['funciona']} | funciona en parte "
            f"{cuenta['funciona en parte']} | no funciona {cuenta['no funciona']} | sin veredicto {sin} | "
            f"aparcadas {sum(1 for f in filas if f['aparcada'] == 'si')} | "
            f"pendientes de ojo {sum(1 for f in filas if f['ev_ojo'] == 'pendiente')} | "
            f"aptas {sum(1 for f in filas if apta(f)[0])}")


def validar(filas, rom):
    errs = errores(filas, rom)
    if errs:
        raise SystemExit("error: el registro no es valido:\n  " + "\n  ".join(errs))


def cmd_verificar(filas, rom):
    validar(filas, rom)
    texto, a, b = bloque_actual()
    if texto[a:b].strip() != tabla(filas).strip():
        viejas = {l.split("|")[1].strip(): l for l in texto[a:b].strip().splitlines()[2:] if l.count("|") > 3}
        nuevas = {l.split("|")[1].strip(): l for l in tabla(filas).splitlines()[2:]}
        distintas = sorted(c for c in set(viejas) | set(nuevas) if viejas.get(c) != nuevas.get(c))
        raise SystemExit("error: la tabla de PRUEBAS.md no coincide con datos/pruebas.csv en: "
                         + ", ".join(distintas or ["(encabezado)"])
                         + "\n  regenerar con: python3 scripts/registro.py tabla ROM")
    print("registro valido y PRUEBAS.md al dia")
    print(resumen(filas))


def cmd_tabla(filas, rom):
    validar(filas, rom)
    texto, a, b = bloque_actual()
    with open(PRUEBAS, "w", encoding="utf-8") as f:
        f.write(texto[:a] + "\n" + tabla(filas) + "\n" + texto[b:])
    print("tabla de PRUEBAS.md regenerada")
    print(resumen(filas))


def cmd_aptas(filas, rom):
    validar(filas, rom)
    si = [f for f in filas if apta(f)[0]]
    print(f"Aptas para una receta de juego: {len(si)}")
    for f in si:
        print(f"  {int(f['indice']):04d} {f['carta']}")
    print(f"No aptas: {len(filas) - len(si)}")
    for f in filas:
        ok, falta = apta(f)
        if not ok:
            print(f"  {int(f['indice']):04d} {f['carta']}: falta {falta}")


def cmd_pendientes(filas, rom):
    validar(filas, rom)
    pend = [f for f in filas if f["ev_ojo"] == "pendiente"]
    print(f"Pendientes de mirar: {len(pend)}")
    for f in pend:
        print(f"  {int(f['indice']):04d} {f['carta']} [{f['veredicto'] or 'sin veredicto'}]"
              f"  estado: {f['estado'] or '(sin estado)'}\n       {f['detalle']}")


def cmd_ojo(filas, rom, args):
    veredicto = None
    if "--veredicto" in args:
        k = args.index("--veredicto")
        veredicto = args[k + 1]
        args = args[:k] + args[k + 2:]
    if len(args) < 2 or args[1] not in ("si", "no"):
        raise SystemExit('uso: registro.py ojo ROM "CARTA" si|no ["que vio"] [--veredicto ...]')
    carta, vio, nota = args[0], args[1], (args[2] if len(args) > 2 else "")
    fila = next((f for f in filas if f["carta"] == carta), None)
    if fila is None:
        raise SystemExit(f"error: {carta!r} no esta en el registro")
    hoy = datetime.date.today().isoformat()
    if vio == "si":
        if veredicto:
            raise SystemExit("error: --veredicto solo se usa con 'no'")
        fila.update(ev_ojo="si", nota_ojo=nota, rom_md5=rom.md5, fecha=hoy)
    else:
        if not nota:
            raise SystemExit("error: con 'no' hay que decir que vio Oscar")
        veredicto = veredicto or "funciona en parte"
        if veredicto not in VEREDICTOS[1:]:
            raise SystemExit(f"error: el veredicto corregido tiene que ser uno de {VEREDICTOS[1:]}")
        antes = fila["veredicto"] or "sin veredicto"
        fila.update(ev_ojo="si", veredicto=veredicto, falla=nota, rom_md5=rom.md5, fecha=hoy,
                    nota_ojo=f"discrepancia: la prueba automatica daba '{antes}'; Oscar vio: {nota}")
    validar(filas, rom)
    escribir(filas)
    print(f"{carta}: ev_ojo = si, veredicto = {fila['veredicto']}")
    print("falta regenerar la tabla: python3 scripts/registro.py tabla ROM")


def main(argv):
    global EN_CURSO
    if "--en-curso" in argv:
        EN_CURSO = True
        argv = [a for a in argv if a != "--en-curso"]
    if len(argv) < 2 or argv[0] not in ("verificar", "tabla", "aptas", "pendientes", "ojo"):
        raise SystemExit(__doc__)
    if not os.path.exists(argv[1]):
        raise SystemExit(f"error: no existe el ROM {argv[1]}")
    rom, filas = Rom(argv[1]), leer()
    if argv[0] == "ojo":
        cmd_ojo(filas, rom, argv[2:])
    else:
        {"verificar": cmd_verificar, "tabla": cmd_tabla, "aptas": cmd_aptas,
         "pendientes": cmd_pendientes}[argv[0]](filas, rom)


if __name__ == "__main__":
    main(sys.argv[1:])
