"""Prueba con Unicorn de efectos/gancho_batalla.s (FUN_08067E60, primer cuadro del calculo de dano):
Neo-Spacian Glow Moss (6771) y Neo-Spacian Grand Mole (6770).

Arma el registro de la batalla (0x02020C20) y el campo a mano y entra al gancho. Los llamados al
motor los anota motor_uc; "SIGUE" es volver al original (0x08067E68: la batalla se calcula) y
"FIN_BP" el evento 0x64 (FUN_0801B8E0: termina la Battle Phase).

  Glow Moss: si ataca o la atacan, el rival muestra y roba la carta de arriba de su mazo:
    Monstruo -> termina la Battle Phase; Magica -> si Glow Moss ataca a un monstruo, ataque directo
    (dano de su ATK y la batalla no se calcula); Trampa -> Glow Moss a defensa y la batalla sigue.
    Con el mazo del rival vacio, nada.
  Grand Mole (solo la del jugador): cuando perderia (el otro en ataque con ATK igual o mayor si Mole
    ataca o esta en ataque; mayor que su DEF si esta en defensa) vuelve a la mano con el otro y la
    batalla no se calcula. Si no pierde, o el otro esta en defensa, la batalla sigue.

Uso: python3 scripts/test_gancho_batalla.py ROM
"""
import struct
import sys

from da_lib import Rom
from motor_uc import J0, LADO, Motor

REG = 0x02020C20
GANCHO, SIGUE, FIN_BP = 0x08067E60, 0x08067E68, 0x0801B8E0
MOSS, MOLE = 6771, 6770
fallas = 0


def ok(nombre, cond, detalle=""):
    global fallas
    print(("  ok   " if cond else "  FALLA"), nombre, detalle)
    fallas += 0 if cond else 1


def batalla(rom, atacante, defensor=None, robada=None, mazo_vacio=False):
    """atacante/defensor: (lado, n, ID o indice, pos, atk, def). robada: tipo de la carta de arriba
    del mazo del rival de Glow Moss (0x15 Trampa, 0x16 Magica, otro = Monstruo).
    Devuelve (motor, registro +0xA)."""
    m = Motor(rom, falsas={SIGUE: ("SIGUE", 0), FIN_BP: ("FIN_BP", 0)})
    ids = []
    for c in (atacante, defensor):
        if c is None:
            continue
        lado, n, carta, pos, atk, de = c
        indice = rom.indice_de(carta) if carta > 1300 else carta
        idr = m.carta(lado, n, indice, pos=pos, atk=atk)
        m.uc.mem_write(m.ranura(lado, n) + 0x2C, struct.pack("<I", de))
        ids.append(idr)
    directo = defensor is None
    # atacante en los bits 13-20 de u32(+0); defensor en los bits 5-12 de u16(+2), que es la mitad
    # alta de esa misma palabra (bits 21-28)
    v = (ids[0] << 13) | (1 if directo else 0) | ((ids[1] << 21) if not directo else 0)
    m.uc.mem_write(REG, struct.pack("<I", v) + bytes(8))
    if robada is not None:
        lado_rival = 1 - atacante[0] if atacante[2] == MOSS else 1 - defensor[0]
        base = J0 + lado_rival * LADO
        m.carta(lado_rival, 40, 3, zona=0xC)
        m.uc.mem_write(m.ranura(lado_rival, 40) + 0x30, bytes([robada]))
        m.uc.mem_write(base + 0x28A4, bytes([(lado_rival << 7) | 40]))
        m.uc.mem_write(base + 0x1C, struct.pack("<H", (0 if mazo_vacio else 20) << 6))
    m.llamar(GANCHO, 0x1234)
    return m, m.uc.mem_read(REG + 0xA, 1)[0]


def glow_moss(rom):
    print("Neo-Spacian Glow Moss")
    moss_ataca = (0, 2, MOSS, 0x10, 300, 900)
    otro = (1, 3, 5, 0x10, 1800, 1000)
    m, f = batalla(rom, moss_ataca, otro, robada=0x05)
    n = m.nombres()
    ok("ataca, el rival roba un Monstruo: termina la Battle Phase", "REVELAR" in n and ("ROBAR", 1, 1) == m.llamadas[n.index("ROBAR")][:3]
       and "FIN_BP" in n and "SIGUE" not in n, str(n))
    m, f = batalla(rom, moss_ataca, otro, robada=0x16)
    n = m.nombres()
    dan = [c[1:3] for c in m.llamadas if c[0] == "DANIO"]
    ok("ataca, roba una Magica: 300 de dano al rival y la batalla no se calcula", dan == [(1, 300)] and f == 6 and "SIGUE" not in n, f"{n} +0xA={f}")
    m, f = batalla(rom, moss_ataca, otro, robada=0x15)
    n = m.nombres()
    pos = [c[1:3] for c in m.llamadas if c[0] == "CAMBIAR_POSICION"]
    ok("ataca, roba una Trampa: Glow Moss a defensa y la batalla sigue", pos == [(0, 2)] and "SIGUE" in n, str(n))
    m, f = batalla(rom, otro, (0, 2, MOSS, 0x10, 300, 900), robada=0x16)
    n = m.nombres()
    ok("la atacan, roba una Magica: solo roba y la batalla sigue", "ROBAR" in n and "DANIO" not in n and "SIGUE" in n, str(n))
    m, f = batalla(rom, moss_ataca, None, robada=0x16)
    n = m.nombres()
    ok("ataque directo, roba una Magica: ya es directo, la batalla sigue", "ROBAR" in n and "DANIO" not in n and "SIGUE" in n, str(n))
    m, f = batalla(rom, moss_ataca, otro, robada=0x05, mazo_vacio=True)
    n = m.nombres()
    ok("mazo del rival vacio: nada", n == ["SIGUE"], str(n))


def grand_mole(rom):
    print("Neo-Spacian Grand Mole")
    casos = [
        ("ataca a uno de ATK mayor: los dos a la mano", (0, 2, MOLE, 0x10, 900, 300), (1, 3, 5, 0x10, 1800, 1000), True),
        ("ataca a uno de ATK igual: los dos a la mano", (0, 2, MOLE, 0x10, 900, 300), (1, 3, 5, 0x10, 900, 1000), True),
        ("ataca a uno de ATK menor: la batalla sigue", (0, 2, MOLE, 0x10, 900, 300), (1, 3, 5, 0x10, 800, 1000), False),
        ("ataca a uno en defensa: la batalla sigue", (0, 2, MOLE, 0x10, 900, 300), (1, 3, 5, 0x30, 1800, 1000), False),
        ("la ataca uno de ATK mayor estando en ataque: los dos a la mano", (1, 3, 5, 0x10, 1800, 1000), (0, 2, MOLE, 0x10, 900, 300), True),
        ("en defensa, la ataca uno con ATK mayor que su DEF: los dos a la mano", (1, 3, 5, 0x10, 400, 1000), (0, 2, MOLE, 0x30, 900, 300), True),
        ("en defensa, la ataca uno con ATK igual a su DEF: la batalla sigue", (1, 3, 5, 0x10, 300, 1000), (0, 2, MOLE, 0x30, 900, 300), False),
        ("la del rival: nada", (1, 2, MOLE, 0x10, 900, 300), (0, 3, 5, 0x10, 1800, 1000), False),
    ]
    for nombre, a, d, vuelve in casos:
        m, f = batalla(rom, a, d)
        n = m.nombres()
        env = [c[1:3] for c in m.llamadas if c[0] == "ENVIAR"]
        mole = (a if a[2] == MOLE else d)
        otro = (d if a[2] == MOLE else a)
        mole_id, otro_id = (mole[0] << 7) | mole[1], (otro[0] << 7) | otro[1]
        if vuelve:
            ok(nombre, env == [(mole_id, 4), (otro_id, otro[0] << 15 | 4)] and "PROCESAR_ACCIONES" in n and f == 6
               and "SIGUE" not in n, f"{env} {n}")
        else:
            ok(nombre, not env and "SIGUE" in n, str(n))


def main(ruta):
    rom = Rom(ruta)
    glow_moss(rom)
    grand_mole(rom)
    print("RESULTADO:", "FUNCIONA" if not fallas else f"{fallas} FALLAS")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
