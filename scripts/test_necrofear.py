"""Prueba con Unicorn de las piezas de la posesion de Dark Necrofear (ID 5222).

Texto: "When this card is destroyed in battle or by your opponent's card effect, during the End
Phase of that turn it is treated as an Equip Spell Card and equipped to 1 face-up monster on your
opponent's side of the field. As long as it is equipped, you control that monster."

Gancho de la End Phase (efectos/gancho_fin_necrofear.s, 0x08064920): busca un Necrofear en el
cementerio destruido este turno (bandera 5 = en batalla; bandera 6 = por un efecto del rival) y,
si el rival controla algun monstruo boca arriba y el dueno tiene una casilla libre de Magicas y
Trampas, encola su efecto con tipo 4 y momento 5.
La bandera 6 se la pone efectos/gancho_enviada_por_rival.s solo si fue destruida: esa parte se
prueba en test_enviada_por_rival.py.
fn_18 (efectos/necrofear_seleccion.s): solo ese pedido llega a la seleccion original.
fn_04 (efectos/necrofear_posesion.s): solo ese pedido, con un monstruo rival boca arriba elegido y
Necrofear todavia en el cementerio: toma el control (FUN_0801A8A4), pasa a Necrofear a una casilla
libre de Magicas y Trampas boca arriba (FUN_080188AC) y la equipa al monstruo (FUN_0801A600).
Gancho del procesador de acciones (efectos/gancho_necrofear_equipo.s, 0x080171B0): cuando la carta
que se mueve es Necrofear, el arbol que devuelve el monstruo de Snatch Steal la toma por ella.

Lo esperado sale del texto de la carta, no del codigo.

Uso: python3 test_necrofear.py rom.gba                        (pip install unicorn)
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
                               UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_LR,
                               UC_ARM_REG_SP, UC_ARM_REG_PC)

from da_lib import *

J0, L = 0x02022250, 0x2B08
TRASPASO, BOCA_ARRIBA, ENCOLAR, ACCIONES = 0x0801A8A4, 0x08010C10, 0x080314B4, 0x08016AEC
CASILLA_LIBRE, MOVER, EQUIPAR = 0x08011120, 0x080188AC, 0x0801A600
SELECCION_ORIGINAL = 0x08052BE0
GANCHO_EQUIPO, SIGUE_EQUIPO = 0x080171B0, 0x080171B8
ID_SNATCH_STEAL, TABLA_IDS = 4898, 0x087A8624
GANCHO, SIGUE = 0x08064920, 0x08064928
ID_NECROFEAR = 5222
NECRO, OBJETIVO = 12, 0x80 | 26        # ranura mia; ranura del rival
EN_BATALLA, POR_EFECTO, POR_EL_RIVAL = 1 << 5, 1 << 4, 1 << 6
FIN_DE_TURNO, AL_SER_DESTRUIDA = 5, 0xE    # momento del pedido: el del gancho y el que hace el motor


def maquina_virtual(rom):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    return uc


def ranura(idc):
    return J0 + (idc >> 7) * L + (idc & 0x7F) * 0x50


def indice_de(rom, id_konami):
    return next(i for i in range(1, N_CARTAS + 1) if rom.id_de(i) == id_konami)


def poner(uc, idc, indice, controla, pos=0x10, zona=0, banderas=0):
    """Carta en una zona, controlada por el lado 'controla' (bit 19 de +0x30)."""
    a = ranura(idc)
    uc.mem_write(a + 0x24, struct.pack("<H", indice))
    uc.mem_write(a + 0x30, struct.pack("<I", (controla << 19) | (zona << 12)))
    uc.mem_write(a + 0x33, bytes([pos]))
    uc.mem_write(a + 0x60, struct.pack("<I", banderas))


def pedido(idc, momento, tipo=4, anulada=0, elegidos=0, objetivo=0):
    """Los 12 bytes que recibe una funcion de efecto: lado y ranura, tipo, momento, eleccion."""
    cabecera = (idc >> 7) | (idc << 1) | (tipo << 9) | (momento << 13) | (anulada << 16)   # bit 8: lado de la ranura
    return struct.pack("<I", cabecera) + bytes([0, 0, 0, 0, elegidos, objetivo, 0, 0])


def funcion(rom, columna):
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    return rom.u32(EFECTOS + EFECTOS_FILA * filas[ID_NECROFEAR] + columna)


def llamar(uc, fn, p):
    uc.mem_write(0x02010000, p)
    uc.reg_write(UC_ARM_REG_R0, 0x02010000)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
    uc.emu_start(fn, 0x03007F00, count=20000)
    return uc.reg_read(UC_ARM_REG_R0)


# --- gancho de la End Phase -------------------------------------------------------------
def fin_de_turno(rom, banderas, lado=0, zona=0xD, id_konami=ID_NECROFEAR, boca_arriba=1, veces=1, casilla=2):
    """Corre el gancho con una carta de 'lado' en 'zona' y esas banderas.
    Devuelve (efectos encolados, lados por los que se pregunto, banderas que quedan, sigue bien)."""
    uc = maquina_virtual(rom)
    idc = (lado << 7) | NECRO
    poner(uc, idc, indice_de(rom, id_konami), lado, zona=zona, banderas=banderas)
    encolados, preguntados, acciones = [], [], []

    def gancho(u, dir_, tam, _):
        if dir_ == BOCA_ARRIBA:
            preguntados.append(tuple(u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)))
            u.reg_write(UC_ARM_REG_R0, boca_arriba)
        elif dir_ == CASILLA_LIBRE:
            u.reg_write(UC_ARM_REG_R0, casilla & 0xFFFFFFFF)
        elif dir_ == ENCOLAR:
            encolados.append(u.reg_read(UC_ARM_REG_R0))
        elif dir_ == ACCIONES:
            acciones.append(dir_)
        else:
            return
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    guardados = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7)
    bien = True
    for _ in range(veces):
        for k, r in enumerate(guardados):
            uc.reg_write(r, 0x1111 * (k + 4))
        uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
        uc.emu_start(GANCHO | 1, SIGUE, count=200000)
        bien = bien and (uc.reg_read(UC_ARM_REG_PC) == SIGUE and uc.reg_read(UC_ARM_REG_SP) == 0x03007E00
                         and uc.reg_read(UC_ARM_REG_R0) == 0x0201FD00 and uc.reg_read(UC_ARM_REG_R1) == 0xC0
                         and [uc.reg_read(r) for r in guardados] == [0x1111 * (k + 4) for k in range(4)])
    bien = bien and len(acciones) == veces
    quedan = struct.unpack("<I", uc.mem_read(ranura(idc) + 0x60, 4))[0]
    return encolados, [p[0] for p in preguntados], quedan, bien


def encolado(lado):
    """Lo que el gancho le pasa a FUN_080314B4: lado, ranura, tipo de efecto 4 y momento 5."""
    return (lado << 31) | (0x54 << 21) | (lado << 7) | NECRO


# --- fn_18 ------------------------------------------------------------------------------
def seleccion(rom, momento):
    """(llego a la seleccion original, resultado)."""
    uc = maquina_virtual(rom)
    poner(uc, NECRO, indice_de(rom, ID_NECROFEAR), 0, zona=0xD)
    llamadas = []

    def gancho(u, dir_, tam, _):
        if dir_ == SELECCION_ORIGINAL:
            llamadas.append(dir_)
            u.reg_write(UC_ARM_REG_R0, 0x7F)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    r = llamar(uc, funcion(rom, 0x18), pedido(NECRO, momento))
    return bool(llamadas), r


# --- fn_04 ------------------------------------------------------------------------------
def posesion(rom, momento=FIN_DE_TURNO, lado=0, controla=None, pos=0x10, zona=0, elegidos=1, anulada=0,
             zona_necro=0xD, casilla=2, se_puede=1):
    """Necrofear de 'lado' con un monstruo elegido que controla 'controla' (por defecto, el otro lado).
    'casilla' = lo que contesta la busqueda de casilla libre de Magicas (-1: no hay); 'se_puede' = lo
    que contesta el traspaso. Devuelve las llamadas al motor, en orden, y lo que devuelve la funcion."""
    uc = maquina_virtual(rom)
    idc = (lado << 7) | NECRO
    objetivo = ((1 - lado) << 7) | 26
    poner(uc, idc, indice_de(rom, ID_NECROFEAR), lado, zona=zona_necro)
    poner(uc, objetivo, 184, 1 - lado if controla is None else controla, pos, zona)
    llamadas = []

    def gancho(u, dir_, tam, _):
        r = [u.reg_read(x) for x in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
        if dir_ == CASILLA_LIBRE:
            llamadas.append(("casilla", r[0]))
            u.reg_write(UC_ARM_REG_R0, casilla & 0xFFFFFFFF)
        elif dir_ == TRASPASO:
            llamadas.append(("traspaso", r[0], r[1]))
            u.reg_write(UC_ARM_REG_R0, se_puede)
        elif dir_ == MOVER:
            llamadas.append(("mover", r[0], r[1]))
        elif dir_ == EQUIPAR:
            llamadas.append(("equipar", r[0], r[1], r[2]))
        else:
            return
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    r = llamar(uc, funcion(rom, 4), pedido(idc, momento, anulada=anulada, elegidos=elegidos, objetivo=objetivo))
    return llamadas, r


def posesion_esperada(lado=0, casilla=2):
    """Texto: toma el control del elegido y Necrofear queda equipada a el, boca arriba, en una casilla
    libre de Magicas y Trampas de su dueno (destino = lado << 15 | zona 5 << 10 | casilla << 4 | 8)."""
    idc, objetivo = (lado << 7) | NECRO, ((1 - lado) << 7) | 26
    return [("casilla", lado), ("traspaso", objetivo, 0),
            ("mover", idc, (lado << 15) | (5 << 10) | (casilla << 4) | 8), ("equipar", lado, idc, objetivo)]


# --- gancho del procesador de acciones ---------------------------------------------------
def deja_el_campo(rom, id_konami):
    """Corre el gancho con la carta de ese ID. Devuelve (ID que ve el arbol, todo lo demas en su lugar)."""
    uc = maquina_virtual(rom)
    indice = indice_de(rom, id_konami)
    fijos = {UC_ARM_REG_R2: J0, UC_ARM_REG_R4: 0x80, UC_ARM_REG_R6: 0x2A, UC_ARM_REG_R7: 0x7F,
             UC_ARM_REG_R8: ranura(0x2A)}
    for r, v in fijos.items():
        uc.reg_write(r, v)
    uc.reg_write(UC_ARM_REG_R0, indice * 2)
    uc.reg_write(UC_ARM_REG_R1, ranura(0x2A))
    uc.reg_write(UC_ARM_REG_R3, L)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.emu_start(GANCHO_EQUIPO | 1, SIGUE_EQUIPO, count=200)
    bien = (uc.reg_read(UC_ARM_REG_PC) == SIGUE_EQUIPO and uc.reg_read(UC_ARM_REG_SP) == 0x03007E00
            and uc.reg_read(UC_ARM_REG_R0) == 0x1432 and uc.reg_read(UC_ARM_REG_R3) == L
            and uc.reg_read(UC_ARM_REG_R5) == TABLA_IDS and all(uc.reg_read(r) == v for r, v in fijos.items()))
    return uc.reg_read(UC_ARM_REG_R1), bien


def main():
    rom = Rom(sys.argv[1])
    ok = True

    def caso(nombre, obtenido, esperado):
        nonlocal ok
        bien = obtenido == esperado
        print(f"{'OK ' if bien else 'MAL'} {nombre}: {obtenido}")
        ok = ok and bien

    caso("destruida en batalla este turno: se encola una vez y se apagan las banderas",
         fin_de_turno(rom, EN_BATALLA), ([encolado(0)], [1], 0, True))
    caso("destruida por un efecto del rival (Raigeki: sin la bandera 4 del motor): se encola",
         fin_de_turno(rom, POR_EL_RIVAL), ([encolado(0)], [1], 0, True))
    caso("destruida por un efecto del rival, con la bandera 4 del motor: se encola igual",
         fin_de_turno(rom, POR_EFECTO | POR_EL_RIVAL), ([encolado(0)], [1], POR_EFECTO, True))
    caso("destruida por un efecto propio: nada", fin_de_turno(rom, POR_EFECTO), ([], [], POR_EFECTO, True))
    caso("en el cementerio desde un turno anterior (sin banderas): nada", fin_de_turno(rom, 0), ([], [], 0, True))
    caso("destruida en batalla pero ya no esta en el cementerio (retirada): nada",
         fin_de_turno(rom, EN_BATALLA, zona=0xE)[0], [])
    caso("todavia en el campo con la bandera de batalla: nada", fin_de_turno(rom, EN_BATALLA, zona=0)[0], [])
    caso("el rival no controla monstruos boca arriba: no se encola",
         fin_de_turno(rom, EN_BATALLA, boca_arriba=0), ([], [1], 0, True))
    caso("Necrofear del rival: se pregunta por mis monstruos y se encola para su lado",
         fin_de_turno(rom, EN_BATALLA, lado=1), ([encolado(1)], [0], 0, True))
    caso("otra carta destruida en batalla (Slate Warrior): nada",
         fin_de_turno(rom, EN_BATALLA, id_konami=5037), ([], [], EN_BATALLA, True))
    caso("dos pasadas por la End Phase del mismo turno: se encola una sola vez",
         fin_de_turno(rom, EN_BATALLA, veces=2), ([encolado(0)], [1], 0, True))

    caso("seleccion, pedido de la End Phase: llega a la original (pide elegir)",
         seleccion(rom, FIN_DE_TURNO), (True, 0x7F))
    caso("seleccion, pedido del motor al ser destruida: no pide nada",
         seleccion(rom, AL_SER_DESTRUIDA), (False, 1))

    caso("el dueno no tiene casilla libre de Magicas y Trampas: no se encola",
         fin_de_turno(rom, EN_BATALLA, casilla=-1), ([], [1], 0, True))

    caso("posesion: toma el control del elegido y Necrofear queda equipada en mi zona de Magicas",
         posesion(rom), (posesion_esperada(), 0))
    caso("posesion, Necrofear del rival: toma mi monstruo y se equipa en su zona",
         posesion(rom, lado=1, casilla=4), (posesion_esperada(lado=1, casilla=4), 0))
    caso("sin casilla libre de Magicas y Trampas: no toma el control ni mueve nada",
         posesion(rom, casilla=-1), ([("casilla", 0)], 0))
    caso("no se puede tomar el control (sin zona de monstruo libre): Necrofear se queda en el cementerio",
         posesion(rom, se_puede=0), ([("casilla", 0), ("traspaso", OBJETIVO, 0)], 0))
    caso("Necrofear ya no esta en el cementerio (retirada antes de resolver): nada",
         posesion(rom, zona_necro=0xE), ([], 0))
    caso("pedido del motor al ser destruida: nada", posesion(rom, momento=AL_SER_DESTRUIDA), ([], 0))
    caso("anulada: nada", posesion(rom, anulada=8), ([], 0))
    caso("sin eleccion: nada", posesion(rom, elegidos=0), ([], 0))
    caso("el elegido esta boca abajo: nada", posesion(rom, pos=0x20), ([], 0))
    caso("el elegido ya no esta en el campo: nada", posesion(rom, zona=0xD), ([], 0))
    caso("el elegido ya lo controla el dueno de Necrofear: nada", posesion(rom, controla=0), ([], 0))

    caso("Necrofear deja el campo: el arbol del motor la toma por Snatch Steal (devuelve el monstruo)",
         deja_el_campo(rom, ID_NECROFEAR), (ID_SNATCH_STEAL, True))
    caso("Snatch Steal deja el campo: sigue siendo Snatch Steal",
         deja_el_campo(rom, ID_SNATCH_STEAL), (ID_SNATCH_STEAL, True))
    caso("otra carta (Slate Warrior) deja el campo: el arbol ve su propio ID",
         deja_el_campo(rom, 5037), (5037, True))

    print("TODO OK" if ok else "HAY FALLAS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
