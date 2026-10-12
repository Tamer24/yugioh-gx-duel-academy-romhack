"""Llena modos vacios de los menus de seleccion de un ROM ya generado.

Uso: python3 parche_menu.py rom_entrada.gba rom_salida.gba MODO=DESTINO [...]
  DESTINO: direccion GBA (0x080266EC) o modo:N para copiar el manejador del modo N.
Ejemplo: python3 parche_menu.py Test.gba Menu6.gba 6=modo:1
No necesita keystone.
"""
import sys

from da_lib import Rom, MENU_VACIO, MENU_N


def main():
    rom = Rom(sys.argv[1])
    for par in sys.argv[3:]:
        modo, destino = par.split("=", 1)
        rom.fijar_modo_menu(int(modo), destino)
        print(f"modo {modo} -> {rom.modo_menu(int(modo)):#010x}")
    vacios = [m for m in range(1, MENU_N + 1) if rom.modo_menu(m) == MENU_VACIO]
    print("modos que siguen vacios:", vacios)
    open(sys.argv[2], "wb").write(rom.d)


if __name__ == "__main__":
    main()
