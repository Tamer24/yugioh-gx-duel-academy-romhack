"""Prueba con Unicorn de la tabla de efectos mudada (scripts/ampliar_efectos.py).

Corre FUN_0806162C (indice de carta -> fila de efecto, o -1) del propio ROM para cada indice y
compara la fila que encuentra con la que encuentra el mismo codigo en un ROM de referencia (el
que no tiene la tabla mudada). Tambien comprueba las filas nuevas por ID.

Uso: python3 scripts/test_tabla_efectos.py ROM_MUDADO ROM_REFERENCIA
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_PROT_ALL
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR

from da_lib import BASE, EFECTOS_FILA, Rom

BUSCAR = 0x0806162C
RET = 0x02000100


def correr(rom):
    mu = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    mu.mem_map(BASE, (len(rom.d) + 0xFFF) & ~0xFFF, UC_PROT_ALL)
    mu.mem_write(BASE, bytes(rom.d))
    mu.mem_map(0x02000000, 0x40000, UC_PROT_ALL)
    mu.mem_map(0x03000000, 0x8000, UC_PROT_ALL)
    mu.mem_write(RET, b"\x70\x47")                     # bx lr (nunca se ejecuta: se corta en RET)

    def fila(indice):
        mu.reg_write(UC_ARM_REG_SP, 0x03007F00)
        mu.reg_write(UC_ARM_REG_LR, RET | 1)
        mu.reg_write(UC_ARM_REG_R0, indice)
        mu.emu_start(BUSCAR | 1, RET, count=2000)
        r = mu.reg_read(UC_ARM_REG_R0)
        return r - (1 << 32) if r >= 1 << 31 else r
    return fila


def contenido(rom, k):
    o = rom.efectos_base + EFECTOS_FILA * k
    return bytes(rom.d[o:o + EFECTOS_FILA])


def main(mudado, referencia):
    m, r = Rom(mudado), Rom(referencia)
    assert m.efectos_mudada and not r.efectos_mudada
    fm, fr = correr(m), correr(r)
    viejas = {f["id"] for f in r.efectos()}
    nuevas = [f for f in m.efectos() if f["id"] not in viejas and f["id"] < 20000]
    ids_nuevos = {f["id"] for f in nuevas}
    malos, con_fila, halladas = [], 0, []
    for i in range(1, m.n + 1):
        km, kr = fm(i), fr(i)
        if m.id_de(i) in ids_nuevos:
            if km < 0 or m.u16(m.efectos_base + EFECTOS_FILA * km) != m.id_de(i):
                malos.append((i, "fila nueva no hallada", km))
            else:
                halladas.append(m.id_de(i))
        elif (km < 0) != (kr < 0):
            malos.append((i, km, kr))
        elif kr >= 0:
            con_fila += 1
            if contenido(m, km) != contenido(r, kr):
                malos.append((i, "fila distinta", km, kr))
    print(f"{con_fila} cartas con fila de efecto; {len(malos)} diferencias")
    for x in malos[:10]:
        print("  ", x)
    print(f"filas nuevas: {sorted(ids_nuevos)}; halladas por el codigo del juego: {sorted(halladas)}")
    if ids_nuevos - set(halladas):
        malos.append("hay filas nuevas que el ROM no usa (la carta no esta en el ROM): " + str(sorted(ids_nuevos - set(halladas))))
    return not malos


if __name__ == "__main__":
    sys.exit(0 if main(*sys.argv[1:3]) else 1)
