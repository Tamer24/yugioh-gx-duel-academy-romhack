"""Prueba con Unicorn de "enviada al cementerio por un efecto del rival" y de las cartas que dependen
de eso: Electric Snake (4469), Minar (4540), Penguin Knight (4205) y Fairy Guardian (5202).

1. efectos/gancho_enviada_por_rival.s (gancho en 0x0801706C). Se ejecuta el tramo original
   0x0801706C..0x08017072 con las variables de pila del procesador de acciones. Lo esperado sale
   de los textos: la bandera 6 y el disparo solo cuando la carta va al cementerio por un efecto
   del rival (no en batalla, no por un efecto o coste propio, no por una regla), Electric Snake y
   Minar solo desde la mano, Penguin Knight solo desde el mazo. A Dark Necrofear (5222) la
   bandera solo se le pone si el efecto del rival la destruyo (la lee su posesion en la End Phase).
2. efectos/penguin_knight.s (fn_04): todo mi cementerio vuelve al mazo y despues se baraja.
3. efectos/fairy_guardian.s (fn_04): en el estado 0x7E la carta elegida va al fondo del mazo.

Uso: python3 test_enviada_por_rival.py rom.gba            (pip install unicorn)
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
                               UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
                               UC_ARM_REG_LR, UC_ARM_REG_SP, UC_ARM_REG_PC)

from da_lib import *

J0, L = 0x02022250, 0x2B08
ESTADO, RESOLVIENDO, ELEGIDA = 0x020204C6, 0x020204A4, 0x02019F24
MOVER, EVENTO3, DISPARAR, EVENTO1 = 0x080188AC, 0x08022034, 0x080314B4, 0x080220D4
LIMPIAR, ENVIAR, PROCESAR = 0x0801848C, 0x08015DC8, 0x08016AEC
CEMENTERIO = 0x2924
SP = 0x03007D00
MIA, CAUSA_RIVAL, CAUSA_MIA = 33, 0x80 | 6, 20


def maquina(rom):
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


def poner(uc, idc, indice, controla, zona):
    a = ranura(idc)
    uc.mem_write(a + 0x24, struct.pack("<H", indice))
    uc.mem_write(a + 0x30, struct.pack("<I", (controla << 19) | (zona << 12)))


def con_ganchos(uc, ganchos):
    """ganchos: {direccion: funcion(registros r0..r3) -> valor de retorno}. Devuelve el manejador."""
    def gancho(u, dir_, tam, _):
        if dir_ in ganchos:
            r = ganchos[dir_](tuple(u.reg_read(x) for x in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)))
            u.reg_write(UC_ARM_REG_R0, r or 0)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
    return uc.hook_add(UC_HOOK_CODE, gancho)


# --- 1. gancho ---------------------------------------------------------------------------
def mover(rom, id_konami=4469, origen=0xF, destino=0xD, causa=CAUSA_RIVAL, banderas=0x41,
          estado=0, resolviendo=0):
    """Una accion del procesador sobre mi carta. Devuelve (banderas puestas, efectos disparados)."""
    uc = maquina(rom)
    poner(uc, MIA, indice_de(rom, id_konami), 0, destino)        # ya movida cuando mira el gancho
    poner(uc, CAUSA_RIVAL, 147, 1, 5)
    poner(uc, CAUSA_MIA, 147, 0, 5)
    uc.mem_write(ESTADO, bytes([estado]))
    uc.mem_write(RESOLVIENDO, struct.pack("<H", resolviendo))
    uc.mem_write(SP + 0x50, struct.pack("<III", banderas, causa, 0))
    uc.mem_write(SP + 0x5C, struct.pack("<I", origen))
    puestas, disparos, movidas = [], [], []
    con_ganchos(uc, {MOVER: lambda r: movidas.append(r[0]),
                     EVENTO3: lambda r: puestas.append(r[:3]),
                     DISPARAR: lambda r: disparos.append((r[0], r[1]))})
    uc.reg_write(UC_ARM_REG_R6, MIA)
    uc.reg_write(UC_ARM_REG_R5, destino)
    uc.reg_write(UC_ARM_REG_R4, 0x1234)
    uc.reg_write(UC_ARM_REG_R7, 0x5678)
    uc.reg_write(UC_ARM_REG_R1, 0x3401)
    uc.reg_write(UC_ARM_REG_SP, SP)
    uc.emu_start(0x0801706C | 1, 0x08017072, count=20000)
    assert movidas == [MIA], "el gancho tiene que hacer el movimiento original"
    assert uc.reg_read(UC_ARM_REG_SP) == SP and uc.reg_read(UC_ARM_REG_R4) == 0x1234 \
        and uc.reg_read(UC_ARM_REG_R7) == 0x5678, "el gancho no conserva la pila o los registros"
    return puestas, disparos


# --- 2. Penguin Knight -------------------------------------------------------------------
def penguin(rom, cementerio, estado=0x80, anulada=0):
    """Devuelve (movimientos al mazo, eventos encolados, estado devuelto)."""
    uc = maquina(rom)
    uc.mem_write(J0 + CEMENTERIO, bytes(cementerio))
    uc.mem_write(J0 + 0x1C, struct.pack("<I", len(cementerio) << 13))
    uc.mem_write(ESTADO, bytes([estado]))
    p = 0x02010000
    uc.mem_write(p, struct.pack("<H", MIA << 1) + bytes([anulada, 0] + [0] * 12))
    movidas, eventos = [], []
    con_ganchos(uc, {MOVER: lambda r: movidas.append((r[0], r[1])), EVENTO1: lambda r: eventos.append(r[0])})
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(rom.efectos_base + EFECTOS_FILA * filas[4205] + 4)
    uc.reg_write(UC_ARM_REG_R0, p)
    uc.reg_write(UC_ARM_REG_SP, SP)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
    uc.emu_start(fn, 0x03007F00, count=50000)
    return movidas, eventos, uc.reg_read(UC_ARM_REG_R0) & 0xFF


# --- 3. Fairy Guardian -------------------------------------------------------------------
def fairy(rom, estado, elegida=41):
    """Devuelve (acciones enviadas, estado devuelto)."""
    uc = maquina(rom)
    uc.mem_write(ESTADO, bytes([estado]))
    uc.mem_write(ELEGIDA, struct.pack("<I", elegida << 11))
    p = 0x02010000
    uc.mem_write(p, struct.pack("<H", MIA << 1) + bytes(14))
    enviadas, orden = [], []
    con_ganchos(uc, {LIMPIAR: lambda r: orden.append("limpiar"),
                     ENVIAR: lambda r: (enviadas.append(r[:3]), orden.append("enviar"))[0],
                     PROCESAR: lambda r: orden.append("procesar"),
                     0x0805AEB0: lambda r: 1, 0x08009744: lambda r: 0, 0x0806BC00: lambda r: 0})
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(rom.efectos_base + EFECTOS_FILA * filas[5202] + 4)
    uc.reg_write(UC_ARM_REG_R0, p)
    uc.reg_write(UC_ARM_REG_SP, SP)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
    uc.emu_start(fn, 0x03007F00, count=50000)
    return enviadas, orden, uc.reg_read(UC_ARM_REG_R0) & 0xFF


def main():
    rom = Rom(sys.argv[1])
    ok = True

    def caso(nombre, obtenido, esperado):
        nonlocal ok
        bien = obtenido == esperado
        print(f"{'OK ' if bien else 'MAL'} {nombre}: {obtenido}")
        ok = ok and bien

    bandera = [(0x3B, MIA, 6)]
    # cabecera y argumento del disparo, como los arma el motor para Night Assailant (0x080194AC)
    disparo = [(0x1C800000 | MIA, ((0xD << 8) | MIA) * 0x10001)]
    caso("Electric Snake, de la mano, por Card Destruction del rival", mover(rom), (bandera, disparo))
    caso("Minar, de la mano, por un efecto del rival", mover(rom, 4540), (bandera, disparo))
    caso("Penguin Knight, del mazo, por un efecto del rival", mover(rom, 4205, origen=0xC), (bandera, disparo))
    caso("Electric Snake desde el campo: bandera, sin disparo", mover(rom, origen=0), (bandera, []))
    caso("Penguin Knight desde la mano: bandera, sin disparo", mover(rom, 4205, origen=0xF), (bandera, []))
    caso("otra carta (Dian Keto) por un efecto del rival: solo la bandera", mover(rom, 4348, origen=5), (bandera, []))
    caso("descartada por un efecto propio: nada", mover(rom, causa=CAUSA_MIA), ([], []))
    caso("destruida en batalla: nada", mover(rom, origen=0, banderas=0x841), ([], []))
    caso("va a la mano, no al cementerio: nada", mover(rom, origen=0, destino=0xF), ([], []))
    caso("sin causante y sin efecto resolviendose (regla o coste): nada", mover(rom, causa=0xFF), ([], []))
    caso("sin causante, resolviendose un efecto del rival (Delinquent Duo)",
         mover(rom, causa=0xFF, estado=0x7F, resolviendo=0x0D), (bandera, disparo))
    caso("sin causante, resolviendose un efecto mio (Graceful Charity): nada",
         mover(rom, causa=0xFF, estado=0x7F, resolviendo=0x0C), ([], []))

    # banderas de la accion medidas en duelo: 0x9041 Raigeki del rival, 0x9001 Card Destruction del
    # rival, 0x1041 Dark Hole propio, 0x8840 destruida en batalla por un monstruo del rival
    caso("Dark Necrofear destruida en el campo por Raigeki del rival: bandera, sin disparo",
         mover(rom, 5222, origen=0, banderas=0x9041), (bandera, []))
    caso("Dark Necrofear equipada (zona de Magicas) destruida por una Magica del rival: nada, no se repite",
         mover(rom, 5222, origen=5, banderas=0x9041), ([], []))
    caso("Dark Necrofear descartada de la mano por Card Destruction del rival: nada",
         mover(rom, 5222, origen=0xF, banderas=0x9001), ([], []))
    caso("Dark Necrofear destruida por un Dark Hole propio: nada",
         mover(rom, 5222, origen=0, causa=CAUSA_MIA, banderas=0x1041), ([], []))
    caso("Dark Necrofear destruida en batalla: nada (esa bandera, la 5, la pone el motor)",
         mover(rom, 5222, origen=0, banderas=0x8840), ([], []))
    caso("otra carta descartada por Card Destruction del rival, con las banderas medidas: bandera",
         mover(rom, 4348, origen=0xF, banderas=0x9001), (bandera, []))

    al_mazo = 0x3008
    caso("Penguin Knight 0x80: las 3 cartas de mi cementerio al mazo, sigue en 0x7F",
         penguin(rom, [33, 12, 40]), ([(33, al_mazo), (12, al_mazo), (40, al_mazo)], [], 0x7F))
    caso("Penguin Knight 0x80 con una carta del rival en mi cementerio: va al mazo del rival",
         penguin(rom, [33, 0x80 | 9]), ([(33, al_mazo), (0x80 | 9, 0x8000 | al_mazo)], [], 0x7F))
    caso("Penguin Knight 0x7F: baraja (evento 0x24) y termina", penguin(rom, [], estado=0x7F), ([], [0x24], 0))
    caso("Penguin Knight anulada: nada", penguin(rom, [33, 12], anulada=8), ([], [], 0))

    caso("Fairy Guardian 0x7E: la elegida va al fondo del mazo y cierra en 0x78",
         fairy(rom, 0x7E), ([(41, 0x20, MIA)], ["limpiar", "enviar", "procesar"], 0x78))
    caso("Fairy Guardian 0x7E sin eleccion: no envia nada", fairy(rom, 0x7E, elegida=0xFF), ([], ["limpiar"], 0x78))
    caso("Fairy Guardian 0x80: la original (candidatas y aviso), sigue en 0x7F", fairy(rom, 0x80), ([], [], 0x7F))
    caso("Fairy Guardian 0x7F: la original (lista), sigue en 0x7E", fairy(rom, 0x7F), ([], [], 0x7E))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
