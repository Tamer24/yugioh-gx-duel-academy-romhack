"""Prueba con Unicorn de los dos ganchos del menu de campo (efectos/gancho_lista_campo.s y
efectos/gancho_menu_campo.s): para los monstruos restaurados de su lista devuelven 1 y para
cualquier otra carta siguen en el codigo original.

  FUN_08015C78(id de ranura)            "tiene un efecto de campo de una vez por turno"
  FUN_08079200(bandera, id de ranura)   "el menu del campo ofrece Activate Effect"

Uso: python3 test_ganchos_campo.py rom.gba            (pip install unicorn)
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_LR, UC_ARM_REG_SP

from da_lib import *

J0, L = 0x02022250, 0x2B08
RETORNO = 0x03007F00
# gancho: (direccion pisada, donde sigue el original, argumentos antes del id de ranura)
GANCHOS = {"lista de efectos de campo": (0x08015C78, 0x08015C80, ()),
           "menu del campo": (0x08079200, 0x08079208, (0,))}
EN_LISTA = ("Goddess of Whim", "Lady Panther", "Fairy Guardian")
FUERA = ("Giant Soldier of Stone", "Mechanicalchaser")


def correr(rom, gancho, indice, idc):
    """'lista' si el gancho devuelve 1, 'original' si sigue en el codigo original."""
    entrada, sigue, previos = GANCHOS[gancho]
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    uc.mem_write(J0 + (idc >> 7) * L + (idc & 0x7F) * 0x50 + 0x24, struct.pack("<H", indice))
    fin = []

    def gancho_codigo(u, dir_, tam, _):
        if dir_ == sigue:
            fin.append("original")
            u.emu_stop()

    uc.hook_add(UC_HOOK_CODE, gancho_codigo)
    for reg, valor in zip((UC_ARM_REG_R0, UC_ARM_REG_R1), previos + (idc,)):
        uc.reg_write(reg, valor)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, RETORNO | 1)
    uc.emu_start(entrada | 1, RETORNO, count=5000)
    if fin:
        return fin[0]
    return "lista" if uc.reg_read(UC_ARM_REG_R0) == 1 else f"devuelve {uc.reg_read(UC_ARM_REG_R0)}"


def main():
    rom = Rom(sys.argv[1])
    indice = {rom.nombre(i): i for i in range(1, N_CARTAS + 1)}
    ok = True
    for gancho in GANCHOS:
        for nombre, esperado in [(n, "lista") for n in EN_LISTA] + [(n, "original") for n in FUERA]:
            for idc in (0x05, 0x85):              # una ranura de cada lado
                obtenido = correr(rom, gancho, indice[nombre], idc)
                bien = obtenido == esperado
                ok = ok and bien
                print(f"{'OK ' if bien else 'MAL'} {gancho}: {nombre} (ranura {idc:#04x}) -> {obtenido}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
