"""Clasifica cartas antes de trabajarlas: que trae el ROM de cada una y cuanto falta.

Es la entrada del sistema para un pack nuevo: se le da una lista de cartas y contesta, por carta,
si ya esta en el juego, si esta recortada (tiene fila de efecto pero no se puede conseguir) o si
no existe en el ROM; y, para las recortadas, que hay en su fila y que hace el motor con su ID.

Uso (desde la raiz del proyecto):
  python3 scripts/triage.py ROM_ORIGINAL "Nombre o ID" [...]     cartas sueltas
  python3 scripts/triage.py ROM_ORIGINAL --archivo pack.txt       una carta por linea
  python3 scripts/triage.py ROM_ORIGINAL --recortadas             todas las recortadas sin restaurar
  python3 scripts/triage.py ROM_ORIGINAL --calibrar               las ya restauradas, contra lo que paso
  ... [--csv salida.csv]

Diagnostico de una recortada, segun su columna fn_04 (el codigo del efecto):
  A  comparte la funcion con cartas que estan en el juego: codigo ya probado por el juego
  C  funcion propia (ninguna carta en juego la usa): codigo sin probar, puede estar incompleto
  D  funcion vacia: el efecto hay que escribirlo de cero
  E  sin funcion de efecto: asi estan en el juego las cartas de efecto continuo (Toon World,
     Insect Barrier), que el motor resuelve por ID. Si el motor nombra a la carta, puede que su
     efecto este; si nadie la nombra, no hay nada. Ninguna de las 30 restauradas era de este
     grupo: es el unico sin calibrar
Aparte del codigo del efecto esta COMO SE ACTIVA la carta, que el diagnostico no ve entero:
  - un monstruo con efecto de campo (tiene fn_10) que no esta en las listas del menu se avisa: se
    arregla agregando su ID a efectos/gancho_lista_campo.s y gancho_menu_campo.s;
  - un disparador ("cuando va al cementerio", "cuando la destruyen") puede no existir en el motor:
    la columna 'motor' dice en cuantas funciones aparece su ID fuera de su fila (0 = nadie la nombra).
Es una estimacion para ordenar el trabajo, no un veredicto: --calibrar la mide contra las cartas ya
restauradas (a cuales hubo que reescribirles la fn_04). El veredicto sale de jugarla.
"""
import csv
import os
import sys

import buscar_id
import funciones
from da_lib import BASE, N_CARTAS, Rom

RAIZ = funciones.RAIZ
COLUMNAS = ("fn_04", "fn_0C", "fn_10", "fn_14", "fn_18")
VACIAS = (bytes.fromhex("00207047"), bytes.fromhex("01207047"))    # movs r0, #0 / #1 ; bx lr
TEXTOS = {"A": "efecto compartido con cartas en juego", "C": "codigo propio sin probar",
          "D": "efecto vacio: de cero", "E": "sin funcion de efecto (continuo, por ID en el motor)"}
MENU_CAMPO = (0x08015C78, 0x08079200)      # las dos listas por ID del menu de un monstruo en el campo


def leer(nombre):
    with open(os.path.join(RAIZ, "datos", nombre), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class Triage:
    def __init__(self, rom):
        self.rom = rom
        self.filas = {int(f["id_konami"]): f for f in leer("efectos.csv")}
        for f in self.filas.values():           # una columna vale si es una direccion (hay "sin_efecto")
            for c in COLUMNAS:
                if not (len(f[c]) == 8 and f[c].startswith("08")):
                    f[c] = ""
        self.restauradas = {int(f["id_konami"]): f for f in leer("huecos.csv")}
        self.tipos = {int(f["id_konami"]): f["tipo"] for f in leer("cartas_recortadas.csv")}
        self.en_juego = {rom.id_de(i): rom.nombre(i) for i in range(1, N_CARTAS + 1)}
        self.por_nombre = {f["nombre"]: k for k, f in self.filas.items()}
        self.por_nombre.update({n: k for k, n in self.en_juego.items()})
        punteros = {int(f[c], 16) & ~1 for f in self.filas.values() for c in COLUMNAS if f[c]}
        funciones.registrar(punteros)
        # quien usa cada funcion, y que IDs compara cada funcion del juego
        self.usuarios = {}
        for cid, f in self.filas.items():
            for c in COLUMNAS:
                if f[c]:
                    self.usuarios.setdefault((c, int(f[c], 16) & ~1), []).append(cid)
        self.ids_de = {}
        for cid, sitios in buscar_id.mapa(rom).items():
            for direccion, _ in sitios:
                self.ids_de.setdefault(funciones.inicio(rom.d, direccion), set()).add(cid)

    def id_de(self, texto):
        if texto.isdigit():
            return int(texto)
        return self.por_nombre.get(texto)

    def vacia(self, direccion):
        return bytes(self.rom.d[direccion - BASE:direccion - BASE + 4]) in VACIAS

    def carta(self, texto):
        cid = self.id_de(texto)
        r = dict(carta=texto, id_konami=cid or "", estado="", tipo="", diagnostico="", por_que="",
                 fn_04="", otras_columnas="", motor="", avisos="")
        if cid is None:
            r["estado"] = "no esta en el ROM"
            r["por_que"] = "sin fila de efecto ni datos: habria que crearla entera (datos, texto, efecto)"
            return r
        fila = self.filas.get(cid)
        r["carta"] = fila["nombre"] if fila else self.en_juego.get(cid, texto)
        r["tipo"] = self.tipos.get(cid, "")
        if cid in self.restauradas:
            r["estado"] = "restaurada (" + self.restauradas[cid]["desde"] + ")"
        elif cid in self.en_juego:
            r["estado"] = "ya esta en el juego"
            return r
        elif not fila:
            r["estado"] = "no esta en el ROM"
            return r
        else:
            r["estado"] = "recortada"
        # --- fn_04
        if not fila["fn_04"]:
            fuera = sorted({funciones.inicio(self.rom.d, d) for d, _ in buscar_id.sitios(self.rom, cid)})
            r["diagnostico"], r["por_que"] = "E", TEXTOS["E"]
            r["fn_04"] = "sin funcion de efecto; " + (f"el motor la nombra en {len(fuera)} funciones" if fuera
                                                       else "el motor no la nombra")
            r["motor"] = f"{len(fuera)} funciones: " + ", ".join(f"{x:08X}" for x in fuera) if fuera else "ninguna"
            return r
        f4 = int(fila["fn_04"], 16) & ~1
        vivos = [c for c in self.usuarios[("fn_04", f4)] if c in self.en_juego and c not in self.restauradas]
        ids_funcion = self.ids_de.get(f4, set())
        if self.vacia(f4):
            r["diagnostico"], r["fn_04"] = "D", f"{f4:08X} vacia"
        elif not vivos:
            otras = len(self.usuarios[("fn_04", f4)]) - 1
            r["diagnostico"] = "C"
            r["fn_04"] = f"{f4:08X} propia" + (f" (la comparte con {otras} recortadas)" if otras else "")
        else:
            ejemplo = self.en_juego[vivos[0]]
            r["diagnostico"] = "A"
            como = ("no distingue por ID" if not ids_funcion else
                    "por ID, con su caso" if cid in ids_funcion else "nombra otros IDs, no el suyo")
            r["fn_04"] = f"{f4:08X} compartida con {len(vivos)} en juego (p. ej. {ejemplo}); {como}"
        r["por_que"] = TEXTOS[r["diagnostico"]]
        # --- las otras columnas
        otras = []
        for c in COLUMNAS[1:]:
            if not fila[c]:
                continue
            d = int(fila[c], 16) & ~1
            vivos = [x for x in self.usuarios[(c, d)] if x in self.en_juego and x not in self.restauradas]
            ids_funcion = self.ids_de.get(d, set())
            if self.vacia(d):
                nota = "vacia"
            elif not vivos:
                nota = "propia"
            elif ids_funcion and cid not in ids_funcion:
                nota = "compartida, por ID, sin su caso"
            else:
                nota = "compartida"
            otras.append(f"{c} {nota}")
        r["otras_columnas"] = "; ".join(otras)
        # --- donde mas la trata el motor
        propias = {int(fila[c], 16) & ~1 for c in COLUMNAS if fila[c]}
        fuera = sorted({funciones.inicio(self.rom.d, d) for d, _ in buscar_id.sitios(self.rom, cid)} - propias)
        r["motor"] = f"{len(fuera)} funciones: " + ", ".join(f"{x:08X}" for x in fuera) if fuera else "ninguna"
        es_monstruo = not any(x in r["tipo"] for x in ("Spell", "Trap"))
        if es_monstruo and fila["fn_10"] and not all(cid in self.ids_de.get(m, ()) for m in MENU_CAMPO):
            r["avisos"] = "efecto de campo fuera del menu: agregar el ID a las dos listas"
        return r


def calibrar(t):
    """Las cartas ya restauradas: el diagnostico contra lo que hubo que hacerles (recetas/lote.json)."""
    import json
    piezas = json.load(open(os.path.join(RAIZ, "recetas", "lote.json"), encoding="utf-8"))["piezas"]
    reescritas = {int(p.split(":")[0]) for p in piezas if p.split(":")[1].lower() == "fn_04"}
    en_menu = set()
    for nombre in ("gancho_lista_campo.s", "gancho_menu_campo.s"):
        for linea in open(os.path.join(RAIZ, "efectos", nombre), encoding="utf-8"):
            if linea.strip().startswith(".hword") and linea.split()[1].isdigit():
                en_menu.add(int(linea.split()[1]))
    cuenta, lineas, menu = {}, [], [0, 0, 0]
    for cid in t.restauradas:
        r = t.carta(str(cid))
        rehecha = cid in reescritas
        cuenta.setdefault(r["diagnostico"], [0, 0])[1 if rehecha else 0] += 1
        aviso, real = bool(r["avisos"]), cid in en_menu
        menu[0 if aviso and real else 1 if aviso else 2 if real else 0] += aviso or real
        lineas.append(f"  {r['diagnostico']}  {'fn_04 reescrita' if rehecha else 'fn_04 original':<16} "
                      f"{'menu: aviso' if aviso else '':<12}{'(hizo falta)' if real else '':<13} {r['carta']:<26} {r['fn_04'][:70]}")
    print("Diagnostico contra lo que paso con las cartas ya restauradas:")
    print("\n".join(sorted(lineas)))
    print("\n  diagnostico                                 fn_04 original   fn_04 reescrita")
    for d in sorted(cuenta):
        print(f"  {d}  {TEXTOS[d]:<40} {cuenta[d][0]:>8} {cuenta[d][1]:>16}")
    print(f"\n  aviso del menu de campo: {menu[0]} acertados, {menu[1]} de mas, {menu[2]} sin avisar")


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)
    rom, args = Rom(argv[0]), argv[1:]
    t = Triage(rom)
    salida = None
    if "--csv" in args:
        salida = args[args.index("--csv") + 1]
        del args[args.index("--csv"):args.index("--csv") + 2]
    if args == ["--calibrar"]:
        return calibrar(t)
    if args == ["--recortadas"]:
        pedidas = [str(c) for c, f in t.filas.items() if f["en_juego"] == "NO" and c not in t.restauradas]
    elif args[0] == "--archivo":
        pedidas = [l.strip() for l in open(args[1], encoding="utf-8") if l.strip() and not l.startswith("#")]
    else:
        pedidas = args
    resultados = sorted((t.carta(x) for x in pedidas), key=lambda r: (r["diagnostico"] or "Z", r["carta"]))
    for r in resultados:
        print(f"{r['diagnostico'] or '-':<2} {r['carta']:<34} {r['estado']:<22} {r['tipo']:<22} {r['fn_04']}")
        extra = [x for x in (r["otras_columnas"], "motor: " + r["motor"] if r["motor"] else "",
                             "AVISO: " + r["avisos"] if r["avisos"] else "") if x]
        if extra:
            print(f"   {'':<34} " + " | ".join(extra)[:200])
    cuenta = {}
    for r in resultados:
        clave = TEXTOS.get(r["diagnostico"], r["estado"])
        cuenta[clave] = cuenta.get(clave, 0) + 1
    print("\n" + " | ".join(f"{k}: {v}" for k, v in cuenta.items()))
    if salida:
        with open(salida, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(resultados[0]))
            w.writeheader()
            w.writerows(resultados)
        print(f"escrito {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
