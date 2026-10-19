"""Prueba con Unicorn de las fn_04 nuevas de los Neo-Spacian y de Butterfly Dagger - Elma.

Usa scripts/motor_uc.py: arma el campo a mano, llama a la funcion de la tabla de efectos del ROM
con el byte de estado que pondria el motor y compara los llamados al motor con el texto de cada carta.

  - Neo-Spacian Air Hummingbird (6769): ganas 500 LP por cada carta de la mano del rival; quita la
    bandera 14 (una vez por turno); con la mano del rival vacia o anulada, nada.
  - Neo-Spacian Dark Panther (6772): 0x80 registra solo los monstruos boca arriba del rival; 0x7E
    copia el indice del elegido (conserva el bit 15) y pone la bandera 25; si el elegido ya no esta
    boca arriba, no copia. La IA (lado 1) no lo usa.
  - Neo-Spacian Aqua Dolphin (6768): 0x7E descarta la elegida de mi mano; 0x7C destruye al elegido
    del rival y le hace 500 si controlo un monstruo boca arriba con ATK igual o mayor; si no, recibo 500.
  - Butterfly Dagger - Elma (5724): con el pedido del gancho (tipo 4, momento 0xE) y Elma en el
    cementerio, la pasa a la mano; con cualquier otro pedido salta a la fn_04 original (la del ROM USA).
La de Neo-Spacian Flare Scarab la prueba test_atk_cuenta.py; las de Grand Mole y Glow Moss,
test_gancho_batalla.py.

Uso: python3 scripts/test_neo_spacian.py ROM ROM_ORIGINAL_USA
"""
import sys

from da_lib import Rom
from motor_uc import Motor

fallas = 0


def ok(nombre, cond, detalle=""):
    global fallas
    print(("  ok   " if cond else "  FALLA"), nombre, detalle)
    fallas += 0 if cond else 1


def air_hummingbird(rom):
    print("Neo-Spacian Air Hummingbird")
    for mano, anulada, esperado in ((3, False, 1500), (6, False, 3000), (0, False, None), (4, True, None)):
        m = Motor(rom)
        fn = m.fila(6769)["fn_04"]
        m.carta(0, 2, rom.indice_de(6769))
        m.mano(1, list(range(10, 10 + mano)))
        r = m.fn_estado(fn, m.entrada(0, 2, anulada=anulada), 0x80)
        lp = [c for c in m.llamadas if c[0] == "GANAR_LP"]
        quita = [c for c in m.llamadas if c[0] == "EVENTO" and c[1:4] == (0x3C, 2, 14)]
        if esperado is None:
            ok(f"mano rival {mano}, anulada {anulada}: no gana LP", not lp and r == 0)
        else:
            ok(f"mano rival {mano}: gana {esperado} y deja de estar disponible",
               lp == [("GANAR_LP", 0, esperado, lp[0][3], lp[0][4])] and len(quita) == 1 and r == 0, str(m.llamadas))


def dark_panther(rom):
    print("Neo-Spacian Dark Panther")
    panther, ox, otro = rom.indice_de(6772), 5, 9
    m = Motor(rom)
    fn = m.fila(6772)["fn_04"]
    m.carta(0, 2, panther)
    m.carta(1, 4, ox, pos=0x10)
    m.carta(1, 5, otro, pos=0x20)                  # boca abajo: no se puede elegir
    m.zonas_monstruo(1, [4, 5])
    r = m.fn_estado(fn, m.entrada(0, 2), 0x80)
    reg = [c[1] for c in m.llamadas if c[0] == "REGISTRAR"]
    ok("0x80 registra solo el boca arriba y pregunta", reg == [0x84] and r == 0x7F, f"{reg} -> {r:#x}")
    m.llamadas.clear()
    m.elegir(0x84)
    r = m.fn_estado(fn, m.entrada(0, 2), 0x7E)
    ev = [c[1:4] for c in m.llamadas if c[0] == "EVENTO"]
    ok("0x7E copia el indice del elegido y pone las banderas 25 y quita la 14",
       m.leer_indice(0, 2) == ox and (0x3B, 2, 25) in ev and (0x3C, 2, 14) in ev and r == 0x64,
       f"indice {m.leer_indice(0, 2)}, eventos {ev}")
    m = Motor(rom)
    m.carta(0, 2, panther | 0x8000)
    m.carta(1, 5, otro, pos=0x20)
    m.elegir(0x85)
    r = m.fn_estado(fn, m.entrada(0, 2), 0x7E)
    ok("0x7E con el elegido boca abajo: no copia", m.leer_indice(0, 2) == panther | 0x8000 and r == 0x64)
    m = Motor(rom)
    m.carta(0, 2, panther)
    m.carta(1, 4, ox)
    m.carta(0, 2, panther | 0x8000)
    m.elegir(0x84)
    m.fn_estado(fn, m.entrada(0, 2), 0x7E)
    ok("conserva el bit 15 del indice", m.leer_indice(0, 2) == ox | 0x8000, hex(m.leer_indice(0, 2)))
    m = Motor(rom)
    m.carta(1, 2, panther)
    r = m.fn_estado(fn, m.entrada(1, 2), 0x80)
    ok("la IA (lado 1): nada", r == 0 and not m.llamadas)


def aqua_dolphin(rom):
    print("Neo-Spacian Aqua Dolphin")
    dolphin = rom.indice_de(6768)
    fn = None
    for mio, suyo, gano in ((1800, 1500, True), (1500, 1500, True), (1000, 1500, False)):
        m = Motor(rom)
        fn = m.fila(6768)["fn_04"]
        m.carta(0, 2, dolphin, atk=600)
        m.carta(0, 3, 7, atk=mio)
        m.zonas_monstruo(0, [2, 3])
        m.carta(1, 20, 8, zona=0xF, atk=suyo)        # el elegido, en la mano del rival
        m.elegir(0x94)
        r = m.fn_estado(fn, m.entrada(0, 2), 0x7C)
        dan = [c[1:3] for c in m.llamadas if c[0] == "DANIO"]
        des = [c[1:3] for c in m.llamadas if c[0] == "A_CEMENTERIO"]
        if gano:
            ok(f"mi mejor {mio} contra {suyo}: destruye al elegido y 500 al rival",
               des == [(1, 0x94)] and dan == [(1, 500)] and r == 0x64, str(m.llamadas))
        else:
            ok(f"mi mejor {mio} contra {suyo}: recibo 500", not des and dan == [(0, 500)] and r == 0x64, str(m.llamadas))
    m = Motor(rom)
    m.carta(0, 2, dolphin, atk=600)
    m.carta(0, 10, 7, zona=0xF)
    m.mano(0, [10])
    m.mano(1, [])
    m.elegir(0x0A)
    r = m.fn_estado(fn, m.entrada(0, 2), 0x7E)
    des = [c[1:4] for c in m.llamadas if c[0] == "A_CEMENTERIO"]
    ev = [c[1:4] for c in m.llamadas if c[0] == "EVENTO"]
    ok("0x7E descarta la elegida y quita la bandera 14; sin monstruos del rival en la mano termina",
       des == [(0, 0x0A, 0xFF)] and (0x3C, 2, 14) in ev and r == 0x64, f"{m.llamadas} -> {r:#x}")
    m = Motor(rom)
    r = m.fn_estado(fn, m.entrada(0, 2, anulada=True), 0x80)
    ok("anulada: nada", r == 0 and not m.llamadas)


def elma(rom, original):
    print("Butterfly Dagger - Elma")
    elma_i = rom.indice_de(5724)
    orig = original.fila_efecto(next(k for k in range(original.efectos_n) if original.fila_efecto(k)["id"] == 5724))["fn_04"]
    pedido = 0x1C800 << 12                          # tipo 4, momento 0xE
    casos = (("pedido del gancho, Elma en el cementerio: a la mano", 0xD, pedido, False, [("MOVER_CARTA", 0x05, 0x3C08)]),
             ("del lado del rival: a la mano del rival", 0xD, pedido, False, None),
             ("pedido del gancho, Elma ya no esta en el cementerio: nada", 0xF, pedido, False, []),
             ("pedido del gancho, anulada: nada", 0xD, pedido, True, []))
    for nombre, zona, cab, anulada, esperado in casos:
        lado = 1 if "rival" in nombre else 0
        m = Motor(rom, falsas={orig: ("ORIGINAL", 0x7F)})
        fn = m.fila(5724)["fn_04"]
        m.carta(lado, 5, elma_i, zona=zona)
        m.fn_estado(fn, m.entrada(lado, 5, anulada=anulada, cabecera=cab >> 12), 0x80)
        mov = [c[:3] for c in m.llamadas if c[0] in ("MOVER_CARTA", "ORIGINAL")]
        if esperado is None:
            esperado = [("MOVER_CARTA", 0x85, 1 << 15 | 0x3C08)]
        ok(nombre, mov == esperado, str(mov))
    m = Motor(rom, falsas={orig: ("ORIGINAL", 0x7F)})
    fn = m.fila(5724)["fn_04"]
    m.carta(0, 5, elma_i, zona=5)
    p = m.entrada(0, 5)
    r = m.fn_estado(fn, p, 0x80)
    ok("cualquier otro pedido (equiparla): la fn_04 original, con la misma entrada",
       m.llamadas == [("ORIGINAL", p, m.llamadas[0][2], m.llamadas[0][3], m.llamadas[0][4])] and r == 0x7F, str(m.llamadas))


def main(ruta, ruta_original):
    rom, original = Rom(ruta), Rom(ruta_original)
    air_hummingbird(rom)
    dark_panther(rom)
    aqua_dolphin(rom)
    elma(rom, original)
    print("RESULTADO:", "FUNCIONA" if not fallas else f"{fallas} FALLAS")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
