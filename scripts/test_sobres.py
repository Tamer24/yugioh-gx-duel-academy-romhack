"""Prueba de scripts/sobres.py: leer y cambiar los sobres de la tienda, sin emulador.

Lo esperado sale del formato (PROYECTO.md 5.5) y del juego original:
  - los 48 sobres se leen y sus listas juntan las 1200 cartas, todas existentes;
  - agregar una carta a un sobre cambia solo la fila de ese sobre y la zona de datos nuevos, y las
    listas de los otros 47 quedan iguales;
  - cambiar nombre, precio y cartas por sobre se lee de vuelta;
  - se rechaza lo que colgaria el juego o no tiene sentido: menos comunes que cartas por sobre, una
    carta que no existe, una repetida, una rareza desconocida, y tocar las cartas del sobre 47.
La compra en pantalla se probo aparte (evidencia/sobres/).

Uso: python3 scripts/test_sobres.py ROM_ORIGINAL
"""
import sys

import sobres
from da_lib import Rom


def main():
    ok = True

    def caso(nombre, bien, detalle=""):
        nonlocal ok
        print(f"{'OK ' if bien else 'MAL'} {nombre}{': ' + detalle if detalle else ''}")
        ok = ok and bien

    def rechaza(nombre, cambio):
        rom = Rom(sys.argv[1])
        try:
            sobres.cambiar(rom, cambio)
            caso(nombre, False, "se acepto")
        except sobres.ErrorSobres as err:
            caso(nombre, True, str(err))

    original = Rom(sys.argv[1])
    todos = [sobres.leer(original, k) for k in range(sobres.N_SOBRES)]
    ids = {c for s in todos for v in s["listas"].values() for c in v}
    caso("48 sobres; entre todos traen las 1200 cartas", len(ids) == 1200 and all(original.indice_de(c) for c in ids),
         f"{len(ids)} cartas distintas")
    caso("el sobre 0 es Basic 1-A: 5 cartas, 100 DP, 40 cartas en listas",
         (todos[0]["nombre"], todos[0]["cartas_por_sobre"], todos[0]["precio"]) == ("Basic 1-A", 5, 100)
         and sum(len(v) for v in todos[0]["listas"].values()) == 40)
    caso("el sobre 47 (Dorothy's Gift) no tiene listas", not any(todos[47]["listas"].values()))
    p = sobres.probabilidades(original, todos[0])
    caso("probabilidades de Basic 1-A: 0,6% secretas, 1,9% ultra, 7,5% super, 80% raras",
         [round(1000 * p[r]) for r in ("secretas", "ultra", "super", "raras")] == [6, 19, 75, 800], str(p))

    rom = Rom(sys.argv[1])
    nueva = todos[1]["listas"]["comunes"][0]                 # una carta de Basic 1-B que no esta en Basic 1-A
    hecho = sobres.cambiar(rom, {"sobre": "Basic 1-A", "agregar": {"raras": [nueva]}})
    caso("agregar una carta: queda al final de su rareza", hecho["listas"]["raras"] == todos[0]["listas"]["raras"] + [nueva]
         and hecho["listas"]["comunes"] == todos[0]["listas"]["comunes"])
    cambiados = [o for o in range(len(rom.d)) if rom.d[o] != original.d[o]]
    caso("agregar una carta: solo cambia el puntero de ese sobre y la zona de datos nuevos",
         all(sobres.TABLA <= o < sobres.TABLA + 4 or sobres.ZONA <= o < sobres.FIN_ZONA for o in cambiados),
         f"{len(cambiados)} bytes")
    caso("agregar una carta: los otros 47 sobres quedan iguales",
         all(sobres.leer(rom, k) == todos[k] for k in range(1, sobres.N_SOBRES)))

    hecho = sobres.cambiar(rom, {"sobre": 3, "nombre": "Neo Space", "comentario": "Fresh from Neo-Space!", "precio": 300,
                                 "cartas_por_sobre": 3, "cartas": {"comunes": todos[3]["listas"]["comunes"][:4],
                                                                   "super": [original.nombre(1)]}})
    caso("cambiar nombre, textos, precio y cartas de un sobre",
         (hecho["nombre"], hecho["comentario"], hecho["precio"], hecho["cartas_por_sobre"]) == ("Neo Space", "Fresh from Neo-Space!", 300, 3)
         and hecho["listas"]["comunes"] == todos[3]["listas"]["comunes"][:4] and hecho["listas"]["super"] == [original.id_de(1)]
         and not hecho["listas"]["raras"] and hecho["consejo"] == todos[3]["consejo"])
    caso("el sobre se encuentra por su nombre nuevo", sobres.numero(rom, "Neo Space") == 3)

    rechaza("menos comunes que cartas por sobre: se rechaza", {"sobre": 0, "cartas": {"comunes": todos[0]["listas"]["comunes"][:4]}})
    rechaza("subir las cartas por sobre por encima de las comunes: se rechaza", {"sobre": 34, "cartas_por_sobre": 9})
    rechaza("carta que no existe: se rechaza", {"sobre": 0, "agregar": {"comunes": ["Carta Inventada"]}})
    rechaza("carta repetida en el sobre: se rechaza", {"sobre": 0, "agregar": {"raras": [todos[0]["listas"]["comunes"][0]]}})
    rechaza("rareza desconocida: se rechaza", {"sobre": 0, "agregar": {"legendarias": [nueva]}})
    rechaza("cartas en el sobre 47: se rechaza", {"sobre": 47, "agregar": {"comunes": [nueva]}})
    rechaza("la carta 1200 como comun no cuenta (el sorteo del juego original la descarta)",
            {"sobre": 34, "cartas_por_sobre": 3, "cartas": {"comunes": [original.id_de(1200)] + todos[34]["listas"]["comunes"][:2]}})
    rechaza("nombre demasiado largo: se rechaza", {"sobre": 0, "nombre": "x" * 24})
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
