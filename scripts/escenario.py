"""Arma escenarios de duelo editando un estado, y comprueba que quedaron como se pidio.

Parte de un estado guardado DENTRO de un duelo (estados/duelo-inicio.ss1) y cambia que
carta ocupa cada posicion de la mano o del mazo de cualquiera de los dos lados. De cada
carta escribe el indice, el ATK, la DEF, el atributo, el tipo y el nivel, para que los
menus y la IA la traten como lo que es. Nunca escribe sobre el estado de partida.

Uso:
  python3 escenario.py ROM BASE.st SALIDA.st [--yo POS:CARTA ...] [--rival POS:CARTA ...]
                                             [--mazo-yo POS:CARTA ...] [--mazo-rival POS:CARTA ...]
  python3 escenario.py ROM ESTADO.st --mostrar

POS cuenta desde 0. En el mazo, la posicion 0 es la proxima carta que se roba.
CARTA es el nombre exacto o el indice (1..1200).

Como modulo: armar() devuelve la ruta del estado; instantanea(duelo) y comprobar(duelo, ...)
trabajan sobre un duelo en marcha (duelo_auto.Duelo).
"""
import os
import struct
import sys
import tempfile

import estado
from da_lib import Rom, N_CARTAS

MAZO = 0x28A4                  # lista de ranuras del mazo; la PRIMERA es la proxima que se roba
CONTADORES = 0x1B              # u64 empaquetado: total, mano, mazo, cementerio (7 bits cada uno)
TIPO_TRAMPA, TIPO_MAGICA = 21, 22
POSICIONES = {0x10: "ataque", 0x30: "defensa", 0x20: "boca abajo"}


class ErrorEscenario(Exception):
    pass


def indice(rom, carta):
    """Nombre exacto o indice -> indice (1..1200)."""
    if isinstance(carta, int) or str(carta).isdigit():
        i = int(carta)
        if not 1 <= i <= N_CARTAS:
            raise ErrorEscenario(f"indice de carta fuera de rango: {carta}")
        return i
    for i in range(1, N_CARTAS + 1):
        if rom.nombre(i) == carta:
            return i
    raise ErrorEscenario(f"la carta {carta!r} no existe en el ROM")


def es_monstruo(rom, i):
    return rom.stats(i)["tipo"] not in (TIPO_TRAMPA, TIPO_MAGICA)


# --- edicion del estado -----------------------------------------------------------------
def _base_lado(lado):
    return estado.WRAM + estado.DUELO + lado * estado.LADO_BYTES


def contadores(e, lado):
    v = struct.unpack_from("<Q", e, _base_lado(lado) + CONTADORES)[0]
    return {"total": v & 0x7F, "mano": (v >> 7) & 0x7F, "mazo": (v >> 14) & 0x7F,
            "cementerio": (v >> 21) & 0x7F}


def _ranura(byte):
    return estado.WRAM + estado.DUELO + (byte & 0x7F) * estado.RANURA + (byte >> 7) * estado.LADO_BYTES


def ranura_mazo(e, lado, pos):
    """Offset de la ranura que ocupa la posicion 'pos' del mazo (0 = la proxima que se roba)."""
    n = contadores(e, lado)["mazo"]
    if not 0 <= pos < n:
        raise ErrorEscenario(f"el mazo del lado {lado} tiene {n} cartas; la posicion {pos} no existe")
    return _ranura(e[_base_lado(lado) + MAZO + pos])


def ranura_mano(e, lado, pos):
    n = estado.cantidad_mano(e, lado)
    if not 0 <= pos < n:
        raise ErrorEscenario(f"la mano del lado {lado} tiene {n} cartas; la posicion {pos} no existe")
    return estado.ranura_mano(e, lado, pos)


def escribir_carta(e, a, rom, i):
    """Convierte la ranura del offset 'a' en la carta de indice 'i'."""
    s = rom.stats(i)
    viejo = struct.unpack_from("<H", e, a + 0x24)[0]
    struct.pack_into("<H", e, a + 0x24, (viejo & 0x8000) | i)
    e[a + 0x30] = ((s["atributo"] & 7) << 5) | (s["tipo"] & 0x1F)
    if es_monstruo(rom, i):
        struct.pack_into("<I", e, a + 0x28, s["atk"])
        struct.pack_into("<I", e, a + 0x2C, s["def"])
        e[a + 0x31] = (e[a + 0x31] & 0xF0) | (s["nivel"] & 0xF)


def leer_carta(e, a):
    return struct.unpack_from("<H", e, a + 0x24)[0] & 0x7FFF


def armar(ruta_rom, base, salida=None, yo=None, rival=None, mazo_yo=None, mazo_rival=None, cursor=None,
          nivel_yo=None):
    """Escribe un estado nuevo con las cartas pedidas. Cada argumento es {posicion: carta}.

    'cursor': carta que el panel muestra bajo el cursor al cargar (cosmetico).
    'nivel_yo': {posicion de mi mano: nivel}. Ayuda de prueba: deja colocar sin tributo un monstruo
    de nivel 5 o mas. El texto y las estrellas de la carta no cambian.
    Devuelve la ruta del estado. Si no se da 'salida', usa un archivo temporal.
    """
    rom = ruta_rom if isinstance(ruta_rom, Rom) else Rom(ruta_rom)
    if salida and os.path.exists(salida) and os.path.samefile(salida, base):
        raise ErrorEscenario("la salida no puede ser el mismo archivo que el estado de partida")
    e = estado.abrir(base)
    estado.comprobar(e)
    pedidos = []                                   # (ranura, indice, descripcion)
    for lado, cambios, donde in ((0, yo, ranura_mano), (1, rival, ranura_mano),
                                 (0, mazo_yo, ranura_mazo), (1, mazo_rival, ranura_mazo)):
        for pos, carta in (cambios or {}).items():
            zona = "mano" if donde is ranura_mano else "mazo"
            pedidos.append((donde(e, lado, int(pos)), indice(rom, carta), f"{zona} del lado {lado}, posicion {pos}"))
    for a, i, _ in pedidos:                        # todo validado: recien ahora se escribe
        escribir_carta(e, a, rom, i)
    niveles = [(ranura_mano(e, 0, int(pos)), int(n)) for pos, n in (nivel_yo or {}).items()]
    for a, n in niveles:
        if not 1 <= n <= 12:
            raise ErrorEscenario(f"nivel fuera de rango: {n}")
        e[a + 0x31] = (e[a + 0x31] & 0xF0) | n
    if cursor is not None:
        struct.pack_into("<H", e, estado.WRAM + 0x19F0C, indice(rom, cursor))
    if salida is None:
        f = tempfile.NamedTemporaryFile(suffix=".st", delete=False)
        salida = f.name
        f.close()
    with open(salida, "wb") as f:
        f.write(e)
    e2 = estado.abrir(salida)                      # releer y comprobar
    for a, i, que in pedidos:
        if leer_carta(e2, a) != i:
            raise ErrorEscenario(f"el estado escrito no tiene la carta pedida en {que}")
    return salida


def mostrar(ruta_rom, ruta_estado):
    rom = Rom(ruta_rom)
    e = estado.abrir(ruta_estado)
    estado.comprobar(e)
    for lado, quien in ((0, "jugador"), (1, "rival")):
        c = contadores(e, lado)
        lp = struct.unpack_from("<I", e, _base_lado(lado))[0]
        print(f"{quien}: LP {lp} | mano {c['mano']} | mazo {c['mazo']} | cementerio {c['cementerio']}")
        for pos in range(c["mano"]):
            i = leer_carta(e, ranura_mano(e, lado, pos))
            print(f"   mano[{pos}] {i:4} {rom.nombre(i)}")
        for pos in range(min(5, c["mazo"])):
            i = leer_carta(e, ranura_mazo(e, lado, pos))
            print(f"   mazo[{pos}] {i:4} {rom.nombre(i)}")


# --- duelo en marcha --------------------------------------------------------------------
def instantanea(d):
    """Lo que se compara para decidir un veredicto. Campo por CONTROLADOR; lo demas por dueno."""
    from duelo_auto import J0, J1, LISTA_ZONAS

    def ranura(idc):
        return (J1 if idc & 0x80 else J0) + (idc & 0x7F) * 0x50

    def nombre(a):
        return d.rom.nombre(d.g.r16(a + 0x24) & 0x7FFF)

    s = {"LP": list(d.lp())}
    for lado, quien in ((0, "yo"), (1, "rival")):
        monstruos, magias = [], []
        for z in range(11):
            idc = d.g.r8(LISTA_ZONAS + 11 * lado + z)
            if idc == 0xFF:
                continue
            a = ranura(idc)
            if z < 5:
                monstruos.append((nombre(a), POSICIONES.get(d.g.r8(a + 0x33), hex(d.g.r8(a + 0x33))),
                                  d.g.r32(a + 0x28), d.g.r32(a + 0x2C)))
            else:
                magias.append(nombre(a))
        s[f"campo_{quien}"] = sorted(monstruos)
        s[f"magias_{quien}"] = sorted(magias)
        s[f"mano_{quien}"] = sorted(n for _, n in d.zona(lado, "f"))
        s[f"cementerio_{quien}"] = sorted(n for _, n in d.zona(lado, "d"))
        s[f"retiradas_{quien}"] = sorted(n for _, n in d.zona(lado, "e"))
        s[f"mazo_{quien}"] = len(d.zona(lado, "c"))
    return s


def comprobar(d, esperado):
    """esperado: {clave de la instantanea: [nombres que tienen que estar] o un numero}.
    Devuelve la lista de diferencias; vacia si la preparacion es la pedida."""
    s = instantanea(d)
    faltas = []
    for clave, pedido in esperado.items():
        if clave not in s:
            faltas.append(f"clave desconocida: {clave}")
        elif isinstance(pedido, int):
            if s[clave] != pedido:
                faltas.append(f"{clave}: se esperaba {pedido}, hay {s[clave]}")
        else:
            hay = [x[0] if isinstance(x, tuple) else x for x in s[clave]]
            for nombre in pedido:
                if nombre in hay:
                    hay.remove(nombre)
                else:
                    faltas.append(f"{clave}: falta {nombre}")
    return faltas


# --- linea de comandos ------------------------------------------------------------------
def _pares(args):
    out = {}
    for a in args:
        pos, sep, carta = a.partition(":")
        if not sep or not pos.isdigit() or not carta:
            raise ErrorEscenario(f"se esperaba POS:CARTA y llego {a!r}")
        out[int(pos)] = carta
    return out


def main(argv):
    if len(argv) >= 3 and argv[2] == "--mostrar":
        return mostrar(argv[0], argv[1])
    if len(argv) < 3:
        raise SystemExit(__doc__)
    ruta_rom, base, salida = argv[:3]
    grupos, actual = {"--yo": [], "--rival": [], "--mazo-yo": [], "--mazo-rival": []}, None
    for a in argv[3:]:
        if a in grupos:
            actual = a
        elif actual is None:
            raise SystemExit(f"argumento inesperado: {a}")
        else:
            grupos[actual].append(a)
    armar(ruta_rom, base, salida, yo=_pares(grupos["--yo"]), rival=_pares(grupos["--rival"]),
          mazo_yo=_pares(grupos["--mazo-yo"]), mazo_rival=_pares(grupos["--mazo-rival"]))
    mostrar(ruta_rom, salida)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except ErrorEscenario as err:
        raise SystemExit(f"error: {err}")
