"""Que codigos de estado devuelve fn_04 de cada carta.

Cada funcion de la fila recibe la carta y el estado actual (byte 0x020204C6) y devuelve
el estado siguiente. Los switch del motor solo atienden 0x62, 0x63, 0x78 y 0x7C..0x80
(ver NOTAS-REVERSE.md): un codigo del rango 0x64..0x7B deja el efecto sin resolver.

Se ejecuta fn_04 con Unicorn partiendo de cada estado posible; toda llamada a una
funcion fuera de la vecindad de la carta se reemplaza por "devolver 0". El recorrido
es aproximado: sirve para ver QUE CODIGOS PUEDE DEVOLVER, no cuando.

Uso: python3 codigos_estado.py rom.gba [salida.csv]       (pip install unicorn)
"""
import csv
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_LR, UC_ARM_REG_SP, UC_ARM_REG_PC

from da_lib import *

ESTADO = 0x020204C6
CARTA = 0x02010000
RETORNO = 0x03007F00
ATENDIDOS = {0x62, 0x63, 0x78, 0x7C, 0x7D, 0x7E, 0x7F, 0x80}
ESTADOS_INICIALES = (0x80, 0x7F, 0x7E, 0x7D, 0x7C, 0x7B, 0x7A, 0x79, 0x78, 0x77)
VENTANA = 0x600          # bytes alrededor de fn_04 que se consideran "la propia carta"


def main():
    rom = Rom(sys.argv[1])
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    ctx = {"ini": 0, "fin": 0}

    def gancho(u, dir_, tam, _):
        if dir_ == RETORNO or ctx["ini"] <= dir_ < ctx["fin"]:
            return
        u.reg_write(UC_ARM_REG_R0, 0)                 # funcion externa: devuelve 0
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    w = csv.writer(open(sys.argv[2], "w", newline="") if len(sys.argv) > 2 else sys.stdout)
    w.writerow(["id_konami", "nombre", "en_juego", "codigos_devueltos", "sin_atender"])
    for k in range(rom.efectos_n):
        base = rom.efectos_base + EFECTOS_FILA * k
        cid, fn4 = rom.u16(base), rom.u32(base + 4)
        if (fn4 & ~1) in (0, SIN_EFECTO & ~1):
            continue
        ctx["ini"], ctx["fin"] = (fn4 & ~1) - 0x40, (fn4 & ~1) + VENTANA
        codigos = set()
        for est in ESTADOS_INICIALES:
            uc.mem_write(ESTADO, bytes([est]))
            uc.mem_write(CARTA, bytes(16))
            uc.reg_write(UC_ARM_REG_R0, CARTA)
            uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
            uc.reg_write(UC_ARM_REG_LR, RETORNO | 1)
            try:
                uc.emu_start(fn4 | 1, RETORNO, count=3000)
            except Exception:
                continue
            r = uc.reg_read(UC_ARM_REG_R0) & 0xFF
            if r:
                codigos.add(r)
        i = rom.indice_de(cid)
        malos = [c for c in sorted(codigos) if c not in ATENDIDOS and 0x60 <= c <= 0x7F]
        w.writerow([cid, rom.nombre(i) if i else "", "si" if i else "NO",
                    " ".join(f"{c:#04x}" for c in sorted(codigos)), " ".join(f"{c:#04x}" for c in malos)])


if __name__ == "__main__":
    main()
