"""Llama a una funcion suelta del motor con Unicorn sobre un volcado de RAM de un duelo real.

Uso: python3 llamar_motor.py rom.gba prefijo DIRECCION r0 [r1]
  prefijo  el de volcar_ram.py (prefijo.ewram / prefijo.iwram)
Imprime el valor devuelto en r0. Sirve para ver que contesta una funcion del motor para una
ranura dada (por ejemplo 0x08079200(0, 32) con Goddess y con Sand Gambler) sin teclear.
Las funciones que tocan hardware (dibujo, sonido) no estan emuladas: usar solo con logica.
"""
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP, UC_ARM_REG_LR

from da_lib import BASE, Rom


def llamar(rom, prefijo, direccion, r0=0, r1=0, cuenta=200000):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_write(0x02000000, open(prefijo + ".ewram", "rb").read())
    uc.mem_map(0x03000000, 0x8000)
    uc.mem_write(0x03000000, open(prefijo + ".iwram", "rb").read())
    uc.mem_map(0x04000000, 0x1000)
    uc.reg_write(UC_ARM_REG_R0, r0)
    uc.reg_write(UC_ARM_REG_R1, r1)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F01)
    uc.emu_start(direccion | 1, 0x03007F00, count=cuenta)
    return uc.reg_read(UC_ARM_REG_R0)


if __name__ == "__main__":
    rom = Rom(sys.argv[1])
    args = [int(x, 0) for x in sys.argv[3:]]
    print(hex(llamar(rom, sys.argv[2], *args)))
