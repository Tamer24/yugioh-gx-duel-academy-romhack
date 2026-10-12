"""Prueba con Unicorn de las piezas de Electromagnetic Bagworm (ID 5040).

Texto: "FLIP: Take control of 1 face-up Machine-Type monster on your opponent's side of the field
until the end of your next turn."

fn_04 (efectos/bagworm_control.s): con una Maquina rival boca arriba elegida, pide el traspaso
(FUN_0801A8A4) y deja en ella una entrada de modificador de tipo 5 con origen en Bagworm; si se
activa en el turno propio la entrada va marcada "saltear" (0x15).
Gancho de la End Phase (efectos/gancho_fin_control.s, 0x08065D20): contesta si el monstruo vuelve
ahora a su dueno. Lo esperado sale del texto: vuelve al terminar el turno siguiente de quien lo
controla, y no antes. Se ejecuta el tramo original 0x08065D1E..0x08065D28 con el motor real.

Segundo efecto: "If this card is destroyed as a result of battle, the ATK and DEF of the monster
that destroyed this card are decreased by 500 points." El motor lo tiene para Slate Warrior (5037)
y Rigorous Reaver (5044): la rutina de destruccion en batalla (FUN_08068C8C) los reconoce por ID en
dos arboles de comparaciones y encola el efecto con tipo 4. Se prueba que
  - los dos arboles mandan a Bagworm a la misma rama que a Slate Warrior y, con el ROM original al
    lado, que ningun otro ID de las 1200 cartas cambio de destino;
  - fn_04 con tipo 4 deja en el monstruo de p[4] un modificador de tipo 10 y no pide traspaso;
  - fn_18 con tipo 4 no pide elegir nada.

Uso: python3 test_bagworm.py rom.gba [original.gba]           (pip install unicorn)
"""
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
                               UC_ARM_REG_LR, UC_ARM_REG_SP, UC_ARM_REG_PC)

from da_lib import *

J0, L = 0x02022250, 0x2B08
TURNO = J0 + 0x562E                   # bit 1 = jugador del turno
TRASPASO, EVENTO_MOD = 0x0801A8A4, 0x0801A5BC
BAGWORM, MAQUINA = 12, 0x80 | 26       # ranura mia; ranura del rival
ID_BAGWORM = 5040


def maquina_virtual(rom):
    uc = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    uc.mem_map(BASE, 0x2000000)
    uc.mem_write(BASE, bytes(rom.d))
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    return uc


def ranura(idc):
    return J0 + (idc >> 7) * L + (idc & 0x7F) * 0x50


def indice_de(rom, id_konami):
    return next(i for i in range(1, N_CARTAS + 1) if rom.id_de(i) == id_konami)


def poner(uc, idc, indice, controla, pos=0x10, zona=0):
    """Carta en una zona del campo, controlada por el lado 'controla' (bit 19 de +0x30)."""
    a = ranura(idc)
    uc.mem_write(a + 0x24, struct.pack("<H", indice))
    uc.mem_write(a + 0x30, struct.pack("<I", (controla << 19) | (zona << 12)))
    uc.mem_write(a + 0x33, bytes([pos]))


# --- fn_04 ------------------------------------------------------------------------------
def activar(rom, turno, tipo_objetivo="Mechanicalchaser", pos=0x10, objetivo=MAQUINA, elegidos=1, anulada=0):
    """Devuelve (llamadas al traspaso, llamadas a FUN_0801A5BC)."""
    uc = maquina_virtual(rom)
    nombres = {rom.nombre(i): i for i in range(1, N_CARTAS + 1)}
    poner(uc, BAGWORM, indice_de(rom, ID_BAGWORM), 0)
    poner(uc, objetivo, nombres[tipo_objetivo], objetivo >> 7, pos)
    uc.mem_write(TURNO, bytes([turno << 1]))
    p = 0x02010000
    uc.mem_write(p, struct.pack("<H", BAGWORM << 1) + bytes([anulada, 0, 0, 0, 0, 0, elegidos, objetivo, 0, 0]))
    traspasos, mods = [], []

    def gancho(u, dir_, tam, _):
        if dir_ == TRASPASO:
            traspasos.append(u.reg_read(UC_ARM_REG_R0))
            u.reg_write(UC_ARM_REG_R0, 1)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif dir_ == EVENTO_MOD:
            mods.append(tuple(u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(EFECTOS + EFECTOS_FILA * filas[ID_BAGWORM] + 4)
    uc.reg_write(UC_ARM_REG_R0, p)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
    uc.emu_start(fn, 0x03007F00, count=20000)
    return traspasos, mods


# --- destruida en batalla ---------------------------------------------------------------
ANIMACION, ASK_QUESTION = 0x08022084, 0x08009744
ARBOLES = {                               # inicio (r1 = ID de Konami) y fin del arbol de comparaciones
    "A": (0x08068CC8, 0x08068D4C),
    "B": (0x08068F8A, 0x08069034),
}


def destruida(rom, zona_atacante=0, anulada=0):
    """fn_04 con tipo de efecto 4 y el monstruo que la destruyo en p[4].
    Devuelve (llamadas al traspaso, llamadas a FUN_0801A5BC)."""
    uc = maquina_virtual(rom)
    nombres = {rom.nombre(i): i for i in range(1, N_CARTAS + 1)}
    poner(uc, BAGWORM, indice_de(rom, ID_BAGWORM), 0, zona=0xD)
    poner(uc, MAQUINA, nombres["Mechanicalchaser"], 1, zona=zona_atacante)
    p = 0x02010000
    uc.mem_write(p, bytes([BAGWORM << 1, 4 << 1, anulada, 0, MAQUINA, 0, 0, 0, 0, 0, 0, 0]))
    traspasos, mods = [], []

    def gancho(u, dir_, tam, _):
        if dir_ == TRASPASO:
            traspasos.append(u.reg_read(UC_ARM_REG_R0))
            u.reg_write(UC_ARM_REG_R0, 1)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif dir_ == EVENTO_MOD:
            mods.append(tuple(u.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)))
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif dir_ == ANIMACION:
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(EFECTOS + EFECTOS_FILA * filas[ID_BAGWORM] + 4)
    uc.reg_write(UC_ARM_REG_R0, p)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
    uc.emu_start(fn, 0x03007F00, count=20000)
    return traspasos, mods


def seleccion_destruida(rom):
    """fn_18 con tipo de efecto 4 y una Maquina rival en el campo: (resultado, avisos pedidos)."""
    uc = maquina_virtual(rom)
    nombres = {rom.nombre(i): i for i in range(1, N_CARTAS + 1)}
    poner(uc, BAGWORM, indice_de(rom, ID_BAGWORM), 0, zona=0xD)
    poner(uc, MAQUINA, nombres["Mechanicalchaser"], 1)
    p = 0x02010000
    uc.mem_write(p, bytes([BAGWORM << 1, 4 << 1, 0, 0, MAQUINA, 0, 0, 0, 0, 0, 0, 0]))
    avisos = []

    def gancho(u, dir_, tam, _):
        if dir_ == ASK_QUESTION:
            avisos.append(dir_)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    uc.hook_add(UC_HOOK_CODE, gancho)
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    fn = rom.u32(EFECTOS + EFECTOS_FILA * filas[ID_BAGWORM] + 0x18)
    uc.reg_write(UC_ARM_REG_R0, p)
    uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
    uc.reg_write(UC_ARM_REG_LR, 0x03007F00 | 1)
    uc.emu_start(fn, 0x03007F00, count=20000)
    return uc.reg_read(UC_ARM_REG_R0), len(avisos)


def destinos_arbol(rom, arbol, ids):
    """{ID de Konami: primera direccion fuera del arbol a la que llega} para cada ID de 'ids'."""
    inicio, fin = ARBOLES[arbol]
    uc = maquina_virtual(rom)
    salida = {}
    llegada = []

    def gancho(u, dir_, tam, _):
        if BASE <= dir_ < BASE + 0x7A8000 and not inicio <= dir_ < fin:
            llegada.append(dir_)
            u.emu_stop()

    uc.hook_add(UC_HOOK_CODE, gancho)
    for id_konami in ids:
        llegada.clear()
        uc.reg_write(UC_ARM_REG_R1, id_konami)
        uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
        uc.emu_start(inicio | 1, 0, count=200)
        salida[id_konami] = llegada[0] if llegada else None
    return salida


def probar_arboles(rom, original, caso):
    ids = sorted({r.id_de(i) for r in (rom, original) if r for i in range(1, N_CARTAS + 1)})
    for arbol in ARBOLES:
        nuevo = destinos_arbol(rom, arbol, ids)
        caso(f"arbol {arbol}: Bagworm va a la rama de Slate Warrior y Rigorous Reaver",
             (nuevo[ID_BAGWORM] == nuevo[5037] == nuevo[5044], nuevo[ID_BAGWORM] is not None), (True, True))
        if original:
            antes = destinos_arbol(original, arbol, ids)
            caso(f"arbol {arbol}: Bagworm no estaba en esa rama en el ROM original",
                 antes[ID_BAGWORM] != antes[5037], True)
            caso(f"arbol {arbol}: ningun otro ID cambio de destino ({len(ids)} IDs)",
                 sorted(i for i in nuevo if i != ID_BAGWORM and nuevo[i] != antes[i]), [])


# --- gancho de la End Phase -------------------------------------------------------------
def fin_de_turno(rom, turno, entradas=(), controla=0, bandera_15=False, origen_id=ID_BAGWORM, veces=1):
    """Corre 'veces' veces el tramo de la End Phase sobre la Maquina del rival.
    Devuelve ([vuelve en cada pasada], entradas que quedan)."""
    uc = maquina_virtual(rom)
    poner(uc, BAGWORM, indice_de(rom, origen_id), 0, zona=0xD)        # ya esta en el cementerio
    poner(uc, MAQUINA, 184, controla)
    a = ranura(MAQUINA)
    uc.mem_write(a + 0x3E, bytes([len(entradas)]))
    for k, tipo in enumerate(entradas):
        uc.mem_write(a + 0x40 + 2 * k, struct.pack("<H", (tipo << 8) | BAGWORM))
    if bandera_15:
        uc.mem_write(a + 0x60, struct.pack("<I", 1 << 0x15))
    uc.mem_write(TURNO, bytes([turno << 1]))
    salidas = []
    for _ in range(veces):
        uc.reg_write(UC_ARM_REG_R4, MAQUINA)
        uc.reg_write(UC_ARM_REG_SP, 0x03007E00)
        uc.emu_start(0x08065D1E | 1, 0x08065D28, count=20000)
        salidas.append(uc.reg_read(UC_ARM_REG_R0) != 0)
    n = uc.mem_read(a + 0x3E, 1)[0] & 0xF
    quedan = [struct.unpack("<H", uc.mem_read(a + 0x40 + 2 * k, 2))[0] >> 8 for k in range(n)]
    return salidas, quedan


def main():
    rom = Rom(sys.argv[1])
    original = Rom(sys.argv[2]) if len(sys.argv) > 2 else None
    ok = True

    def caso(nombre, obtenido, esperado):
        nonlocal ok
        bien = obtenido == esperado
        print(f"{'OK ' if bien else 'MAL'} {nombre}: {obtenido}")
        ok = ok and bien

    caso("volteo en el turno del rival: traspaso y entrada de tipo 5",
         activar(rom, turno=1), ([MAQUINA], [(0, BAGWORM, MAQUINA, 0x05)]))
    caso("volteo en mi turno: la entrada va marcada para saltear ese fin de turno",
         activar(rom, turno=0), ([MAQUINA], [(0, BAGWORM, MAQUINA, 0x15)]))
    caso("el objetivo no es una Maquina: nada", activar(rom, 1, tipo_objetivo="Des Wombat"), ([], []))
    caso("Maquina boca abajo: nada", activar(rom, 1, pos=0x20), ([], []))
    caso("Maquina propia: nada", activar(rom, 1, objetivo=26), ([], []))
    caso("sin eleccion: nada", activar(rom, 1, elegidos=0), ([], []))
    caso("anulada: nada", activar(rom, 1, anulada=8), ([], []))

    probar_arboles(rom, original, caso)
    caso("destruida en batalla: modificador de tipo 10 en el monstruo que la destruyo, sin traspaso",
         destruida(rom), ([], [(0, BAGWORM, MAQUINA, 0x0A)]))
    caso("destruida en batalla y el otro monstruo ya no esta en el campo: nada",
         destruida(rom, zona_atacante=0xD), ([], []))
    caso("destruida en batalla: la seleccion no pide nada", seleccion_destruida(rom), (1, 0))

    caso("fin del turno del rival, la controlo yo: no vuelve todavia",
         fin_de_turno(rom, turno=1, entradas=[0x05]), ([False], [0x05]))
    caso("fin de mi turno siguiente: vuelve y la entrada se quita",
         fin_de_turno(rom, turno=0, entradas=[0x05]), ([True], []))
    caso("activada en mi turno: ese fin de turno no, el siguiente mio si",
         fin_de_turno(rom, turno=0, entradas=[0x15], veces=2), ([False, True], []))
    caso("otras entradas se conservan",
         fin_de_turno(rom, turno=0, entradas=[0x04, 0x05, 0x0A]), ([True], [0x04, 0x0A]))
    caso("sin entrada de Bagworm: no vuelve", fin_de_turno(rom, turno=0), ([False], []))
    caso("entrada de tipo 4 de Bagworm (formato anterior): no vuelve",
         fin_de_turno(rom, turno=0, entradas=[0x04]), ([False], [0x04]))
    caso("entrada de tipo 5 de otra carta: no vuelve",
         fin_de_turno(rom, turno=0, entradas=[0x05], origen_id=5035), ([False], [0x05]))
    caso("la controla su dueno (ya volvio por otro efecto): no se toca",
         fin_de_turno(rom, turno=1, entradas=[0x05], controla=1), ([False], [0x05]))
    caso("bandera 0x15 de Change of Heart (original): vuelve, como antes",
         fin_de_turno(rom, turno=1, bandera_15=True), ([True], []))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
