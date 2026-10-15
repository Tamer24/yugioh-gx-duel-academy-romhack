"""Arma un estado por carta para que Oscar las revise a ojo, a partir de un estado suyo.

Parte de un estado guardado en el primer turno de un duelo (por defecto el slot 1 del ROM
(Lote) en build/) y escribe en estados/revisar/ una copia por carta, con la carta en la mano y
la mano y el mazo del rival preparados para que su efecto se pueda ver. El estado de partida
no se modifica. Tambien escribe la guia con los pasos de cada una.

Uso (desde la raiz del proyecto):
  python3 scripts/armar_revision.py ROM [ESTADO_BASE]

Posiciones de la mano del estado de Oscar del 2026-10-10: 0 Trap Hole (Trampa), 1 Inferno,
2 Upstart Goblin (Magica), 3 Darkfire Soldier #2 (1700, nivel 4), 4 The Thing in the Crater
(1000, nivel 4), 5 Twin-Headed Fire Dragon. Las cartas de prueba van a 0 (Trampas), 1
(monstruos) y 2 (Magicas); Darkfire Soldier #2 queda como monstruo de apoyo.
"""
import os
import sys

import escenario
import registro

RAIZ = registro.RAIZ
SALIDA = os.path.join("estados", "revisar")
GUIA = os.path.join("specs", "001-cerrar-pruebas-lote", "guia-oscar.md")
BASE = os.path.join("build", "Yu-Gi-Oh! GX - Duel Academy (Lote).ss1")
M = "Blue-Eyes White Dragon"           # relleno: el rival no puede jugarlo
MUERTA = {i: M for i in range(5)}
MAZO_MUERTO = {i: M for i in range(8)}   # 8: Card Destruction hace reponer 5
APOYO = "Darkfire Soldier #2"


def rival(**cartas):
    """Mano del rival: relleno salvo las posiciones dadas (p0="Carta", p4="Otra")."""
    return {**MUERTA, **{int(k[1:]): v for k, v in cartas.items()}}


SET = "colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`)"
SET_M = SET[0].upper() + SET[1:]
YES = "cuando el juego pregunte, *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*"

# (seccion, carta, argumentos de escenario.armar, pasos, que deberias ver)
CARTAS = [
    ("Monstruos de volteo", "Rigorous Reaver",
     dict(yo={1: "Rigorous Reaver"}, rival=rival(p0="Mechanicalchaser"), mazo_rival=MAZO_MUERTO),
     f"{SET_M}. El rival invoca a Mechanicalchaser y la ataca.",
     "Los dos jugadores descartan 1 carta y Mechanicalchaser pierde 500 ATK."),
    ("Monstruos de volteo", "Jowls of Dark Demise",
     dict(yo={1: "Jowls of Dark Demise"}, rival=rival(p0="Mechanicalchaser"), mazo_rival=MAZO_MUERTO),
     f"{SET_M}. Cuando Mechanicalchaser la ataque te pide elegir un monstruo rival: elegilo.",
     "Mechanicalchaser pasa a tu campo ese turno."),
    ("Monstruos de volteo", "Electromagnetic Bagworm",
     dict(yo={1: "Electromagnetic Bagworm"}, rival=rival(p0="Mechanicalchaser"), mazo_rival=MAZO_MUERTO),
     f"{SET_M}. Aviso \"Select opponent's Machine monster to gain control of.\": `A`, `A` sobre "
     "Mechanicalchaser, `A`.",
     "Antes del aviso Mechanicalchaser baja de 1850/800 a 1350/300: pierde 500 por destruir a Bagworm en batalla. "
     "Después pasa a tu campo, sigue siendo tuyo durante tu turno siguiente y vuelve al rival cuando terminás ese "
     "turno, siempre con 1350/300."),
    ("Monstruos de volteo", "Dark-Eyes Illusionist",
     dict(yo={1: "Dark-Eyes Illusionist"}, rival=rival(p0="Tongyo"), mazo_rival=MAZO_MUERTO),
     f"{SET_M}. Tongyo (1350) la ataca y no la destruye (DEF 1400). Te pide un objetivo: elegí a Tongyo. "
     "Si el rival no ataca en su primer turno, terminá el tuyo otra vez.",
     "Mientras Dark-Eyes siga boca arriba, Tongyo no vuelve a atacar."),
    ("Monstruos de volteo", "Reaper of the Cards",
     dict(yo={1: "Reaper of the Cards"}, nivel_yo={1: 4}, rival=rival(p4="Call of the Haunted"),
          mazo_rival={0: M, 1: "Giant Orc", 2: M, 3: M}),
     f"{SET_M}. El rival coloca una carta boca abajo. Terminá también tu segundo turno: el rival roba a "
     "Giant Orc y ataca. Aviso \"Select Trap Card to destroy.\": `A`, `ARRIBA` hasta la carta boca abajo, `A`.",
     "La carta boca abajo era Call of the Haunted y se destruye. (Es de nivel 5; en este estado se coloca sin "
     "tributo porque le cambié el nivel dentro del estado.)"),

    ("Trampas", "Windstorm of Etaqua",
     dict(yo={0: "Windstorm of Etaqua"}, rival=rival(p0="Mechanicalchaser"), mazo_rival=MAZO_MUERTO),
     f"{SET_M}. El rival invoca a Mechanicalchaser y ataca: {YES}.",
     "Mechanicalchaser cambia de posición."),
    ("Trampas", "Kunai with Chain",
     dict(yo={0: "Kunai with Chain"}, rival=rival(p0="Mechanicalchaser"), mazo_rival=MAZO_MUERTO),
     f"{SET_M}. El rival ataca: {YES}.",
     "El atacante pasa a defensa y, como no tenés monstruos, Kunai va al cementerio. El segundo efecto (equiparla) "
     "está en la fila 30."),
    ("Trampas", "Magic Drain",
     dict(yo={0: "Magic Drain"}, rival=rival(p0="Dian Keto the Cure Master"), mazo_rival=MAZO_MUERTO),
     f"{SET_M}. El rival juega Dian Keto: \"Will you chain?\" → {YES}.",
     "Dian Keto se niega y se destruye: el rival sigue en 8000 LP."),
    ("Trampas", "Mystical Refpanel",
     dict(yo={0: "Mystical Refpanel"}, rival=rival(p0="Dian Keto the Cure Master"), mazo_rival=MAZO_MUERTO),
     f"{SET_M}. El rival juega Dian Keto: \"Will you chain?\" → {YES}.",
     "Los 1000 LP los ganás vos: quedás en 9000 y el rival en 8000."),
    ("Trampas", "Riryoku Field",
     dict(yo={0: "Riryoku Field"}, rival=rival(p0="Mechanicalchaser", p1="Black Pendant"), mazo_rival=MAZO_MUERTO),
     f"{SET_M}. El rival invoca a Mechanicalchaser y le equipa Black Pendant: \"Will you chain?\" → {YES}.",
     "Black Pendant se niega y se destruye."),
    ("Trampas", "Big Burn",
     dict(yo={0: "Big Burn"}, rival=rival(p0="Card Destruction"),
          mazo_rival={0: M, 1: "Monster Reborn", 2: M, 3: M, 4: M, 5: M, 6: M}),
     f"{SET_M}. El rival juega Card Destruction (los dos descartan la mano) y después Monster Reborn: "
     f"`A` en el aviso del objetivo, \"Will you chain?\" → {YES}.",
     "Todos los monstruos de los dos cementerios se retiran del juego y Monster Reborn no invoca nada."),
    ("Trampas", "Acid Trap Hole",
     dict(yo={0: "Acid Trap Hole"}, rival=rival(p0="Tongyo"), mazo_rival=MAZO_MUERTO),
     f"Invocá a {APOYO}, colocá la trampa y terminá el turno. El rival coloca a Tongyo boca abajo. En tu turno "
     "siguiente: cursor sobre la trampa, `A`, *Activate Effect*, y elegí ese monstruo.",
     "Tongyo se voltea y se destruye."),
    ("Trampas", "Two-Pronged Attack",
     dict(yo={0: "Two-Pronged Attack"}, rival=rival(p0="Tongyo"), mazo_rival=MAZO_MUERTO),
     f"Turno 1: invocá a {APOYO} y colocá la trampa. Turno 2: invocá a The Thing in the Crater. Activá la trampa y "
     "elegí tus dos monstruos y el del rival.",
     "Los tres van al cementerio."),
    ("Trampas", "Ready for Intercepting",
     dict(yo={0: "Ready for Intercepting", 1: "Sonic Maid"}, rival=MUERTA, mazo_rival=MAZO_MUERTO),
     "Turno 1: invocá a Sonic Maid (Guerrero) y colocá la trampa. Turno 2: activá la trampa sobre Sonic Maid.",
     "Sonic Maid queda boca abajo en defensa."),

    ("Mágicas", "The Inexperienced Spy",
     dict(yo={2: "The Inexperienced Spy"}),
     "Activala (menú de la carta, *Activate Effect*).",
     "Se muestra 1 carta al azar de la mano del rival (una de Penguin Soldier, Dekoichi, Fusion Sage, Snatch Steal o Hane-Hane). `B` cierra la lista y la carta va al cementerio."),
    ("Mágicas", "Exchange",
     dict(yo={2: "Exchange"}),
     "Activala. `A` en el aviso, `A` sobre *ALL*, `A` sobre una carta, icono de la mano que apunta (*DECIDE*, el "
     "4.º), `A`.",
     "Esa carta pasa a tu mano y una tuya, al azar, a la del rival."),
    ("Mágicas", "Chosen One",
     dict(yo={2: "Chosen One", 1: "Dian Keto the Cure Master"}),
     f"Activala y marcá 1 monstruo ({APOYO}) y 2 Mágicas o Trampas (Trap Hole y Dian Keto).",
     "El rival saca una al azar. Si es el monstruo, se invoca y las otras 2 van al cementerio; si no, las 3."),
    ("Mágicas", "Seal of the Ancients",
     dict(yo={2: "Seal of the Ancients"}, rival=rival(p0="Tongyo", p4="Call of the Haunted"), mazo_rival=MAZO_MUERTO),
     f"Turno 1: invocá a {APOYO} y terminá. El rival coloca cartas boca abajo. Turno 2: activala.",
     "Pagás 1000 LP y ves, en destellos rápidos, qué son las cartas boca abajo del rival."),
    ("Mágicas", "Share the Pain",
     dict(yo={2: "Share the Pain"}, rival=rival(p0="Tongyo"), mazo_rival=MAZO_MUERTO),
     f"Turno 1: invocá a {APOYO} y terminá. El rival coloca a Tongyo. Turno 2: activala y tributá a {APOYO}.",
     "El rival pierde a Tongyo."),
    ("Mágicas", "Riryoku",
     dict(yo={2: "Riryoku"}, rival=MUERTA, mazo_rival=MAZO_MUERTO),
     f"Turno 1: invocá a {APOYO}. Turno 2: invocá a The Thing in the Crater, activala y elegí los dos.",
     "El primero pierde la mitad del ATK y el segundo la gana, hasta el fin del turno."),
    ("Mágicas", "Monster Recovery",
     dict(yo={2: "Monster Recovery"}),
     f"Invocá a {APOYO} y activala.",
     f"{APOYO} y las 4 cartas de tu mano vuelven al mazo, y robás 4 (las que tenías en la mano)."),

    ("Monstruo con efecto en el campo", "Goddess of Whim",
     dict(yo={1: "Goddess of Whim"}, rival=MUERTA, mazo_rival=MAZO_MUERTO),
     "Invocala. Cursor sobre ella, `A`, *Activate Effect*, elegí cara o cruz.",
     "Avisa si acertaste y el ATK pasa de 950 a 1900 o a 475 hasta el fin del turno."),

    ("Arregladas el 2026-10-11: \"por un efecto del rival\"", "Electric Snake",
     dict(yo={1: "Electric Snake"}, rival=rival(p0="Card Destruction"), mazo_rival=MAZO_MUERTO),
     "Terminá el turno sin jugar nada. El rival juega Card Destruction y descarta tu mano.",
     "Robás 2 cartas de más: quedás con 8 en la mano (las 6 que repone Card Destruction y las 2 de Electric Snake) "
     "en vez de 6."),
    ("Arregladas el 2026-10-11: \"por un efecto del rival\"", "Minar",
     dict(yo={1: "Minar"}, rival=rival(p0="Card Destruction"), mazo_rival=MAZO_MUERTO),
     "Terminá el turno sin jugar nada. El rival juega Card Destruction y descarta tu mano.",
     "El rival pierde 1000 LP (queda en 7000)."),
    ("Arregladas el 2026-10-11: \"por un efecto del rival\"", "Penguin Knight",
     dict(mazo_yo={2: "Penguin Knight"}, rival=rival(p0="Needle Worm"), mazo_rival=MAZO_MUERTO),
     f"Turno 1: invocá a {APOYO} y terminá. El rival coloca a Needle Worm boca abajo. Turno 2: `B`, *Enter Battle "
     "Phase*, y atacalo.",
     "Needle Worm manda 5 cartas de tu mazo al cementerio, Penguin Knight entre ellas, y enseguida todo tu "
     "cementerio vuelve al mazo, que se baraja: el cementerio queda vacío."),
    ("Arregladas el 2026-10-11: \"por un efecto del rival\"", "Fairy Guardian",
     dict(yo={1: "Fairy Guardian", 2: "Dian Keto the Cure Master"}, rival=rival(p0="Magic Jammer"),
          mazo_rival=MAZO_MUERTO),
     "Turno 1: invocá a Fairy Guardian y terminá. El rival coloca Magic Jammer. Turno 2: activá Dian Keto; el rival "
     "la niega. En ese mismo turno: cursor sobre Fairy Guardian, `A`, *Activate Effect*. Aviso \"Select Spell Card "
     "to return to the Deck.\": `A`, `A` sobre *ALL*, `A` sobre Dian Keto, icono de la mano que apunta (el 4.º), `A`.",
     "Fairy Guardian se tributa y Dian Keto sale de tu cementerio y vuelve al fondo de tu mazo."),
    ("Arreglada en la revisión por capturas", "Lady Panther",
     dict(yo={1: "Lady Panther", 3: "Giant Soldier of Stone"}, rival=rival(p0="Mechanicalchaser"),
          mazo_rival=MAZO_MUERTO),
     "Turno 1: colocá boca abajo a Giant Soldier of Stone (DEF 2000) y terminá. El rival invoca a Mechanicalchaser "
     "(1850) y lo ataca: rebota (el rival pierde 150) y Giant Soldier queda boca arriba en defensa. Turno 2: invocá "
     "a Lady Panther; en el menú de Giant Soldier of Stone elegí *Attack Position*; `B`, *Enter Battle Phase*, y "
     "atacá con él (1300) a Mechanicalchaser: pierde, va al cementerio y vos perdés 550 LP. Después `B`, *Go to "
     "Main Phase 2*, cursor sobre Lady Panther, `A`, *Activate Effect*. Unos segundos después sale el aviso "
     "\"Select monster to return to the Deck.\": `A`, `A` sobre *ALL*, `A` sobre Giant Soldier of Stone, icono de "
     "la mano que apunta (el 4.º), `A`.",
     "Lady Panther se tributa y Giant Soldier of Stone vuelve al tope de tu mazo: lo robás en tu turno siguiente. "
     "Antes el menú no ofrecía *Activate Effect*."),

    ("Variantes que pidió Oscar", "Magic Drain",
     dict(yo={0: "Magic Drain"}, rival=rival(p0="Dian Keto the Cure Master", p1="Black Pendant", p2="Black Pendant"),
          mazo_rival=MAZO_MUERTO),
     f"Igual que el 8, pero el rival tiene además 2 Mágicas en la mano (Black Pendant, que no puede jugar porque "
     f"no tiene monstruos). {SET_M}. El rival juega Dian Keto: \"Will you chain?\" → {YES}.",
     "El texto dice que el rival **puede** descartar 1 Mágica para negar a Magic Drain. Mirá si lo hace: si "
     "descarta, Dian Keto cura (rival en 9000) y le queda una Mágica menos; si no, Dian Keto se niega como en el 8."),
    ("Variantes que pidió Oscar", "Windstorm of Etaqua",
     dict(yo={0: "Windstorm of Etaqua"}, rival=rival(p0="Mechanicalchaser", p1="Tongyo"), mazo_rival=MAZO_MUERTO),
     f"Igual que el 6, pero con dos monstruos rivales. {SET_M}. Mientras el rival tenga un solo monstruo, cada vez que "
     f"el juego pregunte contestá *No* (te va a atacar directo). Terminá tu segundo turno: el rival invoca a "
     f"Tongyo y ataca con los dos; ahí {YES}.",
     "Los dos monstruos boca arriba del rival cambian de posición, no solo el que ataca."),

    ("Completadas el 2026-10-11", "Kunai with Chain",
     dict(yo={0: "Kunai with Chain"}, rival=MUERTA, mazo_rival=MAZO_MUERTO),
     f"Segundo efecto. Turno 1: invocá a {APOYO} (1700), colocá Kunai boca abajo y terminá. Al empezar el turno del "
     "rival el juego pregunta \"It's the Draw Phase. Activate the effect...?\": *Yes*, `A`, llevá el cursor a tu "
     f"trampa, `A`, *Activate Effect*. Aviso \"Select your monster to equip.\": `A`, `A` sobre {APOYO}.",
     f"{APOYO} pasa de 1700 a 2200 de ATK y Kunai queda boca arriba en el campo, equipada. Si después tributás o "
     "te destruyen ese monstruo, Kunai va al cementerio con él."),
    ("Completadas el 2026-10-11", "Hiro's Shadow Scout",
     dict(yo={1: "Hiro's Shadow Scout"}, rival=rival(p0="Mechanicalchaser"),
          mazo_rival={**MAZO_MUERTO, 1: "Dian Keto the Cure Master", 3: "Call of the Haunted"}),
     f"{SET_M}. El rival invoca a Mechanicalchaser y la ataca.",
     "El rival roba 3 cartas (antes robaba 1) y se muestran: Dian Keto, que es Mágica, va a su cementerio; Blue-Eyes "
     "y Call of the Haunted quedan en su mano (después coloca la Trampa)."),
    ("Completadas el 2026-10-11", "Reasoning",
     dict(yo={2: "Reasoning"}, mazo_yo={0: "Dian Keto the Cure Master", 1: "Call of the Haunted", 2: "Mechanicalchaser"},
          rival=MUERTA, mazo_rival=MAZO_MUERTO),
     "Activala (menú de la carta, *Activate Effect*). Aviso \"Your opponent declares Level N.\": `A`.",
     "Se revelan Dian Keto, Call of the Haunted y Mechanicalchaser (nivel 4). Si el aviso decía 4, las tres van al "
     "cementerio. Si decía 3 o 2, Mechanicalchaser se invoca (\"Select card position.\") y las otras dos van al "
     "cementerio. El nivel lo elige el juego: 4 la mayoría de las veces. Probala un par de veces para ver las dos."),
    ("Completadas el 2026-10-11", "Dark Necrofear",
     dict(yo={2: "Card Destruction", 1: "Feral Imp", 3: "Lord of the Lamp", 4: "La Jinn the Mystical Genie of the Lamp"},
          mazo_yo={0: "Dark Necrofear", 5: "Heavy Storm"}, rival=MUERTA,
          mazo_rival={**MAZO_MUERTO, 0: "Goblin Attack Force"}),
     "Activá Card Destruction: tus tres Demonios van al cementerio y robás a Dark Necrofear. Menú de Necrofear, "
     "*Special Summon*; aviso \"Select 3 Fiend monsters to remove from the Graveyard.\": `A`, `A` (entra a la "
     "lista), y en cada Demonio `A`, `A` (icono *CHECK*); con los tres marcados, `A`, `DERECHA` cuatro veces hasta "
     "*DECIDE*, `A`. Posición de ataque (`A`) y terminá el turno. El rival invoca a Goblin Attack Force (2300) y "
     "ataca a Necrofear (2200). Al final de su turno, aviso \"Select and gain control of 1 opponent's face-up "
     "monster.\": `A`, `A` sobre Goblin Attack Force. En tu turno robás Heavy Storm: terminá ese turno sin "
     "jugarla, dejá pasar el del rival y, en tu turno siguiente, activala.",
     "Necrofear se invoca retirando los tres Demonios. Cuando la destruyen perdés 100 LP y va al cementerio; "
     "Goblin Attack Force sigue siendo del rival durante el resto de su turno y recién en la End Phase se muestra "
     "la carta de Necrofear y aparece el aviso. Al elegirlo pasa a tu campo y Necrofear queda boca arriba en tu "
     "zona de Mágicas y Trampas, equipada a él. Sigue siendo tuyo en tus turnos siguientes. Cuando Heavy Storm "
     "destruye a Necrofear, va a tu cementerio y Goblin Attack Force vuelve al campo del rival."),
]


def archivo(numero, carta):
    limpio = "".join(c if c.isalnum() else "-" for c in carta.lower()).strip("-")
    while "--" in limpio:
        limpio = limpio.replace("--", "-")
    return os.path.join(SALIDA, f"{numero:02d}-{limpio}.ss1")   # mGBA solo ofrece abrir .ss0 a .ss9


CABECERA = """# Guía para Oscar: qué mirar y cómo

Este archivo lo genera `scripts/armar_revision.py`; para cambiarlo se cambia ese script.

Las 30 cartas ya tienen veredicto. Las filas 1 a 29 se jugaron por script, con capturas
(`evidencia/index.html`); las filas 3, 23 a 26 y 30 a 33 son de cartas arregladas o completadas después de
esas capturas (y vueltas a jugar). Lo que queda es que confirmes vos las que quieras ver. Cada estado de `estados/revisar/` sale de **tu** estado (`{base}`): mismo duelo, mismo
rival, primer turno, con la carta ya en tu mano y la mano del rival preparada.

## Cómo se usa

1. Abrí en mGBA el ROM **`build/Yu-Gi-Oh! GX - Duel Academy (Lote).gba`**.
2. *Archivo → Cargar estado desde archivo...* y elegí el estado de la carta.
3. Seguí los pasos y compará con "Qué deberías ver".
4. Avisame carta por carta: "la vi bien" o qué viste distinto. Yo lo registro.

Para tener en cuenta:

- El panel de abajo puede mostrar el nombre de otra carta hasta que muevas el cursor.
- Las cartas restauradas muestran el dibujo del monstruo que reemplazan. Es esperado.
- Es el primer turno del duelo: no hay Battle Phase. Para terminar el turno: `B`, `A`.
- En casi todos los estados el rival tiene la mano llena de Blue-Eyes White Dragon. Es a
  propósito: no puede jugarlos, así su turno es corto y hace siempre lo mismo.
- Tu mano conserva las cartas de tu estado salvo las que reemplacé: {apoyo} (1700) es el
  monstruo de apoyo en varios pasos.
"""

COLA = """
## Para tener presente

Reasoning: el nivel lo declara siempre el juego (no hay menú para que lo declare una persona), también
si la carta la activara el rival.

Se edita el **estado de un duelo** (manos y mazo de los dos lados). El archivo `.sav` no lo
sé editar todavía: su formato no está ubicado.
"""


def main(argv):
    if not argv or not os.path.exists(argv[0]):
        raise SystemExit(__doc__)
    ruta_rom = argv[0]
    base = argv[1] if len(argv) > 1 else os.path.join(RAIZ, BASE)
    if not os.path.exists(base):
        raise SystemExit(f"error: no existe el estado de partida {base}")
    os.makedirs(os.path.join(RAIZ, SALIDA), exist_ok=True)
    rom = escenario.Rom(ruta_rom)
    lineas = [CABECERA.format(base=os.path.relpath(base, RAIZ), apoyo=APOYO)]
    seccion = None
    for numero, (sec, carta, cambios, pasos, esperado) in enumerate(CARTAS, 1):
        relativa = archivo(numero, carta)
        escenario.armar(rom, base, os.path.join(RAIZ, relativa), cursor=None, **cambios)
        if sec != seccion:
            seccion = sec
            lineas.append(f"\n## {sec}\n\n| N.º | Carta | Estado | Pasos | Qué deberías ver |\n|---|---|---|---|---|")
        lineas.append(f"| {numero} | {carta} | `{relativa}` | {pasos} | {esperado} |")
        print(f"{numero:2} {carta:26} {relativa}")
    lineas.append(COLA)
    with open(os.path.join(RAIZ, GUIA), "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))
    print(f"guia: {GUIA}")


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except escenario.ErrorEscenario as err:
        raise SystemExit(f"error: {err}")
