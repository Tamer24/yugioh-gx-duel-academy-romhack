"""Pruebas en duelo de las cartas del lote que no tenian veredicto (sin ventana).

Cada caso arma su escenario con escenario.py, comprueba que quedo como se pidio, provoca el
disparador de la carta y compara el duelo antes y despues con lo que dice el texto.

Resultado de una corrida:
  PREPARACION INVALIDA      el escenario no quedo armado como se pidio: no hay veredicto
  NO SE DIO EL DISPARADOR   el juego nunca llego al momento en que la carta actua
  FUNCIONA / FUNCIONA EN PARTE / NO FUNCIONA
Resultado de una carta: el de sus corridas si todas coinciden; si no, INESTABLE.

Uso (desde la raiz del proyecto):
  python3 scripts/probar_lote.py ROM [CARTA ...] [--corridas 3] [--fotos CARPETA] [--registrar]
  python3 scripts/probar_lote.py --listar

--registrar escribe el veredicto en datos/pruebas.csv solo si todas las corridas coinciden
en un veredicto. Sin esa opcion no escribe nada fuera de estados/lote/.
"""
import datetime
import os
import sys

import escenario
import registro
from da_lib import Rom
from duelo_auto import Duelo, J0, J1, LISTA_ZONAS

RAIZ = registro.RAIZ
BASE = os.path.join(RAIZ, "estados", "duelo-inicio.ss1")
LOTE = os.path.join("estados", "lote")
INVALIDA, SIN_DISPARO = "PREPARACION INVALIDA", "NO SE DIO EL DISPARADOR"
FUNCIONA, EN_PARTE, NO_FUNCIONA = "FUNCIONA", "FUNCIONA EN PARTE", "NO FUNCIONA"
VEREDICTOS = {FUNCIONA: "funciona", EN_PARTE: "funciona en parte", NO_FUNCIONA: "no funciona"}
# Carta que el rival no puede jugar (nivel 8, sin tributos): rellena su mano y su mazo para
# que el turno del rival sea corto y siempre igual.
MUERTA = "Blue-Eyes White Dragon"
REINTENTOS = 3              # por corrida, solo cuando el disparador no se dio


def res(resultado, detalle="", falla="", **extra):
    return dict(resultado=resultado, detalle=detalle, falla=falla, **extra)


# --- ayudas comunes ---------------------------------------------------------------------
def armar(rom, nombre, **cambios):
    """Estado del caso en estados/lote/NOMBRE.st (se reescribe igual en cada corrida)."""
    os.makedirs(os.path.join(RAIZ, LOTE), exist_ok=True)
    relativa = os.path.join(LOTE, nombre + ".st")
    escenario.armar(rom, BASE, os.path.join(RAIZ, relativa), **cambios)
    return relativa


def abrir(ruta_rom, estado, desfase):
    """'desfase' cambia cuantos cuadros pasan antes de la primera tecla: cada corrida es distinta."""
    d = Duelo(ruta_rom, estado=os.path.join(RAIZ, estado))
    d.g.correr(30 + 11 * desfase)
    return d


def ranura_de(d, lado, carta):
    """Direccion de la ranura de una carta por nombre (la primera del lado)."""
    base = J1 if lado else J0
    for p, s, o, n, z, e in d.cartas():
        if p == lado and n == carta:
            return base + s * 0x50
    return None


def colocar_monstruo(d, carta):
    """Set (boca abajo en defensa) desde la mano. Devuelve la direccion de su ranura."""
    d.ir_mano(carta)
    d.menu(1)
    d.g.correr(60)
    return ranura_de(d, 0, carta)


def fingir_nivel(d, carta, nivel):
    """Ayuda de prueba: cambia el nivel de una carta de mi mano (nibble bajo de ranura+0x31)."""
    a = ranura_de(d, 0, carta)
    d.g.w8(a + 0x31, (d.g.r8(a + 0x31) & 0xF0) | nivel)


def esperar(d, condicion, maximo=6000, tecla_cada=90):
    """Avanza pulsando A cada 'tecla_cada' cuadros (0 = sin teclas) hasta que se cumpla."""
    for t in range(maximo // 6):
        d.g.correr(6)
        if condicion():
            return True
        if tecla_cada and t % (tecla_cada // 6) == tecla_cada // 6 - 1:
            d.tecla("A", 4)
    return False


def hasta_mi_turno(d, maximo=9000, n=None):
    """Deja jugar al rival (A cada 60 cuadros) hasta que robo carta. True si llego.
    'n' = cartas en mi mano antes de empezar a esperar, cuando se midio antes (por si el turno del
    rival termina mientras el caso todavia esta pulsando teclas)."""
    if n is None:
        n = len(d.mano())
    ok = len(d.mano()) > n or esperar(d, lambda: len(d.mano()) > n, maximo, tecla_cada=60)
    d.g.correr(120)
    return ok


def fijando(d, cuadros, direccion, valor, *botones):
    """Corre 'cuadros' cuadros reescribiendo un u32 en cada uno (ayuda de prueba)."""
    for _ in range(cuadros):
        d.g.w32(direccion, valor)
        d.g.correr(1, *botones)


def esperar_volteo(d, a, turnos=3):
    """Tras terminar mi turno: espera a que el rival ataque al monstruo boca abajo de la ranura 'a'.
    Si el rival pasa sin atacar, termina mi turno siguiente y vuelve a esperar ('turnos' veces)."""
    for _ in range(turnos):
        n = len(d.mano())
        if not esperar(d, lambda: d.g.r8(a + 0x33) == 0x30 or len(d.mano()) > n, 6000):
            return False
        if d.g.r8(a + 0x33) == 0x30:
            return True
        d.g.correr(120)
        d.fin_turno(primero=False)
    return False


def controla(d, lado):
    """Nombres de los monstruos que controla un lado (listas de zonas)."""
    return [m[0] for m in escenario.instantanea(d)["campo_yo" if lado == 0 else "campo_rival"]]


def foto(d, fotos, nombre):
    if fotos:
        os.makedirs(fotos, exist_ok=True)
        d.foto(os.path.join(fotos, nombre + ".png"), escala=1)


# --- casos ------------------------------------------------------------------------------
def caso_bagworm(ruta_rom, desfase, fotos):
    carta, maquina = "Electromagnetic Bagworm", "Mechanicalchaser"
    estado = armar(ruta_rom, "bagworm", yo={1: carta},
                   rival={0: maquina, 1: MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                   mazo_rival={0: MUERTA, 1: MUERTA, 2: MUERTA})
    d = abrir(ruta_rom, estado, desfase)
    a = colocar_monstruo(d, carta)
    faltas = escenario.comprobar(d, {"campo_yo": [carta], "mano_rival": [maquina]})
    if faltas:
        return res(INVALIDA, "; ".join(faltas), estado=estado)
    d.fin_turno(primero=True)
    if not esperar_volteo(d, a):
        return res(SIN_DISPARO, "el rival no ataco al monstruo boca abajo", estado=estado)
    if maquina not in controla(d, 1):
        return res(INVALIDA, f"al voltearse, el rival no controla a {maquina}", estado=estado)
    # Antes del aviso se resuelve el -500 a la Maquina que destruyo a Bagworm. El aviso "Select
    # opponent's Machine monster to gain control of." espera sin limite: se lo espera sin teclas
    # (contador de pasos de la seleccion, bits 10-17 de 0x020204C0).
    if not esperar(d, lambda: (d.g.r32(0x020204C0) >> 10) & 0xFF, 1500, tecla_cada=0):
        return res(SIN_DISPARO, "no aparecio el aviso de seleccion de la Maquina", estado=estado)
    d.g.correr(30)
    antes_del_control = next((m[2], m[3]) for m in escenario.instantanea(d)["campo_rival"] if m[0] == maquina)
    foto(d, fotos, "bagworm_aviso")
    en_mano = len(d.mano())
    for _ in range(3):                    # cierra el aviso, elige la Maquina, confirma
        d.tecla("A", 70)
    d.g.correr(120)
    s = escenario.instantanea(d)
    foto(d, fotos, "bagworm_control")
    if maquina not in controla(d, 0):
        return res(NO_FUNCIONA, "al voltearse no toma el control de la Maquina",
                   "no toma el control de la Maquina atacante", estado=estado)
    destruida = carta in s["cementerio_yo"]
    atk, df = next((m[2], m[3]) for m in s["campo_yo"] if m[0] == maquina)
    if not hasta_mi_turno(d, n=en_mano):
        return res(SIN_DISPARO, "no volvio mi turno despues del volteo", estado=estado)
    en_mi_turno = maquina in controla(d, 0)
    d.fin_turno(primero=False)
    hasta_mi_turno(d)
    devuelta = maquina in controla(d, 1) or maquina not in controla(d, 0)
    detalle = (f"Boca abajo, atacada por {maquina} (1850/800): pide elegir una Maquina rival y pasa a mi campo. "
               f"Durante mi turno siguiente {'sigue' if en_mi_turno else 'ya no esta'} bajo mi control y al "
               f"terminarlo {'vuelve al rival' if devuelta else 'no vuelve: sigue siendo mia en el turno rival y en mi turno posterior'}. "
               + (f"La batalla se resuelve igual y Bagworm va al cementerio; la Maquina que la destruyo queda en "
                  f"{atk}/{df} (ya estaba en {antes_del_control[0]}/{antes_del_control[1]} al pedir la eleccion)."
                  if destruida else "Bagworm sobrevive a la batalla."))
    fallas = []
    if not en_mi_turno or not devuelta:
        fallas.append("el control no termina al final de mi turno siguiente: la Maquina sigue en mi campo"
                      if en_mi_turno else "el control se pierde antes de mi turno siguiente")
    if destruida and (atk, df) != (1350, 300):
        fallas.append(f"la Maquina que la destruye en batalla no pierde 500 ATK y DEF (queda en {atk}/{df})")
    return res(EN_PARTE if fallas else FUNCIONA, detalle, "; ".join(fallas), estado=estado)


def _dark_eyes(ruta_rom, desfase, fotos, borrar_bloqueo):
    """Una pasada: devuelve (resultado parcial o None, LP propio antes, LP despues, sigue en el campo)."""
    carta, atacante = "Dark-Eyes Illusionist", "Mechanicalchaser"
    estado = armar(ruta_rom, "dark-eyes", yo={1: carta},
                   rival={0: atacante, 1: MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                   mazo_rival={0: MUERTA, 1: MUERTA, 2: MUERTA})
    d = abrir(ruta_rom, estado, desfase)
    a = colocar_monstruo(d, carta)
    faltas = escenario.comprobar(d, {"campo_yo": [carta], "mano_rival": [atacante]})
    if faltas:
        return res(INVALIDA, "; ".join(faltas), estado=estado), None
    d.fin_turno(primero=True)
    if not esperar_volteo(d, a):
        return res(SIN_DISPARO, "el rival no ataco al monstruo boca abajo", estado=estado), None
    # Ayuda de prueba: el atacante (1850) destruiria a Dark-Eyes (DEF 1400) y el bloqueo no se podria
    # observar. Antes de que se calcule el danio se le baja el ATK a 1000 en memoria; el motor
    # restaura el valor real al cambiar de turno.
    t = ranura_de(d, 1, atacante)
    fijando(d, 450, t + 0x28, 1000)       # aviso de seleccion del objetivo
    foto(d, fotos, "dark-eyes_aviso")
    for _ in range(3):
        fijando(d, 4, t + 0x28, 1000, "A")
        fijando(d, 70, t + 0x28, 1000)
    fijando(d, 120, t + 0x28, 1000)
    if carta not in controla(d, 0) or atacante not in controla(d, 1):
        return res(INVALIDA, "tras el volteo no quedaron los dos monstruos en el campo", estado=estado), None
    marcado = d.g.r8(t + 0x3E) & 0xF      # entradas en la lista de modificadores del objetivo
    if not hasta_mi_turno(d):
        return res(SIN_DISPARO, "no volvio mi turno despues del volteo", estado=estado), None
    # Para que la IA quiera atacar: Dark-Eyes pasa a posicion de ataque (ATK 0) escribiendo en memoria.
    d.g.w8(a + 0x33, 0x10)
    if borrar_bloqueo:                    # pasada de control: se quita el modificador del objetivo
        d.g.w8(t + 0x3E, d.g.r8(t + 0x3E) & 0xF0)
        d.g.w16(t + 0x40, 0)
    lp = d.lp()[0]
    d.fin_turno(primero=False)
    hasta_mi_turno(d)
    foto(d, fotos, "dark-eyes_" + ("control" if borrar_bloqueo else "bloqueo"))
    return None, dict(marcado=marcado, lp_antes=lp, lp_despues=d.lp()[0], sigue=carta in controla(d, 0),
                      estado=estado)


def caso_dark_eyes(ruta_rom, desfase, fotos):
    error, con = _dark_eyes(ruta_rom, desfase, fotos, borrar_bloqueo=False)
    if error:
        return error
    error, sin = _dark_eyes(ruta_rom, desfase, fotos, borrar_bloqueo=True)
    if error:
        return error
    estado = con["estado"]
    if sin["lp_despues"] == sin["lp_antes"]:
        return res(SIN_DISPARO, "en la pasada de control (sin bloqueo) la IA tampoco ataco: no se puede "
                   "distinguir el bloqueo", estado=estado)
    detalle = (f"Al voltearse (atacada por Mechanicalchaser) pide un objetivo y se elige al atacante. En el turno "
               f"rival siguiente, con Dark-Eyes en ataque (ATK 0) y Mechanicalchaser con 1850: "
               f"{'no la ataca' if con['lp_despues'] == con['lp_antes'] else 'la ataca'} "
               f"(LP {con['lp_antes']} a {con['lp_despues']}). Pasada de control con el bloqueo borrado: "
               f"ataca (LP {sin['lp_antes']} a {sin['lp_despues']}). Ayudas de prueba: ATK del atacante bajado "
               f"en memoria durante el volteo para que Dark-Eyes sobreviva, y posicion de Dark-Eyes escrita en memoria.")
    if con["lp_despues"] == con["lp_antes"] and con["sigue"]:
        return res(FUNCIONA, detalle, estado=estado)
    return res(NO_FUNCIONA, detalle, "el objetivo ataca igual mientras Dark-Eyes sigue boca arriba", estado=estado)


def caso_reaper(ruta_rom, desfase, fotos):
    carta, trampa, atacante = "Reaper of the Cards", "Call of the Haunted", "Giant Orc"
    # El rival no tiene monstruo en su primer turno: coloca la Trampa. En el segundo roba al atacante.
    # La IA no ataca a un monstruo boca abajo cuya DEF supera su ATK: hace falta ATK > 1930.
    estado = armar(ruta_rom, "reaper", yo={1: carta}, rival={0: MUERTA, 1: MUERTA, 2: MUERTA, 3: MUERTA},
                   mazo_rival={0: MUERTA, 1: atacante, 2: MUERTA})
    d = abrir(ruta_rom, estado, desfase)
    fingir_nivel(d, carta, 4)             # es de nivel 5: sin esto pediria un tributo para colocarla
    a = colocar_monstruo(d, carta)
    faltas = escenario.comprobar(d, {"campo_yo": [carta], "mano_rival": [trampa]})
    if faltas:
        return res(INVALIDA, "; ".join(faltas), estado=estado)
    d.fin_turno(primero=True)
    if not esperar_volteo(d, a):
        return res(SIN_DISPARO, "el rival no ataco al monstruo boca abajo", estado=estado)
    faltas = escenario.comprobar(d, {"magias_rival": [trampa]})
    if faltas:
        return res(INVALIDA, "al voltearse, el rival no tenia la Trampa colocada", estado=estado)
    d.g.correr(700)                       # aviso "Select Trap Card to destroy."
    foto(d, fotos, "reaper_aviso")
    d.tecla("A", 70)                      # cierra el aviso; el cursor queda sobre el atacante
    d.tecla("UP", 40)                     # sube a la fila de magias y trampas del rival
    d.tecla("A", 120)
    d.g.correr(300)
    s = escenario.instantanea(d)
    foto(d, fotos, "reaper_final")
    detalle = (f"Boca abajo, atacada por {atacante} con {trampa} del rival colocada boca abajo: al voltearse pide "
               f"'Select Trap Card to destroy.', se elige la carta boca abajo y "
               + ("va al cementerio del rival." if trampa in s["cementerio_rival"] else "sigue en el campo.")
               + " Ayuda de prueba: nivel escrito en memoria para colocarla sin tributo.")
    if trampa in s["cementerio_rival"] and trampa not in s["magias_rival"]:
        return res(FUNCIONA, detalle, estado=estado)
    return res(NO_FUNCIONA, detalle, "la Trampa elegida no se destruye", estado=estado)


def caso_hiro(ruta_rom, desfase, fotos):
    carta, atacante = "Hiro's Shadow Scout", "Mechanicalchaser"
    magica, trampa = "Dian Keto the Cure Master", "Call of the Haunted"
    # El rival roba la posicion 0 en su turno; el volteo le hace robar las tres siguientes.
    estado = armar(ruta_rom, "hiro", yo={1: carta},
                   rival={0: atacante, 1: MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                   mazo_rival={0: MUERTA, 1: magica, 2: MUERTA, 3: trampa, 4: MUERTA})
    d = abrir(ruta_rom, estado, desfase)
    a = colocar_monstruo(d, carta)
    faltas = escenario.comprobar(d, {"campo_yo": [carta], "mano_rival": [atacante]})
    if faltas:
        return res(INVALIDA, "; ".join(faltas), estado=estado)
    d.fin_turno(primero=True)
    if not esperar_volteo(d, a):
        return res(SIN_DISPARO, "el rival no ataco al monstruo boca abajo", estado=estado)
    antes = escenario.instantanea(d)
    if magica in antes["cementerio_rival"] or trampa in antes["mano_rival"]:
        return res(INVALIDA, "al voltearse, el rival ya habia robado las cartas de la prueba", estado=estado)
    n = len(d.mano())
    foto(d, fotos, "hiro_volteo")
    # avisos de "mirar la carta": A los cierra. Se deja de pulsar si vuelve mi turno.
    esperar(d, lambda: escenario.instantanea(d)["mazo_rival"] <= antes["mazo_rival"] - 3 or len(d.mano()) > n,
            3000, tecla_cada=90)
    d.g.correr(200)
    s = escenario.instantanea(d)
    foto(d, fotos, "hiro_final")
    salieron = antes["mazo_rival"] - s["mazo_rival"]
    al_cementerio = magica in s["cementerio_rival"]
    # Tras la batalla la IA sigue su turno y puede colocar la Trampa que acaba de robar.
    colocadas = len(s["magias_rival"]) - len(antes["magias_rival"])
    en_mano = (trampa in s["mano_rival"] + s["magias_rival"]
               and len(s["mano_rival"]) + colocadas == len(antes["mano_rival"]) + 2)
    detalle = (f"Boca abajo, atacada por {atacante}: al voltearse salen {salieron} cartas del tope del mazo del rival "
               f"({antes['mazo_rival']} a {s['mazo_rival']}). La Magica ({magica}) "
               + ("va a su cementerio" if al_cementerio else "no va a su cementerio")
               + f" y su mano pasa de {len(antes['mano_rival'])} a {len(s['mano_rival'])} cartas"
               + (f" (entra {trampa})." if trampa in s["mano_rival"]
                  else f" mas {trampa}, que roba y coloca en ese mismo turno." if trampa in s["magias_rival"]
                  else f" ({trampa} no entra)."))
    if salieron == 3 and al_cementerio and en_mano:
        return res(FUNCIONA, detalle, estado=estado)
    if salieron == 0:
        return res(NO_FUNCIONA, detalle, "el rival no roba ninguna carta", estado=estado)
    fallas = []
    if salieron != 3:
        fallas.append(f"salen {salieron} cartas del mazo del rival en vez de 3")
    if not al_cementerio:
        fallas.append("la Magica robada no va al cementerio")
    if not en_mano:
        fallas.append("las cartas que no son Magicas no quedan en la mano del rival")
    return res(EN_PARTE, detalle, "; ".join(fallas), estado=estado)


def _descarte(ruta_rom, desfase, carta, sonda):
    """Hace que un efecto del rival descarte 'carta' de mi mano. Tres sondas:
      mano    la carta esta en mi mano desde el inicio y el rival juega Card Destruction
      robada  la robo del mazo en mi segundo turno y el rival juega Card Destruction en el suyo
      duo     mi mano son 6 copias y el rival juega Delinquent Duo (descarta 1 al azar y 1 que elijo)
    Devuelve (error o None, instantanea antes, instantanea despues, estado)."""
    nombre = "descarte-" + carta.split()[-1].lower() + "-" + sonda
    muertas = {i: MUERTA for i in range(5)}
    if sonda == "mano":
        estado = armar(ruta_rom, nombre, yo={1: carta}, rival={**muertas, 0: "Card Destruction"},
                       mazo_rival={0: MUERTA, 1: MUERTA})
    elif sonda == "robada":
        estado = armar(ruta_rom, nombre, mazo_yo={0: carta}, rival=muertas,
                       mazo_rival={0: MUERTA, 1: "Card Destruction", 2: MUERTA})
    else:
        estado = armar(ruta_rom, nombre, yo={i: carta for i in range(6)}, rival={**muertas, 0: "Delinquent Duo"},
                       mazo_rival={0: MUERTA, 1: MUERTA})
    d = abrir(ruta_rom, estado, desfase)
    primero = True
    if sonda == "robada":
        # Colocar una Magica deja la mano en 5: al robar no se pasa del limite de 6 al terminar el turno.
        d.ir_mano("Monster Reincarnation")
        d.tecla("A", 60)
        d.tecla("UP", 25)
        d.tecla("A", 80)
        d.fin_turno(primero=True)
        if not hasta_mi_turno(d):
            return res(SIN_DISPARO, "no volvio mi turno", estado=estado), None, None, estado
        primero = False
    faltas = escenario.comprobar(d, {"mano_yo": [carta] * (6 if sonda == "duo" else 1)})
    if faltas:
        return res(INVALIDA, "; ".join(faltas), estado=estado), None, None, estado
    antes = escenario.instantanea(d)
    d.fin_turno(primero=primero)
    if sonda == "duo":
        if not esperar(d, lambda: d.lp()[1] == antes["LP"][1] - 1000, 4000):
            return res(SIN_DISPARO, "la IA no jugo Delinquent Duo", estado=estado), None, None, estado
        d.g.correr(600)                   # lista "Select card": A (ALL), A (carta), DECIDE es el 4.o icono
        for tecla in "A A RIGHT RIGHT RIGHT A".split():
            d.tecla(tecla, 50)
        d.g.correr(500)
        # Si las dos copias se disparan a la vez el juego pide "Select the order of effects to add
        # to the chain." y espera: no me llega el turno (no robo). A cierra el aviso, A abre los
        # iconos de la lista, RIGHT va a DECIDE y A confirma; despues la cadena se resuelve sola.
        if not esperar(d, lambda: escenario.instantanea(d)["mazo_yo"] < antes["mazo_yo"], 900, tecla_cada=0):
            for tecla, espera in (("A", 100), ("A", 100), ("RIGHT", 60), ("A", 120)):
                d.tecla(tecla, espera)
            d.g.correr(500)
            d.tecla("A", 240)
            d.tecla("A", 240)
        esperados = 2
    else:
        if not esperar(d, lambda: carta in [n for _, n in d.zona(0, "d")], 5000, tecla_cada=60):
            return res(SIN_DISPARO, "la IA no jugo Card Destruction", estado=estado), None, None, estado
        esperar(d, lambda: False, 600, tecla_cada=60)
        esperados = 1
    despues = escenario.instantanea(d)
    if despues["cementerio_yo"].count(carta) != esperados:
        return res(INVALIDA, f"se esperaban {esperados} copias de {carta} en mi cementerio y hay "
                   f"{despues['cementerio_yo'].count(carta)}", estado=estado), None, None, estado
    return None, antes, despues, estado


SONDAS = (("mano", "en la mano desde el inicio, descartada por Card Destruction del rival"),
          ("robada", "robada del mazo y descartada por Card Destruction del rival"),
          ("duo", "dos copias descartadas por Delinquent Duo del rival"))


def _caso_descarte(ruta_rom, desfase, carta, medir, texto_esperado):
    """'medir(sonda, antes, despues)' devuelve (se disparo, texto de lo observado)."""
    partes, disparos, estado0 = [], [], None
    for sonda, descripcion in SONDAS:
        error, antes, despues, estado = _descarte(ruta_rom, desfase, carta, sonda)
        estado0 = estado0 or estado
        if error:
            return error
        ok, visto = medir(sonda, antes, despues)
        disparos.append(ok)
        partes.append(f"{descripcion}: {visto}")
    detalle = ". ".join(p[0].upper() + p[1:] for p in partes) + "."
    if all(disparos):
        return res(FUNCIONA, detalle, estado=estado0)
    falla = f"el efecto no se dispara en todos los casos: {texto_esperado}."
    return res(EN_PARTE if any(disparos) else NO_FUNCIONA, detalle, falla, estado=estado0)


def caso_electric_snake(ruta_rom, desfase, fotos):
    def medir(sonda, a, b):
        # sin el efecto: Card Destruction repone la mano (mazo - mano); Delinquent Duo no toca el mazo.
        # Un robo normal posterior baja el mazo en 1 como mucho; el efecto lo bajaria en 2 por copia.
        base = a["mazo_yo"] - (len(a["mano_yo"]) if sonda != "duo" else 0)
        extra = base - b["mazo_yo"]
        copias = 2 if sonda == "duo" else 1             # cada copia descartada roba 2
        return extra >= 2 * copias, f"robo {extra} cartas de mas (mazo {a['mazo_yo']} a {b['mazo_yo']})"
    return _caso_descarte(ruta_rom, desfase, "Electric Snake", medir, "no roba 2 cartas")


def caso_minar(ruta_rom, desfase, fotos):
    def medir(sonda, a, b):
        coste = 1000 if sonda == "duo" else 0          # Delinquent Duo le cuesta 1000 LP al rival
        danio = a["LP"][1] - coste - b["LP"][1]
        copias = 2 if sonda == "duo" else 1             # cada copia descartada hace 1000 de dano
        return danio >= 1000 * copias, f"el rival pierde {danio} LP por el efecto (LP {a['LP'][1]} a {b['LP'][1]}" + (
            ", de los cuales 1000 son el coste de Delinquent Duo)" if coste else ")")
    return _caso_descarte(ruta_rom, desfase, "Minar", medir, "el rival no pierde 1000 LP")


def colocar_trampa(d, carta):
    """Coloca boca abajo una Magica o Trampa de la mano. Devuelve su numero de ranura o None."""
    d.ir_mano(carta)
    d.tecla("A", 60)
    d.tecla("UP", 25)
    d.tecla("A", 80)
    return next((s for s, n in d.zona(0, "5") if n == carta), None)


def encadenar(d, ranura):
    """Contesta Yes a "<carta> has activated. Will you chain?" y activa la trampa de 'ranura'.
    Tras Yes y el aviso "Select Spell/Trap Card to activate." el cursor arranca en MI MANO: UP lleva
    a la zona 4 de mi fila de magias y trampas, y de ahi LEFT hasta la zona de la carta."""
    z = d.zona_magia(ranura)
    assert z is not None, "la trampa no esta en la fila de magias y trampas"
    d.tecla("A", 80)                      # Yes
    d.tecla("A", 80)                      # cierra el aviso
    d.tecla("UP", 30)
    for _ in range(4 - z):
        d.tecla("LEFT", 30)
    d.tecla("A", 60)                      # menu: Activate Effect / Detail Screen (queda en Detail)
    d.tecla("UP", 30)
    d.tecla("A", 120)


def caso_big_burn(ruta_rom, desfase, fotos):
    carta, renacer = "Big Burn", "Monster Reborn"
    # El rival juega Card Destruction: los dos cementerios se llenan de monstruos y, de las cartas
    # que repone, la unica jugable es Monster Reborn, que apunta a un monstruo del cementerio.
    estado = armar(ruta_rom, "big-burn", yo={5: carta},
                   rival={0: "Card Destruction", 1: MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                   mazo_rival={0: MUERTA, 1: renacer, 2: MUERTA, 3: MUERTA, 4: MUERTA, 5: MUERTA, 6: MUERTA})
    d = abrir(ruta_rom, estado, desfase)
    rom = d.rom
    ranura = colocar_trampa(d, carta)
    if ranura is None:
        return res(INVALIDA, f"{carta} no quedo colocada", estado=estado)

    def monstruos(nombres):
        return [n for n in nombres if escenario.es_monstruo(rom, escenario.indice(rom, n))]

    d.fin_turno(primero=True)
    if not esperar(d, lambda: renacer in [n for _, n in d.zona(1, "5a")], 4000):
        return res(SIN_DISPARO, f"la IA no jugo {renacer}", estado=estado)
    d.g.correr(200)                       # "<monstruo> has been selected as the target."
    antes = escenario.instantanea(d)
    if not monstruos(antes["cementerio_yo"]) or not monstruos(antes["cementerio_rival"]):
        return res(INVALIDA, "no habia monstruos en los dos cementerios", estado=estado)
    d.tecla("A", 40)
    d.g.correr(270)                       # "Monster Reborn has activated. Will you chain?"
    foto(d, fotos, "big-burn_aviso")
    encadenar(d, ranura)
    d.g.correr(900)
    s = escenario.instantanea(d)
    foto(d, fotos, "big-burn_final")
    if carta not in s["cementerio_yo"]:
        return res(NO_FUNCIONA, f"el rival juega {renacer} apuntando a un monstruo del cementerio y {carta} "
                   "no llega a activarse", "no se ofrece o no se activa en respuesta", estado=estado)
    quedan = monstruos(s["cementerio_yo"]) + monstruos(s["cementerio_rival"])
    n_antes = len(monstruos(antes["cementerio_yo"])) + len(monstruos(antes["cementerio_rival"]))
    n_ret = len(monstruos(s["retiradas_yo"])) + len(monstruos(s["retiradas_rival"]))
    detalle = (f"Colocada boca abajo; el rival juega {renacer} apuntando a un monstruo del cementerio, el juego "
               f"pregunta 'Will you chain?' y se activa: de {n_antes} monstruos en los dos cementerios quedan "
               f"{len(quedan)} y hay {n_ret} retirados del juego. {renacer} "
               + ("no invoca nada." if not s["campo_rival"] else "invoca igual un monstruo."))
    if not quedan and n_ret == n_antes:
        return res(FUNCIONA, detalle, estado=estado)
    return res(EN_PARTE if n_ret else NO_FUNCIONA, detalle,
               "no retira todos los monstruos de los dos cementerios", estado=estado)


def invocar(d, carta):
    """Invocacion Normal en posicion de ataque desde la mano."""
    d.ir_mano(carta)
    d.menu(0)
    d.g.correr(90)
    d.tecla("DOWN", 20)
    d.tecla("A", 60)
    d.g.correr(60)


def zona_monstruo(d, lado, carta):
    """Zona (0..4) del monstruo 'carta' entre los que controla 'lado', o None."""
    for z in range(5):
        idc = d.g.r8(LISTA_ZONAS + 11 * lado + z)
        if idc != 0xFF:
            a = (J1 if idc & 0x80 else J0) + (idc & 0x7F) * 0x50
            if d.rom.nombre(d.g.r16(a + 0x24) & 0x7FFF) == carta:
                return z
    return None


def atacar(d, atacante=None):
    """Desde mi Main Phase 1: entra a la Battle Phase y ataca con 'atacante' (o con el monstruo
    sobre el que cae el cursor) al monstruo rival que el juego propone.
    B abre "Will you end the Main Phase?" con Enter Battle Phase arriba; en la Battle Phase A
    abre el menu del monstruo (Attack / Detail Screen, queda en Detail)."""
    d.tecla("B", 80)
    d.tecla("A", 170)                     # Enter Battle Phase
    if atacante:
        d.mover(y=2)
        d.mover(x=2 + zona_monstruo(d, 0, atacante))
        d.g.correr(20)
    d.tecla("A", 80)                      # menu del monstruo
    d.tecla("UP", 50)
    d.tecla("A", 110)                     # Attack -> "Select your opponent's monster to attack."
    d.tecla("A", 110)                     # cierra el aviso; el cursor queda sobre el monstruo rival
    d.tecla("A", 70)                      # confirma el objetivo


def caso_kunai(ruta_rom, desfase, fotos):
    import probar_trampas
    carta, monstruo, tributador = "Kunai with Chain", "Blazing Inpachi", "Meteor Dragon"
    # Primer efecto: sin monstruos propios, el rival ataca y el atacante pasa a defensa.
    antes, despues, v = probar_trampas.correr(ruta_rom, carta, 0x10)
    if antes is None:
        return res(SIN_DISPARO, f"el rival no ataco con la Trampa colocada ({v})")
    cambiados = [s for s, pos in antes["posicion_rival"].items()
                 if pos == 0x10 and despues["posicion_rival"].get(s) == 0x30]
    posicion = bool(cambiados) and carta in despues["cementerio"]
    # Segundo efecto: con un monstruo propio boca arriba se activa en la primera fase en que el
    # juego pregunta (Draw Phase del rival) y se equipa.
    estado = armar(ruta_rom, "kunai-equipo", yo={5: carta},
                   rival={0: MUERTA, 1: MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                   mazo_rival={0: MUERTA, 1: MUERTA})
    d = abrir(ruta_rom, estado, desfase)
    invocar(d, monstruo)
    ranura = colocar_trampa(d, carta)
    faltas = escenario.comprobar(d, {"campo_yo": [monstruo], "magias_yo": [carta]})
    if faltas or ranura is None:
        return res(INVALIDA, "; ".join(faltas) or "la Trampa no quedo colocada", estado=estado)
    base = next(m[2] for m in escenario.instantanea(d)["campo_yo"] if m[0] == monstruo)
    n = len(d.mano())
    d.fin_turno(primero=True)
    d.g.correr(300)
    d.tecla("A", 200)                     # dialogo del rival; despues: "It's the Draw Phase. Activate...?"
    d.tecla("A", 80)                      # Yes
    d.tecla("A", 80)                      # cierra "Select Spell/Trap Card to activate."
    if len(d.mano()) > n:
        return res(SIN_DISPARO, "el juego no pregunto en la Draw Phase del rival", estado=estado)
    d.mover(y=1)
    d.mover(x=2 + d.zona_magia(ranura))
    d.g.correr(20)
    d.tecla("A", 60)                      # menu: Activate Effect / Detail Screen (queda en Detail)
    d.tecla("UP", 30)
    d.tecla("A", 240)                     # aviso "Select your monster to equip."
    foto(d, fotos, "kunai_aviso")
    d.tecla("A", 80)                      # lo cierra; el cursor queda sobre mi monstruo
    d.tecla("A", 120)
    d.g.correr(120)
    s1 = escenario.instantanea(d)
    foto(d, fotos, "kunai_equipada")
    atk1 = next((m[2] for m in s1["campo_yo"] if m[0] == monstruo), None)
    equipada = atk1 == base + 500 and carta in s1["magias_yo"]
    if not hasta_mi_turno(d):
        return res(SIN_DISPARO, "no volvio mi turno despues de equiparla", estado=estado)
    s2 = escenario.instantanea(d)
    atk2 = next((m[2] for m in s2["campo_yo"] if m[0] == monstruo), None)
    dura = atk2 == base + 500 and carta in s2["magias_yo"]
    # Invocacion por tributo del monstruo equipado: el equipo tiene que ir al cementerio con el.
    d.ir_mano(tributador)
    d.menu(0)
    for _ in range(3):
        d.tecla("A", 80)
    d.g.correr(120)
    s3 = escenario.instantanea(d)
    foto(d, fotos, "kunai_tributo")
    if monstruo not in s3["cementerio_yo"]:
        return res(INVALIDA, f"no se pudo tributar a {monstruo} para ver que pasa con el equipo", estado=estado)
    se_va = carta in s3["cementerio_yo"] and carta not in s3["magias_yo"]
    detalle = (f"Sin monstruos propios, el rival ataca: el atacante "
               + ("pasa de ataque a defensa y la carta va al cementerio. " if posicion else "no cambia de posicion. ")
               + f"Con {monstruo} ({base}) en mi campo se activa en la Draw Phase del rival: pide 'Select your "
               f"monster to equip.', el ATK queda en {atk1} y la carta "
               + ("queda boca arriba en el campo" if carta in s1["magias_yo"] else "no queda en el campo")
               + f"; en mi turno siguiente el ATK es {atk2}. Al tributar a {monstruo} la carta "
               + ("va al cementerio con el." if se_va else "no va al cementerio."))
    fallas = []
    if not posicion:
        fallas.append("el atacante no cambia de posicion")
    if not equipada:
        fallas.append("no queda equipada con +500 ATK")
    elif not dura:
        fallas.append("el equipo no dura hasta mi turno siguiente")
    if equipada and not se_va:
        fallas.append("la carta no va al cementerio cuando el monstruo equipado deja el campo")
    if not fallas:
        return res(FUNCIONA, detalle, estado=estado)
    return res(NO_FUNCIONA if not posicion and not equipada else EN_PARTE, detalle, "; ".join(fallas), estado=estado)


def _reasoning(ruta_rom, desfase, forzar):
    """Activa Reasoning con una Magica, una Trampa y un monstruo de nivel 4 en el tope de mi mazo.
    'forzar' = nivel que se escribe en memoria como declarado (ayuda de prueba) o None.
    Devuelve (error o None, nivel declarado, instantanea antes, instantanea despues, estado)."""
    carta, magica, trampa, monstruo = "Reasoning", "Dian Keto the Cure Master", "Call of the Haunted", "Mechanicalchaser"
    estado = armar(ruta_rom, "reasoning", yo={5: carta}, mazo_yo={0: magica, 1: trampa, 2: monstruo})
    d = abrir(ruta_rom, estado, desfase)
    faltas = escenario.comprobar(d, {"mano_yo": [carta]})
    if faltas:
        return res(INVALIDA, "; ".join(faltas), estado=estado), None, None, None, estado
    antes = escenario.instantanea(d)
    d.ir_mano(carta)
    d.tecla("A", 50)                      # menu: Activate Effect / Set / Detail Screen (queda en Detail)
    d.tecla("UP", 28)
    d.tecla("UP", 28)
    d.tecla("A", 100)
    d.g.correr(120)                       # aviso "Your opponent declares Level N."
    if carta not in escenario.instantanea(d)["magias_yo"]:
        return res(SIN_DISPARO, "la carta no se activo", estado=estado), None, None, None, estado
    declarado = d.g.r8(0x020204C7)
    if forzar is not None:
        d.g.w8(0x020204C7, forzar)
        declarado = forzar
    d.tecla("A", 60)                      # cierra el aviso: revela desde el tope del mazo
    d.g.correr(600)
    if monstruo not in escenario.instantanea(d)["cementerio_yo"]:
        d.tecla("A", 200)                 # "Select card position.": ataque
    d.g.correr(120)
    return None, declarado, antes, escenario.instantanea(d), estado


def caso_reasoning(ruta_rom, desfase, fotos):
    carta, magica, trampa, monstruo = "Reasoning", "Dian Keto the Cure Master", "Call of the Haunted", "Mechanicalchaser"
    partes, fallas, estado0 = [], [], None
    # una corrida con el nivel que declara el juego y las dos ramas forzadas (el monstruo es de nivel 4)
    for forzar, rotulo in ((None, "Con el nivel que declara el juego"), (4, "Con el nivel 4 escrito en memoria"),
                           (3, "Con el nivel 3 escrito en memoria")):
        error, declarado, antes, s, estado = _reasoning(ruta_rom, desfase, forzar)
        estado0 = estado0 or estado
        if error:
            return error
        en_campo = monstruo in [m[0] for m in s["campo_yo"]]
        en_cementerio = monstruo in s["cementerio_yo"]
        partes.append(f"{rotulo} ({declarado}): revela {magica}, {trampa} y {monstruo} (nivel 4); "
                      + ("el monstruo se invoca" if en_campo else "el monstruo va al cementerio" if en_cementerio
                         else "el monstruo queda en el mazo")
                      + f" y el mazo pasa de {antes['mazo_yo']} a {s['mazo_yo']}")
        if not 2 <= declarado <= 12:
            fallas.append(f"el nivel declarado no es un nivel ({declarado})")
        if magica not in s["cementerio_yo"] or trampa not in s["cementerio_yo"]:
            fallas.append("las cartas reveladas antes del monstruo no van al cementerio")
        if carta not in s["cementerio_yo"]:
            fallas.append("Reasoning no va al cementerio al terminar")
        if s["mazo_yo"] != antes["mazo_yo"] - 3:
            fallas.append(f"salen {antes['mazo_yo'] - s['mazo_yo']} cartas del mazo en vez de 3")
        if declarado == 4 and not (en_cementerio and not en_campo):
            fallas.append("con el nivel acertado el monstruo no va al cementerio")
        if declarado != 4 and not (en_campo and not en_cementerio):
            fallas.append("con otro nivel el monstruo no se invoca")
    detalle = ". ".join(partes) + ". Ayuda de prueba: nivel declarado escrito en memoria para ver las dos ramas."
    if not fallas:
        return res(FUNCIONA, detalle, estado=estado0)
    return res(EN_PARTE, detalle, "; ".join(sorted(set(fallas))), estado=estado0)


def caso_penguin(ruta_rom, desfase, fotos):
    carta, gusano, mio = "Penguin Knight", "Needle Worm", "Blazing Inpachi"
    # Needle Worm del rival (volteo: manda 5 cartas del tope de mi mazo al cementerio). Robo la
    # posicion 0 del mazo en mi segundo turno; Penguin Knight queda entre las 5 siguientes.
    estado = armar(ruta_rom, "penguin", mazo_yo={2: carta},
                   rival={0: gusano, 1: MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                   mazo_rival={0: MUERTA, 1: MUERTA, 2: MUERTA})
    d = abrir(ruta_rom, estado, desfase)
    invocar(d, mio)
    d.fin_turno(primero=True)
    if not hasta_mi_turno(d):
        return res(SIN_DISPARO, "no volvio mi turno", estado=estado)
    antes = escenario.instantanea(d)
    boca_abajo = [m for m in antes["campo_rival"] if m[0] == gusano and m[1] == "boca abajo"]
    if mio not in controla(d, 0) or not boca_abajo:
        return res(SIN_DISPARO, f"el rival no coloco a {gusano} boca abajo", estado=estado)
    atacar(d)
    esperar(d, lambda: False, 900, tecla_cada=0)
    s = escenario.instantanea(d)
    foto(d, fotos, "penguin_final")
    enviadas = antes["mazo_yo"] - s["mazo_yo"]
    if carta not in s["cementerio_yo"] and enviadas == 0 and gusano in controla(d, 1):
        return res(SIN_DISPARO, "el ataque no volteo a Needle Worm", estado=estado)
    detalle = (f"Ataco con {mio} a {gusano} del rival boca abajo: su volteo manda 5 cartas del tope de mi mazo al "
               f"cementerio, {carta} entre ellas. Despues: mazo {antes['mazo_yo']} a {s['mazo_yo']}, cementerio "
               f"con {len(s['cementerio_yo'])} cartas.")
    if not s["cementerio_yo"] and s["mazo_yo"] == antes["mazo_yo"]:
        return res(FUNCIONA, detalle, estado=estado)
    if carta not in s["cementerio_yo"] and len(s["cementerio_yo"]) == 5:
        return res(INVALIDA, f"{carta} no estaba entre las 5 cartas enviadas", estado=estado)
    return res(NO_FUNCIONA, detalle, "el cementerio no vuelve al mazo: el efecto no se dispara. El juego no trae "
               "ninguna carta original con este disparador para usar de comparacion.", estado=estado)


def activar_desde_el_campo(d, carta, exito, fotos, nombre_foto):
    """En mi Main Phase: abre el menu de mi monstruo 'carta' y prueba sus opciones de arriba hacia
    abajo hasta que 'exito()' sea cierto. El menu arranca en la ultima opcion (Detail Screen) y da
    la vuelta, asi que cada intento parte del mismo punto (se guarda y se recarga el estado).
    Devuelve True si alguna opcion del menu disparo el efecto."""
    punto = d.g.guardar_estado()
    for subidas in (1, 2):
        d.g.cargar_estado(punto)
        d.g.correr(2)
        d.mover(y=2)
        d.mover(x=2 + zona_monstruo(d, 0, carta))
        d.g.correr(20)
        d.tecla("A", 60)
        if subidas == 1:
            foto(d, fotos, nombre_foto)
        for _ in range(subidas):
            d.tecla("UP", 30)
        d.tecla("A", 120)
        for _ in range(8):                # avisos o confirmaciones del efecto
            d.tecla("A", 90)
            if exito():
                return True
    return False


def elegir_en_lista(d):
    """Con un aviso de seleccion abierto: lo cierra, entra a la lista (A sobre ALL), abre los iconos
    de la primera carta y elige el 4.o (la mano que apunta)."""
    d.tecla("A", 90)
    d.tecla("A", 60)
    d.tecla("A", 60)
    for _ in range(3):
        d.tecla("RIGHT", 20)
    d.tecla("A", 90)


def tope_del_mazo(d, lado=0):
    base = J1 if lado else J0
    idc = d.g.r8(base + escenario.MAZO)
    return d.rom.nombre(d.g.r16((J1 if idc & 0x80 else J0) + (idc & 0x7F) * 0x50 + 0x24) & 0x7FFF)


def fondo_del_mazo(d, lado=0):
    """Nombre de la ultima carta del mazo (la que se robaria al final)."""
    base = J1 if lado else J0
    n = len(d.zona(lado, "c"))
    idc = d.g.r8(base + escenario.MAZO + n - 1)
    return d.rom.nombre(d.g.r16((J1 if idc & 0x80 else J0) + (idc & 0x7F) * 0x50 + 0x24) & 0x7FFF)


def caso_lady_panther(ruta_rom, desfase, fotos):
    carta, debil, rival = "Lady Panther", "Needle Worm", "Tongyo"
    estado = armar(ruta_rom, "lady-panther", yo={2: carta},
                   rival={0: rival, 1: MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                   mazo_rival={0: MUERTA, 1: MUERTA, 2: MUERTA})
    d = abrir(ruta_rom, estado, desfase)
    invocar(d, carta)
    d.fin_turno(primero=True)
    if not hasta_mi_turno(d):
        return res(SIN_DISPARO, "no volvio mi turno", estado=estado)
    invocar(d, debil)
    faltas = escenario.comprobar(d, {"campo_yo": [carta, debil], "campo_rival": [rival]})
    if faltas:
        return res(INVALIDA, "; ".join(faltas), estado=estado)
    # Ayuda de prueba: la IA coloca a Tongyo boca abajo en defensa; se lo pasa a ataque en memoria
    # para que mi monstruo debil (750) muera al atacarlo (1350).
    d.g.w8(ranura_de(d, 1, rival) + 0x33, 0x10)
    d.g.correr(30)
    atacar(d, debil)
    d.g.correr(400)
    antes = escenario.instantanea(d)
    if debil not in antes["cementerio_yo"] or carta not in controla(d, 0):
        return res(SIN_DISPARO, f"{debil} no fue destruido en batalla", estado=estado)
    d.tecla("B", 80)                      # "Will you end the Battle Phase?": Go to Main Phase 2
    d.tecla("A", 170)
    def tributada():
        return carta in [n for _, n in d.zona(0, "d")]

    ofrecido = activar_desde_el_campo(d, carta, tributada, fotos, "lady-panther_menu")
    if ofrecido:
        # "Select monster to return to the Deck." -> lista "Your Graveyard" con el destruido en batalla
        d.g.correr(240)
        foto(d, fotos, "lady-panther_aviso")
        elegir_en_lista(d)
        d.g.correr(240)
    s = escenario.instantanea(d)
    foto(d, fotos, "lady-panther_final")
    if ofrecido and debil not in s["cementerio_yo"] and tope_del_mazo(d) == debil:
        return res(FUNCIONA, f"El turno en que {debil} es destruido en batalla, el menu de {carta} ofrece el efecto: "
                   f"se tributa y {debil} vuelve al tope del mazo.", estado=estado)
    if ofrecido:
        return res(EN_PARTE, f"El menu de {carta} ofrece el efecto y se tributa, pero {debil} no vuelve al tope del "
                   f"mazo (tope: {tope_del_mazo(d)}).", "el monstruo destruido no vuelve al tope del mazo", estado=estado)
    detalle = (f"{debil} (750) ataca a {rival} (1350) y es destruido en batalla. En la Main Phase 2 de ese turno el "
               f"menu de {carta} solo trae Defense Position y Detail Screen: ninguna opcion la tributa y {debil} "
               f"sigue en el cementerio. Control: con el mismo metodo, el menu de Goddess of Whim si trae Activate "
               f"Effect. Ayuda de prueba: posicion de {rival} escrita en memoria.")
    return res(NO_FUNCIONA, detalle, "el menu del monstruo no ofrece activar el efecto. [HIP] Mismo sintoma que tenia "
               "Goddess of Whim: la lista de efectos de campo que arma el menu no incluye a esta carta.", estado=estado)


def caso_fairy_guardian(ruta_rom, desfase, fotos):
    carta, magica, contra = "Fairy Guardian", "Dian Keto the Cure Master", "Magic Jammer"
    # El rival coloca Magic Jammer en su primer turno. En el mio activo una Magica: la IA la niega y
    # la destruye, asi que va a mi cementerio por un efecto del rival durante mi turno.
    estado = armar(ruta_rom, "fairy-guardian", yo={2: carta, 5: magica},
                   rival={0: contra, 1: MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                   mazo_rival={0: MUERTA, 1: MUERTA, 2: MUERTA})
    d = abrir(ruta_rom, estado, desfase)
    invocar(d, carta)
    d.fin_turno(primero=True)
    if not hasta_mi_turno(d):
        return res(SIN_DISPARO, "no volvio mi turno", estado=estado)
    faltas = escenario.comprobar(d, {"campo_yo": [carta], "mano_yo": [magica]})
    if faltas:
        return res(INVALIDA, "; ".join(faltas), estado=estado)
    if contra not in escenario.instantanea(d)["magias_rival"]:
        return res(SIN_DISPARO, f"el rival no coloco {contra}", estado=estado)
    lp, mazo = d.lp()[0], len(d.zona(0, "c"))
    d.ir_mano(magica)
    d.tecla("A", 50)                      # menu: Activate Effect / Set / Detail Screen (queda en Detail)
    d.tecla("UP", 28)
    d.tecla("UP", 28)
    d.tecla("A", 100)
    if not esperar(d, lambda: magica in [n for _, n in d.zona(0, "d")], 3000, tecla_cada=60):
        return res(SIN_DISPARO, f"{magica} no llego al cementerio", estado=estado)
    d.g.correr(200)
    antes = escenario.instantanea(d)
    if antes["LP"][0] != lp or contra not in antes["cementerio_rival"]:
        return res(SIN_DISPARO, f"la IA no nego {magica} con {contra}", estado=estado)

    def tributada():
        return carta in [n for _, n in d.zona(0, "d")]

    ofrecido = activar_desde_el_campo(d, carta, tributada, fotos, "fairy-guardian_menu")
    if ofrecido:
        # "Select Spell Card to return to the Deck." -> lista "Your Graveyard" con la Magica negada
        d.g.correr(240)
        foto(d, fotos, "fairy-guardian_aviso")
        elegir_en_lista(d)
        d.g.correr(240)
    s = escenario.instantanea(d)
    foto(d, fotos, "fairy-guardian_final")
    fondo = fondo_del_mazo(d)
    if ofrecido and magica not in s["cementerio_yo"] and s["mazo_yo"] == mazo + 1 and fondo == magica:
        return res(FUNCIONA, f"El turno en que {contra} del rival niega y destruye mi {magica}, el menu de {carta} "
                   f"ofrece el efecto: se tributa, pide elegir la Magica en la lista del cementerio y la Magica "
                   f"vuelve al fondo del mazo ({mazo} a {s['mazo_yo']} cartas; la ultima es {fondo}).", estado=estado)
    if ofrecido:
        return res(EN_PARTE, f"El menu de {carta} ofrece el efecto y se tributa, pero {magica} no vuelve al fondo "
                   f"del mazo (mazo {mazo} a {s['mazo_yo']}; la ultima carta es {fondo}).",
                   "la Magica no vuelve al fondo del mazo", estado=estado)
    detalle = (f"En mi turno activo {magica}; el rival la niega y destruye con {contra} y va a mi cementerio. En esa "
               f"misma Main Phase ninguna opcion del menu de {carta} la tributa: no ofrece Activate Effect y "
               f"{magica} sigue en el cementerio. Control: con el mismo metodo, el menu de Goddess of Whim si lo ofrece.")
    return res(NO_FUNCIONA, detalle, "el menu del monstruo no ofrece activar el efecto. [HIP] Mismo sintoma que tenia "
               "Goddess of Whim: la lista de efectos de campo que arma el menu no incluye a esta carta.", estado=estado)


FASES = {2: "Main Phase 1", 3: "Battle Phase", 4: "Main Phase 2", 5: "End Phase"}


def _volver_necrofear(d, a, lado, debil):
    """Ayuda de prueba: Necrofear no admite Invocacion Normal (se invoca retirando 3 Demonios), asi que
    un monstruo ya invocado pasa a ser ella: indice, tipo, atributo, nivel, ATK y DEF de su ranura 'a'.
    'debil': ademas un modificador de tipo 10 (-500 ATK y DEF, el de Slate Warrior) la deja en
    1700/2300 para que Mechanicalchaser (1850) la pueda destruir en batalla."""
    i = escenario.indice(d.rom, "Dark Necrofear")
    datos = d.rom.stats(i)
    d.g.w16(a + 0x24, (d.g.r16(a + 0x24) & 0x8000) | i)
    d.g.w8(a + 0x30, ((datos["atributo"] & 7) << 5) | (datos["tipo"] & 0x1F))
    d.g.w8(a + 0x31, (d.g.r8(a + 0x31) & 0xF0) | (datos["nivel"] & 0xF))
    d.g.w32(a + 0x28, datos["atk"])
    d.g.w32(a + 0x2C, datos["def"])
    if debil:
        d.g.w16(a + 0x40, (0x1A << 8) | (lado << 7) | ((a - (J1 if lado else J0)) // 0x50))
        d.g.w8(a + 0x3E, (d.g.r8(a + 0x3E) & 0xF0) | 1)
    d.g.correr(60)


def _fase(d):
    """(fase, lado del turno): ver FASES."""
    b = d.g.r8(J0 + 0x562E)
    return b >> 2, (b >> 1) & 1


def _aviso(d):
    """Contador de pasos de la seleccion en curso."""
    return (d.g.r32(0x020204C0) >> 10) & 0xFF


def _zona_carta(d, a):
    return (d.g.r32(a + 0x30) >> 12) & 0x7F


def _id_ranura(a):
    return ((a - J1) // 0x50) | 0x80 if a >= J1 else (a - J0) // 0x50


def _equipada_a(d, equipo, monstruo):
    """La carta de la ranura 'equipo' esta boca arriba en la zona de Magicas y Trampas, apunta al
    monstruo (ranura+0x3C) y figura en su lista de modificadores como equipo (tipo 1)."""
    if monstruo is None or _zona_carta(d, equipo) != 5 or not d.g.r8(equipo + 0x33) & 0x10:
        return False
    entradas = [d.g.r16(monstruo + 0x40 + 2 * k) for k in range(d.g.r8(monstruo + 0x3E) & 0xF)]
    return d.g.r8(equipo + 0x3C) == _id_ranura(monstruo) and (0x100 | _id_ranura(equipo)) in entradas


def _necrofear(ruta_rom, desfase, fotos, sonda):
    """Una pasada de Dark Necrofear en mi campo. Dos sondas:
      batalla  el rival la destruye atacando con Mechanicalchaser
      efecto   el rival la destruye con Raigeki (la IA no juega Fissure, Smashing Ground ni Hammer
               Shot contra un monstruo mas fuerte que los suyos; Raigeki y Dark Hole si)
    Devuelve (resultado sin veredicto o None, lo visto, fallas)."""
    carta, base, suyo = "Dark Necrofear", "Mechanicalchaser", "Mechanicalchaser"
    estado = armar(ruta_rom, "necrofear-" + sonda, yo={1: base},
                   rival={0: suyo, 1: "Raigeki" if sonda == "efecto" else MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                   mazo_rival={0: MUERTA, 1: MUERTA, 2: MUERTA})
    d = abrir(ruta_rom, estado, desfase)
    invocar(d, base)
    a = ranura_de(d, 0, base)
    _volver_necrofear(d, a, 0, debil=sonda == "batalla")
    faltas = escenario.comprobar(d, {"campo_yo": [carta], "mano_rival": [suyo]})
    if faltas:
        return res(INVALIDA, "; ".join(faltas), estado=estado), "", []
    foto(d, fotos, f"necrofear_{sonda}_armado")
    en_mano = len(d.mano())
    d.fin_turno(primero=True)

    def zona():
        return (d.g.r32(a + 0x30) >> 12) & 0x7F

    def fase():                              # ver FASES
        return d.g.r8(J0 + 0x562E) >> 2

    def aviso():                             # contador de pasos de la seleccion
        return (d.g.r32(0x020204C0) >> 10) & 0xFF

    if not esperar(d, lambda: zona() == 0xD or len(d.mano()) > en_mano, 6000):
        return res(SIN_DISPARO, "el rival no llego a jugar", estado=estado), "", []
    if zona() != 0xD:
        return res(SIN_DISPARO, "el rival no destruyo a Dark Necrofear", estado=estado), "", []
    fase_destruida = fase()
    foto(d, fotos, f"necrofear_{sonda}_destruida")
    # El aviso "Select and gain control of 1 opponent's face-up monster." espera sin limite. Antes
    # hay que cerrar con A los dialogos del rival; con el aviso abierto no se pulsa nada mas.
    if not esperar(d, lambda: aviso() or len(d.mano()) > en_mano, 3000):
        return res(SIN_DISPARO, "el turno del rival no termino", estado=estado), "", []
    fallas = []
    if not aviso():
        return None, (f"Destruida ({'en batalla' if sonda == 'batalla' else 'por Raigeki del rival'}) y enviada al "
                      "cementerio: el turno del rival termina sin que el juego pida elegir un monstruo."), \
            ["no hay posesion: en la End Phase no pide elegir un monstruo del rival"]
    fase_aviso = fase()
    suyos_antes = controla(d, 1)
    d.g.correr(30)
    foto(d, fotos, f"necrofear_{sonda}_aviso")
    for _ in range(3):                    # cierra el aviso, elige el monstruo, confirma
        d.tecla("A", 80)
    d.g.correr(120)
    foto(d, fotos, f"necrofear_{sonda}_control")
    tomado = suyo in controla(d, 0)
    equipada = _equipada_a(d, a, ranura_de(d, 1, suyo))
    if not hasta_mi_turno(d, n=en_mano):
        return res(SIN_DISPARO, "no volvio mi turno despues de la End Phase", estado=estado), "", []
    en_mi_turno = suyo in controla(d, 0)
    d.fin_turno(primero=False)
    hasta_mi_turno(d)
    despues = suyo in controla(d, 0)
    foto(d, fotos, f"necrofear_{sonda}_despues")
    s = escenario.instantanea(d)
    sigue_equipada = carta in s["magias_yo"] and _equipada_a(d, a, ranura_de(d, 1, suyo))
    visto = (f"Destruida {'en batalla por ' + suyo if sonda == 'batalla' else 'por Raigeki del rival'} "
             f"en la {FASES.get(fase_destruida, fase_destruida)} del rival: va al cementerio y el rival sigue "
             f"controlando a {' y '.join(suyos_antes) or 'nadie'} hasta la {FASES.get(fase_aviso, fase_aviso)}, donde "
             f"el juego pide elegir un monstruo rival boca arriba. Elegido {suyo}: "
             f"{'pasa a mi campo' if tomado else 'no cambia de lado'}; "
             f"en mi turno siguiente {'sigue' if en_mi_turno else 'no esta'} bajo mi control y despues de otro turno "
             f"del rival {'sigue siendo mio' if despues else 'ya no'}. Necrofear "
             + ("queda boca arriba en mi zona de Magicas y Trampas, equipada a el."
                if equipada and sigue_equipada else "no queda equipada a el."))
    if fase_aviso != 5:
        fallas.append(f"la posesion no se pide en la End Phase (fase {fase_aviso})")
    if suyo not in suyos_antes:
        fallas.append("el control cambia antes de la End Phase")
    if not tomado:
        fallas.append("no toma el control del monstruo elegido")
    elif not en_mi_turno or not despues:
        fallas.append("el control no dura: el monstruo deja mi campo")
    if tomado and not (equipada and sigue_equipada):
        fallas.append("Necrofear no queda equipada al monstruo")
    return None, visto, fallas


def _necrofear_rival(ruta_rom, desfase, fotos, sonda):
    """Dark Necrofear del lado del rival: la destruyo yo y la IA tiene que elegir sola en mi End Phase.
      batalla  mi Mechanicalchaser la ataca (debilitada a 1700)
      efecto   mi Raigeki
    Ningun mazo rival la lleva: el Mechanicalchaser que invoca el rival pasa a ser ella.
    Devuelve (resultado sin veredicto o None, lo visto, fallas)."""
    carta, mio, suyo = "Dark Necrofear", "Mechanicalchaser", "Mechanicalchaser"
    estado = armar(ruta_rom, "necrofear-rival-" + sonda, yo={1: mio, 2: "Raigeki"},
                   rival={0: suyo, 1: MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                   mazo_rival={i: MUERTA for i in range(4)})
    d = abrir(ruta_rom, estado, desfase)
    d.fin_turno(primero=True)
    if not hasta_mi_turno(d):
        return res(SIN_DISPARO, "no volvio mi turno", estado=estado), "", []
    a = ranura_de(d, 1, suyo)
    if a is None or suyo not in controla(d, 1):
        return res(SIN_DISPARO, f"el rival no invoco a {suyo}", estado=estado), "", []
    _volver_necrofear(d, a, 1, debil=sonda == "batalla")
    invocar(d, mio)
    faltas = escenario.comprobar(d, {"campo_yo": [mio], "campo_rival": [carta]})
    if faltas:
        return res(INVALIDA, "; ".join(faltas), estado=estado), "", []
    foto(d, fotos, f"necrofear_rival_{sonda}_armado")
    if sonda == "batalla":
        atacar(d)
    else:
        d.ir_mano("Raigeki")
        d.menu(0)
        for _ in range(3):
            d.tecla("A", 80)
    if not esperar(d, lambda: _zona_carta(d, a) == 0xD, 1200):
        return res(INVALIDA, "no pude destruir a la Dark Necrofear del rival", estado=estado), "", []
    d.g.correr(120)
    fase_destruida = _fase(d)[0]
    if mio not in controla(d, 0):
        return res(INVALIDA, f"{mio} no quedo en mi campo", estado=estado), "", []
    en_mano = len(d.mano())
    d.fin_turno(primero=False)
    # La IA elige sola: no hay aviso que cerrar. Se mira en que fase cambia el control.
    esperar(d, lambda: mio in controla(d, 1) or len(d.mano()) > en_mano, 6000)
    tomado, fase_control = mio in controla(d, 1), _fase(d)
    d.g.correr(60)
    equipada = _equipada_a(d, a, ranura_de(d, 0, mio))
    foto(d, fotos, f"necrofear_rival_{sonda}_control")
    if not hasta_mi_turno(d, n=en_mano):
        return None, (f"Dark Necrofear del rival destruida "
                      f"{'en batalla' if sonda == 'batalla' else 'por mi Raigeki'}: el duelo no sigue."), \
            ["con Necrofear del rival el duelo se detiene despues de mi End Phase"]
    despues = mio in controla(d, 1)
    foto(d, fotos, f"necrofear_rival_{sonda}_despues")
    visto = (f"Del rival, destruida {'en batalla por mi ' + mio if sonda == 'batalla' else 'por mi Raigeki'} en mi "
             f"{FASES.get(fase_destruida, fase_destruida)}: "
             + (f"en mi {FASES.get(fase_control[0], fase_control[0])} la IA elige sola a {mio}, que pasa a su campo, "
                f"y Necrofear {'queda equipada a el en la zona de Magicas del rival' if equipada else 'no queda equipada'}; "
                f"en mi turno siguiente {'sigue siendo suyo' if despues else 'ya no lo controla'}."
                if tomado else f"la IA no toma a {mio}."))
    fallas = []
    if not tomado:
        fallas.append("la IA no toma el control de mi monstruo")
    else:
        if fase_control != (5, 0):
            fallas.append(f"la IA toma el control fuera de mi End Phase (fase {fase_control})")
        if not despues:
            fallas.append("el control de la IA no dura")
        if not equipada:
            fallas.append("la Necrofear del rival no queda equipada a mi monstruo")
    return None, visto, fallas


def _necrofear_no(ruta_rom, desfase, fotos, sonda):
    """Casos en los que NO tiene que haber posesion, con un monstruo rival boca arriba en la End Phase:
      descarte  Necrofear en mi mano, descartada por Card Destruction del rival
      propio    Necrofear en mi campo, destruida por mi Offerings to the Doomed
    Devuelve (resultado sin veredicto o None, lo visto, fallas)."""
    carta, base, suyo = "Dark Necrofear", "Mechanicalchaser", "Mechanicalchaser"
    if sonda == "descarte":
        # Con la mano muerta la IA juega Card Destruction; despues roba a Mechanicalchaser y lo invoca.
        estado = armar(ruta_rom, "necrofear-no-descarte", yo={1: carta},
                       rival={0: "Card Destruction", 1: MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                       mazo_rival={0: MUERTA, 1: suyo, 2: suyo, 3: MUERTA, 4: MUERTA, 5: MUERTA, 6: MUERTA})
        d = abrir(ruta_rom, estado, desfase)
        a = ranura_de(d, 0, carta)
        aviso0 = _aviso(d)
        d.fin_turno(primero=True)
        como = "descartada de mi mano por Card Destruction del rival"
    else:
        estado = armar(ruta_rom, "necrofear-no-propio", yo={1: base}, mazo_yo={0: "Offerings to the Doomed"},
                       rival={0: suyo, 1: MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                       mazo_rival={i: MUERTA for i in range(4)})
        d = abrir(ruta_rom, estado, desfase)
        invocar(d, base)
        a = ranura_de(d, 0, base)
        _volver_necrofear(d, a, 0, debil=False)
        d.fin_turno(primero=True)
        if not hasta_mi_turno(d):
            return res(SIN_DISPARO, "no volvio mi turno", estado=estado), "", []
        d.g.correr(120)
        # Offerings es de juego rapido: con ella en la mano el juego pregunta en la Draw Phase y en la
        # Standby Phase si activo algo. No, hasta llegar a la Main Phase 1.
        for _ in range(4):
            if _fase(d)[0] >= 2:
                break
            d.tecla("DOWN", 30)
            d.tecla("A", 120)
        b = ranura_de(d, 1, suyo)
        if _fase(d) != (2, 0) or b is None or suyo not in controla(d, 1) or carta not in controla(d, 0):
            return res(SIN_DISPARO, f"no llegue a mi Main Phase 1 con {carta} y el {suyo} del rival en el campo",
                       estado=estado), "", []
        # Ayuda de prueba: la IA coloca a su monstruo boca abajo; se lo deja boca arriba en defensa
        # para que en la End Phase haya a quien poseer.
        d.g.w8(b + 0x33, 0x30)
        d.g.correr(30)
        d.ir_mano("Offerings to the Doomed")
        d.tecla("A", 60)                  # menu: Activate Effect / Set / Detail Screen (queda en Detail)
        d.tecla("UP", 30)
        d.tecla("UP", 30)
        d.tecla("A", 120)
        d.tecla("A", 80)                  # cierra "Select monster to destroy."
        d.mover(y=2)
        d.mover(x=2 + zona_monstruo(d, 0, carta))
        d.g.correr(30)
        d.tecla("A", 120)                 # elige a Necrofear
        d.tecla("A", 120)                 # cierra el aviso que sigue
        if not esperar(d, lambda: _zona_carta(d, a) == 0xD, 900, tecla_cada=0):
            return res(SIN_DISPARO, "no pude destruir a Dark Necrofear con Offerings to the Doomed",
                       estado=estado), "", []
        d.g.correr(200)
        aviso0 = _aviso(d)
        d.tecla("B", 50)                  # como fin_turno, pero sin esperar despues de la A: la End
        d.tecla("DOWN", 30)               # Phase dura menos de un segundo y hay que verla pasar
        d.tecla("A", 4)
        como = "destruida en mi campo por mi Offerings to the Doomed"
    # Hasta que pasa la End Phase del turno en que fue al cementerio: quien controla que, y si hubo aviso.
    lado_turno = 1 if sonda == "descarte" else 0
    visto = dict(aviso=False, en_fin=None, cementerio=False, pasado=False)

    def paso():
        f = _fase(d)
        visto["aviso"] = visto["aviso"] or _aviso(d) != aviso0
        visto["cementerio"] = visto["cementerio"] or _zona_carta(d, a) == 0xD
        if f == (5, lado_turno) and visto["cementerio"] and visto["en_fin"] is None:      # al entrar
            visto["en_fin"] = [m[0] for m in escenario.instantanea(d)["campo_rival"] if m[1] != "boca abajo"]
        if visto["en_fin"] is not None and f[1] != lado_turno:
            visto["pasado"] = True
        return visto["pasado"]

    esperar(d, paso, 6000, tecla_cada=60 if sonda == "descarte" else 90)
    d.g.correr(120)
    foto(d, fotos, f"necrofear_no_{sonda}")
    if not visto["cementerio"]:
        return res(SIN_DISPARO, "la IA no jugo Card Destruction", estado=estado), "", []
    mios = controla(d, 0)
    if not visto["en_fin"] and not visto["aviso"] and suyo not in mios:
        return res(SIN_DISPARO, "el rival no tenia un monstruo boca arriba en la End Phase: no hay a quien poseer",
                   estado=estado), "", []
    texto = (f"{como[0].upper() + como[1:]}, con {' y '.join(visto['en_fin'] or [])} boca arriba en el campo del rival: "
             + ("la End Phase pasa sin aviso y el rival conserva su monstruo."
                if visto["pasado"] and not visto["aviso"] and suyo not in mios
                else f"aviso {'si' if visto['aviso'] else 'no'}, mis monstruos despues {mios}."))
    fallas = []
    if visto["aviso"] or suyo in mios:
        fallas.append("hay posesion cuando no corresponde")
    if not visto["pasado"]:
        fallas.append("el turno no termina")
    return None, texto, fallas


def _necrofear_equipada(ruta_rom, desfase, fotos, sonda):
    """Con Necrofear ya equipada a un Mechanicalchaser del rival (posesion por batalla). Tres sondas:
      tormenta  mi Heavy Storm destruye a Necrofear: el monstruo tiene que volver al rival
      agujero   mi Dark Hole destruye al monstruo: Necrofear va al cementerio
      plumero   Harpie's Feather Duster del rival destruye a Necrofear: el monstruo vuelve y, aunque
                la destruyo un efecto del rival, en la End Phase no hay otra posesion
    Devuelve (resultado sin veredicto o None, lo visto, fallas)."""
    carta, base, suyo = "Dark Necrofear", "Mechanicalchaser", "Mechanicalchaser"
    mia = {"tormenta": "Heavy Storm", "agujero": "Dark Hole"}.get(sonda)
    estado = armar(ruta_rom, "necrofear-equipada-" + sonda, yo={1: base, 2: mia} if mia else {1: base},
                   rival={0: suyo, 1: MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                   mazo_rival={0: MUERTA, 1: MUERTA if mia else "Harpie's Feather Duster", 2: MUERTA, 3: MUERTA,
                               4: MUERTA})
    d = abrir(ruta_rom, estado, desfase)
    invocar(d, base)
    a = ranura_de(d, 0, base)
    _volver_necrofear(d, a, 0, debil=True)
    en_mano = len(d.mano())
    d.fin_turno(primero=True)
    if not esperar(d, lambda: _aviso(d) or len(d.mano()) > en_mano, 6000) or not _aviso(d):
        return res(SIN_DISPARO, "el rival no destruyo a Dark Necrofear o no salio el aviso", estado=estado), "", []
    d.g.correr(30)
    for _ in range(3):
        d.tecla("A", 80)
    if not hasta_mi_turno(d, n=en_mano):
        return res(SIN_DISPARO, "no volvio mi turno despues de la posesion", estado=estado), "", []
    b = ranura_de(d, 1, suyo)
    if suyo not in controla(d, 0) or not _equipada_a(d, a, b):
        return res(INVALIDA, "Necrofear no quedo equipada al monstruo del rival", estado=estado), "", []
    foto(d, fotos, f"necrofear_equipada_{sonda}_antes")
    if mia:
        d.ir_mano(mia)
        d.tecla("A", 60)                  # menu: Activate / Set / Detail Screen (queda en Detail)
        d.tecla("UP", 30)
        d.tecla("UP", 30)
        d.tecla("A", 120)
        for _ in range(3):
            d.tecla("A", 90)
        if not esperar(d, lambda: _zona_carta(d, a) == 0xD, 900, tecla_cada=0):
            return res(SIN_DISPARO, f"no pude jugar {mia}", estado=estado), "", []
        d.g.correr(200)
    else:
        en_mano = len(d.mano())
        d.fin_turno(primero=False)
        # El rival roba Harpie's Feather Duster y la juega; despues se deja pasar su End Phase. Si ahi
        # saliera el aviso de otra posesion, las A lo contestarian y el monstruo volveria a mi campo.
        esperar(d, lambda: _zona_carta(d, a) == 0xD or len(d.mano()) > en_mano, 6000)
        if _zona_carta(d, a) != 0xD:
            return res(SIN_DISPARO, "el rival no jugo Harpie's Feather Duster", estado=estado), "", []
        marcada = bool(d.g.r32(a + 0x60) & 0x40)
        if not hasta_mi_turno(d, n=en_mano):
            return None, "Necrofear equipada, destruida por Harpie's Feather Duster del rival: el duelo no sigue.", \
                ["el turno del rival no termina despues de destruir a Necrofear equipada"]
    foto(d, fotos, f"necrofear_equipada_{sonda}_despues")
    s = escenario.instantanea(d)
    mios, suyos = controla(d, 0), controla(d, 1)
    en_cementerio = carta in s["cementerio_yo"] and carta not in s["magias_yo"]
    fallas = []
    if not en_cementerio:
        fallas.append("Necrofear no va a mi cementerio")
    if sonda == "agujero":
        visto = (f"Equipada, y mi Dark Hole destruye al monstruo: {suyo} "
                 f"{'va al cementerio del rival' if suyo in s['cementerio_rival'] else 'no esta en el cementerio del rival'} "
                 f"y Necrofear {'va a mi cementerio' if en_cementerio else 'no va a mi cementerio'}.")
        if suyo not in s["cementerio_rival"] or suyo in mios or suyo in suyos:
            fallas.append("el monstruo destruido no va al cementerio de su dueno")
    else:
        con = "mi Heavy Storm" if mia else "Harpie's Feather Duster del rival"
        visto = (f"Equipada, y {con} la destruye: Necrofear {'va a mi cementerio' if en_cementerio else 'no va a mi cementerio'} "
                 f"y {suyo} {'vuelve al campo del rival' if suyo in suyos else 'no vuelve al rival'}"
                 + ("." if mia else f"; en la End Phase de ese turno {'no hay' if suyo not in mios else 'hay'} otra posesion."))
        if suyo not in suyos or suyo in mios:
            fallas.append("el monstruo no vuelve al rival al destruirse Necrofear"
                          if mia or not en_cementerio or carta in s["magias_yo"] else
                          "hay una segunda posesion despues de destruirla estando equipada")
        if not mia and marcada:
            fallas.append("queda marcada como destruida por el rival estando equipada")
    return None, visto, fallas


def caso_necrofear(ruta_rom, desfase, fotos):
    """La posesion. La invocacion (retirar 3 Demonios) se revisa por capturas: evidencia/ronda7."""
    vistos, fallas = [], []
    sondas = ([(_necrofear, s, s) for s in ("batalla", "efecto")]
              + [(_necrofear_rival, s, "del rival, " + s) for s in ("batalla", "efecto")]
              + [(_necrofear_no, s, "sin posesion, " + s) for s in ("descarte", "propio")]
              + [(_necrofear_equipada, s, "equipada, " + s) for s in ("tormenta", "agujero", "plumero")])
    for funcion, sonda, nombre in sondas:
        r, visto, f = funcion(ruta_rom, desfase, fotos, sonda)
        if r:
            return r
        vistos.append(visto)
        fallas += [f"{x} ({nombre})" for x in f]
    estado = os.path.join(LOTE, "necrofear-batalla.st")
    nota = "La invocacion (retirar 3 Demonios) no la cubre este caso: evidencia/ronda7/33-dark-necrofear."
    return res(EN_PARTE if fallas else FUNCIONA, " ".join(vistos + [nota]), "; ".join(fallas), estado=estado)


def _caso_equipo(ruta_rom, desfase, fotos, carta, monstruo, delta, turnos=1, descarta=False):
    """Equipo jugado desde la mano sobre mi monstruo: el ATK tiene que subir (o bajar) 'delta' y
    mantenerse cuando vuelve mi turno ('turnos' veces; si delta es una lista, el de cada turno)."""
    estado = armar(ruta_rom, "equipo-" + carta.split()[0].lower().strip("-"), yo={5: carta, 4: monstruo},
                   rival={0: MUERTA, 1: MUERTA, 2: MUERTA, 3: MUERTA, 4: MUERTA},
                   mazo_rival={0: MUERTA, 1: MUERTA})
    d = abrir(ruta_rom, estado, desfase)
    invocar(d, monstruo)
    faltas = escenario.comprobar(d, {"campo_yo": [monstruo]})
    if faltas:
        return res(INVALIDA, "; ".join(faltas), estado=estado)

    def atk():
        s = escenario.instantanea(d)
        return next((m[2] for m in s["campo_yo"] if m[0] == monstruo), None), s
    base, _ = atk()
    d.ir_mano(carta)
    d.menu(0)
    d.g.correr(120)
    foto(d, fotos, "equipo_aviso")
    if descarta:                          # "Discard hand.": elegir la carta que se descarta
        elegir_en_lista(d)
        d.g.correr(150)
    d.tecla("A", 80)                      # cierra "Select your monster to equip."
    d.tecla("A", 120)
    d.g.correr(150)
    a1, s1 = atk()
    foto(d, fotos, "equipo_equipada")
    if carta not in s1["magias_yo"]:
        return res(NO_FUNCIONA, f"{carta} no quedo en el campo (ATK {base} -> {a1})", "no se equipa", estado=estado)
    vistos = [a1]
    esperado = [base + (delta if not isinstance(delta, list) else delta[0])]
    for k in range(turnos):
        d.fin_turno(primero=(k == 0))
        if not hasta_mi_turno(d):
            return res(SIN_DISPARO, "no volvio mi turno", estado=estado)
        a, s = atk()
        vistos.append(a)
        if isinstance(delta, list):
            esperado.append(base + delta[min(k + 1, len(delta) - 1)])
        else:
            esperado.append(base + delta)
    detalle = f"{monstruo} ({base} de ATK) equipado con {carta}: ATK por turno {vistos}; esperado {esperado}."
    if vistos == esperado:
        return res(FUNCIONA, detalle, estado=estado)
    return res(EN_PARTE if vistos[0] == esperado[0] else NO_FUNCIONA, detalle, f"ATK {vistos}, esperado {esperado}", estado=estado)


CASOS = {
    "Dark Necrofear": caso_necrofear,
    "Electromagnetic Bagworm": caso_bagworm,
    "Dark-Eyes Illusionist": caso_dark_eyes,
    "Reaper of the Cards": caso_reaper,
    "Hiro's Shadow Scout": caso_hiro,
    "Kunai with Chain": caso_kunai,
    "Electric Snake": caso_electric_snake,
    "Minar": caso_minar,
    "Big Burn": caso_big_burn,
    "Penguin Knight": caso_penguin,
    "Lady Panther": caso_lady_panther,
    "Fairy Guardian": caso_fairy_guardian,
    "Reasoning": caso_reasoning,
    "Stim-Pack": lambda r, d, f: _caso_equipo(r, d, f, "Stim-Pack", "Blazing Inpachi", [700, 500], 2),
    "Butterfly Dagger - Elma": lambda r, d, f: _caso_equipo(r, d, f, "Butterfly Dagger - Elma", "Blazing Inpachi", 300),
    "Fusion Sword Murasame Blade": lambda r, d, f: _caso_equipo(r, d, f, "Fusion Sword Murasame Blade", "Axe Raider", 800),
    "Shooting Star Bow - Ceal": lambda r, d, f: _caso_equipo(r, d, f, "Shooting Star Bow - Ceal", "Blazing Inpachi", -1000),
    "Wicked-Breaking Flamberge - Baou": lambda r, d, f: _caso_equipo(r, d, f, "Wicked-Breaking Flamberge - Baou", "Blazing Inpachi", 500, descarta=True),
    "Twin Swords of Flashing Light - Tryce": lambda r, d, f: _caso_equipo(r, d, f, "Twin Swords of Flashing Light - Tryce", "Blazing Inpachi", -500, descarta=True),
}


# --- corredor ---------------------------------------------------------------------------
def correr_carta(ruta_rom, carta, corridas, fotos):
    salidas = []
    for k in range(corridas):
        for intento in range(REINTENTOS):    # la IA decide con azar: si no dispara, otra oportunidad
            try:
                r = CASOS[carta](ruta_rom, k + 7 * intento, os.path.join(fotos, f"corrida{k + 1}") if fotos else None)
            except (AssertionError, RuntimeError) as err:  # el corredor no llego a la carta o al menu
                r = res(INVALIDA, f"el corredor se detuvo: {err}")
            if r["resultado"] != SIN_DISPARO:
                break
        print(f"  corrida {k + 1}: {r['resultado']}")
        print(f"     {r['detalle']}")
        if r["falla"]:
            print(f"     falla: {r['falla']}")
        salidas.append(r)
    distintos = {r["resultado"] for r in salidas}
    final = salidas[0]["resultado"] if len(distintos) == 1 else "INESTABLE"
    print(f"  RESULTADO: {final}" + ("" if len(distintos) == 1 else f" ({sorted(distintos)})"))
    return final, salidas[0]


def registrar(ruta_rom, veredictos):
    rom, filas = Rom(ruta_rom), registro.leer()
    for carta, r in veredictos.items():
        fila = next(f for f in filas if f["carta"] == carta)
        fila.update(veredicto=VEREDICTOS[r["resultado"]], detalle=r["detalle"], falla=r["falla"],
                    ev_auto=f'python3 scripts/probar_lote.py ROM "{carta}"', rom_md5=rom.md5,
                    estado=r.get("estado", ""), fecha=datetime.date.today().isoformat(),
                    ev_ojo="no" if r["resultado"] == NO_FUNCIONA else "pendiente", nota_ojo="")
    registro.EN_CURSO = True                 # las cartas que aun no se probaron pueden seguir vacias
    registro.validar(filas, rom)
    registro.escribir(filas)
    print(f"registrados en datos/pruebas.csv: {', '.join(veredictos)}")


def main(argv):
    if argv == ["--listar"]:
        print("\n".join(CASOS))
        return 0
    opciones = {"--corridas": "3", "--fotos": None}
    args, hacer_registro, k = [], False, 0
    while k < len(argv):
        if argv[k] in opciones:
            opciones[argv[k]] = argv[k + 1]
            k += 2
        elif argv[k] == "--registrar":
            hacer_registro = True
            k += 1
        else:
            args.append(argv[k])
            k += 1
    if not args or not os.path.exists(args[0]):
        raise SystemExit(__doc__)
    ruta_rom, cartas = args[0], args[1:] or list(CASOS)
    desconocidas = [c for c in cartas if c not in CASOS]
    if desconocidas:
        raise SystemExit(f"error: no hay caso para {desconocidas}. Casos: {', '.join(CASOS)}")
    veredictos, pendientes = {}, []
    for carta in cartas:
        print(f"=== {carta}")
        final, r = correr_carta(ruta_rom, carta, int(opciones["--corridas"]), opciones["--fotos"])
        if final in VEREDICTOS:
            veredictos[carta] = r
        else:
            pendientes.append(carta)
    if hacer_registro and veredictos:
        registrar(ruta_rom, veredictos)
    if pendientes:
        print("sin veredicto:", ", ".join(pendientes))
    return 1 if pendientes else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
