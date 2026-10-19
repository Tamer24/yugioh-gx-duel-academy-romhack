"""Prueba con Unicorn de los ganchos de Wicked-Breaking Flamberge - Baou (efectos/gancho_baou_a.s en
0x080245CC y efectos/gancho_baou_b.s en 0x08024598): antes de llamar a la fn_04 de un eslabon,
marcan anulada (bit 3 de p[2]) la entrada cuya carta fue destruida en batalla por un monstruo con
Baou equipada.

Arma a mano el campo, el registro de la batalla (0x02020C20) y el arreglo de eslabones
(r8 + 24 x indice), ejecuta desde la direccion del gancho hasta la llamada (0x080245D4 o 0x080245B6)
y comprueba la bandera y que los registros que usa el original quedan como los dejaria el original.

Uso: python3 scripts/test_baou.py ROM
"""
import struct
import sys

from unicorn.arm_const import (UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                               UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R8, UC_ARM_REG_SP)

from da_lib import Rom
from motor_uc import Motor, PILA

REG = 0x02020C20
ESLABONES = 0x02020004 - 24 * 0          # r8: medido en el juego con Mystic Tomato
R6 = 0x02020000 - 0x7D4 + 0x100          # cualquier base: r6 + 0x7D4 guarda la fn
FN = 0x08123457
BAOU = 5727
fallas = 0


def ok(nombre, cond, detalle=""):
    global fallas
    print(("  ok   " if cond else "  FALLA"), nombre, detalle)
    fallas += 0 if cond else 1


def correr(rom, rama, baou=True, baou_zona=5, baou_pos=0x10, baou_objetivo=None, bandera5=True,
           tomato_defiende=True, indice=0):
    """Mi Inpachi (0, 2) contra el Tomato del rival (1, 3). Devuelve (anulada, maquina)."""
    m = Motor(rom)
    uc = m.uc
    inpachi = m.carta(0, 2, rom.indice_de(4130) or 5)
    tomato = m.carta(1, 3, rom.indice_de(4110) or 6, banderas=(1 << 5) if bandera5 else 0)
    if baou:
        b = m.carta(0, 7, rom.indice_de(BAOU), zona=baou_zona, pos=baou_pos)
        uc.mem_write(m.ranura(0, 7) + 0x3C, bytes([inpachi if baou_objetivo is None else baou_objetivo]))
    at, de = (inpachi, tomato) if tomato_defiende else (tomato, inpachi)
    uc.mem_write(REG, struct.pack("<I", (at << 13) | (de << 21)))
    entrada = ESLABONES + 24 * indice
    uc.mem_write(entrada, struct.pack("<I", (tomato << 1) | 1) + bytes(20))
    uc.mem_write(R6 + 0x7D4, struct.pack("<I", FN))
    uc.reg_write(UC_ARM_REG_R8, ESLABONES)
    uc.reg_write(UC_ARM_REG_R6, R6)
    uc.reg_write(UC_ARM_REG_SP, PILA)
    if rama == "a":                        # eslabon 0 o 1: llega con r1 = indice, r2 = r6 + 0x7D4
        uc.reg_write(UC_ARM_REG_R1, indice)
        uc.reg_write(UC_ARM_REG_R0, indice * 2)
        uc.reg_write(UC_ARM_REG_R2, R6 + 0x7D4)
        uc.emu_start(0x080245CC | 1, 0x080245D4, count=200000)
        assert uc.reg_read(UC_ARM_REG_PC) == 0x080245D4
        ok_regs = (uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R2)) == (entrada, FN)
    else:                                  # eslabon 2 en adelante: r0 = indice, r5 = 0x7D4
        uc.reg_write(UC_ARM_REG_R0, indice)
        uc.reg_write(UC_ARM_REG_R4, indice << 25)
        uc.reg_write(UC_ARM_REG_R5, 0x7D4)
        uc.emu_start(0x08024598 | 1, 0x080245B6, count=200000)
        assert uc.reg_read(UC_ARM_REG_PC) == 0x080245B6
        ok_regs = (uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R2), uc.reg_read(UC_ARM_REG_R3)) == (entrada, FN, R6 + 0x7D4)
    ok_regs = ok_regs and uc.reg_read(UC_ARM_REG_SP) == PILA
    return bool(uc.mem_read(entrada + 2, 1)[0] & 8), ok_regs


def main(ruta):
    rom = Rom(ruta)
    assert rom.indice_de(BAOU), "Baou no esta en el ROM"
    casos = [
        ("destruido por el equipado con Baou: anulado", {}, True),
        ("el destruido atacaba al equipado: anulado", {"tomato_defiende": False}, True),
        ("sin Baou: nada", {"baou": False}, False),
        ("Baou equipada a otro monstruo: nada", {"baou_objetivo": 9}, False),
        ("Baou boca abajo: nada", {"baou_pos": 0x20}, False),
        ("Baou en el cementerio: nada", {"baou_zona": 0xD}, False),
        ("no fue destruido en batalla este turno (bandera 5): nada", {"bandera5": False}, False),
    ]
    for rama in ("a", "b"):
        print(f"gancho {rama} ({'0x080245CC' if rama == 'a' else '0x08024598'})")
        for nombre, kw, esperado in casos:
            indice = 1 if rama == "a" else 3
            anulada, regs = correr(rom, rama, indice=indice, **kw)
            ok(nombre, anulada == esperado and regs, f"anulada {anulada}, registros {'bien' if regs else 'MAL'}")
    print("RESULTADO:", "FUNCIONA" if not fallas else f"{fallas} FALLAS")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
