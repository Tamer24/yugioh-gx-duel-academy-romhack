"""Prueba con Unicorn de efectos/reasoning.s (fn_04 de Reasoning, ID 5530).

Texto: "Your opponent declares a monster Level. Reveal cards from the top of your Deck until you
reveal a monster that can be Normal Summoned. If its Level is the declared one, send all revealed
cards to the Graveyard. If not, Special Summon it and send the rest to the Graveyard."

Lo esperado sale del texto. Las funciones del motor que muestran, mandan al cementerio o invocan
se reemplazan por ganchos que anotan la llamada; los predicados de "no se puede Invocar de forma
Normal" (FUN_080DD328) y "Spirit" (FUN_080DCE18) son los del ROM.

Uso: python3 test_reasoning.py rom.gba            (pip install unicorn)
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                               UC_ARM_REG_LR, UC_ARM_REG_SP, UC_ARM_REG_PC)

from da_lib import *

J0, L = 0x02022250, 0x2B08
ESTADO, DECLARADO, MAZO = 0x020204C6, 0x020204C7, 0x28A4
AZAR, ASK, REVELAR, A_CEMENTERIO, INVOCAR = 0x080E5740, 0x08009744, 0x0801AB04, 0x08018518, 0x0806C7C4
PROPIA = 38
MAGICA, TRAMPA, NIVEL4, NIVEL3 = "Dian Keto the Cure Master", "Call of the Haunted", "Mechanicalchaser", "Sangan"
FUSION, SPIRIT = "Flame Swordsman", "Yata-Garasu"


def correr(rom, mazo=(), estado=0x7F, declarado=3, azar=0, lado=0, anulada=0):
    """mazo: nombres desde el tope. Devuelve dict con lo que hizo y el estado devuelto."""
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    indices = {rom.nombre(i): i for i in range(1, N_CARTAS + 1)}
    base = J0 + lado * L
    ranuras = []
    for k, nombre in enumerate(mazo):
        s = 40 + k
        uc.mem_write(base + s * 0x50 + 0x24, struct.pack("<H", indices[nombre]))
        ranuras.append((lado << 7) | s)
    uc.mem_write(base + MAZO, bytes(ranuras + [0xFF] * (60 - len(ranuras))))
    uc.mem_write(base + 0x1C, struct.pack("<H", len(ranuras) << 6))
    uc.mem_write(ESTADO, bytes([estado, declarado]))
    p = 0x02010000
    uc.mem_write(p, struct.pack("<H", (PROPIA << 1) | lado) + bytes([anulada, 0] + [0] * 12))
    r = {"revela": [], "cementerio": [], "invoca": [], "aviso": None}
    nombre_de = dict(zip(ranuras, mazo))

    def gancho(u, dir_, tam, _):
        a = [u.reg_read(x) for x in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        ret = 0
        if dir_ == AZAR:
            ret = azar
        elif dir_ == ASK:
            r["aviso"] = bytes(u.mem_read(a[0], 40)).split(b"\0")[0].decode()
        elif dir_ == REVELAR:
            assert a[0] == lado
            r["revela"].append(nombre_de[a[1]])
        elif dir_ == A_CEMENTERIO:
            assert (a[0], a[2]) == (lado, PROPIA)
            r["cementerio"].append(nombre_de[a[1]])
        elif dir_ == INVOCAR:
            assert (a[0], a[2], a[3]) == (lado, 1, 0)
            r["invoca"].append(nombre_de[a[1]])
        else:
            return
        u.reg_write(UC_ARM_REG_R0, ret)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(rom.efectos_base + EFECTOS_FILA * filas[5530] + 4)
    uc.reg_write(UC_ARM_REG_R0, p)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
    uc.emu_start(fn, 0x03007F00, count=200000)
    r["devuelve"] = uc.reg_read(UC_ARM_REG_R0) & 0xFF
    r["declarado"] = uc.mem_read(DECLARADO, 1)[0]
    return r


def main():
    rom = Rom(sys.argv[1])
    ok = True

    def caso(nombre, r, **esperado):
        nonlocal ok
        obtenido = {k: r[k] for k in esperado}
        bien = obtenido == esperado
        print(f"{'OK ' if bien else 'MAL'} {nombre}: {obtenido}")
        ok = ok and bien

    niveles = set()
    for azar in range(8):
        r = correr(rom, estado=0x80, azar=azar)
        niveles.add(r["declarado"])
        caso(f"0x80 con azar {azar}: declara un nivel, lo avisa y sigue en 0x7F", r,
             aviso=f"Your opponent declares Level {r['declarado']}.", devuelve=0x7F, revela=[], cementerio=[], invoca=[])
    caso("0x80: los niveles declarados son de 2 a 4 y el 4 esta entre ellos",
         {"niveles": sorted(niveles)}, niveles=[2, 3, 4])

    tope = [MAGICA, TRAMPA, NIVEL4, MAGICA]
    caso("0x7F, declarado 3, monstruo de nivel 4: lo invoca y el resto al cementerio",
         correr(rom, tope, declarado=3), revela=tope[:3], cementerio=[MAGICA, TRAMPA], invoca=[NIVEL4], devuelve=0x0A)
    caso("0x7F, declarado 4, monstruo de nivel 4: todo al cementerio",
         correr(rom, tope, declarado=4), revela=tope[:3], cementerio=[MAGICA, TRAMPA, NIVEL4], invoca=[], devuelve=0)
    caso("el monstruo esta en el tope: solo se revela esa carta",
         correr(rom, [NIVEL3, MAGICA], declarado=4), revela=[NIVEL3], cementerio=[], invoca=[NIVEL3], devuelve=0x0A)
    caso("un monstruo de Fusion no cuenta: se revela y sigue hasta el siguiente",
         correr(rom, [FUSION, NIVEL4], declarado=2), revela=[FUSION, NIVEL4], cementerio=[FUSION], invoca=[NIVEL4],
         devuelve=0x0A)
    caso("un Spirit se puede Invocar de forma Normal pero no especial: va al cementerio",
         correr(rom, [MAGICA, SPIRIT], declarado=4), revela=[MAGICA, SPIRIT], cementerio=[MAGICA, SPIRIT], invoca=[],
         devuelve=0)
    caso("mazo sin monstruos: no hace nada",
         correr(rom, [MAGICA, TRAMPA], declarado=4), revela=[], cementerio=[], invoca=[], devuelve=0)
    caso("mazo vacio: no hace nada", correr(rom, [], declarado=4), revela=[], cementerio=[], invoca=[], devuelve=0)
    caso("carta anulada: nada", correr(rom, tope, anulada=8), revela=[], cementerio=[], invoca=[], devuelve=0)
    caso("la activa el rival (lado 1): usa su mazo",
         correr(rom, tope, declarado=3, lado=1), revela=tope[:3], cementerio=[MAGICA, TRAMPA], invoca=[NIVEL4],
         devuelve=0x0A)
    caso("otro estado: nada", correr(rom, tope, estado=0x7E), revela=[], cementerio=[], invoca=[], devuelve=0)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
