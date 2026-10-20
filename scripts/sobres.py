"""Los sobres de la tienda: verlos y cambiarles las cartas, el nombre, el precio y los textos.

La tienda tiene 48 sobres fijos (0 a 47). Cada uno es una fila de 16 bytes en TABLA:
  +0  puntero a 5 pares (puntero a lista de IDs de Konami u16, cantidad u32), uno por RAREZA
  +4  u16 cartas por sobre      +6  u16 precio en DP
  +8  u16 cuantos repone        +10 u16 cada cuantas semanas repone      +12 u16 cuantos se van
y tres textos (TEXTOS: 3 offsets u32 por sobre, relativos a TEXTOS_BASE): el nombre, lo que dice
la vendedora y un consejo. La cantidad en venta de cada sobre esta en la partida, no en el ROM.

Como se arma un sobre al comprarlo (FUN_080BD89C): se tira un numero de 0 a 17999 y la primera
carta sale de la lista mas rara que tenga cartas y cuyo UMBRAL supere al numero; el resto se
completa con comunes, sin repetir carta dentro del sobre. Por eso un sobre necesita por lo menos
tantas comunes como cartas trae: con menos, el juego se queda sorteando para siempre.
El sorteo descarta la carta de indice igual a la cantidad de cartas del ROM (la 1200 en el juego
original); scripts/ampliar.py lo corrige para las cartas que agrega.
El sobre 47 (Dorothy's Gift) no tiene listas: reparte cartas de todo el juego y no se puede cambiar.

Los datos nuevos (listas y textos) van desde ZONA, que empieza con MARCA y el offset libre.

En una receta (restaurar.py) o con --sobres en ampliar.py, la clave "sobres" es una lista de:
  {"sobre": "Basic 1-A",                  nombre exacto o numero
   "nombre": "...", "comentario": "...", "consejo": "...", "precio": 150, "cartas_por_sobre": 5,
   "repone": 40, "semanas": 1, "se_van": 10,
   "agregar": {"comunes": ["Elemental Hero Neos"]},     cartas por nombre exacto o ID de Konami
   "quitar": ["Tyhone"],
   "cartas": {"comunes": [...], "raras": [...]}}        reemplaza todas las listas del sobre
Todas las claves salvo "sobre" son opcionales.

Uso (desde la raiz del proyecto):
  python3 scripts/sobres.py listar ROM
  python3 scripts/sobres.py ver ROM SOBRE
  python3 scripts/sobres.py aplicar ROM cambios.json SALIDA     cambios.json = {"sobres": [...]}
"""
import json
import struct
import sys

from da_lib import BASE, Rom

N_SOBRES = 48
TABLA = 0x17F2844
TEXTOS = 0x17F2B44
TEXTOS_BASE = 0x14EDD78
UMBRALES = 0x17F0DC4           # 4 x u16: 112, 450, 1800, 16200 (sobre 18000)
TIRADA = 18000
REGALO = 47                    # Dorothy's Gift
# posicion del par en el sobre; la 0 completa el sobre y las otras dan, a lo sumo, la primera carta
RAREZAS = ("comunes", "raras", "super", "ultra", "secretas")
CAMPOS = (("cartas_por_sobre", 4), ("precio", 6), ("repone", 8), ("semanas", 10), ("se_van", 12))
CLAVES_TEXTO = ("nombre", "comentario", "consejo")
LARGO_TEXTO = (23, 84, 68)     # los mas largos que trae el juego
ZONA, FIN_ZONA = 0x1E00000, 0x1F00000
MARCA = b"DA-SOBRES-1\0"


class ErrorSobres(Exception):
    pass


def leer(rom, k):
    """El sobre k: sus campos, sus textos y sus listas de IDs de Konami por rareza."""
    fila = TABLA + 16 * k
    s = {"sobre": k, "listas": {}}
    for clave, o in CAMPOS:
        s[clave] = rom.u16(fila + o)
    for j, clave in enumerate(CLAVES_TEXTO):
        s[clave] = rom.cstr(TEXTOS_BASE + rom.u32(TEXTOS + 12 * k + 4 * j))
    pares = rom.u32(fila) - BASE
    for j, rareza in enumerate(RAREZAS):
        lista, n = rom.u32(pares + 8 * j), rom.u32(pares + 8 * j + 4)
        s["listas"][rareza] = [rom.u16(lista - BASE + 2 * i) for i in range(n)] if lista else []
    return s


def numero(rom, sobre):
    if isinstance(sobre, int) or str(sobre).isdigit():
        k = int(sobre)
        if not 0 <= k < N_SOBRES:
            raise ErrorSobres(f"el sobre {k} no existe: van de 0 a {N_SOBRES - 1}")
        return k
    for k in range(N_SOBRES):
        if leer(rom, k)["nombre"] == sobre:
            return k
    raise ErrorSobres(f"no hay un sobre que se llame {sobre!r}")


def probabilidades(rom, s):
    """De cada rareza con cartas: la probabilidad de que la primera carta del sobre salga de ahi."""
    umbrales = [rom.u16(UMBRALES + 2 * j) for j in range(4)]      # secretas, ultra, super, raras
    p, antes = {}, 0
    for j, umbral in enumerate(umbrales):
        rareza = RAREZAS[4 - j]
        if s["listas"][rareza]:
            p[rareza] = (umbral - antes) / TIRADA
            antes = umbral
    return p


def _id(rom, carta):
    if isinstance(carta, int) or str(carta).isdigit():
        cid = int(carta)
        if not rom.indice_de(cid):
            raise ErrorSobres(f"el ID {cid} no es de una carta de este ROM")
        return cid
    for i in range(1, rom.n + 1):
        if rom.nombre(i) == carta:
            return rom.id_de(i)
    raise ErrorSobres(f"la carta {carta!r} no existe en este ROM")


def _espacio(rom):
    """Offset libre de ZONA (la abre si hace falta)."""
    if bytes(rom.d[ZONA:ZONA + len(MARCA)]) != MARCA:
        rom.d[ZONA:ZONA + len(MARCA)] = MARCA
        rom.w32(ZONA + len(MARCA), ZONA + len(MARCA) + 4)
    return rom.u32(ZONA + len(MARCA))


def _poner(rom, datos):
    o = _espacio(rom)
    fin = (o + len(datos) + 3) & ~3
    if fin > FIN_ZONA:
        raise ErrorSobres("no queda lugar para los datos de los sobres")
    rom.d[o:o + len(datos)] = datos
    rom.w32(ZONA + len(MARCA), fin)
    return o


def cambiar(rom, cambio):
    """Aplica un cambio (ver el formato arriba) al ROM. Devuelve el sobre como queda."""
    desconocidas = set(cambio) - {"sobre", "agregar", "quitar", "cartas"} - {c for c, _ in CAMPOS} - set(CLAVES_TEXTO)
    if desconocidas:
        raise ErrorSobres(f"claves que no entiendo: {', '.join(sorted(desconocidas))}")
    k = numero(rom, cambio["sobre"])
    s = leer(rom, k)
    fila = TABLA + 16 * k
    listas = {r: list(v) for r, v in s["listas"].items()}
    if any(c in cambio for c in ("agregar", "quitar", "cartas")):
        if k == REGALO:
            raise ErrorSobres(f"el sobre {k} ({s['nombre']}) reparte cartas de todo el juego: no tiene listas")
        for clave in ("agregar", "cartas"):
            for rareza in cambio.get(clave, {}):
                if rareza not in RAREZAS:
                    raise ErrorSobres(f"rareza desconocida: {rareza!r} (son {', '.join(RAREZAS)})")
        if "cartas" in cambio:
            listas = {r: [_id(rom, c) for c in cambio["cartas"].get(r, [])] for r in RAREZAS}
        for carta in cambio.get("quitar", []):
            cid = _id(rom, carta)
            if not any(cid in v for v in listas.values()):
                raise ErrorSobres(f"{carta!r} no esta en el sobre {s['nombre']}")
            listas = {r: [c for c in v if c != cid] for r, v in listas.items()}
        for rareza, cartas in cambio.get("agregar", {}).items():
            listas[rareza] += [_id(rom, c) for c in cartas]
    for clave, o in CAMPOS:
        if clave in cambio:
            if not 0 <= int(cambio[clave]) <= 0xFFFF:
                raise ErrorSobres(f"{clave} fuera de rango: {cambio[clave]}")
            rom.w16(fila + o, int(cambio[clave]))
    por_sobre = rom.u16(fila + 4)
    if k != REGALO:
        todas = [c for v in listas.values() for c in v]
        repetidas = sorted({rom.nombre(rom.indice_de(c)) for c in todas if todas.count(c) > 1})
        if repetidas:
            raise ErrorSobres(f"cartas repetidas en el sobre {s['nombre']}: {', '.join(repetidas)}")
        salen = [c for c in listas["comunes"] if rom.indice_de(c) < rom.n or _sale_la_ultima(rom)]
        if len(salen) < por_sobre:
            raise ErrorSobres(f"el sobre {s['nombre']} trae {por_sobre} cartas y tiene {len(salen)} comunes "
                              "que pueden salir: el juego se quedaria sorteando para siempre")
        if listas != s["listas"]:
            pares = b""
            for rareza in RAREZAS:
                ids = listas[rareza]
                lista = _poner(rom, struct.pack(f"<{len(ids)}H", *ids)) if ids else 0
                pares += struct.pack("<II", BASE + lista if ids else 0, len(ids))
            rom.w32(fila, BASE + _poner(rom, pares))
    for j, clave in enumerate(CLAVES_TEXTO):
        if clave in cambio and cambio[clave] != s[clave]:
            datos = cambio[clave].encode("latin1")
            if not datos or len(datos) > LARGO_TEXTO[j]:
                raise ErrorSobres(f"{clave} del sobre {k}: de 1 a {LARGO_TEXTO[j]} letras, y tiene {len(datos)}")
            rom.w32(TEXTOS + 12 * k + 4 * j, _poner(rom, datos + b"\0") - TEXTOS_BASE)
    return leer(rom, k)


def _sale_la_ultima(rom):
    """Si el sorteo ya acepta la carta de indice igual a la cantidad (lo corrige ampliar.py)."""
    return bytes(rom.d[0xBD980:0xBD982]) == bytes.fromhex("c4d9")


def aplicar(rom, cambios):
    """Aplica una lista de cambios y comprueba que ninguna carta de un sobre haya quedado sin existir."""
    hechos = [cambiar(rom, c) for c in cambios]
    for k in range(N_SOBRES):
        for rareza, ids in leer(rom, k)["listas"].items():
            for c in ids:
                assert rom.indice_de(c), f"sobre {k}, {rareza}: el ID {c} no es de una carta de este ROM"
    return hechos


def _mostrar(rom, s):
    p = probabilidades(rom, s)
    print(f"{s['sobre']:2d} {s['nombre']}: {s['cartas_por_sobre']} cartas, {s['precio']} DP; repone {s['repone']} "
          f"cada {s['semanas']} semana(s), se van {s['se_van']}")
    print(f"   vendedora: {s['comentario']!r}\n   consejo: {s['consejo']!r}")
    for rareza in RAREZAS:
        ids = s["listas"][rareza]
        if not ids:
            continue
        nota = "completan el sobre" if rareza == "comunes" else f"primera carta en el {100 * p[rareza]:.1f}% de los sobres"
        print(f"   {rareza} ({len(ids)}; {nota}):")
        for c in ids:
            i = rom.indice_de(c)
            print(f"      {c:5d}  {rom.nombre(i)}" + ("   (indice igual a la cantidad: no sale)"
                                                       if i == rom.n and not _sale_la_ultima(rom) else ""))


def main(argv):
    if len(argv) == 2 and argv[0] == "listar":
        rom = Rom(argv[1])
        for k in range(N_SOBRES):
            s = leer(rom, k)
            cuenta = "/".join(str(len(s["listas"][r])) for r in RAREZAS)
            print(f"{k:2d} {s['nombre']:24} x{s['cartas_por_sobre']} {s['precio']:5d} DP  repone {s['repone']:2d} "
                  f"cada {s['semanas']} sem., se van {s['se_van']:2d}  cartas {cuenta}")
    elif len(argv) == 3 and argv[0] == "ver":
        rom = Rom(argv[1])
        _mostrar(rom, leer(rom, numero(rom, argv[2])))
    elif len(argv) == 4 and argv[0] == "aplicar":
        rom = Rom(argv[1])
        for s in aplicar(rom, json.load(open(argv[2], encoding="utf-8"))["sobres"]):
            _mostrar(rom, s)
        open(argv[3], "wb").write(rom.d)
        print(f"{argv[3]}: datos de sobres en {ZONA:07X}-{_espacio(rom):07X}")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except (ErrorSobres, OSError) as err:
        raise SystemExit(f"error: {err}")
