"""Prueba con Unicorn de Seal of the Ancients (ID 5011): costo de LP y condicion.

fn_14 elige cuantos LP paga una carta segun su ID (cadena de comparaciones) y llama a
FUN_0801ABD0(lado, cantidad). Si el ID no esta en la cadena, no se paga nada.

Uso: python3 test_seal.py rom.gba            (pip install unicorn)
"""
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_LR, UC_ARM_REG_SP, UC_ARM_REG_PC

from da_lib import *

ID_SEAL = 5011
DUELO, LADO = 0x02022250, 0x2B08
CARTA = 0x02010000
PAGAR_LP = 0x0801ABD0
RETORNO = 0x03007F00


def costo(rom, indice, lado=0):
    """Que cantidad de LP paga fn_14 de la carta con ese indice de juego."""
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    # carta en la ranura 0 del lado pedido, con ese indice
    ranura = DUELO + lado * LADO
    uc.mem_write(ranura + 0x24, indice.to_bytes(2, "little"))
    # puntero a carta: u16 con ranura en bits 1..7 y lado en bit 8
    uc.mem_write(CARTA, ((lado << 8) | (0 << 1)).to_bytes(2, "little") + bytes(8))
    llamadas = []

    def gancho(u, dir_, tam, _):
        if dir_ == PAGAR_LP:
            llamadas.append((u.reg_read(UC_ARM_REG_R0), u.reg_read(UC_ARM_REG_R1)))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(EFECTOS + EFECTOS_FILA * filas[rom.id_de(indice)] + 0x14)
    uc.reg_write(UC_ARM_REG_R0, CARTA)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, RETORNO | 1)
    uc.emu_start(fn & ~1 | 1, RETORNO, count=20000)
    return llamadas


def main():
    rom = Rom(sys.argv[1])
    ind = rom.indice_de(ID_SEAL)
    print(f"Seal of the Ancients: indice {ind}, nombre {rom.nombre(ind)!r}")
    llamadas = costo(rom, ind)
    pagos = [c for _, c in llamadas]
    print("fn_14 llama a pagar_LP(lado, cantidad):", llamadas)
    assert pagos == [1000], f"se esperaba pagar 1000 LP y paga {pagos}"
    print("ok: paga 1000 LP, como dice la carta")


if __name__ == "__main__":
    main()
