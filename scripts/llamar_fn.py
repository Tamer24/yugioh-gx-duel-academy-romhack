"""Ejecuta con Unicorn una funcion pura del ROM (sin RAM del duelo) para cada carta.

Uso: python3 llamar_fn.py rom.gba DIRECCION        (direccion GBA en hexadecimal)
Llama a la funcion con r0 = indice de carta (1..1200) e imprime las cartas para las que
devuelve algo distinto de 0. Sirve para listar que cartas reconoce un predicado por ID.
"""
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_LR, UC_ARM_REG_SP

from da_lib import BASE, N_CARTAS, Rom


def llamar(uc, fn, *args):
    for k, v in enumerate(args):
        uc.reg_write(UC_ARM_REG_R0 + k, v)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
    uc.emu_start(fn | 1, 0x03007F00, count=100000)
    return uc.reg_read(UC_ARM_REG_R0)


def maquina(rom):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    return uc


def main():
    rom = Rom(sys.argv[1])
    fn = int(sys.argv[2], 16)
    uc = maquina(rom)
    for i in range(1, N_CARTAS + 1):
        r = llamar(uc, fn, i)
        if r:
            print(f"{i:5} {rom.id_konami(i) if hasattr(rom, 'id_konami') else ''} {rom.nombre(i)} -> {r}")


if __name__ == "__main__":
    main()
