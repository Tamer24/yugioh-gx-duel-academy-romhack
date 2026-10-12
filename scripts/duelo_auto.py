"""Ayudas para probar cartas en un duelo real, sin ventana (experimental).

Maneja el juego con gba.py: arranca una partida, carga un mazo de prueba en la
RAM, entra a un duelo y permite mover el cursor, elegir opciones de menu y
leer el estado del duelo (mano, campo, cementerio, puntos de vida).

Ejemplo:

    from duelo_auto import *
    d = Duelo("ROM.gba")                     # usa estados/sabado-cuarto.st si existe
    d.preparar([520] * 20 + [968] * 20)      # 40 indices de carta
    d.entrar_duelo()                         # el rival y el lugar cambian segun el dia
    d.estado()
    d.ir_mano("Jowls of Dark Demise"); d.menu(1)     # 1 = segunda opcion (Set)
    d.fin_turno(primero=True); d.pasar_rival()

Las secuencias de botones estan medidas para este juego y pueden desfasarse:
conviene sacar una captura (d.foto) cuando algo no da lo esperado.
"""
import os

from PIL import Image

from da_lib import Rom
from gba import GBA

BAUL = 0x02000000            # 12 bytes por carta, indice - 1
MAZO = 0x02003858            # mazo activo: indices u16
J0 = 0x02022250              # duelo, jugador; el rival esta 0x2B08 mas adelante
J1 = J0 + 0x2B08
CURSOR = 0x02028188          # x, y, indice en la mano. y: 0 mano, 1 M/T, 2 monstruos, 3 y 4 rival
EVENTO = 0x0202048C          # ultima solicitud de respuesta: bits 13-18 = tipo (0x10 = ataque declarado)
LISTA_ZONAS = J0 + 0x5610    # 11 bytes por lado: 5 zonas de monstruo, 5 de magia/trampa, 1 de campo
ZONAS = {"0": "campo", "5": "magia/trampa", "a": "campo (magia)", "b": "fusion",
         "c": "mazo", "d": "cementerio", "e": "retirada", "f": "mano"}

# Botones desde el encendido hasta el menu del cuarto, sabado 7 de octubre.
NUEVA_PARTIDA = [
    "w900 START w120 " + "A w120 " * 7 + "w30",
    "A w90 A w60 START w60 A w60 A w90 A w90 A w90 A w90 w30",
    "A*6 w60 " * 12 + "w30",
    "A*22 w60 A w60 A w60 A w60 B w90 B w90 B w90 w90",
    "A w60 A w60 RIGHT w30 A w90 A w90 A w90 A w90 " + "RIGHT w30 " * 7 + "w30",
    "LEFT w30 A w120 A w120 A w90 " + "A*8 w60 " * 11 + "w30",
    "A w60 " * 11 + "w30", "A*5 w60 " * 11 + "w30", "A w70 " * 11 + "w30", "A w70 " * 8 + "w30",
    "w120 A w90 A w90 A w90 A w90 RIGHT w40 RIGHT w40 RIGHT w40 w30",
]


class Duelo:
    def __init__(self, ruta_rom, estado=None, dir_guardado=None):
        import tempfile
        self.rom = Rom(ruta_rom)
        # los guardados del nucleo van a una carpeta temporal para no tocar build/
        self.g = GBA(ruta_rom, dir_guardado=dir_guardado or tempfile.mkdtemp(prefix="da_"))
        aqui = os.path.dirname(os.path.abspath(__file__))
        estado = estado or os.path.join(aqui, "..", "estados", "sabado-cuarto.st")
        if os.path.exists(estado):
            self.g.correr(2)
            self.g.cargar_estado(estado)
            self.g.correr(1)
        else:
            for tramo in NUEVA_PARTIDA:
                self.seq(tramo)

    # --- botones ------------------------------------------------------------
    def seq(self, texto):
        """'A w60 DOWN*3': botones, esperas en cuadros (wN) y repeticiones (*N)."""
        for t in texto.split():
            if t[0] == "w" and t[1:].isdigit():
                self.g.correr(int(t[1:]))
                continue
            boton, _, veces = t.partition("*")
            for _ in range(int(veces or 1)):
                self.g.apretar(boton, mantener=4, soltar=20)

    def tecla(self, boton, espera=22):
        self.g.apretar(boton, mantener=4, soltar=espera)

    def foto(self, ruta, escala=2):
        self.g.correr(2)
        self.g.imagen(escala).save(ruta)

    # --- preparacion --------------------------------------------------------
    def preparar(self, mazo):
        """Carga 40 indices en el mazo activo y pone esas cartas en el baul."""
        assert len(mazo) == 40
        for k, c in enumerate(mazo):
            self.g.w16(MAZO + 2 * k, c)
        for c in set(mazo):
            a = BAUL + 12 * (c - 1)
            self.g.w16(a + 4, (16 << 3) | 2)
            self.g.w32(a + 8, 0xFFFFFFFF)

    def entrar_duelo(self, lugar=0):
        """Duerme, va a Duel Academy y entra al lugar 'lugar' de la lista (0 = Front of School)."""
        self.seq("LEFT w40 A w200 A w120 RIGHT w60 RIGHT w60 A w100")
        self.seq("DOWN w50 " * lugar + "A w200 A w90 A w90 A w90 A w90 A w90 A w90 A w120 A w120 A w120 A w120 w220 A w80 w80")

    # --- lectura del duelo --------------------------------------------------
    def cartas(self):
        """(jugador, ranura, indice, nombre, zona, estado) de cada carta del duelo."""
        out = []
        for p, base in ((0, J0), (1, J1)):
            for s in range(100):
                a = base + s * 0x50
                o = self.g.r16(a + 0x24) & 0x7FFF
                if 0 < o <= self.rom.n:
                    z = "%x" % (self.g.r8(a + 0x31) >> 4)
                    out.append((p, s, o, self.rom.nombre(o), z, self.g.r8(a + 0x33)))
        return out

    def zona(self, jugador, zonas):
        return [(s, n) for p, s, o, n, z, e in self.cartas() if p == jugador and z in zonas]

    def mano(self, jugador=0):
        return self.zona(jugador, "f")

    def lp(self):
        return self.g.r16(J0), self.g.r16(J1)

    def cursor(self):
        return self.g.r8(CURSOR), self.g.r8(CURSOR + 1), self.g.r8(CURSOR + 2)

    def estado(self):
        for p, quien in ((0, "yo"), (1, "rival")):
            print(f"  {quien}: mano {[n for s, n in self.mano(p)]}")
            print(f"      campo {[n for s, n in self.zona(p, '05a')]} | cementerio {[n for s, n in self.zona(p, 'd')]}"
                  f" | retiradas {[n for s, n in self.zona(p, 'e')]}")
        print("  LP", self.lp(), "| cursor", self.cursor())

    # --- acciones -----------------------------------------------------------
    def mover(self, x=None, y=None):
        for _ in range(14):
            cx, cy, _i = self.cursor()
            if y is not None and cy != y:
                self.tecla("UP" if cy < y else "DOWN")
            elif x is not None and cx != x:
                self.tecla("RIGHT" if cx < x else "LEFT")
            else:
                return True
        return False

    def ir_mano(self, nombre):
        """Cursor sobre una carta de la mano. No funciona con un menu abierto."""
        m = dict(self.mano())
        lista = list(self.g.leer(J0 + 0x2824, len(m)))      # ranuras en el orden de la mano
        destino = [i for i, s in enumerate(lista) if m.get(s) == nombre]
        assert destino, f"{nombre} no esta en la mano"
        self.mover(y=0)
        for _ in range(12):
            x, y, i = self.cursor()
            if y == 0 and i == destino[0]:        # en la fila de la mano y sobre la carta
                return lista[destino[0]]
            if y != 0:
                self.mover(y=0)
            else:
                self.tecla("RIGHT")
        raise RuntimeError("no llegue a la carta; puede haber un menu abierto")

    def menu(self, k, espera=100):
        """Abre el menu de la carta bajo el cursor y elige la opcion k (0 = la de arriba)."""
        self.tecla("A", 50)
        for _ in range(k + 1):
            self.tecla("DOWN", 28)
        self.tecla("A", espera)
        self.g.correr(40)

    def fin_turno(self, primero=False):
        """primero=True en el primer turno del duelo, que no tiene Battle Phase."""
        self.tecla("B", 50)
        if not primero:
            self.tecla("DOWN", 30)
        self.tecla("A", 120)

    def pasar_rival(self, maximo=70):
        """Avanza el turno rival contestando No a las preguntas, hasta robar carta."""
        n = len(self.mano())
        for i in range(maximo):
            self.tecla("DOWN", 16)
            self.tecla("A", 70)
            if len(self.mano()) > n:
                self.g.correr(150)
                return i
        return -1

    # --- respuesta del jugador a una accion del rival (trampas) ------------------------
    def tipo_evento(self):
        """Tipo de la ultima solicitud de respuesta del motor (0x10 = ataque declarado)."""
        return (self.g.r32(EVENTO) >> 13) & 0x3F

    def zona_magia(self, ranura):
        """Posicion (0..4) de una ranura en la fila de magias/trampas propia, o None."""
        for z in range(5):
            if self.g.r8(LISTA_ZONAS + 5 + z) == ranura:
                return z
        return None

    def esperar_evento(self, tipo, maximo=6000, a_cada=90):
        """Avanza el turno del rival (pulsa A cada 'a_cada' cuadros para pasar los dialogos)
        hasta que el motor pida respuesta al evento 'tipo'. Devuelve True si llego."""
        for i in range(maximo // 2):
            self.g.correr(2)
            if self.tipo_evento() == tipo:
                return True
            if i % (a_cada // 2) == a_cada // 2 - 1:
                self.tecla("A", 10)
        return False

    def responder_con_trampa(self, ranura, opcion_activar=1):
        """Contesta "Activate the effect...?" con Yes, elige la carta de la fila de magias/trampas
        y abre su menu. 'opcion_activar' = cuantas veces subir hasta Activate Effect.

        Medido con Mirror Force: el aviso aparece unos 100 cuadros despues del evento y espera
        sin limite; tras Yes viene "Select Spell/Trap Card to activate." (A) y el cursor arranca
        sobre el atacante: DOWN, DOWN lleva al borde derecho de mi fila y de ahi hay que ir a
        la zona con LEFT (zona 0 = cuatro LEFT)."""
        z = self.zona_magia(ranura)
        assert z is not None, f"la ranura {ranura} no esta en la fila de magias/trampas"
        self.g.correr(120)
        self.tecla("A", 60)                 # Yes
        self.tecla("A", 60)                 # cierra el aviso de seleccion
        self.tecla("DOWN", 30)
        self.tecla("DOWN", 30)
        for _ in range(4 - z):
            self.tecla("LEFT", 30)
        self.tecla("A", 60)                 # menu de la carta
        for _ in range(opcion_activar):
            self.tecla("UP", 25)
        self.tecla("A", 80)

