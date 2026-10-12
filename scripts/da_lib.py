"""Tablas de Yu-Gi-Oh! GX Duel Academy (USA, BYGE).

Todos los offsets son de archivo. Direccion GBA = offset + 0x08000000.
Verificado contra el ROM con MD5 f62c47cbe08e1e3bcfcf9f1b84841a76.
"""
import hashlib
import struct

BASE = 0x08000000
MD5_USA = "f62c47cbe08e1e3bcfcf9f1b84841a76"

N_CARTAS = 1200
CANTIDAD = 0x7A8620        # u16: cantidad de cartas (la lee la busqueda ID -> indice)
IDS = 0x7A8624             # 1201 x u16: indice -> ID de Konami, ORDENADA (busqueda binaria)
CLAVES = 0x7A8F88          # 1201 x u32: claves de contrasena
PALETAS = 0x7AA24C         # 1201 x 128 bytes (64 colores BGR555)
ARTE = 0x7CFACC            # 1201 x 6400 bytes (80x80, 8bpp, en tiles de 8x8)
STATS = 0xF243CC           # 1201 x u32
NOMBRES = 0xF25690         # base de nombres
NOMBRES_OFF = 0xF2A68C     # 1201 x u32, relativos a NOMBRES
DESCS = 0xF2B950           # base de descripciones
DESCS_OFF = 0xF58294       # 1201 x u32, relativos a DESCS
ORDEN_ALFA = 0xF59558      # 1201 x u16: puesto alfabetico (0..1199) de cada indice; [0] = FFFF
# El dibujo chico (32x32) que se ve al abrir un sobre y en las listas con miniaturas: 5 referencias
MINI_PALETAS = 0xF61184    # 1201 x 64 bytes (32 colores BGR555)
MINI_ARTE = 0xF73DC4       # 1201 x 1024 bytes (32x32, 8bpp, en tiles de 8x8; valores 0..31)

# Tabla de efectos por carta: 901 filas de 28 bytes, ORDENADA por ID de Konami.
# La busca FUN_0806162C por busqueda binaria; el indice maximo (900) esta fijo en el codigo.
EFECTOS = 0x17D9BEC
EFECTOS_FILAS = 901
EFECTOS_FILA = 28          # u16 id, u16 0, fn +4, u32 flags +8, fn +0xC, +0x10, +0x14, +0x18
SIN_EFECTO = 0x08061629    # card_effect_handler_no_effect

# Mazos: tabla de 36 entradas de 12 bytes {puntero, cantidad de renglones, 0}.
# Cada renglon del mazo es {u32 ID de Konami, u32 copias}.
MAZOS = 0x17E1294
MAZOS_N = 36

LISTAS_INI = 0x17DFE78     # listas de IDs (fusiones, IA, examenes, sobres) hasta FIN_DATOS
FIN_DATOS = 0x17FD89C      # desde aca hasta el final el ROM es relleno aleatorio
LIBRE = 0x1800000          # donde este proyecto empieza a escribir datos nuevos

# ROM ampliado (scripts/ampliar.py, experimental): las tablas por carta mudadas al espacio libre
# para pasar de 1200. Empieza con MARCA y sigue con un u32 por cada nombre de TABLAS: la capacidad
# y el offset de archivo de cada tabla. Rom lo lee solo: sus metodos sirven para los dos ROMs.
AMPLIADO = 0x1B00000
MARCA = b"DA-AMPLIADO-2\0\0\0"      # la 1 no mudaba los dibujos chicos (MINI_*)
TABLAS = ("CAPACIDAD", "CANTIDAD", "IDS", "CLAVES", "STATS", "NOMBRES", "NOMBRES_OFF", "DESCS",
          "DESCS_OFF", "ORDEN_ALFA", "PALETAS", "ARTE", "MINI_PALETAS", "MINI_ARTE")

# Menus de seleccion del duelo: FUN_08026614 despacha por modo (1..29) con esta
# tabla de direcciones GBA. Las entradas vacias apuntan a MENU_VACIO (movs r0,#0).
MENU_TABLA = 0x26678
MENU_N = 29
MENU_VACIO = 0x08026628

EXAMEN_OFF = 0x1430BE0     # 204 x u32 relativos a EXAMEN (preguntas del examen escrito)
EXAMEN = 0x1430F10
EXAMEN_N = 204

ATRIBUTOS = ["", "LIGHT", "DARK", "WATER", "FIRE", "EARTH", "WIND"]
TIPOS = ["", "Dragon", "Zombie", "Fiend", "Pyro", "Sea Serpent", "Rock", "Machine",
         "Fish", "Dinosaur", "Insect", "Beast", "Beast-Warrior", "Plant", "Aqua",
         "Warrior", "Winged Beast", "Fairy", "Spellcaster", "Thunder", "Reptile",
         "Trap", "Spell"]
CLASES = ["Normal", "Effect", "Fusion", "Ritual"]


class Rom:
    def __init__(self, ruta):
        self.d = bytearray(open(ruta, "rb").read())
        self.md5 = hashlib.md5(self.d).hexdigest()
        self.leer_tablas()

    def leer_tablas(self):
        """Donde esta cada tabla por carta: las direcciones de siempre o las de un ROM ampliado."""
        g = globals()
        for nombre in TABLAS[1:]:
            setattr(self, nombre, g[nombre])
        self.CAPACIDAD = N_CARTAS
        self.ampliado = bytes(self.d[AMPLIADO:AMPLIADO + len(MARCA)]) == MARCA
        assert self.ampliado or bytes(self.d[AMPLIADO:AMPLIADO + 11]) != MARCA[:11], \
            "ROM ampliado con un formato viejo: hay que rearmarlo con scripts/ampliar.py"
        if self.ampliado:
            for k, nombre in enumerate(TABLAS):
                setattr(self, nombre, self.u32(AMPLIADO + len(MARCA) + 4 * k))

    @property
    def n(self):
        """Cantidad de cartas del ROM (1200 salvo en un ROM ampliado)."""
        return self.u16(self.CANTIDAD)

    def u16(self, o): return struct.unpack_from("<H", self.d, o)[0]
    def u32(self, o): return struct.unpack_from("<I", self.d, o)[0]
    def w16(self, o, v): struct.pack_into("<H", self.d, o, v)
    def w32(self, o, v): struct.pack_into("<I", self.d, o, v)

    def cstr(self, o):
        return self.d[o:self.d.index(b"\0", o)].decode("latin1")

    # --- menus de seleccion -----------------------------------------------
    def modo_menu(self, modo):
        assert 1 <= modo <= MENU_N, f"modo de menu fuera de rango: {modo}"
        return self.u32(MENU_TABLA + 4 * (modo - 1))

    def fijar_modo_menu(self, modo, destino):
        """Pone el manejador de un modo vacio. destino: direccion GBA o 'modo:N' (copia el modo N)."""
        if isinstance(destino, str) and destino.startswith("modo:"):
            destino = self.modo_menu(int(destino[5:]))
        elif isinstance(destino, str):
            destino = int(destino, 0)
        assert self.modo_menu(modo) == MENU_VACIO, f"el modo {modo} ya tiene manejador"
        assert 0x08000000 <= destino < 0x08000000 + 0x2000000, f"destino invalido: {destino:#x}"
        self.w32(MENU_TABLA + 4 * (modo - 1), destino)

    # --- cartas -----------------------------------------------------------
    def id_de(self, i): return self.u16(self.IDS + 2 * i)
    def nombre(self, i): return self.cstr(self.NOMBRES + self.u32(self.NOMBRES_OFF + 4 * i))
    def desc(self, i): return self.cstr(self.DESCS + self.u32(self.DESCS_OFF + 4 * i))

    def indice_de(self, cid):
        """ID de Konami -> indice (1..1200) o 0. Busqueda lineal: no depende del orden."""
        for i in range(1, self.n + 1):
            if self.id_de(i) == cid:
                return i
        return 0

    def stats(self, i):
        v = self.u32(self.STATS + 4 * i)
        return {"def": (v & 0x1FF) * 10, "atk": ((v >> 9) & 0x1FF) * 10,
                "clase": (v >> 18) & 3, "sub17": (v >> 17) & 1, "tipo": (v >> 20) & 0x1F,
                "nivel": (v >> 25) & 0xF, "atributo": v >> 29, "u32": v}

    @staticmethod
    def empaquetar_monstruo(atk, de, nivel, atributo, tipo, clase):
        return ((atributo & 7) << 29 | (nivel & 0xF) << 25 | (tipo & 0x1F) << 20 |
                (clase & 3) << 18 | ((atk // 10) & 0x1FF) << 9 | ((de // 10) & 0x1FF))

    # --- efectos ----------------------------------------------------------
    def fila_efecto(self, k):
        o = EFECTOS + EFECTOS_FILA * k
        return {"id": self.u16(o), "fn_04": self.u32(o + 4), "flags": self.u32(o + 8),
                "fn_c": self.u32(o + 0xC), "fn_10": self.u32(o + 0x10),
                "fn_14": self.u32(o + 0x14), "fn_18": self.u32(o + 0x18)}

    def efectos(self):
        return [self.fila_efecto(k) for k in range(EFECTOS_FILAS)]

    # --- mazos ------------------------------------------------------------
    def mazos(self):
        out = {}
        for k in range(MAZOS_N):
            p, n = self.u32(MAZOS + 12 * k), self.u32(MAZOS + 12 * k + 4)
            if p:
                o = p - BASE
                out[k] = [(o + 8 * j, self.u32(o + 8 * j), self.u32(o + 8 * j + 4)) for j in range(n)]
        return out

    def renglones_u32(self):
        """Offsets de todos los renglones {u32 ID, u32 copias} de la zona de datos.

        Incluye los mazos de los rivales y los mazos iniciales del jugador
        (0x17F3D44 en adelante). Se detectan por forma: corridas de 5 o mas
        renglones con ID valido y 1 a 3 copias.
        """
        validos = {self.id_de(i) for i in range(1, self.n + 1)}
        out, o = [], LISTAS_INI & ~3
        while o < FIN_DATOS - 8:
            if self.u32(o) in validos and 1 <= self.u32(o + 4) <= 3:
                a = o
                while o < FIN_DATOS - 8 and self.u32(o) in validos and 1 <= self.u32(o + 4) <= 3:
                    o += 8
                if (o - a) // 8 >= 5:
                    out += list(range(a, o, 8))
            else:
                o += 4
        return out

    # --- contrasenas ------------------------------------------------------
    @staticmethod
    def _relleno(i):
        return (((i * 0x343FD + 0x269EC3) >> 16) | 0x9EC30000) & 0xFFFFFFFF

    def contrasena(self, i):
        h = self.u32(self.CLAVES + 4 * i) ^ self._relleno(i)
        return "".join("%X" % ((h >> (4 * k)) & 0xF) for k in range(7, -1, -1))

    def fijar_contrasena(self, i, digitos):
        h = 0
        for c in digitos:
            h = (h << 4) | int(c)
        self.w32(self.CLAVES + 4 * i, h ^ self._relleno(i))
