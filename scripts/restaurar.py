"""Restaura cartas recortadas ocupando el hueco de un monstruo Normal.

El motor busca el efecto de una carta por su ID de Konami. Si a un indice del
juego le cambiamos el ID por el de una carta que tiene fila en la tabla de
efectos, ese hueco pasa a ser esa carta, con su efecto.

Una carta que el juego nunca tuvo (sin fila de efecto) entra igual si es un
monstruo Normal ("clase": "Normal"): no necesita efecto, solo los datos.

La receta (JSON) puede pedir parches de codigo en "parches":

  "busqueda_ids": true        cualquier hueco sirve para cualquier carta. Sin
                              este parche el hueco tiene que ser vecino del ID
                              nuevo, porque la tabla de IDs debe quedar ordenada.
  "invocacion_tipo": [...]    entradas {id_konami, tipo, cantidad} para la
                              invocacion especial retirando del Cementerio.
  "contrasenas_gratis": true  la maquina de contrasenas no descuenta DP. Solo
                              para ROMs de prueba.
  "efectos_nuevos": [{"id_konami": 4848, "columna": "fn_04", "fuente": "efectos/spy_mano.s"}]
                              pone una funcion propia (ensamblada con las
                              binutils de ARM) en una columna de la fila de
                              efecto. 'fuente' es relativa a la carpeta del
                              proyecto. Ver parches.efecto_nuevo.
  "menu_modos": {"6": "modo:1"}
                              llena modos vacios de los menus de seleccion
                              (tabla en 0x26678). El valor es una direccion
                              GBA o "modo:N" para copiar el manejador del
                              modo N. Es solo datos: no necesita keystone.
  "baul_inicial": 3           una partida nueva arranca con esa cantidad de
                              copias de cada carta de la receta en el baul.
                              Solo para ROMs de prueba.

Fuera de "parches":

  "hereda": "test.json"       toma las cartas y los parches de otra receta de la misma
                              carpeta; lo que se declare aca se suma o lo reemplaza. Una carta
                              con el "hueco" de una heredada corrige solo las claves que trae.
  "piezas": ["4848:fn_04:efectos/spy_mano.s", "G:08015C78:efectos/gancho_lista_campo.s",
             "T:08012C64:08013B4C:efectos/modificador_atk.s"]
                              funciones de efecto, ganchos (G:) y entradas de tabla (T:) de
                              efectos/, con la sintaxis de parche_efecto.py y en ese orden.
                              El codigo va desde 0x1A00000.

Cada carta lleva "clase": Normal, Effect, Fusion o Ritual para monstruos, o una
de SUBTIPOS para magicas y trampas. "anular_columnas" pone en cero columnas de
su fila de efecto (por ejemplo ["fn_c", "fn_18"]).
"arte" (opcional) es la ruta de un PNG, relativa a la carpeta del proyecto, con el
dibujo de la carta; sin esa clave la carta muestra el dibujo del hueco. Ver arte.py.

"sobres" (opcional, fuera de "parches") es una lista de cambios a los sobres de la tienda: que
cartas trae cada uno, el nombre, el precio. Se aplican despues de las cartas. Ver sobres.py.

Uso: python3 restaurar.py original.gba receta.json salida.gba
"""
import bisect
import json
import os
import re
import sys

from da_lib import *

# u32 de estadisticas que usa el juego para cada subtipo de magica y trampa
SUBTIPOS = {
    "Spell": 0x01600000, "Spell Field": 0x01640000, "Spell Equip": 0x01660000,
    "Spell Continuous": 0x01680000, "Spell Quick-Play": 0x016A0000, "Spell Ritual": 0x016C0000,
    "Trap": 0x21500000, "Trap Counter": 0x21520000, "Trap Continuous": 0x21580000,
}
COLUMNAS = {"fn_04": 4, "flags": 8, "fn_c": 0xC, "fn_10": 0x10, "fn_14": 0x14, "fn_18": 0x18}


def comprobar_huecos(receta, ruta_receta):
    """El registro de huecos (datos/huecos.csv) dice que indice ocupa cada carta restaurada. Tiene
    que ser el mismo en todas las versiones: si una carta cambia de indice, una partida guardada
    con una version anterior pasa a tener otra carta en el baul. Una receta no puede poner una
    carta registrada en otro hueco, ni usar el hueco de otra, ni traer una carta sin registrar."""
    if receta.get("historica"):
        return
    ruta = os.path.join(os.path.dirname(os.path.abspath(ruta_receta)), "..", "datos", "huecos.csv")
    assert os.path.exists(ruta), "falta datos/huecos.csv (el registro de huecos)"
    import csv
    filas = list(csv.DictReader(open(ruta, encoding="utf-8")))
    por_carta = {f["carta"]: f for f in filas}
    por_indice = {int(f["indice"]): f for f in filas}
    assert len(por_carta) == len(filas) == len(por_indice), "datos/huecos.csv tiene cartas o indices repetidos"
    for c in receta["cartas"]:
        r = por_carta.get(c["nombre"])
        if r is None:
            ocupa = por_indice.get(c["hueco"])
            assert ocupa is None, (f"{c['nombre']}: el hueco {c['hueco']} es de {ocupa['carta']} "
                                   f"segun datos/huecos.csv")
            raise AssertionError(f"{c['nombre']} no esta en datos/huecos.csv: registrala ahi (indice "
                                 f"{c['hueco']}, {c['hueco_nombre']}) antes de armar un ROM con ella")
        assert int(r["indice"]) == c["hueco"], (f"{c['nombre']}: la receta la pone en el hueco {c['hueco']} "
                                                f"y datos/huecos.csv dice {r['indice']}")
        assert int(r["id_konami"]) == c["id_konami"], f"{c['nombre']}: el ID no coincide con datos/huecos.csv"
        assert r["hueco_nombre"] == c["hueco_nombre"], f"{c['nombre']}: el hueco no coincide con datos/huecos.csv"


def main(ruta_rom, ruta_receta, ruta_salida):
    rom = Rom(ruta_rom)
    assert rom.md5 == MD5_USA, "este script solo esta verificado con el ROM USA"
    receta = json.load(open(ruta_receta, encoding="utf-8"))
    if "hereda" in receta:                       # las cartas y parches de otra receta de la carpeta
        base = json.load(open(os.path.join(os.path.dirname(os.path.abspath(ruta_receta)), receta["hereda"]),
                              encoding="utf-8"))
        assert "hereda" not in base, "una receta heredada no puede heredar de otra"
        # Una carta de esta receta con el mismo hueco que una heredada la corrige: solo hace falta
        # declarar las claves que cambian (por ejemplo "descripcion" o "anular_columnas").
        cartas = [dict(c) for c in base.get("cartas", [])]
        por_hueco = {c["hueco"]: c for c in cartas}
        for c in receta.get("cartas", []):
            if c["hueco"] in por_hueco:
                por_hueco[c["hueco"]].update(c)
            else:
                cartas.append(c)
        receta = {**base, **receta, "parches": {**base.get("parches", {}), **receta.get("parches", {})},
                  "cartas": cartas}
    comprobar_huecos(receta, ruta_receta)
    parches_pedidos = receta.get("parches", {})
    libre_orden = bool(parches_pedidos.get("busqueda_ids"))
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    cursor = LIBRE
    informe = []

    def escribir_texto(txt):
        nonlocal cursor
        datos = txt.encode("latin1") + b"\0"
        o = cursor
        rom.d[o:o + len(datos)] = datos
        cursor = (o + len(datos) + 3) & ~3
        return o

    renglones = rom.renglones_u32()     # mazos de rivales y mazos iniciales
    huecos_usados = set()
    for c in receta["cartas"]:
        i, nuevo = c["hueco"], c["id_konami"]
        viejo = rom.id_de(i)
        s = rom.stats(i)
        assert i not in huecos_usados, f"el hueco {i} esta repetido"
        huecos_usados.add(i)
        assert rom.nombre(i) == c["hueco_nombre"], f"el hueco {i} es {rom.nombre(i)!r}, no {c['hueco_nombre']!r}"
        assert s["tipo"] <= 20 and s["clase"] == 0, f"{rom.nombre(i)} no es un monstruo Normal"
        assert nuevo in filas or c["clase"] == "Normal", f"el ID {nuevo} no tiene fila de efecto"
        assert rom.indice_de(nuevo) == 0, f"el ID {nuevo} ya esta en el juego"
        assert len(c["nombre"]) <= 45, f"nombre demasiado largo: {c['nombre']}"
        if not libre_orden:
            abajo = rom.id_de(i - 1) if i > 1 else 0
            arriba = rom.id_de(i + 1) if i < N_CARTAS else 0xFFFF
            assert abajo < nuevo < arriba, f"el ID {nuevo} no entra entre {abajo} y {arriba}: romperia el orden"

        rom.w16(IDS + 2 * i, nuevo)
        if c["clase"] in SUBTIPOS:
            rom.w32(STATS + 4 * i, SUBTIPOS[c["clase"]])
        else:
            rom.w32(STATS + 4 * i, Rom.empaquetar_monstruo(
                c["atk"], c["def"], c["nivel"], ATRIBUTOS.index(c["atributo"]),
                TIPOS.index(c["tipo"]), CLASES.index(c["clase"])))
        rom.w32(NOMBRES_OFF + 4 * i, escribir_texto(c["nombre"]) - NOMBRES)
        rom.w32(DESCS_OFF + 4 * i, escribir_texto(c["descripcion"]) - DESCS)
        if c.get("contrasena"):
            rom.fijar_contrasena(i, c["contrasena"])
        for col in c.get("anular_columnas", []):
            rom.w32(EFECTOS + EFECTOS_FILA * filas[nuevo] + COLUMNAS[col], 0)
        if c.get("arte"):                    # dibujo propio; sin esta clave queda el del hueco
            import arte
            ruta_arte = os.path.join(os.path.dirname(os.path.abspath(ruta_receta)), "..", c["arte"])
            assert os.path.exists(ruta_arte), f"{c['nombre']}: no existe el dibujo {c['arte']}"
            arte.escribir(rom, i, ruta_arte)

        # Referencias al ID viejo, que deja de existir.
        tocados = []
        en_mazos = set(renglones)
        n_mazos = 0
        for o in renglones:
            if rom.u32(o) == viejo:
                rom.w32(o, nuevo)
                n_mazos += 1
        if n_mazos:
            tocados.append(f"{n_mazos} renglones de mazo")
        for o in range(LISTAS_INI, FIN_DATOS - 1, 2):
            if rom.u16(o) != viejo or o in en_mazos:
                continue
            # la mitad baja de un puntero a una lista de IDs (los pares de los sobres) no es un ID
            if o % 4 == 0 and 0x0800 <= rom.u16(o + 2) < 0x0A00:
                destino = rom.u32(o) - BASE
                if 0 < destino < len(rom.d) - 2 and rom.indice_de(rom.u16(destino)):
                    continue
            # solo si esta dentro de una lista de cartas: algun vecino tambien es un ID valido
            if rom.indice_de(rom.u16(o - 2)) or rom.indice_de(rom.u16(o + 2)):
                rom.w16(o, nuevo)
                tocados.append(f"lista {o:07X}")
            else:
                tocados.append(f"DUDOSO sin tocar {o:07X}")
        for q in range(EXAMEN_N):
            e = EXAMEN + rom.u32(EXAMEN_OFF + 4 * q)
            for campo in (2, 0xA, 0xC, 0xE):
                if rom.u16(e + campo) == viejo:
                    rom.w16(e + campo, nuevo)
                    tocados.append(f"examen {q}")
        informe.append((i, c["hueco_nombre"], viejo, c["nombre"], nuevo, rom.contrasena(i), tocados))

    # Orden alfabetico: el editor de mazos ordena por nombre con una tabla fija.
    # Se conserva el orden original y solo se recolocan las cartas renombradas.
    clave = lambda t: re.sub(r"[^a-z0-9 ]", "", t.lower())
    cambiados = {x[0] for x in informe}
    orden = sorted((i for i in range(1, N_CARTAS + 1) if i not in cambiados),
                   key=lambda i: rom.u16(ORDEN_ALFA + 2 * i))
    for i in sorted(cambiados):
        claves = [clave(rom.nombre(j)) for j in orden]
        orden.insert(bisect.bisect_left(claves, clave(rom.nombre(i))), i)
    for puesto, i in enumerate(orden):
        rom.w16(ORDEN_ALFA + 2 * i, puesto)

    # Parches de datos (sin ensamblador).
    for modo, destino in parches_pedidos.get("menu_modos", {}).items():
        rom.fijar_modo_menu(int(modo), destino)

    # Parches de codigo.
    if {k for k, v in parches_pedidos.items() if v and k != "menu_modos"}:
        import parches
        esp = parches.Espacio(rom)
        if libre_orden:
            parches.busqueda_ids(rom, esp)
        if parches_pedidos.get("invocacion_tipo"):
            parches.invocacion_tipo(rom, esp, [
                (e["id_konami"], parches.TIPO | TIPOS.index(e["tipo"]),
                 parches.TIPO | TIPOS.index(e["tipo"]), e["cantidad"])
                for e in parches_pedidos["invocacion_tipo"]])
        if parches_pedidos.get("contrasenas_gratis"):
            parches.contrasenas_gratis(rom)
        if parches_pedidos.get("baul_inicial"):
            parches.baul_inicial(rom, esp, [c["hueco"] for c in receta["cartas"]],
                                 int(parches_pedidos["baul_inicial"]))
        for e in parches_pedidos.get("efectos_nuevos", []):
            fuente = os.path.join(os.path.dirname(os.path.abspath(ruta_receta)), "..", e["fuente"])
            parches.efecto_nuevo(rom, esp, e["id_konami"], e["columna"], fuente)
        print(f"codigo nuevo en {parches.CODIGO:07X}-{esp.cur:07X}")

    # Piezas de efectos/ (funciones de efecto, ganchos y entradas de tabla), en el orden dado.
    if receta.get("piezas"):
        import parche_efecto
        raiz = os.path.join(os.path.dirname(os.path.abspath(ruta_receta)), "..")
        parche_efecto.aplicar(Rom(ruta_rom), rom, receta["piezas"], raiz)

    # Sobres de la tienda: despues de las cartas, para poder nombrar a las restauradas.
    if receta.get("sobres"):
        import sobres
        for hecho in sobres.aplicar(rom, receta["sobres"]):
            print(f"sobre {hecho['sobre']} ({hecho['nombre']}): "
                  + ", ".join(f"{len(v)} {r}" for r, v in hecho["listas"].items() if v))

    # Comprobaciones finales sobre el resultado.
    ids = [rom.id_de(i) for i in range(1, N_CARTAS + 1)]
    assert len(set(ids)) == N_CARTAS, "hay IDs repetidos"
    assert libre_orden or ids == sorted(ids), "la tabla de IDs quedo desordenada"
    for i, _, _, nombre, nuevo, _, _ in informe:
        assert rom.indice_de(nuevo) == i and rom.nombre(i) == nombre
    assert rom.renglones_u32() == renglones, "cambio la forma de las listas de mazos"
    validos = set(ids)
    for o in renglones:
        assert rom.u32(o) in validos, f"renglon de mazo {o:07X} con ID inexistente"
    pw = [x[5] for x in informe]
    assert len(set(pw)) == len(pw), "contrasenas repetidas"

    open(ruta_salida, "wb").write(rom.d)
    for i, hn, viejo, nombre, nuevo, pw, tocados in informe:
        print(f"indice {i}: {hn} ({viejo}) -> {nombre} ({nuevo}), contrasena {pw}")
        print("   referencias actualizadas:", ", ".join(tocados) or "ninguna")
    print(f"textos nuevos en {LIBRE:07X}-{cursor:07X}")
    assert cursor <= 0x1900000, "los textos pisan la zona de codigo"


if __name__ == "__main__":
    main(*sys.argv[1:4])
