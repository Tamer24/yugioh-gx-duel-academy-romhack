"""Pone funciones propias (.s) en la fila de efecto de cartas de un ROM ya generado.

Uso: python3 parche_efecto.py original.gba base.gba salida.gba ID:COLUMNA:archivo.s [...]
  ID       ID de Konami de la carta (p. ej. 4848 = The Inexperienced Spy)
  COLUMNA  fn_04, fn_0c, fn_10, fn_14 o fn_18
  Un gancho de codigo (reemplaza 8 bytes de una funcion del juego por un salto a codigo propio):
  G:DIRECCION:archivo.s   (p. ej. G:08015C78:../efectos/gancho_lista_campo.s)
  Una entrada de tabla de saltos (u32 con la direccion del codigo propio, sin bit Thumb):
  T:DIRECCION:VALOR_ORIGINAL:archivo.s   (p. ej. T:08012C64:08013B4C:../efectos/modificador_atk.s; el original queda como ORIGINAL)
  Unos bytes sueltos del codigo del juego (en hexadecimal, en el orden del archivo):
  B:DIRECCION:BYTES_ORIGINALES:BYTES_NUEVOS   (p. ej. B:0801786E:2BD0:C046 cambia un beq por un nop)
Ejemplo: python3 parche_efecto.py USA.gba Test.gba Spy.gba 4848:fn_04:../efectos/spy_mano.s

El codigo va desde ESPACIO_INICIO. Se comprueba contra el ROM original que esa
zona no fue usada por otro parche. Requiere arm-none-eabi-binutils, no keystone.
"""
import os
import sys

from da_lib import Rom, MD5_USA, BASE
import parches

ESPACIO_INICIO = 0x1A00000
ESPACIO_MAX = 0x20000


def aplicar(original, base, piezas, raiz=""):
    """Aplica 'piezas' (lista de textos con la sintaxis de la linea de comandos) sobre el ROM
    'base' (da_lib.Rom, se modifica). 'original' es el ROM USA, para comprobar que no se pisa
    nada ya tocado. Las rutas de las fuentes son relativas a 'raiz'. Devuelve donde termina el
    codigo nuevo."""
    assert original.md5 == MD5_USA, "el primer ROM debe ser el original USA"
    zona = slice(ESPACIO_INICIO, ESPACIO_INICIO + ESPACIO_MAX)
    assert base.d[zona] == original.d[zona], "la zona de codigo nuevo ya esta ocupada en el ROM base"
    esp = parches.Espacio(base, ESPACIO_INICIO)

    def leer(fuente):
        return open(os.path.join(raiz, fuente), encoding="utf-8").read()

    for par in piezas:
        if par.startswith("G:"):
            _, dir_orig, fuente = par.split(":", 2)
            donde = int(dir_orig, 16) - BASE
            assert donde % 4 == 0, "la direccion del gancho debe estar alineada a 4"
            assert base.d[donde:donde + 8] == original.d[donde:donde + 8], "el gancho pisa codigo ya tocado"
            dest = esp.asm_gnu(leer(fuente), **parches.MOTOR)
            parches._salto_largo(base, donde, dest)
            print(f"gancho {int(dir_orig, 16):#010x} -> {dest | 1:#010x} ({fuente})")
            continue
        if par.startswith("B:"):
            _, dir_b, antes, despues = par.split(":", 3)
            donde, antes, despues = int(dir_b, 16) - BASE, bytes.fromhex(antes), bytes.fromhex(despues)
            assert len(antes) == len(despues), "los bytes nuevos deben ocupar lo mismo que los originales"
            assert original.d[donde:donde + len(antes)] == antes, "los bytes originales no son los esperados"
            assert base.d[donde:donde + len(antes)] == antes, "esos bytes ya fueron tocados"
            base.d[donde:donde + len(antes)] = despues
            print(f"bytes {int(dir_b, 16):#010x}: {antes.hex()} -> {despues.hex()}")
            continue
        if par.startswith("T:"):
            _, dir_t, valor, fuente = par.split(":", 3)
            donde = int(dir_t, 16) - BASE
            assert base.u32(donde) == int(valor, 16), "la entrada de la tabla no tiene el valor esperado"
            dest = esp.asm_gnu(leer(fuente), ORIGINAL=int(valor, 16) | 1, **parches.MOTOR)
            assert dest % 2 == 0, "el codigo de una entrada de tabla debe quedar alineado a 2"
            base.w32(donde, dest)
            print(f"tabla {int(dir_t, 16):#010x} -> {dest:#010x} ({fuente})")
            continue
        cid, columna, fuente = par.split(":", 2)
        dir_ = parches.efecto_nuevo(base, esp, int(cid), columna, os.path.join(raiz, fuente))
        print(f"ID {cid} {columna} -> {dir_ | 1:#010x} ({fuente})")
    assert esp.cur - ESPACIO_INICIO <= ESPACIO_MAX, "el codigo nuevo no entra en la zona reservada"
    print(f"codigo nuevo en {ESPACIO_INICIO:07X}-{esp.cur:07X}")
    return esp.cur


def main():
    original, base, salida = Rom(sys.argv[1]), Rom(sys.argv[2]), sys.argv[3]
    aplicar(original, base, sys.argv[4:])
    open(salida, "wb").write(base.d)


if __name__ == "__main__":
    main()
