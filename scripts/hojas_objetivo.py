"""Para cada ID de la tabla de efectos, a que funcion de seleccion llega FUN_0805AEB0.

FUN_0805AEB0(lado, ID, 0) es un despachador por ID de carta. Se ejecuta con
Unicorn y se anota la primera llamada que sale del cuerpo del despachador.

Uso: python3 hojas_objetivo.py rom.gba [salida.csv]       (pip install unicorn)
"""
import csv
import json
import os
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_LR, UC_ARM_REG_SP, UC_ARM_REG_PC

from da_lib import *

DESPACHADOR = 0x0805AEB0
LIMPIAR_ZONA = 0x0800B89C      # clear_zone_effects: se simula como "volver"
RETORNO = 0x03007F00


def main(ruta_rom, ruta_csv=None):
    rom = Rom(ruta_rom)
    nombres_json = os.path.join(os.path.dirname(__file__), "..", "ghidra", "nombres_yugiohgx-da.json")
    inicios = sorted(int(k, 16) & ~1 for k in json.load(open(nombres_json)))
    fin = next(a for a in inicios if a > DESPACHADOR)

    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x800000)
    uc.mem_write(BASE, bytes(rom.d[:0x800000]))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)

    estado = {"hoja": None}

    def gancho(u, dir_, tam, _):
        if dir_ == LIMPIAR_ZONA:
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))   # LR trae el bit Thumb
            return
        if estado["hoja"] is None and not (DESPACHADOR <= dir_ < fin) and dir_ != RETORNO:
            estado["hoja"] = dir_
            u.emu_stop()

    uc.hook_add(UC_HOOK_CODE, gancho)
    salida = []
    for fila in rom.efectos():
        cid = fila["id"]
        estado["hoja"] = None
        uc.reg_write(UC_ARM_REG_R0, 0)
        uc.reg_write(UC_ARM_REG_R1, cid)
        uc.reg_write(UC_ARM_REG_R2, 0)
        uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
        uc.reg_write(UC_ARM_REG_LR, RETORNO | 1)
        try:
            uc.emu_start(DESPACHADOR | 1, RETORNO, count=20000)
            sin = "vuelve" if estado["hoja"] is None else ""
        except Exception as e:                      # salto a memoria no mapeada, etc.
            sin = f"error:{type(e).__name__}"
        i = rom.indice_de(cid)
        salida.append((cid, rom.nombre(i) if i else "", "si" if i else "NO",
                       f"{estado['hoja']:08X}" if estado["hoja"] else "", sin))
    w = csv.writer(open(ruta_csv, "w", newline="") if ruta_csv else sys.stdout)
    w.writerow(["id_konami", "nombre", "en_juego", "hoja", "nota"])
    w.writerows(salida)


if __name__ == "__main__":
    main(*sys.argv[1:3])
