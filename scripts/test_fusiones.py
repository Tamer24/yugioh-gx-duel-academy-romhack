"""Prueba con Unicorn de la tabla de fusiones mudada (scripts/ampliar_fusiones.py).

Corre card_type_classifier (0x0804FB3C: ranura -> fila de la receta de fusion, o -1) para cada
carta de Fusion del ROM y comprueba que la fila hallada es la de esa carta y trae los materiales
pedidos; que las recetas originales siguen igual que en el ROM de referencia; y que una carta
que no es fusion da -1.

Uso: python3 scripts/test_fusiones.py ROM_AMPLIADO ROM_ORIGINAL
"""
import struct
import sys

from unicorn import UC_ARCH_ARM, UC_MODE_THUMB, Uc
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_SP

import ampliar_fusiones as F
from da_lib import BASE, Rom

CLASIFICADOR = 0x0804FB3C
J, LADO = 0x02022250, 0x2B08


def maquina(rom):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    return uc


def fila_de(uc, indice):
    uc.mem_write(J + 5 * 0x50 + 0x24, struct.pack("<H", indice))     # ranura 5 del lado 0
    uc.reg_write(UC_ARM_REG_R0, 5)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F01)
    uc.emu_start(CLASIFICADOR | 1, 0x03007F00, count=4000)
    r = uc.reg_read(UC_ARM_REG_R0)
    return r - (1 << 32) if r >= 1 << 31 else r


def main(ruta, ruta_original):
    rom, orig = Rom(ruta), Rom(ruta_original)
    uc, uo = maquina(rom), maquina(orig)
    marca = bytes(rom.d[F.FUSIONES_NUEVA:F.FUSIONES_NUEVA + 16])
    assert marca == F.MARCA, "ese ROM no tiene la tabla de fusiones mudada"
    base = F.FUSIONES_NUEVA + 16
    filas = []
    k = 0
    while True:
        f = struct.unpack_from("<8H", rom.d, base + 16 * k)
        filas.append(f)
        if f[0] == 0:
            break
        k += 1
    print(f"{len(filas) - 1} recetas (mas la fila final)")
    malos = 0
    viejos = {struct.unpack_from("<8H", orig.d, F.TABLA + 16 * j)[0]: struct.unpack_from("<8H", orig.d, F.TABLA + 16 * j)
              for j in range(80)}
    for i in range(1, rom.n + 1):
        cid = rom.id_de(i)
        r = fila_de(uc, i)
        esperado = next((j for j, f in enumerate(filas[:-1]) if f[0] == cid), -1)
        if r != esperado:
            malos += 1
            print(f"MAL: {rom.nombre(i)} ({cid}): fila {r}, esperada {esperado}")
        elif r >= 0 and cid in viejos and filas[r] != viejos[cid]:
            malos += 1
            print(f"MAL: {rom.nombre(i)}: la receta original cambio")
    # las originales tambien en el ROM original: misma fila hallada por el mismo codigo
    for cid, f in viejos.items():
        if cid and orig.indice_de(cid):
            j = fila_de(uo, orig.indice_de(cid))
            assert struct.unpack_from("<8H", orig.d, F.TABLA + 16 * j) == f
    print("TODO BIEN" if not malos else f"{malos} FALLAS")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
