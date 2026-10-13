"""Prueba con Unicorn del gancho de ATK por cuenta (efectos/gancho_atk_cuenta.s, FUN_08012460).

Compara el calculador de ATK/DEF del ROM de antes (sin el gancho) y el de ahora, con muchas
cartas en una ranura y las zonas del campo al azar: tiene que dar lo mismo para toda carta
salvo Neo-Spacian Flare Scarab, que suma 400 por cada Magica o Trampa del rival.

Uso: python3 scripts/test_atk_cuenta.py ROM_ANTES ROM_AHORA datos/volcado_goddess
"""
import random
import struct
import sys

from unicorn import UC_ARCH_ARM, UC_MODE_THUMB, Uc
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_SP

from da_lib import BASE, Rom

J, LADO = 0x02022250, 0x2B08
CALCULADOR, SALIDA = 0x08012460, 0x0203F000
FLARE = 6773


def maquina(rom, prefijo):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_write(0x02000000, open(prefijo + ".ewram", "rb").read())
    uc.mem_map(0x03000000, 0x8000)
    uc.mem_write(0x03000000, open(prefijo + ".iwram", "rb").read())
    uc.mem_map(0x04000000, 0x1000)
    return uc


def calcular(uc, ranura, mascara=3):
    uc.mem_write(SALIDA, bytes(32))
    uc.reg_write(UC_ARM_REG_R0, ranura)
    uc.reg_write(UC_ARM_REG_R1, SALIDA)
    uc.reg_write(UC_ARM_REG_R2, mascara)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F01)
    uc.emu_start(CALCULADOR | 1, 0x03007F00, count=400000)
    return bytes(uc.mem_read(SALIDA, 16))


def main(antes, ahora, prefijo):
    r0, r1 = Rom(antes), Rom(ahora)
    u0, u1 = maquina(r0, prefijo), maquina(r1, prefijo)
    azar = random.Random(5)
    flare = r1.indice_de(FLARE)
    assert flare and r0.indice_de(FLARE) == flare
    fallas = distintos = 0
    for k in range(600):
        # escenario al azar, igual en las dos maquinas
        indice = flare if k % 5 == 0 else azar.randrange(1, r1.n + 1)
        lado, ranura = azar.randrange(2), azar.randrange(0, 20)
        id_ranura = lado << 7 | ranura
        zonas = bytes(azar.choice([0xFF, 0xFF, azar.randrange(0, 40)]) for _ in range(22))
        posiciones = {}
        for u in (u0, u1):
            u.mem_write(J + 0x5610, zonas)
            a = J + lado * LADO + ranura * 0x50
            u.mem_write(a + 0x24, struct.pack("<H", indice))
            u.mem_write(a + 0x30, struct.pack("<I", 0x00000000))   # zona 0 de monstruos
            u.mem_write(a + 0x33, bytes([0x10]))                   # boca arriba, en ataque
            u.mem_write(a + 0x3E, bytes([0]))                      # sin modificadores
        s0, s1 = calcular(u0, id_ranura), calcular(u1, id_ranura)
        esperado_flare = 400 * sum(1 for z in zonas[(1 - lado) * 11 + 5:(1 - lado) * 11 + 11] if z != 0xFF)
        if indice == flare:
            atk0, atk1 = struct.unpack_from("<I", s0, 4)[0], struct.unpack_from("<I", s1, 4)[0]
            if atk1 != atk0 + esperado_flare or s0[:4] != s1[:4] or s0[8:] != s1[8:]:
                fallas += 1
                print(f"FALLA Flare Scarab: ATK {atk0} -> {atk1}, esperado +{esperado_flare}")
        elif s0 != s1:
            fallas += 1
            print(f"FALLA carta {r1.nombre(indice)}: {s0.hex()} != {s1.hex()}")
    print("TODO BIEN" if not fallas else f"{fallas} FALLAS")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
