"""Desensambla Thumb del ROM con anotacion de literales (ldr rN,[pc,#x]).

Uso: python3 desensamblar.py rom.gba DESDE HASTA [nombres.json]
(direcciones GBA en hexadecimal; nombres.json = ghidra_functions.json de
yugiohgx-da, anota cada `bl` con el nombre de la funcion)
Requiere: pip install capstone
"""
import json
import re
import struct
import sys

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs

from da_lib import BASE


def main():
    rom = open(sys.argv[1], "rb").read()
    a = int(sys.argv[2], 16) - BASE
    b = int(sys.argv[3], 16) - BASE
    nombres = {}
    if len(sys.argv) > 4:
        nombres = {int(k, 16): v for k, v in json.load(open(sys.argv[4])).items()}
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    for i in md.disasm(rom[a:b], BASE + a):
        linea = f"{i.address:08X} {i.mnemonic:6} {i.op_str}"
        if i.mnemonic == "ldr" and "pc" in i.op_str:
            imm = int(i.op_str.split("#")[-1].rstrip("]"), 0)
            lit = ((i.address + 4) & ~3) + imm
            linea += f"  ;=0x{struct.unpack_from('<I', rom, lit - BASE)[0]:08X}"
        if i.mnemonic in ("bl", "b") and nombres:
            m = re.match(r"#0x([0-9a-f]+)", i.op_str)
            if m and int(m.group(1), 16) in nombres:
                linea += f"  ; {nombres[int(m.group(1), 16)]}"
        print(linea)


if __name__ == "__main__":
    main()
