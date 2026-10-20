"""Parches de codigo para Duel Academy (USA).

Los parches antiguos se ensamblan con keystone-engine (pip install keystone-engine,
solo se importa si hace falta). Los efectos nuevos (efecto_nuevo) se ensamblan
con las binutils de ARM: brew install arm-none-eabi-binutils.

    busqueda_ids(rom)      La busqueda ID -> indice deja de depender de que la
                           tabla de IDs este ordenada. Permite usar cualquier
                           hueco para cualquier carta.
    invocacion_tipo(rom)   La invocacion especial "retirando monstruos del
                           Cementerio" acepta requisitos por TIPO y de 3
                           cartas. Agrega la entrada de Dark Necrofear.
    contrasenas_gratis(rom) La maquina de contrasenas no descuenta DP.
    baul_inicial(rom)      Una partida nueva arranca con cartas extra en el baul.
    efecto_nuevo(rom, esp) Pone una funcion propia (archivo .s) en una columna de
                           la fila de efecto de una carta.

Todo el codigo nuevo va al espacio libre, desde CODIGO. Los parches sobre el
codigo original son ganchos de 4 u 8 bytes.
"""
import os
import shutil
import struct
import subprocess
import tempfile

from da_lib import *

CODIGO = 0x1900000          # offset de archivo donde empieza el codigo nuevo
_ks = None


def _keystone():
    global _ks
    if _ks is None:
        from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB
        _ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    return _ks


class Espacio:
    """Reparte el espacio libre de a bloques alineados a 4."""
    def __init__(self, rom, inicio=CODIGO):
        self.rom, self.cur = rom, inicio

    def reservar(self, n):
        o = self.cur
        self.cur = (o + n + 3) & ~3
        return o

    def poner(self, datos):
        o = self.reservar(len(datos))
        self.rom.d[o:o + len(datos)] = datos
        return o

    def asm(self, fuente, **simbolos):
        """Ensambla en la posicion actual y devuelve la direccion GBA (sin bit Thumb)."""
        o = self.cur
        for k, v in simbolos.items():
            fuente = fuente.replace("{" + k + "}", f"0x{v:08x}")
        try:
            ks = _keystone()
        except ImportError:
            # Sin keystone-engine (no hay paquete para todos los Python): las mismas fuentes se
            # ensamblan con las binutils de ARM. El resultado se comprueba aparte: restaurar.py
            # con recetas/test.json tiene que dar el MD5 del ROM (Test) de siempre.
            # keystone rellena con el nop de Thumb-2 (00 BF) antes de las constantes y no agrega
            # nada si no hay constantes: se hace igual para que el ROM salga byte a byte identico.
            cola = "\n    .balignw 4, 0xbf00\n    .pool\n" if "=" in fuente else "\n"
            return self.asm_gnu("    .syntax unified\n    .thumb\n    .text\n    .global _start\n_start:\n"
                                + fuente + cola)
        cod, _ = ks.asm(fuente, BASE + o)
        self.poner(bytes(cod))
        return BASE + o

    def asm_gnu(self, fuente, **simbolos):
        """Ensambla un .s (sintaxis GNU, Thumb) con las binutils de ARM en la
        posicion actual. 'simbolos' pasan a ser constantes del archivo. La
        etiqueta _start es la entrada. Devuelve la direccion GBA (sin bit Thumb)."""
        herr = {n: shutil.which("arm-none-eabi-" + n) for n in ("as", "ld", "objcopy")}
        faltan = [n for n, r in herr.items() if not r]
        assert not faltan, "faltan las binutils de ARM (brew install arm-none-eabi-binutils)"
        o = self.cur
        with tempfile.TemporaryDirectory() as t:
            cab = "".join(f".set {k}, 0x{v:08x}\n" for k, v in simbolos.items())
            open(f"{t}/e.s", "w").write(cab + fuente)
            for cmd in ([herr["as"], "-mthumb", "-march=armv4t", "-o", f"{t}/e.o", f"{t}/e.s"],
                        [herr["ld"], f"-Ttext=0x{BASE + o:08x}", "-e", "_start", "-o", f"{t}/e.elf", f"{t}/e.o"],
                        [herr["objcopy"], "-O", "binary", f"{t}/e.elf", f"{t}/e.bin"]):
                r = subprocess.run(cmd, capture_output=True, text=True)
                assert r.returncode == 0, f"{os.path.basename(cmd[0])}: {r.stderr.strip()}"
            self.poner(open(f"{t}/e.bin", "rb").read())
        return BASE + o


def _salto_largo(rom, donde, destino, reg=3):
    """Gancho de 8 bytes en una direccion alineada a 4: ldr rN,[pc]; bx rN; .word destino|1"""
    assert donde % 4 == 0
    ldr = 0x4800 | (reg << 8)            # ldr rN, [pc, #0]
    bx = 0x4700 | (reg << 3)             # bx rN
    rom.d[donde:donde + 8] = struct.pack("<HHI", ldr, bx, destino | 1)


def _bl(rom, donde, destino):
    """Escribe un BL de Thumb (4 bytes) en 'donde' hacia la direccion GBA 'destino'."""
    off = destino - (BASE + donde + 4)
    assert -0x400000 <= off < 0x400000 and off % 2 == 0, "BL fuera de alcance"
    off >>= 1
    rom.d[donde:donde + 4] = struct.pack("<HH", 0xF000 | ((off >> 11) & 0x7FF), 0xF800 | (off & 0x7FF))


# ---------------------------------------------------------------------------
# 1. Busqueda ID -> indice con tabla propia
# ---------------------------------------------------------------------------
FN_INDICE_DE = 0xDD72C       # get_ordinal_id original (busqueda binaria sobre IDS)


def busqueda_ids(rom, esp):
    """Llamar DESPUES de cambiar los IDs: arma la tabla de pares ordenada."""
    pares = sorted((rom.id_de(i), i) for i in range(1, N_CARTAS + 1))
    assert len({p[0] for p in pares}) == N_CARTAS, "hay IDs repetidos"
    tabla = esp.poner(b"".join(struct.pack("<HH", c, i) for c, i in pares))
    fn = esp.asm("""
        push {r4, r5}
        lsls r0, r0, #16
        lsrs r0, r0, #16
        ldr r4, =0x{pares}
        movs r1, #0
        ldr r2, =0x087a8620
        ldrh r2, [r2]
    bucle:
        cmp r1, r2
        bhs nada
        adds r3, r1, r2
        lsrs r3, r3, #1
        lsls r5, r3, #2
        ldrh r5, [r4, r5]
        cmp r5, r0
        beq hallado
        bhi arriba
        adds r1, r3, #1
        b bucle
    arriba:
        adds r2, r3, #0
        b bucle
    hallado:
        lsls r3, r3, #2
        adds r3, r3, r4
        ldrh r0, [r3, #2]
        b fin
    nada:
        movs r0, #0
    fin:
        pop {r4, r5}
        bx lr
    """.replace("0x{pares}", f"0x{BASE + tabla:08x}"))
    _salto_largo(rom, FN_INDICE_DE, fn, reg=1)
    return {"tabla_pares": tabla, "funcion": fn}


# ---------------------------------------------------------------------------
# 2. Invocacion especial retirando del Cementerio: tipos y 3 cartas
# ---------------------------------------------------------------------------
REQ_TABLA = 0x17DFF44        # 12 x {u16 id, u8 req0, u8 req1, u8 cantidad, 3 de relleno}
REQ_N = 12
REQ_LITERALES = [0x6FD70, 0x6FDCC, 0x6FF44, 0x70054, 0x70200, 0x7022C, 0x7039C]
REQ_LIMITE = 0x6FD5E         # cmp r2, #0xB en FUN_0806FD38 (busqueda lineal)
FN_ATRIBUTO = 0xDDC0         # FUN_0800DDC0(ranura, atributo) -> 0/1
FN_COINCIDE = 0x6FDD0        # FUN_0806FDD0(entrada, k, ranura) -> 0/1; su cuerpo queda libre
GANCHO_TEXTO = 0x7004C       # paso 1: "b 0x080700D2" + relleno
GANCHO_VALIDA = 0x70228      # paso 3: "b 0x080703AC" + relleno
GANCHO_FINAL = 0x7042E       # final: "bl process_card_actions"
TERCERA = 0x02022250 + 0x566E  # byte libre junto a las dos ranuras elegidas (0x566C/0x566D)

TIPO = 0x80                  # un requisito con este bit compara TIPO en vez de atributo


def invocacion_tipo(rom, esp, entradas_nuevas):
    """entradas_nuevas: lista de (id_konami, req0, req1, cantidad). Para tipos, req = TIPO | codigo."""
    assert rom.u16(REQ_LIMITE) == 0x2A0B and rom.u32(REQ_LITERALES[0]) == BASE + REQ_TABLA
    viejas = bytes(rom.d[REQ_TABLA:REQ_TABLA + 8 * REQ_N])
    nuevas = b"".join(struct.pack("<HBBB3x", *e) for e in entradas_nuevas)
    n = REQ_N + len(entradas_nuevas)
    tabla = BASE + esp.poner(viejas + nuevas)
    for lit in REQ_LITERALES:
        assert rom.u32(lit) == BASE + REQ_TABLA
        rom.w32(lit, tabla)
    rom.w16(REQ_LIMITE, 0x2A00 | (n - 1))

    stub = esp.asm("bx r3")          # para llamadas largas: ldr r3,=fn ; bl stub

    # FUN_0800DDC0 ampliada: codigos >= 0x80 comparan el tipo de la ranura.
    f_attr = esp.asm("""
        cmp r1, #0x7f
        bhi por_tipo
        push {r4, r5, r6, lr}
        adds r4, r0, #0
        adds r5, r1, #0
        ldr r6, =0x0800ddc9
        cmp r4, #0xff
        bx r6
    por_tipo:
        cmp r0, #0xff
        beq no
        movs r2, #0x7f
        ands r2, r0
        movs r3, #0x50
        muls r2, r3
        lsrs r0, r0, #7
        movs r3, #1
        ands r0, r3
        ldr r3, =0x2b08
        muls r0, r3
        adds r2, r2, r0
        ldr r3, =0x02022250
        adds r2, r2, r3
        adds r2, #0x30
        ldrb r2, [r2]
        movs r3, #0x1f
        ands r2, r3
        movs r3, #0x7f
        ands r1, r3
        cmp r2, r1
        bne no
        movs r0, #1
        bx lr
    no:
        movs r0, #0
        bx lr
    """)
    _salto_largo(rom, FN_ATRIBUTO, f_attr, reg=2)

    # FUN_0806FDD0 nueva: el requisito k >= 2 repite req1, asi una entrada de 3 cartas funciona.
    f_coin = esp.asm("""
        push {r4, lr}
        cmp r0, #{nmax}
        bhi falla
        cmp r1, #2
        bhi falla
        cmp r1, #1
        bls sigue
        movs r1, #1
    sigue:
        adds r4, r2, #0
        lsls r0, r0, #3
        adds r0, r0, r1
        ldr r3, ={tabla}
        adds r0, r0, r3
        ldrb r1, [r0, #2]
        movs r2, #0x7f
        ands r2, r4
        movs r3, #0x50
        muls r2, r3
        lsrs r0, r4, #7
        movs r3, #1
        ands r0, r3
        ldr r3, =0x2b08
        muls r0, r3
        adds r2, r2, r0
        ldr r3, =0x02022250
        adds r2, r2, r3
        adds r2, #0x30
        ldrb r2, [r2]
        movs r3, #0x1f
        ands r2, r3
        cmp r2, #0x15
        beq falla
        cmp r2, #0x16
        beq falla
        adds r0, r4, #0
        ldr r3, ={f_attr}
        bl {stub}
        lsls r0, r0, #16
        cmp r0, #0
        beq falla
        movs r0, #1
        b listo
    falla:
        movs r0, #0
    listo:
        pop {r4}
        pop {r1}
        bx r1
    """.replace("#{nmax}", f"#{n - 1}").replace("={tabla}", f"=0x{tabla:08x}")
           .replace("={f_attr}", f"=0x{f_attr | 1:08x}").replace("{stub}", f"0x{stub:08x}"))
    _salto_largo(rom, FN_COINCIDE, f_coin, reg=3)

    # Paso 1: texto del pedido cuando la cantidad no es 1 ni 2.
    f_texto = esp.asm("""
        ldrb r0, [r5, #4]
        cmp r0, #3
        bne sale
        ldrb r2, [r5, #2]
        cmp r2, #0x7f
        bhi tipo
        ldr r1, =0x097d7b9c
        b nombre
    tipo:
        movs r1, #0x7f
        ands r2, r1
        ldr r1, =0x097d7b38
    nombre:
        lsls r2, r2, #2
        ldr r2, [r1, r2]
        mov r0, sp
        ldr r1, =0x0946a0be
        ldr r3, =0x080e1f01
        bl {stub}
        add r0, sp, #0x100
        mov r1, sp
        ldrb r2, [r5, #4]
        ldr r3, =0x080e1ff1
        bl {stub}
    sale:
        ldr r3, =0x080700d3
        bx r3
    """.replace("{stub}", f"0x{stub:08x}"))

    # Paso 3: validar tres elegidas y guardarlas.
    f_valida = esp.asm("""
        cmp r0, #3
        bne mal
        ldr r5, =0x02019f24
        movs r6, #0
    otra:
        lsls r0, r6, #2
        ldr r0, [r5, r0]
        lsls r0, r0, #13
        lsrs r0, r0, #24
        ldrb r1, [r4, #2]
        ldr r3, ={f_attr}
        bl {stub}
        lsls r0, r0, #16
        cmp r0, #0
        beq mal
        adds r6, #1
        cmp r6, #3
        blt otra
        ldr r0, [r5]
        lsls r0, r0, #13
        lsrs r0, r0, #24
        ldr r1, [r5, #4]
        lsls r1, r1, #13
        lsrs r1, r1, #24
        lsls r1, r1, #8
        orrs r0, r1
        ldr r2, ={elegidas}
        strh r0, [r2]
        ldr r0, [r5, #8]
        lsls r0, r0, #13
        lsrs r0, r0, #24
        strb r0, [r2, #2]
        ldr r3, =0x080702ad
        bx r3
    mal:
        ldr r3, =0x080703ad
        bx r3
    """.replace("={f_attr}", f"=0x{f_attr | 1:08x}").replace("{stub}", f"0x{stub:08x}")
           .replace("={elegidas}", f"=0x{TERCERA - 2:08x}"))

    # Final: retirar tambien la tercera carta.
    f_final = esp.asm("""
        push {lr}
        adds r0, r7, #0
        ldr r3, =0x0806fd39
        bl {stub}
        adds r1, r0, #1
        beq termina
        lsls r0, r0, #3
        ldr r1, ={tabla}
        adds r0, r0, r1
        ldrb r0, [r0, #4]
        cmp r0, #3
        bne termina
        ldr r0, ={tercera}
        ldrb r0, [r0]
        cmp r0, #0xff
        beq termina
        movs r1, #1
        ands r1, r4
        lsls r1, r1, #15
        movs r2, #2
        orrs r1, r2
        lsls r2, r5, #16
        lsrs r2, r2, #16
        ldr r3, =0x08015dc9
        bl {stub}
    termina:
        ldr r3, =0x08016aed
        bl {stub}
        pop {r3}
        bx r3
    """.replace("{stub}", f"0x{stub:08x}").replace("={tabla}", f"=0x{tabla:08x}")
           .replace("={tercera}", f"=0x{TERCERA:08x}"))

    # Trampolines en el cuerpo ya muerto de FUN_0806FDD0, al alcance de un BL.
    v_texto, v_valida, v_final = FN_COINCIDE + 8, FN_COINCIDE + 16, FN_COINCIDE + 24
    _salto_largo(rom, v_texto, f_texto)
    _salto_largo(rom, v_valida, f_valida)
    _salto_largo(rom, v_final, f_final)
    assert rom.u16(GANCHO_TEXTO) >> 11 == 0b11100 and rom.u16(GANCHO_VALIDA) >> 11 == 0b11100
    _bl(rom, GANCHO_TEXTO, BASE + v_texto)
    _bl(rom, GANCHO_VALIDA, BASE + v_valida)
    _bl(rom, GANCHO_FINAL, BASE + v_final)
    return {"tabla": tabla, "entradas": n, "f_attr": f_attr, "f_coincide": f_coin,
            "f_texto": f_texto, "f_valida": f_valida, "f_final": f_final}


# ---------------------------------------------------------------------------
# 3. Contrasenas gratis (solo para ROMs de prueba)
# ---------------------------------------------------------------------------
RESTA_DP = 0xD5FA8           # "subs r0, r0, r1" en la compra por contrasena (FUN_080D5EE0)


def contrasenas_gratis(rom):
    """La maquina de contrasenas sigue pidiendo 1000 DP, pero no los descuenta."""
    assert rom.u16(RESTA_DP) == 0x1A40
    rom.w16(RESTA_DP, 0x46C0)        # nop


# ---------------------------------------------------------------------------
# 4. Cartas extra en el baul al empezar una partida (solo para ROMs de prueba)
# ---------------------------------------------------------------------------
FIN_MAZOS_INICIALES = 0xE1632   # epilogo de FUN_080E15CC, que reparte los 4 mazos iniciales
FN_AL_BAUL = 0xE58B8            # FUN_080E58B8(indice, copias)


def baul_inicial(rom, esp, indices, copias=3):
    """Despues de repartir los mazos iniciales, agrega 'copias' de cada indice al baul."""
    assert bytes(rom.d[FIN_MAZOS_INICIALES:FIN_MAZOS_INICIALES + 14]) == bytes.fromhex(
        "38bc9846a146aa46f0bc01bc0047"), "el epilogo no es el esperado"
    assert 0 < len(indices) < 256 and 0 < copias < 256
    lista = BASE + esp.poner(b"".join(struct.pack("<H", i) for i in indices))
    stub = esp.asm("bx r3")
    fn = esp.asm("""
        ldr r4, ={lista}
        movs r5, #{n}
    bucle:
        ldrh r0, [r4]
        movs r1, #{copias}
        ldr r3, ={al_baul}
        bl {stub}
        adds r4, #2
        subs r5, #1
        bne bucle
        pop {r3, r4, r5}
        mov r8, r3
        mov r9, r4
        mov r10, r5
        pop {r4, r5, r6, r7}
        pop {r0}
        bx r0
    """.replace("={lista}", f"=0x{lista:08x}").replace("#{n}", f"#{len(indices)}")
           .replace("#{copias}", f"#{copias}").replace("={al_baul}", f"=0x{BASE + FN_AL_BAUL + 1:08x}")
           .replace("{stub}", f"0x{stub:08x}"))
    # Gancho en una direccion no alineada: ldr r0,[pc,#4]; bx r0; nop; .word
    rom.d[FIN_MAZOS_INICIALES:FIN_MAZOS_INICIALES + 10] = struct.pack("<HHHI", 0x4801, 0x4700, 0x46C0, fn | 1)
    return {"lista": lista, "funcion": fn}


# ---------------------------------------------------------------------------
# 5. Efectos nuevos: una funcion propia en una columna de la fila de efecto
# ---------------------------------------------------------------------------
COLUMNAS_FILA = {"fn_04": 4, "fn_0c": 0xC, "fn_10": 0x10, "fn_14": 0x14, "fn_18": 0x18}
# Funciones del motor que usan los efectos nuevos (direcciones Thumb, bit 0 en 1).
MOTOR = {
    "CLEAR_ZONE": 0x0800B89D,   # clear_zone_effects(zona, 0): vacia el registro de candidatas
    "REGISTRAR": 0x0800B641,    # remove_card_from_effect_register(carta): agrega al registro
    "DIALOGO": 0x080875F5,      # init_effect_dialogue(0, n, 0x02019F24, flag)
    "AZAR": 0x080E5741,          # FUN_080E5740(): numero aleatorio (usado por la IA al elegir cartas)
    "CANDIDATAS": 0x0805AEB1,    # FUN_0805AEB0(lado, ID, 0): registra los candidatos de la carta con ese ID
    "A_CEMENTERIO": 0x08018519,  # FUN_08018518(lado, id de ranura, ranura de la carta que lo causa): manda al cementerio
    "INVOCAR": 0x0806C7C5,       # record_monster_set(lado, id de ranura, 1, 0): pide la invocacion de esa carta
    "CAMBIAR_POSICION": 0x0801A36D,  # FUN_0801A36C(lado, id de ranura, 0, 0): cambia de posicion (como Block Attack)
    "EVENTO_MOD": 0x0801A5BD,    # FUN_0801A5BC(lado, ranura origen, ranura destino, tipo): evento 0x4B, agrega un modificador
    "ASK_QUESTION": 0x08009745,  # ask_question(texto): encola el aviso; deja elegir entre los candidatos
    "EQUIPAR": 0x0801A601,       # FUN_0801A600(lado, ranura del equipo, ranura del monstruo): equipa (como Metalmorph)
    "CONTAR_MONSTRUOS": 0x08010C11,  # FUN_08010C10(lado, 1, 0): cuantos monstruos boca arriba controla ese lado
    "REVELAR": 0x0801AB05,       # FUN_0801AB04(lado, ranura): muestra una carta del mazo (como Cyber Jar)
    "SOLO_ESPECIAL": 0x080DD329, # FUN_080DD328(indice): 1 si no se puede Invocar de forma Normal (Fusion, Ritual...)
    "ES_SPIRIT": 0x080DCE19,     # FUN_080DCE18(indice): 1 si es un monstruo Spirit (no admite invocacion especial)
    "MOVER_CARTA": 0x080188AD,   # FUN_080188AC(ranura, lado << 15 | zona << 10 | ...): cambia de zona en el acto (0x3008 = al mazo)
    "LIMPIAR_ACCIONES": 0x0801848D,   # cleanup_card_actions(): vacia la cola de acciones
    "ENVIAR": 0x08015DC9,        # send_card_to_graveyard(ranura, banderas, causante): encola la accion (0x41 cementerio, 0x10 tope del mazo, 0x20 fondo, 4 mano)
    "PROCESAR_ACCIONES": 0x08016AED,  # process_card_actions(): ejecuta la cola
    "TOMAR_CONTROL": 0x0801A8A5,  # FUN_0801A8A4(id de ranura, 0): pasa el monstruo al lado contrario; 0 si no se pudo
    "CASILLA_MAGIAS": 0x08011121,  # FUN_08011120(lado): casilla libre de Magicas y Trampas (0..4) o -1
    "ENCOLAR_EFECTO": 0x080314B5,  # FUN_080314B4(lado << 31 | (momento << 4 | tipo) << 21 | id, d | d << 16): encola un efecto disparado
    "EVENTO": 0x08022035,        # drawing_FUN_08022034(evento, a1, a2): 0x3B / 0x3C ponen y quitan la bandera a2 de la ranura a1
    "TIENE_BANDERA": 0x0800E159,  # FUN_0800E158(id de ranura, bandera): lee una bandera de ranura+0x60
    "PAGAR_LP": 0x0801ABD1,      # FUN_0801ABD0(lado, cantidad): paga LP (coste de Seal of the Ancients)
    "DANIO": 0x0801ABF1,         # FUN_0801ABF0(lado que lo recibe, cantidad): dano (familia Ookazi, 0x0803A48C)
    "GANAR_LP": 0x0801AD6D,      # FUN_0801AD6C(lado, cantidad): gana LP (familia Dian Keto, 0x0803A20C)
    "ROBAR": 0x0801B28D,         # FUN_0801B28C(lado, cantidad): roba cartas (Pot of Greed, Electric Snake)
}


def efecto_nuevo(rom, esp, id_konami, columna, ruta_fuente):
    """Ensambla ruta_fuente y lo pone en 'columna' de la fila de efecto de la carta.
    El valor anterior de la columna queda disponible en el .s como ORIGINAL."""
    assert columna in COLUMNAS_FILA, f"columna desconocida: {columna}"
    filas = {f["id"]: k for k, f in enumerate(rom.efectos())}
    assert id_konami in filas, f"el ID {id_konami} no tiene fila de efecto"
    donde = rom.efectos_base + EFECTOS_FILA * filas[id_konami] + COLUMNAS_FILA[columna]
    original = rom.u32(donde)
    assert original != 0, f"la columna {columna} de {id_konami} esta vacia: nada que reemplazar"
    direccion = esp.asm_gnu(open(ruta_fuente, encoding="utf-8").read(), ORIGINAL=original, **MOTOR)
    rom.w32(donde, direccion | 1)
    return direccion
