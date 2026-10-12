"""Prueba de logica del baul ampliado (scripts/ampliar.py), con Unicorn y sin emulador.

Llama a las rutinas del juego que tocan el baul con cartas de los dos lados del limite y mira que
bytes de la memoria cambian: una carta hasta la 1200 tiene que caer en el baul de siempre, una
posterior en su bloque aparte, y ninguna en la fecha, los DP ni los mazos (0x02003840 en adelante).

Uso: python3 scripts/test_ampliado.py "ROM (Ampliado).gba"
"""
import struct
import sys

import random

from unicorn import UC_ARCH_ARM, UC_HOOK_CODE, UC_MODE_THUMB, Uc
from unicorn.arm_const import (UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                               UC_ARM_REG_PC, UC_ARM_REG_SP)

import ampliar
from da_lib import BASE, N_CARTAS, Rom

SUMAR, FALTA, CONTAR = 0x080E58B8, 0x080B7064, 0x080E57E0      # (indice, cuantas), (indice) -> 1 si no la tengo, (0)
EWRAM, IWRAM = 0x02000000, 0x03000000
fallos = 0


def ok(bien, texto):
    global fallos
    fallos += not bien
    print(("OK    " if bien else "FALLA ") + texto)


def maquina(rom):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(EWRAM, 0x40000)
    uc.mem_map(IWRAM, 0x8000)
    return uc


def llamar(uc, fn, *args):
    for k, v in enumerate(args):
        uc.reg_write(UC_ARM_REG_R0 + k, v)
    uc.reg_write(UC_ARM_REG_SP, IWRAM + 0x7E00)
    uc.reg_write(UC_ARM_REG_LR, (IWRAM + 0x7F00) | 1)
    uc.emu_start(fn | 1, IWRAM + 0x7F00, count=2000000)
    return uc.reg_read(UC_ARM_REG_R0)


def entrada(i):
    """Donde tiene que estar la carta 'i' (el inicio de sus 12 bytes)."""
    return ampliar.BAUL + 12 * (i - 1) if i <= N_CARTAS else ampliar.EXT + 12 * (i - N_CARTAS - 1)


GUARDAR, CARGAR_VENTANA, CARGAR_FIN = 0x080E6F38, 0x080E1BD0, 0x080E1BD8
ESCRIBIR_SRAM, LEER_SRAM = 0x080F2398, 0x080F2260
SIN_EFECTO_FNS = (0x080E6EA8, 0x080E6F18)          # las otras dos piezas del guardado: no importan aca


def guardado(uc, rom):
    """Guardar y cargar del bloque del baul con la SRAM simulada: lo que escribe el guardado
    (FUN_080E6F38) y lo que lee la ventana de carga (FUN_080E1B9C) en el ROM ampliado."""
    sram = bytearray(0x8000)

    def gancho(uc_, direccion, tamano, datos):
        if direccion in SIN_EFECTO_FNS:
            uc_.reg_write(UC_ARM_REG_R0, 0)
        elif direccion in (ESCRIBIR_SRAM, LEER_SRAM):
            r0, r1, r2 = (uc_.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
            if r2 and r2 <= 0x8000:
                if direccion == ESCRIBIR_SRAM:       # (RAM, SRAM, n)
                    sram[r1 - 0x0E000000:r1 - 0x0E000000 + r2] = uc_.mem_read(r0, r2)
                else:                                # (SRAM, RAM, n)
                    uc_.mem_write(r1, bytes(sram[r0 - 0x0E000000:r0 - 0x0E000000 + r2]))
        else:
            return
        uc_.reg_write(UC_ARM_REG_R0, 0)
        uc_.reg_write(UC_ARM_REG_R3, 0)
        uc_.reg_write(UC_ARM_REG_PC, uc_.reg_read(UC_ARM_REG_LR))                    # volver ya
    uc.hook_add(UC_HOOK_CODE, gancho, begin=BASE, end=BASE + 0x2000000)
    azar = random.Random(7)
    bloque = bytearray(ampliar.BLOQUE_BYTES)
    struct.pack_into("<I", bloque, 0, ampliar.MARCA_BAUL)
    for k in range(ampliar.EXTRA):
        o = 4 + 12 * k
        struct.pack_into("<HHHHI", bloque, o, azar.randrange(1 << 16) if k < 3 else 0, 0,
                         azar.randrange(1 << 16), 0, azar.randrange(1 << 32))
    # guardar
    uc.mem_write(ampliar.BLOQUE, bytes(bloque))
    uc.reg_write(UC_ARM_REG_SP, IWRAM + 0x7E00)
    uc.reg_write(UC_ARM_REG_LR, (IWRAM + 0x7F00) | 1)
    uc.emu_start(GUARDAR | 1, IWRAM + 0x7F00, count=2000000)
    ok(bytes(sram[0x6200:0x6204]) == struct.pack("<I", ampliar.MARCA_BAUL), "el guardado deja la marca del bloque en la SRAM 0x6200")
    ok(0x6200 + ampliar.COMPACTO_BYTES <= 0x8000, f"el bloque compacto ({ampliar.COMPACTO_BYTES} bytes) entra en los 32 KB")
    # cargar: con la memoria sucia, el bloque tiene que volver igual
    uc.mem_write(ampliar.BLOQUE, bytes(random.Random(1).randrange(256) for _ in range(ampliar.BLOQUE_BYTES)))
    for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2):
        uc.reg_write(r, 0)
    uc.reg_write(UC_ARM_REG_SP, IWRAM + 0x7E00)
    uc.emu_start(CARGAR_VENTANA | 1, CARGAR_FIN, count=2000000)
    vuelto = bytes(uc.mem_read(ampliar.BLOQUE, ampliar.BLOQUE_BYTES))
    ok(vuelto[:-4] == bytes(bloque)[:-4], "guardar y cargar con la memoria sucia: el bloque vuelve igual")
    # una SRAM sin la marca (partida de otro ROM): el bloque queda en cero
    sram[0x6200:0x6204] = b"\0\0\0\0"
    uc.mem_write(ampliar.BLOQUE, bytes(random.Random(2).randrange(256) for _ in range(ampliar.BLOQUE_BYTES)))
    uc.reg_write(UC_ARM_REG_SP, IWRAM + 0x7E00)
    uc.emu_start(CARGAR_VENTANA | 1, CARGAR_FIN, count=2000000)
    vuelto = bytes(uc.mem_read(ampliar.BLOQUE, ampliar.BLOQUE_BYTES))
    ok(not any(vuelto[4:]), "una SRAM sin la marca: el bloque carga en cero")


def main(ruta):
    rom = Rom(ruta)
    assert rom.ampliado, "ese ROM no esta ampliado"
    uc = maquina(rom)
    print(f"{rom.n} cartas; baul aparte en {ampliar.EXT:08X}")
    ok(all(llamar(uc, FALTA, i) == 1 for i in (1, N_CARTAS, N_CARTAS + 1, rom.n)), "con el baul vacio no tengo ninguna")
    for i in (1, 600, N_CARTAS, N_CARTAS + 1, rom.n):
        antes = bytes(uc.mem_read(EWRAM, 0x40000))
        llamar(uc, SUMAR, i, 2)
        ahora = bytes(uc.mem_read(EWRAM, 0x40000))
        cambios = [EWRAM + k for k in range(0x40000) if antes[k] != ahora[k]]
        e = entrada(i)
        copias = (struct.unpack_from("<H", ahora, e + 4 - EWRAM)[0] >> 3) & 0xFF
        ok(bool(cambios) and all(e <= c < e + 12 for c in cambios) and copias == 2,
           f"sumar 2 copias de la carta {i} ({rom.nombre(i)}): cambia {[hex(c) for c in cambios]}, copias {copias}")
        ok(llamar(uc, FALTA, i) == 0, f"el juego ve que tengo la carta {i}")
    cola = bytes(uc.mem_read(ampliar.FIN_BAUL, 0x2950))
    ok(not any(cola), "nada escrito entre 0x02003840 y el final del bloque guardado (fecha, DP, mazos)")
    ok(llamar(uc, CONTAR, 0) == 5, "la cuenta de cartas distintas del baul ve las 5")
    guardado(maquina(rom), rom)
    print("TODO BIEN" if not fallos else f"{fallos} FALLAS")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
