"""Prueba con Unicorn de la rama de la IA de Chosen One (efectos/chosen_one.s).

La IA (lado 1) activa la carta en el estado 0x80: debe elegir sola el primer monstruo y las
dos primeras Magicas/Trampas de su mano (sin contar la propia carta), dejarlas en p[9..11] y
devolver 0x7A con el sorteo preparado (contador 0, sin carta anterior). Con una mano que no
alcanza no hace nada (devuelve 0).

Uso: python3 test_chosen.py rom.gba            (pip install unicorn)
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_LR, UC_ARM_REG_SP

from da_lib import *

J0, L = 0x02022250, 0x2B08
MONSTRUO, MAGICA = 0x0A, 0x16


def correr(rom, mano_ia, propia):
    """mano_ia: [(ranura, tipo)] en el orden de la lista de mano; propia: ranura de la carta."""
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    b = J0 + L
    n = len(mano_ia)
    uc.mem_write(b + 0x1B, bytes([(n & 1) << 7, n >> 1]))
    for k, (slot, tipo) in enumerate(mano_ia):
        uc.mem_write(b + 0x2824 + k, bytes([slot | 0x80]))
        uc.mem_write(J0 + L + slot * 0x50 + 0x30, bytes([tipo, 0, 0, 0]))
    uc.mem_write(0x020204C6, bytes([0x80, 5, 0]))      # estado; contador y "anterior" con restos
    carta = 0x02010000
    uc.mem_write(carta, bytes([((propia << 1) | 1) & 0xFF, 1, 0, 0] + [0] * 12))   # bit 8 = dueno del lado 1
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(rom.efectos_base + EFECTOS_FILA * filas[5101] + 4)
    uc.reg_write(UC_ARM_REG_R0, carta)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
    uc.emu_start(fn, 0x03007F00, count=50000)
    return uc.reg_read(UC_ARM_REG_R0), bytes(uc.mem_read(carta + 8, 4)), bytes(uc.mem_read(0x020204C7, 2))


def main():
    rom = Rom(sys.argv[1])
    casos = [
        ("mano completa", [(7, MAGICA), (3, MONSTRUO), (4, MAGICA), (5, MAGICA), (6, MONSTRUO)], 7,
         (0x7A, None)),
        ("sin monstruo", [(7, MAGICA), (4, MAGICA), (5, MAGICA), (6, MAGICA)], 7, (0, None)),
        ("una sola Magica", [(7, MAGICA), (3, MONSTRUO), (4, MAGICA)], 7, (0, None)),
    ]
    ok = True
    for nombre, mano, propia, (esp_ret, _) in casos:
        ret, p8, sorteo = correr(rom, mano, propia)
        bien = ret == esp_ret
        if esp_ret == 0x7A:
            # posiciones en la mano [7, 3, 4, 5, 6]: monstruo 3 -> 1, Magicas 4 y 5 -> 2 y 3
            bien = bien and p8[1:4] == bytes([1, 2, 3]) and p8[0] & 0xF == 3
            # sorteo: contador 0 y sin "anterior" (0xFF); con anterior = 0 el monstruo no salia nunca
            bien = bien and sorteo == bytes([0, 0xFF])
        print(f"{'OK ' if bien else 'MAL'} {nombre}: devuelve {ret:#x}, p[8..11] = {p8.hex()}, "
              f"sorteo (contador, anterior) = {sorteo.hex()}")
        ok = ok and bien
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
