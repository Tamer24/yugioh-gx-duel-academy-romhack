"""Ejecuta rutinas sueltas del juego con Unicorn para comprobar un ROM modificado.

No reemplaza probar en mGBA: solo corre las tres busquedas de las que depende
una carta restaurada (ID -> indice, indice -> fila de efecto, indice -> nombre).

Uso: python3 emular.py rom.gba indice [indice ...]      (pip install unicorn)
"""
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_LR, UC_ARM_REG_SP

from da_lib import *

FN_FILA_EFECTO = 0x0806162C   # r0 = indice de carta -> fila de la tabla de efectos o -1
FN_INDICE = 0x080DD72C        # r0 = ID de Konami -> indice o 0
FN_NOMBRE = 0x0800DCB4        # r0 = indice -> puntero al nombre
RETORNO = 0x03007F00


def llamar(uc, fn, r0):
    uc.reg_write(UC_ARM_REG_R0, r0)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, RETORNO | 1)
    uc.emu_start(fn | 1, RETORNO, count=200000)
    return uc.reg_read(UC_ARM_REG_R0)


def main():
    rom = Rom(sys.argv[1])
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    for i in map(int, sys.argv[2:]):
        cid = rom.id_de(i)
        ind = llamar(uc, FN_INDICE, cid)
        fila = llamar(uc, FN_FILA_EFECTO, i)
        fila = fila - (1 << 32) if fila & 0x80000000 else fila
        p = llamar(uc, FN_NOMBRE, i)
        nombre = rom.cstr(p - BASE)
        f = rom.fila_efecto(fila) if fila >= 0 else None
        print(f"indice {i}: ID {cid} -> indice {ind} | nombre {nombre!r} | fila {fila}"
              + (f" (ID {f['id']}, fn_04 {f['fn_04']:08X})" if f else " (sin fila)"))


if __name__ == "__main__":
    main()
