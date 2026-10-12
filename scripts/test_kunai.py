"""Prueba con Unicorn de las piezas de Kunai with Chain (ID 4657).

fn_04 (efectos/kunai_cadena.s):
  - ataque declarado (tipo 0x10) de un monstruo del rival boca arriba en ataque: se llama a
    FUN_0801A36C(lado, id, 0, 0), que lo pasa a defensa;
  - con un monstruo propio elegido (p[8] & 0xF != 0, id en p[9]), la carta boca arriba en la zona
    de Magicas/Trampas y el monstruo boca arriba en su zona: FUN_0801A600(lado, ranura, monstruo).
Gancho de FUN_080236C4 (efectos/gancho_queda_campo.s): la carta ya activada (bandera 0x20) va al
cementerio (1) salvo que se haya equipado (0). Se compara con una Trampa normal y con Metalmorph (originales).

Uso: python3 test_kunai.py rom.gba            (pip install unicorn)
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                               UC_ARM_REG_LR, UC_ARM_REG_SP, UC_ARM_REG_PC)

from da_lib import *

J0, L = 0x02022250, 0x2B08
CAMBIAR, EQUIPAR, QUEDA, BANDERA = 0x0801A36C, 0x0801A600, 0x080236C4, 0x0800E158
PROPIA, MONSTRUO = 38, 10


def maquina(rom):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    return uc


def ranura(idc):
    return J0 + (idc >> 7) * L + (idc & 0x7F) * 0x50


def poner(uc, idc, zona, pos, indice=0):
    a = ranura(idc)
    uc.mem_write(a + 0x24, struct.pack("<H", indice))
    uc.mem_write(a + 0x31, bytes([zona << 4, 0, pos]))


def carta(uc, tipo, lado, atacante=0, anulada=0, elegidos=0, objetivo=0):
    p = 0x02010000
    cab = (tipo << 13) | (PROPIA << 1) | lado
    uc.mem_write(p, struct.pack("<I", cab) + bytes([atacante, 0, 0, 0, elegidos, objetivo, 0, 0]))
    uc.mem_write(p + 2, bytes([(cab >> 16) & 0xFF | anulada]))
    return p


def llamar(uc, fn, p, ganchos):
    def gancho(u, dir_, tam, _):
        if dir_ in ganchos:
            r = ganchos[dir_](tuple(u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)))
            u.reg_write(UC_ARM_REG_R0, r or 0)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    h = uc.hook_add(UC_HOOK_CODE, gancho)
    uc.reg_write(UC_ARM_REG_R0, p)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
    uc.emu_start(fn | 1, 0x03007F00, count=20000)
    uc.hook_del(h)
    return uc.reg_read(UC_ARM_REG_R0)


def efecto(rom, id_atacante=0x80 | 31, pos=0x10, tipo=0x10, anulada=0, lado=0,
           elegidos=0, zona_propia=5, cara_propia=0x10, zona_obj=0, cara_obj=0x10):
    """Devuelve (llamadas a cambiar posicion, llamadas a equipar)."""
    uc = maquina(rom)
    poner(uc, id_atacante, 0, pos)
    poner(uc, PROPIA, zona_propia, cara_propia)
    poner(uc, MONSTRUO, zona_obj, cara_obj)
    p = carta(uc, tipo, lado, id_atacante, anulada, elegidos, MONSTRUO)
    cambiar, equipar = [], []
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(EFECTOS + EFECTOS_FILA * filas[4657] + 4)
    llamar(uc, fn & ~1, p, {CAMBIAR: cambiar.append, EQUIPAR: lambda r: equipar.append(r[:3])})
    return cambiar, equipar


def queda(rom, nombre, elegidos, anulada=0):
    """Lo que devuelve FUN_080236C4 para una carta boca arriba en la zona de Magicas/Trampas."""
    uc = maquina(rom)
    indice = next(i for i in range(1, N_CARTAS + 1) if rom.nombre(i) == nombre)
    poner(uc, PROPIA, 5, 0x10, indice)
    p = carta(uc, 0x10, 0, elegidos=elegidos, anulada=anulada)
    # FUN_0800E158(ranura, n) lee la bandera n de la carta: la 0x20 es "se activo y espera destino"
    return llamar(uc, QUEDA, p, {BANDERA: lambda r: 1 if r[1] == 0x20 else 0})


def main():
    rom = Rom(sys.argv[1])
    ataque, equipo = [(0, 0x9F, 0, 0)], [(0, PROPIA, MONSTRUO)]
    casos = [
        ("ataque del rival, cara arriba en ataque", dict(), (ataque, [])),
        ("el atacante ya esta en defensa", dict(pos=0x30), ([], [])),
        ("atacante boca abajo", dict(pos=0x20), ([], [])),
        ("atacante propio", dict(id_atacante=31), ([], [])),
        ("otro tipo de evento", dict(tipo=0x05), ([], [])),
        ("carta anulada", dict(anulada=8), ([], [])),
        ("ataque del rival y monstruo propio elegido: los dos efectos", dict(elegidos=1), (ataque, equipo)),
        ("sin ataque, monstruo propio elegido: solo equipa", dict(tipo=0x01, elegidos=1), ([], equipo)),
        ("monstruo elegido boca abajo: no equipa", dict(tipo=0x01, elegidos=1, cara_obj=0x20), ([], [])),
        ("el elegido ya no esta en una zona de monstruo: no equipa",
         dict(tipo=0x01, elegidos=1, zona_obj=0xD), ([], [])),
        ("la carta ya no esta en el campo: no equipa", dict(tipo=0x01, elegidos=1, zona_propia=0xD), ([], [])),
        ("anulada con monstruo elegido: nada", dict(elegidos=1, anulada=8), ([], [])),
    ]
    ok = True
    for nombre, kw, esperado in casos:
        r = efecto(rom, **kw)
        bien = r == esperado
        print(f"{'OK ' if bien else 'MAL'} {nombre}: posicion={r[0]} equipo={r[1]}")
        ok = ok and bien
    for nombre, args, esperado in [
        ("Kunai sin equipar: va al cementerio", ("Kunai with Chain", 0), 1),
        ("Kunai equipada: queda en el campo", ("Kunai with Chain", 1), 0),
        ("Metalmorph (original): queda en el campo", ("Metalmorph", 1), 0),
        ("Mirror Force con p[8] = 1 (original): va al cementerio", ("Mirror Force", 1), 1),
    ]:
        r = queda(rom, *args)
        bien = r == esperado
        print(f"{'OK ' if bien else 'MAL'} {nombre}: {r}")
        ok = ok and bien
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
