"""Corredor de pruebas automaticas para Trampas que responden a un ataque (sin ventana).

Por cada carta: parte de estados/duelo-inicio.ss1, la pone en la mano (en la posicion de una
Magica, con tipo Trampa), la coloca boca abajo, termina el turno y deja que el rival ataque.
Cuando el motor pide respuesta al ataque declarado (tipo 0x10) contesta Yes, elige la trampa
y la activa. Compara el duelo antes y despues y clasifica:

  NO SE OFRECIO   el rival no llego a atacar (o el motor nunca pidio respuesta)
  NO HACE NADA    se activo pero no cambio nada salvo la propia carta
  CAMBIA          cambio algo mas: LP, campo, cementerio, posicion de un monstruo...

Protocolo de botones medido en NOTAS-REVERSE.md ("Trampas: la ventana de respuesta").

Uso: python3 probar_trampas.py rom.gba [NOMBRE ...]
"""
import os
import struct
import sys
import tempfile

import estado
from da_lib import Rom
from duelo_auto import Duelo, J0, J1

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("ESTADO_BASE") or os.path.join(AQUI, "..", "estados", "duelo-inicio.ss1")
POS = 5                       # posicion de la mano que ocupa una Magica
TIPO_TRAMPA = 0x15

# nombre -> (tipo de evento que la dispara, mano del jugador antes: monstruos a invocar)
CARTAS = {
    "Mirror Force": (0x10, []),
    "Kunai with Chain": (0x10, []),
    "Sakuretsu Armor": (0x10, []),
    "Negate Attack": (0x10, []),
    # el rival activa una Magica (tipo 0x03): Dian Keto la juega en su 3.er turno
    "Magic Drain": (0x03, []),
    "Riryoku Field": (0x03, []),
}
# Trampas que se activan en mi propio turno: ver EN_MI_TURNO


def estado_con(rom, nombre):
    idx = next(i for i in range(1, 1201) if rom.nombre(i) == nombre)
    e = estado.abrir(BASE)
    estado.comprobar(e)
    a = estado.ranura_mano(e, 0, POS)
    struct.pack_into("<H", e, a + 0x24, idx)
    e[a + 0x30] = (e[a + 0x30] & 0xE0) | TIPO_TRAMPA
    struct.pack_into("<H", e, estado.WRAM + 0x19F0C, idx)
    f = tempfile.NamedTemporaryFile(suffix=".st", delete=False)
    f.write(e)
    f.close()
    return f.name


def instantanea(d):
    z = d.zona
    pos = {s: d.g.r8(J1 + s * 0x50 + 0x33) for s, n in z(1, "0")}
    return {
        "LP": d.lp(),
        "campo": sorted(n for s, n in z(0, "05a")),
        "campo_rival": sorted(n for s, n in z(1, "05a")),
        "cementerio": sorted(n for s, n in z(0, "d")),
        "cementerio_rival": sorted(n for s, n in z(1, "d")),
        "posicion_rival": pos,
        "mano_rival": len(d.mano(1)),
    }


def correr(ruta_rom, nombre, tipo=0x10, fotos=None):
    rom = Rom(ruta_rom)
    d = Duelo(ruta_rom, estado=estado_con(rom, nombre))
    d.g.correr(30)
    d.ir_mano(nombre)
    d.tecla("A", 60)
    d.tecla("UP", 25)
    d.tecla("A", 80)                                   # Set
    ranura = next((s for s, n in d.zona(0, "5") if n == nombre), None)
    if ranura is None:
        return None, None, "NO SE COLOCO"
    llego = False
    for ciclo in range(6):                 # la IA recien juega Magicas y ataca en su 3.er turno
        d.fin_turno(primero=(ciclo == 0))
        if d.esperar_evento(tipo, maximo=2500):
            llego = True
            break
        if not pasar_a_mi_turno(d):
            break
    if not llego:
        return None, instantanea(d), "NO SE OFRECIO"
    antes = instantanea(d)
    d.responder_con_trampa(ranura)
    d.g.correr(400)
    if fotos:
        d.foto(os.path.join(fotos, f"{nombre}_final.png"))
    despues = instantanea(d)
    propio = {k: v for k, v in despues.items() if k not in ("campo", "cementerio")}
    base = {k: v for k, v in antes.items() if k not in ("campo", "cementerio")}
    ofrecida = nombre not in despues["campo"]
    if propio != base or ofrecida and nombre in despues["cementerio"] and (
            despues["posicion_rival"] != antes["posicion_rival"]):
        veredicto = "CAMBIA"
    elif nombre in despues["cementerio"]:
        veredicto = "NO HACE NADA"
    else:
        veredicto = "NO SE ACTIVO"
    return antes, despues, veredicto


def pasar_a_mi_turno(d, maximo=40):
    """Pulsa A (dialogos del rival) hasta que el cursor vuelve a la mano."""
    for _ in range(maximo):
        try:
            d.mover(y=0)
            if d.cursor()[1] == 0:
                return True
        except Exception:
            pass
        d.tecla("A", 50)
    return False


ULTIMO = None      # el ultimo Duelo de correr_turno_propio (para depurar a mano)


def correr_turno_propio(ruta_rom, nombre, preparacion=("Blazing Inpachi",), condicion=None,
                        teclas_extra="A A A A A A", fotos=None, un_monstruo_por_turno=()):
    """Trampa que se activa en mi turno: la coloca, pasa turnos hasta que se cumpla 'condicion'
    (funcion de d), abre su menu en el campo, la activa y pulsa 'teclas_extra' (seleccion)."""
    rom = Rom(ruta_rom)
    global ULTIMO
    d = ULTIMO = Duelo(ruta_rom, estado=estado_con(rom, nombre))
    d.g.correr(30)
    for m in preparacion:
        d.ir_mano(m)
        d.menu(0)
        d.g.correr(90)
        d.tecla("DOWN", 20)
        d.tecla("A", 60)
    d.ir_mano(nombre)
    d.tecla("A", 60)
    d.tecla("UP", 25)
    d.tecla("A", 80)
    ranura = next((s for s, n in d.zona(0, "5") if n == nombre), None)
    if ranura is None:
        return None, None, "NO SE COLOCO"
    ok = False
    pendientes = list(un_monstruo_por_turno)
    for ciclo in range(8):
        d.fin_turno(primero=(ciclo == 0))
        if not pasar_a_mi_turno(d):
            break
        if pendientes:                       # una invocacion por turno
            m = pendientes.pop(0)
            d.ir_mano(m)
            d.menu(0)
            d.g.correr(90)
            d.tecla("DOWN", 20)
            d.tecla("A", 60)
        if condicion is None or condicion(d):
            ok = True
            break
    if not ok:
        return None, instantanea(d), "NO SE DIO LA CONDICION"
    antes = instantanea(d)
    # cursor sobre la carta en la fila de magias/trampas
    # fila de magias/trampas: el cursor recorre x = 1..7; las 5 zonas estan en x = 2..6
    z = d.zona_magia(ranura)
    d.mover(y=1)
    d.mover(x=2 + (z or 0))
    d.g.correr(20)
    d.tecla("A", 60)
    d.foto(os.path.join(fotos or ".", f"{nombre}_menu.png"), escala=1) if fotos else None
    d.tecla("UP", 25)
    d.tecla("A", 80)
    d.g.correr(240)                         # la animacion de activacion antes del primer aviso
    for t in teclas_extra.split():
        d.tecla(t, 80)                      # las transiciones de seleccion piden margen
    d.g.correr(300)
    despues = instantanea(d)
    if nombre in despues["cementerio"] and (
            {k: v for k, v in despues.items() if k not in ("campo", "cementerio")} !=
            {k: v for k, v in antes.items() if k not in ("campo", "cementerio")}):
        veredicto = "CAMBIA"
    elif nombre in despues["cementerio"]:
        veredicto = "NO HACE NADA"
    else:
        veredicto = "NO SE ACTIVO"
    return antes, despues, veredicto


def con_monstruo_boca_abajo(d):
    return any(d.g.r8(J1 + s * 0x50 + 0x33) == 0x20 for s, n in d.zona(1, "0"))


def dos_mios_y_uno_rival(d):
    return len(d.zona(0, "0")) >= 2 and len(d.zona(1, "0")) >= 1


# nombre -> parametros de correr_turno_propio
EN_MI_TURNO = {
    "Acid Trap Hole": dict(condicion=con_monstruo_boca_abajo),
    # avisos "Select your 1st monster." / 2nd / "Select 1 opponent's monster": A cierra, A elige,
    # RIGHT va al otro monstruo propio y UP sube a la fila del rival
    "Two-Pronged Attack": dict(condicion=dos_mios_y_uno_rival, un_monstruo_por_turno=("Needle Worm",),
                               teclas_extra="A A A RIGHT A A UP A A A A"),
}


def main():
    args = sys.argv[1:]
    ruta_rom, nombres = args[0], args[1:] or list(CARTAS)
    for nombre in nombres:
        tipo, _ = CARTAS.get(nombre, (0x10, []))
        print(f"=== {nombre}")
        if nombre in EN_MI_TURNO:
            antes, despues, veredicto = correr_turno_propio(ruta_rom, nombre, **EN_MI_TURNO[nombre])
        else:
            antes, despues, veredicto = correr(ruta_rom, nombre, tipo)
        print("  antes  :", antes)
        print("  despues:", despues)
        print("  VEREDICTO:", veredicto, flush=True)


if __name__ == "__main__":
    main()
