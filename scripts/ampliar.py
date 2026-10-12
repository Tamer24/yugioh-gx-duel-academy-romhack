"""EXPERIMENTAL: pasa de las 1200 cartas. Devuelve al juego, como cartas 1201 en adelante, los
monstruos Normales que las cartas restauradas pisaron (datos/huecos.csv), sin sacar ninguna.

Sirve para averiguar que limites son reales: el ROM que sale es para probar, no para jugar.

Que hace sobre una copia del ROM de trabajo (Lote):
  1. Muda al espacio libre (da_lib.AMPLIADO) las tablas por carta, con lugar para CAPACIDAD
     cartas: cantidad, IDs, contrasenas, estadisticas, nombres, descripciones, orden alfabetico
     y paletas, y los dibujos chicos con sus paletas (los que se ven al abrir un sobre). El codigo
     las usa por su direccion exacta: se reemplaza ese literal en todos lados y se comprueba que
     la cuenta sea la medida (706 la de IDs, 303 la de estadisticas, ...).
  2. El arte no se muda (son 7,7 MB): las tablas que estaban pegadas atras del arte ya no se usan
     y ese lugar pasa a ser el dibujo de las cartas 1201 a 1234. De ahi sale la CAPACIDAD.
  3. Rehace la busqueda ID -> indice (parches.busqueda_ids) con la cantidad nueva.
  4. Agrega las cartas: datos, textos, contrasena y dibujo, copiados del ROM original.
  5. El baul. En la memoria el baul son 12 bytes por carta desde 0x02000000 y termina pegado a la
     fecha, los DP y los mazos: la carta 1201 caeria encima. Las cartas 1201 en adelante tienen
     su pedazo de baul aparte (EXT). Cada lugar del juego que llega a una carta del baul se
     engancha para que, pasada la 1200, vaya a EXT: los 17 que calculan (indice - 1) * 12
     (SITIOS_X12) y los 5 recorridos que avanzan de a 12 (SITIOS_PASO).
  6. El guardado. Guardar y cargar son una copia de 0x6188 bytes entre 0x02000000 y la SRAM: se
     agrega una segunda copia para EXT (SRAM 0x6200) y partida nueva lo limpia. EXT lleva una
     marca: una partida guardada con otro ROM carga con las cartas nuevas en cero.
  7. Los sobres. El sorteo de un sobre descarta la carta de indice igual a la cantidad (la ultima):
     se corrige la comparacion para que la ultima carta agregada tambien salga. Cada carta que
     vuelve se agrega a los sobres donde estaba en el juego original, con la misma rareza
     (sobres.py): ahi quedo, desde restaurar.py, la carta restaurada que ocupo su lugar.

Uso (desde la raiz del proyecto):
  python3 scripts/ampliar.py ROM_ORIGINAL ROM_LOTE SALIDA [--cuantas N] [--sobres cambios.json]
N = 1 si no se dice. cambios.json = {"sobres": [...]} son mas cambios a los sobres de la tienda
(formato en scripts/sobres.py), que se aplican al final.
"""
import csv
import os
import re
import struct
import sys

import parches
import sobres
from da_lib import *

EXTRA = 34                          # dibujos que entran entre el final del arte y la tabla 0xF59EBC
CAPACIDAD_NUEVA = N_CARTAS + EXTRA
FIN_LUGAR_ARTE = 0xF59EBC           # tabla sin identificar (36 referencias): no se pisa
ZONA_CODIGO = (0, 0x100000)         # codigo del juego y sus literales
ZONA_PROPIA = (LIBRE, AMPLIADO)     # textos y codigo que agrega este proyecto
REFERENCIAS = {"CANTIDAD": 41, "IDS": 706, "CLAVES": 1, "STATS": 303, "NOMBRES": 43, "NOMBRES_OFF": 43,
               "DESCS": 3, "DESCS_OFF": 3, "ORDEN_ALFA": 1, "PALETAS": 10,
               "MINI_PALETAS": 5, "MINI_ARTE": 5}                               # medidas en el ROM original
# Al sortear un sobre (FUN_080BD89C) el juego pide indice < cantidad: la ultima carta no sale nunca.
# En el original es la 1200; aca seria la ultima agregada. (offset, bytes del juego, bytes nuevos)
SORTEO_ULTIMA = ((0xBD980, "c4d3", "c4d9"), (0xBD9D4, "06d2", "06d8"))         # blo -> bls, bhs -> bhi
BUSQUEDA = """
    push {r4, r5}
    lsls r0, r0, #16
    lsrs r0, r0, #16
    ldr r4, =PARES
    movs r1, #0
    ldr r2, =CUENTA
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
"""


# --- el baul de las cartas 1201 en adelante ---------------------------------------------------
BAUL = 0x02000000
FIN_BAUL = BAUL + 12 * N_CARTAS             # 0x02003840: donde caeria la carta 1201
BLOQUE = 0x0203AE00                         # RAM libre (en cero en 52 estados; ver PROYECTO.md 9.1)
BLOQUE_BYTES = 0x1A0                        # marca + 34 cartas de 12 bytes + 4 del ultimo campo
EXT = BLOQUE + 4                            # donde va la carta 1201
DELTA = EXT - FIN_BAUL
MARCA_BAUL = 0x31584144                     # "DAX1"
SRAM_BLOQUE = 0x0E006200                    # el guardado del juego usa 0x0E000000-0x0E006188
# (indice - 1) * 12: direccion del `lsls rA, rB, #1` de cada sitio
SITIOS_X12 = (0x08010308, 0x080782AA, 0x0808CF96, 0x080B5972, 0x080B706C, 0x080BDCF0, 0x080C1670,
              0x080C7F96, 0x080D26E2, 0x080D4406, 0x080D5338, 0x080D5C08, 0x080D5F88, 0x080E1590,
              0x080E5840, 0x080E58C4, 0x080E5938)
# recorridos: (direccion donde empieza el enganche, despues de cuantas instrucciones va el arreglo,
#              registro que lleva el puntero, registro libre para saltar)
SITIOS_PASO = ((0x080AAF6C, 1, "r6", 0), (0x080AB200, 2, "r3", 3), (0x080BD7DE, 1, "r1", 0),
               (0x080E5808, 1, "r2", 0), (0x080ABD06, 2, "sb", 0))
FN_LIMPIAR, FN_LEER_SRAM, FN_ESCRIBIR_SRAM = 0x080E1C58, 0x080F2260, 0x080F2398
CABEZA = "    .syntax unified\n    .thumb\n    .text\n    .global _start\n_start:\n"
VOLVER = """
    push {{r0, r1}}
    ldr r0, ={destino:#x}
    str r0, [sp, #4]
    pop {{r0, pc}}
"""
ARREGLO_X12 = """
    push {{{s}}}
    ldr {s}, ={limite}
    cmp {indice}, {s}
    blt 1f
    ldr {s}, ={delta:#x}
    adds {destino}, {destino}, {s}
1:  pop {{{s}}}
"""
ARREGLO_PASO = """
    push {{r4, r5}}
    {traer}
    ldr r5, ={fin:#x}
    subs r5, r4, r5
    cmp r5, #12
    bhs 1f
    ldr r5, ={delta:#x}
    adds r4, r4, r5
    {llevar}
1:  pop {{r4, r5}}
"""


def instrucciones(rom, inicio, largo):
    """[(direccion, bytes, mnemonico, operandos)] de la ventana [inicio, inicio + largo)."""
    from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs
    o = inicio - BASE
    lista = [(i.address, bytes(i.bytes), i.mnemonic, i.op_str)
             for i in Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(bytes(rom.d[o:o + largo]), inicio)]
    assert sum(len(x[1]) for x in lista) == largo, f"{inicio:08X}: la ventana corta una instruccion"
    return lista


def saltos_adentro(rom, inicio, largo):
    """Saltos del codigo vecino que caen dentro de la ventana (no en su primera instruccion)."""
    malos = []
    for a in range(inicio - 0x900, inicio + 0x900, 2):
        if inicio <= a < inicio + largo:
            continue
        w = rom.u16(a - BASE)
        if w & 0xF000 == 0xD000 and (w >> 8) & 0xF < 0xE:                 # salto condicional
            d = w & 0xFF
            t = a + 4 + 2 * (d - 0x100 if d & 0x80 else d)
        elif w & 0xF800 == 0xE000:                                         # salto corto
            d = w & 0x7FF
            t = a + 4 + 2 * (d - 0x800 if d & 0x400 else d)
        else:
            continue
        if inicio < t < inicio + largo:
            malos.append(a)
    return malos


def enganchar(rom, original, esp, inicio, libre, arreglo, despues_de):
    """Reemplaza la ventana que empieza en 'inicio' (8 bytes si esta alineada a 4, 10 si no) por un
    salto a una copia de sus instrucciones con 'arreglo' intercalado despues de la instruccion
    'despues_de' (contando desde 1). 'libre' es un registro que la ventana pisa antes de leer.
    Una carga de literal se rehace con su valor; si la ventana termina en un salto condicional,
    la copia vuelve a uno u otro lado."""
    largo = 8 if inicio % 4 == 0 else 10
    o = inicio - BASE
    assert rom.d[o:o + largo] == original.d[o:o + largo], f"{inicio:08X}: otra pieza ya toco ese lugar"
    adentro = saltos_adentro(rom, inicio, largo)
    assert not adentro, f"{inicio:08X}: saltan adentro de la ventana desde {[hex(a) for a in adentro]}"
    cuerpo, fin = [], inicio + largo
    for k, (a, crudo, mnem, ops) in enumerate(instrucciones(rom, inicio, largo), 1):
        if mnem == "ldr" and "[pc" in ops:
            valor = rom.u32(((a + 4) & ~3) + int(ops.split("#")[-1].rstrip("]"), 0) - BASE)
            cuerpo.append(f"    ldr {ops.split(',')[0]}, ={valor:#x}")
        elif mnem.startswith("b") and mnem not in ("bics", "bic"):
            assert a + len(crudo) == fin and len(crudo) == 2 and mnem not in ("b", "bx", "bl", "blx"), \
                f"{a:08X}: no se mudar '{mnem} {ops}'"
            cuerpo.append(f"    {mnem} 9f")
            cuerpo.append(VOLVER.format(destino=fin | 1))
            cuerpo.append("9:" + VOLVER.format(destino=int(ops.lstrip("#"), 0) | 1))
            fin = None
        else:
            assert "pc" not in ops, f"{a:08X}: no se mudar '{mnem} {ops}'"
            cuerpo += [f"    .hword {struct.unpack_from('<H', crudo, j)[0]:#06x}" for j in range(0, len(crudo), 2)]
        if k == despues_de:
            cuerpo.append(arreglo)
    if fin:
        cuerpo.append(VOLVER.format(destino=fin | 1))
    copia = esp.asm_gnu(CABEZA + "\n".join(cuerpo) + "\n    .balign 4\n    .pool\n")
    if largo == 8:
        rom.d[o:o + 8] = struct.pack("<HHI", 0x4800 | (libre << 8), 0x4700 | (libre << 3), copia | 1)
    else:                       # sin alinear: el literal queda en +6 y los 2 bytes de +4 no se ejecutan
        rom.d[o:o + 10] = struct.pack("<HHHI", 0x4801 | (libre << 8), 0x4700 | (libre << 3), 0x46C0, copia | 1)
    return copia


def baul(rom, original, esp):
    """Pasos 5 y 6: el baul de las cartas 1201 en adelante y su guardado."""
    hechos = []
    for a in SITIOS_X12:
        w1, w2, w3 = (rom.u16(a - BASE + k) for k in (0, 2, 4))
        ra, rb, rx = w1 & 7, (w1 >> 3) & 7, w3 & 7
        assert w1 & 0xFFC0 == 0x0040 and ra != rb and w3 & 0xFFF8 == (0x0080 | ra << 3) \
            and w2 in (0x1800 | rb << 6 | ra << 3 | ra, 0x1800 | ra << 6 | rb << 3 | ra), f"{a:08X}: no es un indice * 12"
        s = next(f"r{k}" for k in range(8) if k not in (rb, rx))
        arreglo = ARREGLO_X12.format(s=s, limite=N_CARTAS, indice=f"r{rb}", destino=f"r{rx}", delta=DELTA)
        hechos.append(enganchar(rom, original, esp, a, ra, arreglo, 3))
    for a, despues, puntero, libre in SITIOS_PASO:
        alto = not puntero[1:].isdigit()            # en 'sb' va el desplazamiento, no la direccion
        arreglo = ARREGLO_PASO.format(traer=f"mov r4, {puntero}" if alto else f"adds r4, {puntero}, #0",
                                      llevar=f"mov {puntero}, r4" if alto else f"adds {puntero}, r4, #0",
                                      fin=FIN_BAUL - BAUL if alto else FIN_BAUL, delta=DELTA)
        hechos.append(enganchar(rom, original, esp, a, libre, arreglo, despues))
    llamar = "    ldr r3, ={fn:#x}\n    bl por_r3\n"
    extra = CABEZA + "{antes}" + """
    ldr r0, ={a:#x}
    ldr r1, ={b:#x}
    ldr r2, ={n}
""" + llamar + "{despues}" + VOLVER + "por_r3:\n    bx r3\n    .balign 4\n    .pool\n"
    marcar = f"    ldr r0, ={BLOQUE:#x}\n    ldr r1, ={MARCA_BAUL:#x}\n    str r1, [r0]\n"
    limpiar = f"    ldr r0, ={BLOQUE:#x}\n    ldr r1, ={BLOQUE_BYTES}\n" + llamar.format(fn=FN_LIMPIAR | 1) + marcar

    def ventana(inicio, esperado, fuente):
        o = inicio - BASE
        assert rom.d[o:o + 8] == original.d[o:o + 8], f"{inicio:08X}: otra pieza ya toco ese lugar"
        if esperado:            # None: se reemplaza la funcion entera y no se vuelve a ella
            assert [x[2] for x in instrucciones(rom, inicio, 8)] == esperado
            assert not saltos_adentro(rom, inicio, 8)
        copia = esp.asm_gnu(fuente)
        rom.d[o:o + 8] = struct.pack("<HHI", 0x4B00, 0x4718, copia | 1)        # ldr r3, [pc] ; bx r3
        hechos.append(copia)

    # guardar (FUN_080E6F38 entera): lo de siempre y despues el bloque a la SRAM
    assert bytes(rom.d[0xE6F38:0xE6F42]) == bytes.fromhex("00b5fff7b5fffff7ebff")    # push {lr} ; bl ; bl
    ventana(0x080E6F38, None, CABEZA + f"""
    push {{lr}}
""" + llamar.format(fn=0x080E6EA8 | 1) + llamar.format(fn=0x080E6F18 | 1) + f"""
    ldr r0, ={BAUL:#x}
    movs r1, #0xE0
    lsls r1, r1, #20
    ldr r2, =0x6188
""" + llamar.format(fn=FN_ESCRIBIR_SRAM | 1) + f"""
    ldr r0, ={BLOQUE:#x}
    ldr r1, ={SRAM_BLOQUE:#x}
    ldr r2, ={BLOQUE_BYTES}
""" + llamar.format(fn=FN_ESCRIBIR_SRAM | 1) + """
    pop {r0}
    bx r0
por_r3:
    bx r3
    .balign 4
    .pool
""")
    # cargar (en FUN_080E1B9C): la copia de siempre, el bloque desde la SRAM y, si no trae la marca
    # (partida de otro ROM o SRAM vacia), el bloque en cero
    ventana(0x080E1BD0, ["bl", "bl"], extra.format(
        antes=llamar.format(fn=FN_LEER_SRAM | 1), a=SRAM_BLOQUE, b=BLOQUE, n=BLOQUE_BYTES, fn=FN_LEER_SRAM | 1,
        despues=f"""
    ldr r0, ={BLOQUE:#x}
    ldr r0, [r0]
    ldr r1, ={MARCA_BAUL:#x}
    cmp r0, r1
    beq 1f
{limpiar}1:
""" + llamar.format(fn=0x080E6ED0 | 1), destino=0x080E1BD8 | 1))
    # partida nueva (en FUN_080E14CC): limpiar tambien el bloque
    ventana(0x080E14D4, ["bl", "bl"], CABEZA + llamar.format(fn=FN_LIMPIAR | 1) + limpiar
            + llamar.format(fn=0x080E14A8 | 1) + VOLVER.format(destino=0x080E14DC | 1)
            + "por_r3:\n    bx r3\n    .balign 4\n    .pool\n")
    return hechos


def error(texto):
    raise SystemExit("error: " + texto)


def pisados():
    """Los monstruos Normales que ya no estan en el juego, en el orden de datos/huecos.csv."""
    raiz = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    with open(os.path.join(raiz, "datos", "huecos.csv"), newline="", encoding="utf-8") as f:
        return [(int(x["indice"]), x["hueco_nombre"]) for x in csv.DictReader(f)]


def reemplazar_literal(rom, viejo, nuevo):
    """Cambia la direccion GBA 'viejo' por 'nuevo' donde aparece como literal. Devuelve cuantas
    veces estaba en el codigo del juego (lo que se compara con REFERENCIAS)."""
    patron, en_juego = struct.pack("<I", viejo), 0
    for ini, fin in (ZONA_CODIGO, ZONA_PROPIA):
        o = rom.d.find(patron, ini, fin)
        while o != -1:
            if o % 4 == 0:
                rom.w32(o, nuevo)
                en_juego += ini == 0
            o = rom.d.find(patron, o + 1, fin)
    return en_juego


def ampliar(original, rom, cuantas):
    assert original.md5 == MD5_USA, "el primer ROM tiene que ser el original USA"
    assert not rom.ampliado, "ese ROM ya esta ampliado"
    assert rom.n == N_CARTAS
    assert rom.d[AMPLIADO:sobres.ZONA] == original.d[AMPLIADO:sobres.ZONA], "la zona de las tablas nuevas no esta libre"
    assert ARTE + 6400 * (CAPACIDAD_NUEVA + 1) <= FIN_LUGAR_ARTE
    volver = pisados()
    if not 1 <= cuantas <= min(EXTRA, len(volver)):
        error(f"se pueden agregar de 1 a {min(EXTRA, len(volver))} cartas")
    volver = volver[:cuantas]
    entradas = CAPACIDAD_NUEVA + 1                      # la entrada 0 es una carta vacia
    esp = parches.Espacio(rom, AMPLIADO)
    cabecera = esp.reservar(len(MARCA) + 4 * len(TABLAS))

    # --- 1. las tablas, mudadas ------------------------------------------------------------
    def copia(desde, bytes_viejos, bytes_nuevos):
        o = esp.reservar(bytes_nuevos)
        rom.d[o:o + bytes_nuevos] = bytes(bytes_nuevos)
        rom.d[o:o + bytes_viejos] = rom.d[desde:desde + bytes_viejos]
        return o

    viejas = N_CARTAS + 1
    nuevo = {"CAPACIDAD": CAPACIDAD_NUEVA, "ARTE": ARTE}
    nuevo["CANTIDAD"] = copia(CANTIDAD, 4 + 2 * viejas, 4 + 2 * entradas)      # la cantidad va pegada a los IDs
    nuevo["IDS"] = nuevo["CANTIDAD"] + 4
    for nombre, ancho in (("CLAVES", 4), ("STATS", 4), ("ORDEN_ALFA", 2), ("PALETAS", 128),
                          ("MINI_PALETAS", 64), ("MINI_ARTE", 1024)):
        nuevo[nombre] = copia(globals()[nombre], ancho * viejas, ancho * entradas)
    # Los textos: se copian enteros y los offsets se rehacen contra una base nueva, LIBRE, que queda
    # por debajo de todos (los del juego, ya mudados, y los que escribio restaurar.py).
    for base, offs, fin in (("NOMBRES", "NOMBRES_OFF", NOMBRES_OFF), ("DESCS", "DESCS_OFF", DESCS_OFF)):
        vieja = globals()[base]
        bloque = copia(vieja, fin - vieja, fin - vieja)
        tabla = esp.reservar(4 * entradas)
        for i in range(entradas):
            a = vieja + rom.u32(globals()[offs] + 4 * i) if i < viejas else LIBRE
            if vieja <= a < fin:
                a = bloque + (a - vieja)
            assert a >= LIBRE, f"texto de la carta {i} fuera de lugar: {a:07X}"
            rom.w32(tabla + 4 * i, a - LIBRE)
        nuevo[base], nuevo[offs] = LIBRE, tabla
    for nombre, cuenta in REFERENCIAS.items():
        hechas = reemplazar_literal(rom, BASE + globals()[nombre], BASE + nuevo[nombre])
        assert hechas == cuenta, f"{nombre}: {hechas} referencias en el codigo y se esperaban {cuenta}"
    rom.d[cabecera:cabecera + len(MARCA)] = MARCA
    for k, nombre in enumerate(TABLAS):
        rom.w32(cabecera + len(MARCA) + 4 * k, nuevo[nombre])
    rom.leer_tablas()
    assert rom.ampliado and rom.n == N_CARTAS
    for i in range(N_CARTAS + 1):                       # mudadas sin cambiar nada
        assert (rom.id_de(i), rom.stats(i)["u32"]) == (rom.u16(IDS + 2 * i), rom.u32(STATS + 4 * i))
        assert rom.nombre(i) == rom.cstr(NOMBRES + rom.u32(NOMBRES_OFF + 4 * i))
        assert rom.desc(i) == rom.cstr(DESCS + rom.u32(DESCS_OFF + 4 * i))

    # --- 2. las cartas nuevas --------------------------------------------------------------
    def texto(t):
        return esp.poner(t.encode("latin1") + b"\0") - LIBRE

    informe = []
    for k, (i_viejo, nombre) in enumerate(volver):
        i = N_CARTAS + 1 + k
        assert original.nombre(i_viejo) == nombre, f"el indice {i_viejo} del original no es {nombre}"
        cid = original.id_de(i_viejo)
        assert rom.indice_de(cid) == 0, f"{nombre} ({cid}) ya esta en el juego"
        rom.w16(rom.IDS + 2 * i, cid)
        rom.w32(rom.STATS + 4 * i, original.stats(i_viejo)["u32"])
        rom.w32(rom.NOMBRES_OFF + 4 * i, texto(nombre))
        rom.w32(rom.DESCS_OFF + 4 * i, texto(original.desc(i_viejo)))
        rom.fijar_contrasena(i, original.contrasena(i_viejo))
        rom.d[rom.PALETAS + 128 * i:rom.PALETAS + 128 * (i + 1)] = original.d[PALETAS + 128 * i_viejo:PALETAS + 128 * (i_viejo + 1)]
        rom.d[ARTE + 6400 * i:ARTE + 6400 * (i + 1)] = original.d[ARTE + 6400 * i_viejo:ARTE + 6400 * (i_viejo + 1)]
        for tabla, vieja, ancho in ((rom.MINI_PALETAS, MINI_PALETAS, 64), (rom.MINI_ARTE, MINI_ARTE, 1024)):
            rom.d[tabla + ancho * i:tabla + ancho * (i + 1)] = original.d[vieja + ancho * i_viejo:vieja + ancho * (i_viejo + 1)]
        informe.append((i, nombre, cid))
    total = N_CARTAS + len(volver)
    rom.w16(rom.CANTIDAD, total)
    # orden alfabetico de todas, con la misma clave que restaurar.py
    clave = lambda t: re.sub(r"[^a-z0-9 ]", "", t.lower())
    viejo_orden = sorted(range(1, N_CARTAS + 1), key=lambda i: rom.u16(rom.ORDEN_ALFA + 2 * i))
    import bisect
    for i, _, _ in informe:
        claves = [clave(rom.nombre(j)) for j in viejo_orden]
        viejo_orden.insert(bisect.bisect_left(claves, clave(rom.nombre(i))), i)
    for puesto, i in enumerate(viejo_orden):
        rom.w16(rom.ORDEN_ALFA + 2 * i, puesto)

    # --- 3. la busqueda ID -> indice, con la cantidad nueva ----------------------------------
    pares = sorted((rom.id_de(i), i) for i in range(1, total + 1))
    assert len({p[0] for p in pares}) == total, "hay IDs repetidos"
    tabla = esp.poner(b"".join(struct.pack("<HH", c, i) for c, i in pares))
    fn = esp.asm_gnu("    .syntax unified\n    .thumb\n    .text\n    .global _start\n_start:\n" + BUSQUEDA
                     + "\n    .balign 4\n    .pool\n", PARES=BASE + tabla, CUENTA=BASE + rom.CANTIDAD)
    parches._salto_largo(rom, parches.FN_INDICE_DE, fn, reg=1)
    for i, nombre, cid in informe:
        assert rom.indice_de(cid) == i and rom.nombre(i) == nombre
    baul(rom, original, esp)
    # --- 7. los sobres: la ultima carta tambien sale, y cada carta vuelve a los suyos ---------
    for o, juego, nuevo_ in SORTEO_ULTIMA:
        assert bytes(rom.d[o:o + 2]) == bytes.fromhex(juego), f"{o:06X}: el sorteo de sobres no es el esperado"
        rom.d[o:o + 2] = bytes.fromhex(nuevo_)
    en_sobres = {}
    for k in range(sobres.N_SOBRES):
        for rareza, ids in sobres.leer(original, k)["listas"].items():
            for cid in ids:
                en_sobres.setdefault(cid, []).append((k, rareza))
    for k_informe, (i, nombre, cid) in enumerate(informe):
        for k, rareza in en_sobres.get(cid, []):
            sobres.cambiar(rom, {"sobre": k, "agregar": {rareza: [cid]}})
        informe[k_informe] = (i, nombre, cid, [f"{sobres.leer(rom, k)['nombre']} ({rareza})" for k, rareza in en_sobres.get(cid, [])])
    return informe, esp.cur


def main(argv):
    cuantas = 1
    if "--cuantas" in argv:
        k = argv.index("--cuantas")
        cuantas = int(argv[k + 1])
        argv = argv[:k] + argv[k + 2:]
    ruta_sobres = None
    if "--sobres" in argv:
        k = argv.index("--sobres")
        ruta_sobres = argv[k + 1]
        argv = argv[:k] + argv[k + 2:]
    if len(argv) != 3:
        raise SystemExit(__doc__)
    original, rom = Rom(argv[0]), Rom(argv[1])
    informe, fin = ampliar(original, rom, cuantas)
    if ruta_sobres:
        import json
        for hecho in sobres.aplicar(rom, json.load(open(ruta_sobres, encoding="utf-8"))["sobres"]):
            print(f"sobre {hecho['sobre']} ({hecho['nombre']}): "
                  + ", ".join(f"{len(v)} {r}" for r, v in hecho["listas"].items() if v))
    open(argv[2], "wb").write(rom.d)
    print(f"{argv[2]}: {rom.n} cartas (capacidad {rom.CAPACIDAD}); tablas nuevas en {AMPLIADO:07X}-{fin:07X}")
    for i, nombre, cid, donde in informe:
        print(f"  indice {i}: {nombre} (ID {cid}), contrasena {rom.contrasena(i)}; sobres: {', '.join(donde) or 'ninguno'}")


if __name__ == "__main__":
    main(sys.argv[1:])
