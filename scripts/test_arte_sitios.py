"""Prueba con Unicorn de los 9 ganchos del arte (scripts/ampliar.py, SITIOS_ARTE), uno por uno.

Cada sitio del juego calcula ARTE + 6400 * indice con registros distintos. Para cada uno se corre
su ventana en el ROM original y en el ampliado, con la misma entrada, hasta donde termina, y se
comprueba que:
  - el registro con la direccion del dibujo trae la del ROM ampliado (Rom.arte_dir) y,
    para los indices que ya estaban, la misma que en el original;
  - ningun otro registro (r0 a r12) ni la pila cambia respecto del original.

Uso: python3 scripts/test_arte_sitios.py ROM_ORIGINAL ROM_AMPLIADO
"""
import sys

from unicorn import UC_ARCH_ARM, UC_MODE_THUMB, Uc
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R8, UC_ARM_REG_SP, UC_ARM_REG_IP,
                               UC_ARM_REG_SB, UC_ARM_REG_SL, UC_ARM_REG_FP)

import ampliar
from da_lib import ARTE, BASE, Rom

REGS = [UC_ARM_REG_R0 + k for k in range(8)] + [UC_ARM_REG_R8, UC_ARM_REG_SB, UC_ARM_REG_SL,
                                                UC_ARM_REG_FP, UC_ARM_REG_IP]
# sitio: (donde termina la ventana, registro con el resultado, como entra cada registro dado el indice)
#   entran: dict registro -> funcion(indice)
SITIOS = {
    0x080022DC: (0x080022E4, 1, {1: lambda i: 6400 * i}),
    0x08085888: (0x080858B4, 0, {0: lambda i: 25 * i}),
    0x08097A08: (0x08097A10, 6, {1: lambda i: 6400 * i}),
    0x0809D5AC: (0x0809D5B4, 0, {0: lambda i: 6400 * i}),
    0x080A5EE6: (0x080A5EF0, 6, {2: lambda i: 6400 * i}),
    0x080A60D0: (0x080A60D8, 3, {1: lambda i: 25 * i}),
    0x080A62A0: (0x080A62A8, 4, {1: lambda i: 6400 * i}),
    0x080B65F6: (0x080B6600, 1, {0: lambda i: i, 1: lambda i: 3 * i}),
    0x080D669C: (0x080D66A4, 1, {1: lambda i: 25 * i}),
}


# (indices en REGS: el 8 es r8). En 080B65F6 r2 es el registro del salto: nadie lo lee antes de que
# 080B660C lo cargue de nuevo.
DERIVADOS = {0x0809D5AC: {8}, 0x080A62A0: {7}, 0x080A60D0: {5}, 0x080B65F6: {2}}


def correr(rom, inicio, fin, entra, indice):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    for k, r in enumerate(REGS):
        uc.reg_write(r, 0x11110000 + 0x1111 * k)
    for reg, f in entra.items():
        uc.reg_write(UC_ARM_REG_R0 + reg, f(indice))
    uc.reg_write(UC_ARM_REG_SP, 0x03007000)
    uc.emu_start(inicio | 1, fin, count=2000)
    return [uc.reg_read(r) for r in REGS], bytes(uc.mem_read(0x03007000, 0x100)), uc.reg_read(UC_ARM_REG_SP)


def main(original, ampliado):
    orig, amp = Rom(original), Rom(ampliado)
    assert amp.ampliado
    indices = [1, 600, 1200, 1201, 1443, 1444, 1445, 1700, 1843, amp.n]
    malos = 0
    for inicio, (fin, res, entra) in SITIOS.items():
        for i in indices:
            ro, so, spo = correr(orig, inicio, fin, entra, i)
            ra, sa, spa = correr(amp, inicio, fin, entra, i)
            esperado = BASE + amp.arte_dir(i)
            bien = ra[res] == esperado and sa == so and spa == spo
            # lo que puede cambiar: el resultado, el desplazamiento que se corrige y lo que se
            # copia del resultado dentro de la misma ventana (r8 en 0809D5AC, r7 en 080A62A0, r5 en 080A60D0)
            propios = {res, *entra} | DERIVADOS.get(inicio, set())
            resto = [k for k in range(len(REGS)) if k not in propios and ra[k] != ro[k]]
            if i < ampliar.LIMITE_IDX and any(ra[k] != ro[k] for k in range(len(REGS))
                                              if k not in DERIVADOS.get(inicio, set())):
                resto.append("indice viejo distinto")
            if not bien or resto:
                malos += 1
                print(f"MAL   {inicio:08X} indice {i}: resultado {ra[res]:08X} esperado {esperado:08X}; "
                      f"registros distintos: {resto}; pila igual: {sa == so}")
        print(f"ok    sitio {inicio:08X}: {len(indices)} indices")
    print("TODO BIEN" if not malos else f"{malos} FALLAS")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
