"""Emulador de GBA sin ventana, manejado desde Python (nucleo libretro de mGBA).

Sirve para probar un ROM por script: apretar botones, sacar capturas, leer y
escribir la RAM, guardar y cargar estados.

Requiere el nucleo mgba_libretro (en Ubuntu: apt install libretro-mgba) y
Pillow para las capturas.

    from gba import GBA
    g = GBA("rom.gba")
    g.correr(600)                 # 10 segundos
    g.apretar("A")                # pulsa y suelta
    g.captura("pantalla.png")
    g.r16(0x02000004); g.w8(0x02000004, 0x08)
"""
import ctypes as C
import os
import struct

_AQUI = os.path.dirname(os.path.abspath(__file__))
NUCLEOS = [os.path.join(_AQUI, "..", "nucleos", "mgba_libretro.dylib"),     # macOS (nucleos/)
           os.path.join(_AQUI, "..", "nucleos", "mgba_libretro.so"),
           "/usr/lib/x86_64-linux-gnu/libretro/mgba_libretro.so",
           "/usr/lib/libretro/mgba_libretro.so",
           os.path.expanduser("~/.config/retroarch/cores/mgba_libretro.so")]
BOTONES = {"B": 0, "SELECT": 2, "START": 3, "UP": 4, "DOWN": 5, "LEFT": 6,
           "RIGHT": 7, "A": 8, "L": 10, "R": 11}


class _GameInfo(C.Structure):
    _fields_ = [("path", C.c_char_p), ("data", C.c_void_p), ("size", C.c_size_t), ("meta", C.c_char_p)]


class _MemDesc(C.Structure):
    _fields_ = [("flags", C.c_uint64), ("ptr", C.c_void_p), ("offset", C.c_size_t), ("start", C.c_size_t),
                ("select", C.c_size_t), ("disconnect", C.c_size_t), ("len", C.c_size_t), ("addrspace", C.c_char_p)]


class _MemMap(C.Structure):
    _fields_ = [("descriptors", C.POINTER(_MemDesc)), ("num", C.c_uint)]


ENV = C.CFUNCTYPE(C.c_bool, C.c_uint, C.c_void_p)
VIDEO = C.CFUNCTYPE(None, C.c_void_p, C.c_uint, C.c_uint, C.c_size_t)
AUDIO1 = C.CFUNCTYPE(None, C.c_int16, C.c_int16)
AUDION = C.CFUNCTYPE(C.c_size_t, C.c_void_p, C.c_size_t)
POLL = C.CFUNCTYPE(None)
STATE = C.CFUNCTYPE(C.c_int16, C.c_uint, C.c_uint, C.c_uint, C.c_uint)


class GBA:
    _abierto = None           # el nucleo es uno solo por proceso: abrir otro GBA cierra el anterior

    def __init__(self, rom, nucleo=None, dir_guardado=None):
        if GBA._abierto is not None:
            GBA._abierto.cerrar()
        GBA._abierto = self
        nucleo = nucleo or next(p for p in NUCLEOS if os.path.exists(p))
        self.lib = C.CDLL(nucleo)
        self.botones = 0
        self.formato = 0          # 0 = 0RGB1555, 1 = XRGB8888, 2 = RGB565
        self.cuadro = None
        self.regiones = []
        self._dir = (dir_guardado or "/tmp").encode()
        self._dirbuf = C.create_string_buffer(self._dir)

        def env(cmd, data):
            cmd &= 0xFFFF
            if cmd == 3:      # GET_CAN_DUPE
                C.cast(data, C.POINTER(C.c_bool))[0] = True
                return True
            if cmd == 10:     # SET_PIXEL_FORMAT
                self.formato = C.cast(data, C.POINTER(C.c_int))[0]
                return True
            if cmd in (9, 31):  # SYSTEM / SAVE DIRECTORY
                C.cast(data, C.POINTER(C.c_char_p))[0] = C.cast(self._dirbuf, C.c_char_p)
                return True
            if cmd == 36:     # SET_MEMORY_MAPS
                mm = C.cast(data, C.POINTER(_MemMap))[0]
                for i in range(mm.num):
                    d = mm.descriptors[i]
                    if d.ptr:
                        self.regiones.append((d.start, d.len, d.ptr + d.offset))
                return True
            return False

        def video(data, w, h, pitch):
            if data:
                self.cuadro = (C.string_at(data, pitch * h), w, h, pitch)

        def state(port, device, index, ident):
            if port == 0 and device == 1:
                if ident == 256:          # mascara completa
                    return self.botones
                return (self.botones >> ident) & 1
            return 0

        self._cbs = (ENV(env), VIDEO(video), AUDIO1(lambda l, r: None),
                     AUDION(lambda d, n: n), POLL(lambda: None), STATE(state))
        L = self.lib
        L.retro_set_environment(self._cbs[0])
        L.retro_set_video_refresh(self._cbs[1])
        L.retro_set_audio_sample(self._cbs[2])
        L.retro_set_audio_sample_batch(self._cbs[3])
        L.retro_set_input_poll(self._cbs[4])
        L.retro_set_input_state(self._cbs[5])
        L.retro_init()
        self._rom = open(rom, "rb").read()
        self._rombuf = C.create_string_buffer(self._rom, len(self._rom))
        info = _GameInfo(os.path.abspath(rom).encode(), C.cast(self._rombuf, C.c_void_p), len(self._rom), None)
        L.retro_load_game.argtypes = [C.POINTER(_GameInfo)]
        L.retro_load_game.restype = C.c_bool
        assert L.retro_load_game(C.byref(info)), "el nucleo no pudo cargar el ROM"
        L.retro_get_memory_data.restype = C.c_void_p
        L.retro_get_memory_data.argtypes = [C.c_uint]
        L.retro_get_memory_size.restype = C.c_size_t
        L.retro_get_memory_size.argtypes = [C.c_uint]
        L.retro_serialize_size.restype = C.c_size_t
        L.retro_serialize.argtypes = [C.c_void_p, C.c_size_t]
        L.retro_serialize.restype = C.c_bool
        L.retro_unserialize.argtypes = [C.c_void_p, C.c_size_t]
        L.retro_unserialize.restype = C.c_bool
        self.frames = 0

    def cerrar(self):
        """Descarga el ROM y suelta sus copias (unos 75 MB por instancia). Sin esto no se liberaban
        nunca, y un proceso que abre un GBA por paso (repetir_sesion.py, 810 pasos) llegaba a
        decenas de gigas. Lo llama solo el GBA siguiente; despues de cerrado no se puede usar."""
        if self._cbs is None:
            return
        if GBA._abierto is self:
            GBA._abierto = None
        self.lib.retro_unload_game()
        self.lib.retro_deinit()
        self._cbs = self._rom = self._rombuf = self.cuadro = None    # _cbs cierra el ciclo con self
        self.regiones = []

    # --- ejecucion ----------------------------------------------------------
    def correr(self, n=1, *botones):
        self.botones = sum(1 << BOTONES[b] for b in botones)
        for _ in range(n):
            self.lib.retro_run()
        self.frames += n
        self.botones = 0

    def apretar(self, boton, mantener=4, soltar=12):
        self.correr(mantener, boton)
        self.correr(soltar)

    def secuencia(self, texto, soltar=12):
        """'A A DOWN START' -> pulsa cada boton en orden."""
        for b in texto.split():
            self.apretar(b, soltar=soltar)

    # --- memoria ------------------------------------------------------------
    def _ptr(self, addr, n):
        for start, largo, ptr in self.regiones:
            if start <= addr and addr + n <= start + largo:
                return ptr + (addr - start)
        if 0x02000000 <= addr < 0x02040000:
            base = self.lib.retro_get_memory_data(2)
            if base:
                return base + (addr - 0x02000000)
        raise ValueError(f"direccion fuera de las regiones expuestas: {addr:08X}")

    def leer(self, addr, n): return C.string_at(self._ptr(addr, n), n)
    def escribir(self, addr, datos): C.memmove(self._ptr(addr, len(datos)), datos, len(datos))
    def r8(self, a): return self.leer(a, 1)[0]
    def r16(self, a): return struct.unpack("<H", self.leer(a, 2))[0]
    def r32(self, a): return struct.unpack("<I", self.leer(a, 4))[0]
    def w8(self, a, v): self.escribir(a, bytes([v & 0xFF]))
    def w16(self, a, v): self.escribir(a, struct.pack("<H", v & 0xFFFF))
    def w32(self, a, v): self.escribir(a, struct.pack("<I", v & 0xFFFFFFFF))

    # --- estados ------------------------------------------------------------
    def guardar_estado(self, ruta=None):
        n = self.lib.retro_serialize_size()
        buf = C.create_string_buffer(n)
        assert self.lib.retro_serialize(buf, n)
        if ruta:
            open(ruta, "wb").write(buf.raw)
        return buf.raw

    def cargar_estado(self, datos):
        if isinstance(datos, str):
            datos = open(datos, "rb").read()
        buf = C.create_string_buffer(datos, len(datos))
        assert self.lib.retro_unserialize(buf, len(datos))

    # --- video --------------------------------------------------------------
    def imagen(self, escala=2):
        from PIL import Image
        datos, w, h, pitch = self.cuadro
        if self.formato == 1:
            img = Image.frombuffer("RGBA", (w, h), datos, "raw", "BGRA", pitch, 1).convert("RGB")
        else:
            modo = "BGR;16" if self.formato == 2 else "BGR;15"
            img = Image.frombuffer("RGB", (w, h), datos, "raw", modo, pitch, 1)
        return img.resize((w * escala, h * escala), Image.NEAREST) if escala != 1 else img

    def captura(self, ruta, escala=2):
        self.imagen(escala).save(ruta)
        return ruta
