# Cómo probar las cartas restauradas

ROM de prueba: `build/Yu-Gi-Oh! GX - Duel Academy (Test).gba`. Trae todo junto:
las 30 cartas, los parches, **3 copias de cada carta en el baúl al empezar** y
**contraseñas gratis** (la máquina pregunta por los 1000 DP pero no los descuenta).

> **ROMs en `build/`:** solo queda el de la prueba en curso. Los demás se
> regeneran exactos desde su `.bps`:
> `python3 scripts/bps.py --aplicar "<ROM original>.gba" build/test.bps "build/Yu-Gi-Oh! GX - Duel Academy (Test).gba"`
> (también `prueba3`, `menu6`, `candidatas`, `spy`). `parche_efecto.py` usa
> `Test` como base: regeneralo primero.

## Pasos

1. Abrí el ROM en el emulador y empezá una **partida nueva**: las cartas se
   entregan al crear la partida, no aparecen en una partida ya guardada.
2. Avanzá la introducción hasta llegar a tu cuarto.
3. Abrí la PDA, *Edit Deck*. Las 30 cartas ya están en el baúl, marcadas como
   nuevas. Ordenado por número, el número de cada carta está en la tabla.
   Armá un mazo con pocas cartas distintas así salen seguido.
4. Buscá un duelo en el mapa y fijate en lo que dice la columna "Qué mirar".
5. Anotá por carta: **anda**, **anda a medias** (qué parte falla) o **no anda**.

Las contraseñas de la tabla siguen sirviendo en la tienda (*Use Password
Machine*) si querés más copias.

El dibujo de cada carta es todavía el del monstruo que reemplaza.

## Revisión por capturas (sin ventana, de a pasos)

`scripts/paso.py` juega un duelo de a pasos: cada llamada carga donde quedó la anterior, aprieta
botones, saca capturas y muestra el duelo leído de la memoria. Con eso un subagente (o cualquiera)
sigue la fila de la guía y mira lo que mira una persona. Instrucciones: `evidencia/COMO-REVISAR.md`.

```
ROM="build/Yu-Gi-Oh! GX - Duel Academy (Lote).gba"
python3 scripts/paso.py "$ROM" evidencia/rondaN/NN-carta --desde estados/revisar/NN-carta.ss1
python3 scripts/paso.py "$ROM" evidencia/rondaN/NN-carta "mano:Carta" "A w50 UP*2 f A w120"
python3 scripts/armar_evidencia.py evidencia           # galería: evidencia/index.html
python3 scripts/repetir_sesion.py "$ROM" evidencia/ronda*/*    # regresión tras rearmar el ROM
```

`repetir_sesion.py` vuelve a jugar cada sesión con las mismas teclas y compara la memoria paso a
paso con su `registro.txt`. Tiene que dar `IGUAL` salvo en las sesiones anteriores a un arreglo. Con
el ROM `(Lote)` de hoy (MD5 `57e98b8c…`, corrida del 2026-10-12) son 41 `IGUAL` y 11 `DISTINTA`: `ronda1/03`, `ronda1/15`,
`ronda1/23`, `ronda1/24`, `ronda1/25`, `ronda1/27`, `ronda1/28`, `ronda2/17`, `ronda3/22`, `ronda4/27`
(no se puede repetir: le falta el paso 0) y `ronda6/03`. Las de `ronda7` y `ronda8` dan `IGUAL`.

Tarda unos 2 minutos y usa 1,7 GB de memoria. **Correrla de a un proceso por vez.**

La revisión por capturas **no reemplaza** la columna "A ojo": esa es de Oscar.

## Pruebas automáticas (sin ventana)

El proyecto maneja el juego por script con el núcleo libretro de mGBA
(`scripts/gba.py` y `scripts/duelo_auto.py`): carga un estado, aprieta botones, lee
la RAM (LP, manos, campo, cementerio) y saca capturas. Funciona en la Mac.

**Preparación (una vez)**

```
mkdir -p nucleos && cd nucleos
curl -O https://buildbot.libretro.com/nightly/apple/osx/arm64/latest/mgba_libretro.dylib.zip
unzip mgba_libretro.dylib.zip && rm mgba_libretro.dylib.zip
pip install pillow unicorn capstone      # en un entorno aparte
```

**Pruebas hechas**

| Script | Qué comprueba |
|---|---|
| `scripts/prueba_seal.py ROM` | Termina el turno, deja jugar al rival, activa Seal y comprueba que paga 1000 LP y sale de la mano. Pasa. |
| `scripts/test_spy.py ROM` | La función de la Spy con un duelo armado a mano (Unicorn). |
| `scripts/test_seal.py ROM` | El costo de Seal (Unicorn). |
| `scripts/test_exchange.py`, `test_chosen.py`, `test_share.py`, `test_kunai.py`, `test_two_pronged.py`, `test_ganchos_campo.py`, `test_hiro.py`, `test_bagworm.py`, `test_enviada_por_rival.py`, `test_reasoning.py`, `test_necrofear.py` `ROM` | La lógica de cada pieza nueva (Unicorn). `test_enviada_por_rival.py` cubre el gancho de "enviada al cementerio por un efecto del rival", Penguin Knight y Fairy Guardian. `test_bagworm.py` acepta el ROM original como segundo argumento para comprobar que ningún otro ID cambió de rama. |
| `scripts/test_arte.py ROM` | El conversor de dibujos, ida y vuelta con arte del propio juego, y que el dibujo chico (el de los sobres) salga parecido al del juego. |
| `scripts/test_sobres.py ROM_ORIGINAL` | `scripts/sobres.py`: leer los 48 sobres, cambiarles cartas, nombre y precio, y rechazar lo que colgaría el juego (menos comunes que cartas por sobre). Sin emulador. |
| `scripts/probar_sobres.py ROM [SOBRE] [--cuantos 5]` | Compra un sobre en la tienda desde `estados/tienda.ss1` (estado de Oscar: 3000 DP, sobres 0 a 3 en venta) y comprueba DP, cantidad en venta, cuántas cartas entraron al baúl y que todas sean de ese sobre. Sirve en el ROM `(Lote)` y en el `(Ampliado)`. |
| `scripts/test_modificadores.py ROM datos/volcado_goddess` | Goddess of Whim y Riryoku: moneda y modificadores de ATK (Unicorn). |
| `scripts/probar_lote.py ROM`, `probar_trampas.py`, `probar_cadena.py` | Duelos armados por carta, 3 corridas cada uno. `probar_lote.py --listar` muestra los 13 casos. |
| `scripts/repetir_sesion.py ROM evidencia/ronda*/*` | Regresión: repite las partidas grabadas y compara. Las sesiones de una carta que después se arregló dan DISTINTA (es lo esperado): la evidencia vigente de cada carta es su última ronda. |

**Qué se puede y qué no**

- Se automatiza bien: números (LP, cantidad de cartas, qué zona ocupa cada carta),
  si el menú ofrece la acción y si algo cambió al activarla.
- No se automatiza: si algo *se ve bien* (cuánto dura un destello, un texto
  cortado). Eso queda para la vista, con las capturas que saca el script.
- Cartas que necesitan un escenario armado (trampas que reaccionan al rival,
  monstruos de volteo) requieren un guion por carta.

## Experimento: Exchange y Spy (ROM `Efectos`)

ROM: `build/Yu-Gi-Oh! GX - Duel Academy (Efectos).gba` (parche `build/efectos.bps`). Es `Test`
más dos funciones propias: The Inexperienced Spy y **Exchange**. Estado de prueba:
`estados/duelo-exchange.st` (ya copiado como ranura 1 del ROM: tecla **F1**).

Con Exchange en la mano (posición 5):

1. Activala (menú: *Activate Effect*). Esperá ~3 segundos: se muestra la carta.
2. Aparece **"Select card in the list to swap from your opponent's hand."** Cerralo con `A`.
3. Aparece "Select card" con un filtro: `A` sobre *ALL*.
4. Aparece la lista "Hand" con las cartas del rival. `A` sobre la carta abre un menú de
   iconos: elegí el de **la mano que apunta a una carta** (el 4º desde la izquierda) y `A`.
5. Esa carta pasa a tu mano y una tuya, al azar, pasa a la del rival.

Anotá: si el aviso y la lista aparecen, si la carta cambia de mano y si la tuya se ve bien.

## Banco de pruebas: estados guardados

Un estado guardado *dentro del juego* conserva todo y sirve para cualquier ROM de
la familia `Test` (guarda la RAM, no el ROM). Editar los bytes del baúl o de los
mazos **no** funciona (el editor usa listas que arma el propio juego), pero la
**mano de un duelo** sí se puede editar si se cambia por una carta del mismo tipo.

Estados en `estados/`:

| Archivo | Qué es |
|---|---|
| `duelo-inicio.ss1` | Inicio de un duelo, partida nueva con el ROM `Spy`. Mano: Meteor Dragon, Needle Worm, Blazing Inpachi, Salamandra, Twin-Headed Fire Dragon, Monster Reincarnation |
| `duelo-spy.st` | El mismo, con **The Inexperienced Spy** en lugar de Monster Reincarnation (ambas Mágicas). El panel de nombre sigue mostrando el nombre viejo hasta que movés el cursor |
| `duelo-seal.st` | El mismo, con **Seal of the Ancients** (Nº 0538) en lugar de Monster Reincarnation. Para probarla el rival tiene que tener cartas boca abajo: pasá turnos hasta que ponga alguna |
| `duelo-exchange.st` | El mismo, con **Exchange** (Nº 0492) en lugar de Monster Reincarnation |
| `duelo-spy2.st` | Igual, y además cambia la "carta bajo el cursor" (`0x02019F0C`) para que el panel ya diga la Spy |

Cargar: *Archivo → Cargar estado desde archivo…* con el ROM `Spy` abierto.

Generar otro: `python3 scripts/estado.py mano estados/duelo-inicio.ss1 salida.st 0 5 INDICE`
(`duelo` muestra las manos). Reemplazá una carta por otra del mismo tipo.

## Experimento: menú del modo 6 (ROM `Menu6`)

ROM: `build/Yu-Gi-Oh! GX - Duel Academy (Menu6).gba` (parche `build/menu6.bps`).
Es idéntico a `Test` salvo **1 byte** (`0x2668C`): el modo 6 de los menús de
selección, que estaba vacío, ahora usa el manejador del modo 1 (elegir una
carta de la mano). Cambia solo a **Exchange**, la única carta que lo pide.

Partida **nueva**, como en los pasos de arriba. Armá un mazo con Exchange (Nº
0492) y activala en tu turno con cartas en la mano de los dos. Anotá cuál pasa:

| Qué ves | Qué significa |
|---|---|
| Aparece un menú con **la mano del rival** | El modelo es correcto. Anotá si te deja elegir una carta y qué le pasa (se espera que vaya al cementerio) |
| Aparece un menú con **tu propia mano** | El modelo es correcto, pero Exchange pasa el lado propio primero. Anotá lo mismo |
| Nada: va al cementerio como antes | El modo 6 no estaba solo vacío; el modelo está incompleto |
| Se congela, pantalla rara o reinicio | Anotá en qué momento. También es información útil |

Un resultado de cualquiera de las cuatro filas sirve; no hace falta que la carta
quede bien.

## Experimento: The Inexperienced Spy con función propia (ROM `Spy`)

ROM: `build/Yu-Gi-Oh! GX - Duel Academy (Spy).gba` (parche `build/spy.bps`).
Es `Test` más **una función nueva** (208 bytes, `efectos/spy_mano.s`) enganchada
en la fila de efecto de la Spy. No toca ninguna otra carta. La función registra
las cartas de la mano del rival y abre la pantalla de visualización, igual que
Ancient Telescope hace con el mazo.

Partida **nueva**. La carta es **The Inexperienced Spy, Nº 0084**, contraseña
81820689 (ya viene en el baúl). Es una Mágica: armá un mazo con ella y
activala en tu turno. Fijate:

| Qué ves | Qué significa |
|---|---|
| Aparece una pantalla con **las cartas de la mano del rival** | Funciona. Anotá si se ven todas, si es solo mirar y si la carta se va al cementerio después |
| Se ve la pantalla pero **vacía o con cartas que no son las de su mano** | La función llega al diálogo pero registra mal. Anotá qué muestra |
| Se va al cementerio sin mostrar nada, como antes | El motor no pasa por el estado `0x80` de esta carta; el modelo está incompleto |
| Se congela o reinicia | Anotá en qué momento: sirve para ubicar el error |

Probala también con el rival **sin cartas en la mano** (si lo lográs): no
debería dejarte activarla, como en el original.

Las pruebas automáticas (`scripts/test_spy.py`, Unicorn) pasan: llaman a la
función con un duelo armado a mano y comprueban qué registra, qué diálogo abre
y qué devuelve. Eso solo valida la lógica, no cómo se ve en pantalla.

## Resultados del lote de 30

Esta tabla **se genera** desde `datos/pruebas.csv`; no la edites a mano.
Para cambiar un resultado se cambia el CSV (o se usa `scripts/registro.py ojo`) y se
regenera con `python3 scripts/registro.py tabla ROM`. `python3 scripts/registro.py verificar ROM`
avisa si la tabla y el CSV no coinciden.

Columnas de evidencia (Principio IV de la constitución): **Lógica** = prueba con Unicorn
(solo para cartas con piezas nuevas), **Duelo** = prueba dentro del juego, **A ojo** = Oscar
la vio funcionar. Una carta puede ir a un ROM de juego cuando funciona y tiene las tres.

<!-- registro:inicio -->
| Carta | Nº | Veredicto | Lógica | Duelo | A ojo | Qué se observó | Cómo reproducir |
|---|---|---|---|---|---|---|---|
| Acid Trap Hole | 0533 | funciona | n/a | sí | sí (capturas) | Con un monstruo rival boca abajo en defensa (Nimble Momonga): se selecciona y va al cementerio. Revisada por capturas (coincide): evidencia/ronda2/12-acid-trap-hole. **Capturas:** evidencia/ronda2/12-acid-trap-hole: sesion repetida en el ROM f5ea439 el 2026-10-18: IGUAL paso a paso | ROM `f5ea439a`; `estados/v0.2/listas/acid-trap-hole.ss1`; `python3 scripts/probar_trampas.py ROM "Acid Trap Hole"` |
| Big Burn | 0564 | funciona | n/a | sí | sí (capturas) | Colocada boca abajo; el rival juega Monster Reborn apuntando a un monstruo del cementerio, el juego pregunta 'Will you chain?' y se activa: de 9 monstruos en los dos cementerios quedan 0 y hay 9 retirados del juego. Monster Reborn no invoca nada. Revisada por capturas (coincide): evidencia/ronda1/11-big-burn. **Capturas:** evidencia/ronda1/11-big-burn: sesion repetida en el ROM f5ea439 el 2026-10-18: IGUAL paso a paso | ROM `f5ea439a`; `estados/v0.2/listas/big-burn.ss1`; `python3 scripts/probar_lote.py ROM "Big Burn"` |
| Butterfly Dagger - Elma | 0246 | funciona | n/a | sí | **pendiente** | Blazing Inpachi (1850 de ATK) equipado con Butterfly Dagger - Elma: ATK por turno [2150, 2150]; esperado [2150, 2150]. Solo se midio el bono de ATK; devolverla a la mano al irse del campo, sin probar. | ROM `e8893dd2`; `estados/lote/equipo-butterfly.st`; `python3 scripts/probar_lote.py ROM "Butterfly Dagger - Elma"` |
| Chosen One | 0070 | funciona | sí | sí | sí (capturas) | Pide 3 cartas de la mano (1 monstruo y 2 Magicas o Trampas); el rival saca una al azar: si es el monstruo se invoca y las otras 2 van al cementerio; si no, las 3. Probadas las dos ramas. Arreglada el 2026-10-11: antes el rival nunca sacaba el monstruo (el sorteo arrancaba con 'anterior' = 0 y no repite el anterior). En 24 corridas por script: 10 veces el monstruo, 7 y 7 las otras dos. Revisada por capturas (coincide): evidencia/ronda3/17-chosen-one. **Capturas:** evidencia/ronda3/17-chosen-one: sesion repetida en el ROM f5ea439 el 2026-10-18: IGUAL paso a paso | ROM `f5ea439a`; `estados/v0.2/listas/chosen-one.ss1`; `python3 scripts/repetir_sesion.py ROM evidencia/ronda3/17-chosen-one` |
| Dark Necrofear | 0968 | funciona | sí | sí | sí (Oscar) | Con 3 Demonios en el cementerio el menu ofrece Special Summon y se invoca retirandolos (parche invocacion_tipo). Destruida en batalla por Mechanicalchaser en la Battle Phase del rival: va al cementerio y el rival sigue controlando a Mechanicalchaser hasta la End Phase, donde el juego pide elegir un monstruo rival boca arriba. Elegido Mechanicalchaser: pasa a mi campo; en mi turno siguiente sigue bajo mi control y despues de otro turno del rival sigue siendo mio. Necrofear queda boca arriba en mi zona de Magicas y Trampas, equipada a el. Destruida por Raigeki del rival en la Main Phase 1 del rival: va al cementerio y el rival sigue controlando a Mechanicalchaser hasta la End Phase, donde el juego pide elegir un monstruo rival boca arriba. Elegido Mechanicalchaser: pasa a mi campo; en mi turno siguiente sigue bajo mi control y despues de otro turno del rival sigue siendo mio. Necrofear queda boca arriba en mi zona de Magicas y Trampas, equipada a el. Del rival, destruida en batalla por mi Mechanicalchaser en mi Battle Phase: en mi End Phase la IA elige sola a Mechanicalchaser, que pasa a su campo, y Necrofear queda equipada a el en la zona de Magicas del rival; en mi turno siguiente sigue siendo suyo. Del rival, destruida por mi Raigeki en mi Main Phase 1: en mi End Phase la IA elige sola a Mechanicalchaser, que pasa a su campo, y Necrofear queda equipada a el en la zona de Magicas del rival; en mi turno siguiente sigue siendo suyo. Descartada de mi mano por Card Destruction del rival, con Mechanicalchaser boca arriba en el campo del rival: la End Phase pasa sin aviso y el rival conserva su monstruo. Destruida en mi campo por mi Offerings to the Doomed, con Mechanicalchaser boca arriba en el campo del rival: la End Phase pasa sin aviso y el rival conserva su monstruo. Equipada, y mi Heavy Storm la destruye: Necrofear va a mi cementerio y Mechanicalchaser vuelve al campo del rival. Equipada, y mi Dark Hole destruye al monstruo: Mechanicalchaser va al cementerio del rival y Necrofear va a mi cementerio. Equipada, y Harpie's Feather Duster del rival la destruye: Necrofear va a mi cementerio y Mechanicalchaser vuelve al campo del rival; en la End Phase de ese turno no hay otra posesion. Su carta se muestra una sola vez, en la End Phase. Version fiel desde el 2026-10-11 (antes el control era permanente y Necrofear quedaba en el cementerio). Jugada por capturas desde el estado de Oscar, con la invocacion y la devolucion del monstruo al destruirla (coincide): evidencia/ronda7/33-dark-necrofear. **Oscar:** Oscar 2026-10-18: todo perfecto (invocacion y posesion) | ROM `f5ea439a`; `estados/v0.2/listas/dark-necrofear.ss1`; `python3 scripts/probar_lote.py ROM "Dark Necrofear"` |
| Dark-Eyes Illusionist | 0057 | funciona | n/a | sí | sí (Oscar) | Al voltearse (atacada por Mechanicalchaser) pide un objetivo y se elige al atacante. En el turno rival siguiente, con Dark-Eyes en ataque (ATK 0) y Mechanicalchaser con 1850: no la ataca (LP 8000 a 8000). Pasada de control con el bloqueo borrado: ataca (LP 8000 a 6150). Ayudas de prueba: ATK del atacante bajado en memoria durante el volteo para que Dark-Eyes sobreviva, y posicion de Dark-Eyes escrita en memoria. Revisada por capturas (coincide): evidencia/ronda2/04-dark-eyes-illusionist. **Oscar:** Oscar: Tongyo no volvio a atacar; queda el icono de efecto continuo en los dos monstruos | ROM `Lote (2026-10-11, antes de completar)`; `estados/v0.2/listas/dark-eyes-illusionist.ss1`; `python3 scripts/probar_lote.py ROM "Dark-Eyes Illusionist"` |
| Electric Snake | 0936 | funciona | sí | sí | sí (Oscar) | En la mano desde el inicio, descartada por Card Destruction del rival: robo 2 cartas de mas (mazo 34 a 26). Robada del mazo y descartada por Card Destruction del rival: robo 2 cartas de mas (mazo 33 a 25). Dos copias descartadas por Delinquent Duo del rival: robo 5 cartas de mas (mazo 34 a 29). Arreglada o completada el 2026-10-11. Jugada por capturas desde el estado de Oscar (coincide): evidencia/ronda6/23-electric-snake. **Oscar:** Oscar 2026-10-18: perfecto | ROM `f5ea439a`; `estados/v0.2/listas/electric-snake.ss1`; `python3 scripts/probar_lote.py ROM "Electric Snake"` |
| Electromagnetic Bagworm | 0522 | funciona | sí | sí | sí (Oscar) | Boca abajo, atacada por Mechanicalchaser (1850/800): pide elegir una Maquina rival y pasa a mi campo. Durante mi turno siguiente sigue bajo mi control y al terminarlo vuelve al rival. La batalla se resuelve igual y Bagworm va al cementerio; la Maquina que la destruyo queda en 1350/300 (ya estaba en 1350/300 al pedir la eleccion). Completada el 2026-10-11. Jugada por capturas desde el estado de Oscar (coincide): evidencia/ronda7/03-electromagnetic-bagworm. **Oscar:** Oscar 2026-10-17/18: perfecto con Mechanicalchaser; con monstruos no Maquina no deja tomar el control (atacada por Blazing Inpachi y volteada con solo Tongyo) | ROM `f5ea439a`; `estados/v0.2/listas/electromagnetic-bagworm.ss1`; `python3 scripts/probar_lote.py ROM "Electromagnetic Bagworm"` |
| Elemental Hero Neos | 0007 | funciona | n/a | sí | sí (capturas) | Carta nueva (el juego nunca la tuvo), monstruo Normal. La pantalla de detalle muestra nombre, dibujo, LIGHT, 7 estrellas, Warrior, texto y 2500/2000. Pide 2 tributos, se invoca en ataque con ATK 2500 y al atacar a Des Wombat (1600) lo destruye y el rival pierde 900. Jugada por capturas: evidencia/ronda8/34-elemental-hero-neos. **Capturas:** evidencia/ronda8/34-elemental-hero-neos: sesion repetida en el ROM f5ea439 el 2026-10-18: IGUAL paso a paso | ROM `f5ea439a`; `estados/v0.2/listas/elemental-hero-neos.ss1`; `python3 scripts/repetir_sesion.py ROM evidencia/ronda8/34-elemental-hero-neos` |
| Exchange | 0492 | funciona | sí | sí | sí (capturas) | Aparece 'Select card in the list to swap from your opponent's hand.', elegis una carta de la mano del rival y se intercambia por una de la tuya elegida al azar. 3 corridas. Revisada por capturas (coincide): evidencia/ronda1/16-exchange. **Capturas:** evidencia/ronda1/16-exchange: sesion repetida en el ROM f5ea439 el 2026-10-18: igual hasta el intercambio; la carta propia que pasa al rival es al azar (salio otra), el intercambio se hace bien | ROM `f5ea439a`; `estados/v0.2/listas/exchange.ss1`; `python3 scripts/repetir_sesion.py ROM evidencia/ronda1/16-exchange` |
| Fairy Guardian | 0530 | funciona | sí | sí | sí (Oscar) | El turno en que Magic Jammer del rival niega y destruye mi Dian Keto the Cure Master, el menu de Fairy Guardian ofrece el efecto: se tributa, pide elegir la Magica en la lista del cementerio y la Magica vuelve al fondo del mazo (33 a 34 cartas; la ultima es Dian Keto the Cure Master). Arreglada o completada el 2026-10-11. Jugada por capturas desde el estado de Oscar (coincide): evidencia/ronda6/26-fairy-guardian. **Oscar:** Oscar 2026-10-18: perfecto | ROM `f5ea439a`; `estados/v0.2/listas/fairy-guardian.ss1`; `python3 scripts/probar_lote.py ROM "Fairy Guardian"` |
| Fusion Sword Murasame Blade | 0309 | funciona | n/a | sí | **pendiente** | Axe Raider (1700 de ATK) equipado con Fusion Sword Murasame Blade: ATK por turno [2500, 2500]; esperado [2500, 2500]. Solo se midio el bono de ATK sobre un Warrior; el resto del texto real, sin probar. | ROM `e8893dd2`; `estados/lote/equipo-fusion.st`; `python3 scripts/probar_lote.py ROM "Fusion Sword Murasame Blade"` |
| Goddess of Whim | 0525 | funciona | sí | sí | sí (capturas) | En el campo ofrece Activate Effect una vez por turno, pide cara o cruz, avisa si acertaste y el ATK se duplica o se reduce a la mitad hasta el fin del turno. Arreglada el 2026-10-11: el cartel de la moneda (Correct! / Miss!) y el efecto ahora coinciden siempre; antes la pieza tiraba una segunda moneda y la mitad de las veces se contradecian. 12 corridas por script, todas coherentes. Revisada por capturas (coincide): evidencia/ronda4/22-goddess-of-whim. **Capturas:** evidencia/ronda4/22-goddess-of-whim: sesion repetida en el ROM f5ea439 el 2026-10-18: IGUAL paso a paso | ROM `f5ea439a`; `estados/v0.2/listas/goddess-of-whim.ss1`; `python3 scripts/repetir_sesion.py ROM evidencia/ronda4/22-goddess-of-whim` |
| Hiro's Shadow Scout | 0532 | funciona | sí | sí | sí (Oscar) | Boca abajo, atacada por Mechanicalchaser: al voltearse salen 3 cartas del tope del mazo del rival (47 a 44). La Magica (Dian Keto the Cure Master) va a su cementerio y su mano pasa de 5 a 6 cartas mas Call of the Haunted, que roba y coloca en ese mismo turno. Arreglada o completada el 2026-10-11. Jugada por capturas desde el estado de Oscar (coincide): evidencia/ronda6/31-hiro-s-shadow-scout. **Oscar:** Oscar 2026-10-18: funciona bien | ROM `f5ea439a`; `estados/v0.2/listas/hiro-s-shadow-scout.ss1`; `python3 scripts/probar_lote.py ROM "Hiro's Shadow Scout"` |
| Jowls of Dark Demise | 0520 | funciona | n/a | sí | sí (Oscar) | Al voltearse pide elegir un monstruo rival y toma su control ese turno. El monstruo vuelve al rival al terminar el turno. Revisada por capturas (coincide): evidencia/ronda1/02-jowls-of-dark-demise. **Oscar:** Oscar: toma el control del monstruo y al final del turno del rival vuelve a el, como dice el texto (hasta el fin de este turno) | ROM `Lote (2026-10-11, antes de completar)`; `estados/v0.2/listas/jowls-of-dark-demise.ss1`; `python3 scripts/repetir_sesion.py ROM evidencia/ronda1/02-jowls-of-dark-demise` |
| Kunai with Chain | 0569 | funciona | sí | sí | sí (Oscar) | Sin monstruos propios, el rival ataca: el atacante pasa de ataque a defensa y la carta va al cementerio. Con Blazing Inpachi (1850) en mi campo se activa en la Draw Phase del rival: pide 'Select your monster to equip.', el ATK queda en 2350 y la carta queda boca arriba en el campo; en mi turno siguiente el ATK es 2350. Al tributar a Blazing Inpachi la carta va al cementerio con el. Arreglada o completada el 2026-10-11. Jugada por capturas desde el estado de Oscar (coincide): evidencia/ronda6/30-kunai-with-chain. **Oscar:** Oscar 2026-10-18: perfecto en los dos efectos: equipada suma 500; ante un ataque pone al atacante en defensa y suma 500 al monstruo elegido | ROM `f5ea439a`; `estados/v0.2/listas/kunai-with-chain-2.ss1`; `python3 scripts/probar_lote.py ROM "Kunai with Chain"` |
| Lady Panther | 0063 | funciona | sí | sí | sí (capturas) | Arreglada el 2026-10-11 agregando su ID a las dos listas de efectos de campo (las mismas de Goddess of Whim). En la Main Phase 2 del turno en que un monstruo mio muere en batalla, el menu ofrece Activate Effect: Lady Panther se tributa, pide 'Select monster to return to the Deck.' y el monstruo vuelve al tope del mazo (se roba al turno siguiente). 3 de 3 corridas de probar_lote.py (con Tongyo pasado a ataque en memoria) y una partida entera sin ayudas. Revisada por capturas (coincide): evidencia/ronda5/27-lady-panther. **Capturas:** evidencia/ronda5/27-lady-panther: sesion repetida en el ROM f5ea439 el 2026-10-18: IGUAL paso a paso | ROM `f5ea439a`; `estados/v0.2/listas/lady-panther.ss1`; `python3 scripts/probar_lote.py ROM "Lady Panther"` |
| Magic Drain | 0536 | funciona | n/a | sí | sí (Oscar) | Colocada boca abajo; el rival juega Dian Keto, el juego pregunta si encadenar, se activa y la Magica se niega y destruye (LP 8000 sin curar). Con 2 Magicas en la mano del rival (variante pedida por Oscar): la IA no descarta para negarla; Dian Keto se niega igual (evidencia/ronda1/28-magic-drain). La rama del descarte no se pudo provocar. Revisada por capturas (coincide): evidencia/ronda1/08-magic-drain. **Oscar:** Oscar: nego la Magica; falta ver la rama en que el rival descarta una Magica para negarla | ROM `Lote (2026-10-11, antes de completar)`; `estados/v0.2/listas/magic-drain.ss1`; `python3 scripts/probar_cadena.py ROM "Magic Drain"` |
| Minar | 0970 | funciona | sí | sí | sí (Oscar) | En la mano desde el inicio, descartada por Card Destruction del rival: el rival pierde 1000 LP por el efecto (LP 8000 a 7000). Robada del mazo y descartada por Card Destruction del rival: el rival pierde 1000 LP por el efecto (LP 8000 a 7000). Dos copias descartadas por Delinquent Duo del rival: el rival pierde 2000 LP por el efecto (LP 8000 a 5000, de los cuales 1000 son el coste de Delinquent Duo). Arreglada o completada el 2026-10-11. Jugada por capturas desde el estado de Oscar (coincide): evidencia/ronda6/24-minar. **Oscar:** Oscar 2026-10-18: perfecto | ROM `f5ea439a`; `estados/v0.2/listas/minar.ss1`; `python3 scripts/probar_lote.py ROM "Minar"` |
| Monster Recovery | 0227 | funciona | n/a | sí | sí (capturas) | Con un monstruo en el campo: vuelve al mazo (34 a 35) y la mano se renueva con 4 cartas nuevas. Revisada por capturas (coincide): evidencia/ronda1/21-monster-recovery. **Capturas:** evidencia/ronda1/21-monster-recovery: sesion repetida en el ROM f5ea439 el 2026-10-18: IGUAL paso a paso | ROM `f5ea439a`; `estados/v0.2/listas/monster-recovery.ss1`; `python3 scripts/probar_magicas.py ROM "Monster Recovery"` |
| Mystical Refpanel | 0657 | funciona | n/a | sí | sí (Oscar) | Contra Dian Keto del rival: la curacion de 1000 LP pasa al jugador (9000 / 8000). Revisada por capturas (coincide): evidencia/ronda1/09-mystical-refpanel. **Oscar:** Oscar 2026-10-18: funciona con Dian Keto | ROM `f5ea439a`; `estados/v0.2/listas/mystical-refpanel.ss1`; `python3 scripts/probar_cadena.py ROM "Mystical Refpanel"` |
| Neo-Spacian Air Hummingbird | 0335 | funciona | n/a | sí | **pendiente** | Neo-Spacian Air Hummingbird en el campo con 5 cartas en la mano del rival: LP 8000 -> 10500 (esperado 10500). Una segunda vez en el mismo turno no hace nada. | ROM `2ba105a9`; `estados/lote/air-hummingbird.st`; `python3 scripts/probar_lote.py ROM "Neo-Spacian Air Hummingbird"` |
| Neo-Spacian Aqua Dolphin | 0328 | funciona | n/a | sí | **pendiente** | monstruo fuerte en la mano del rival: (mis LP, LP rival, mi mano, mi cementerio, mano rival, cementerio rival) (7500, 8000, 4, 1, 5, 0); esperado (7500, 8000, 4, 1, 5, 0). \| monstruo debil en la mano del rival: (mis LP, LP rival, mi mano, mi cementerio, mano rival, cementerio rival) (8000, 7500, 4, 1, 4, 1); esperado (8000, 7500, 4, 1, 4, 1). | ROM `2ba105a9`; `estados/lote/aqua-dolphin-pierde.st`; `python3 scripts/probar_lote.py ROM "Neo-Spacian Aqua Dolphin"` |
| Neo-Spacian Dark Panther | 0535 | funciona | n/a | sí | **pendiente** | Neo-Spacian Dark Panther copia a Battle Ox: nombre Battle Ox, ATK 1000 -> 1000, DEF 500; despues de la End Phase: Neo-Spacian Dark Panther. | ROM `2ba105a9`; `estados/lote/dark-panther.st`; `python3 scripts/probar_lote.py ROM "Neo-Spacian Dark Panther"` |
| Neo-Spacian Flare Scarab | 0568 | funciona | n/a | sí | **pendiente** | Neo-Spacian Flare Scarab con 0, 3 y 1 Magicas/Trampas del rival: ATK [500, 1700, 900]; esperado [500, 1700, 900]. | ROM `2ba105a9`; `estados/lote/flare-scarab.st`; `python3 scripts/probar_lote.py ROM "Neo-Spacian Flare Scarab"` |
| Neo-Spacian Glow Moss | 0515 | funciona | n/a | sí | **pendiente** | monstruo: rival robo 1 carta(s), LP (8000, 8000) -> (8000, 8000), posiciones de Glow Moss vistas ['0x10'], campos (['Neo-Spacian Glow Moss'], ['Meteor Dragon']) \| magica: rival robo 1 carta(s), LP (8000, 8000) -> (8000, 7700), posiciones de Glow Moss vistas ['0x10'], campos (['Neo-Spacian Glow Moss'], ['Meteor Dragon']) \| trampa: rival robo 1 carta(s), LP (8000, 8000) -> (6500, 8000), posiciones de Glow Moss vistas ['0x10', '0x30'], campos ([], ['Meteor Dragon']) | ROM `8a8f09c1`; `python3 scripts/probar_lote.py ROM "Neo-Spacian Glow Moss"` |
| Neo-Spacian Grand Mole | 0484 | funciona | n/a | sí | **pendiente** | Neo-Spacian Grand Mole ataca a Meteor Dragon (1800): Mole en mi mano True, Meteor Dragon en la mano del rival True, campos ([], []), LP (8000, 8000) -> (8000, 8000). | ROM `8a8f09c1`; `python3 scripts/probar_lote.py ROM "Neo-Spacian Grand Mole"` |
| Penguin Knight | 0972 | funciona | sí | sí | sí (Oscar) | Ataco con Blazing Inpachi a Needle Worm del rival boca abajo: su volteo manda 5 cartas del tope de mi mazo al cementerio, Penguin Knight entre ellas. Despues: mazo 33 a 33, cementerio con 0 cartas. Arreglada o completada el 2026-10-11. Jugada por capturas desde el estado de Oscar (coincide): evidencia/ronda6/25-penguin-knight. **Oscar:** Oscar 2026-10-18: funciona bien | ROM `f5ea439a`; `estados/v0.2/listas/penguin-knight.ss1`; `python3 scripts/probar_lote.py ROM "Penguin Knight"` |
| Ready for Intercepting | 0534 | funciona | n/a | sí | sí (capturas) | Activada sobre un Guerrero o Lanzador de Conjuros boca arriba: queda boca abajo en defensa. Revisada por capturas (coincide): evidencia/ronda1/14-ready-for-intercepting. **Capturas:** evidencia/ronda1/14-ready-for-intercepting: sesion repetida en el ROM f5ea439 el 2026-10-18: IGUAL paso a paso | ROM `f5ea439a`; `estados/v0.2/listas/ready-for-intercepting.ss1`; `python3 scripts/repetir_sesion.py ROM evidencia/ronda1/14-ready-for-intercepting` |
| Reaper of the Cards | 0971 | funciona | n/a | sí | sí (Oscar) | Boca abajo, atacada por Giant Orc con Call of the Haunted del rival colocada boca abajo: al voltearse pide 'Select Trap Card to destroy.', se elige la carta boca abajo y va al cementerio del rival. Ayuda de prueba: nivel escrito en memoria para colocarla sin tributo. Revisada por capturas (coincide): evidencia/ronda1/05-reaper-of-the-cards. **Oscar:** Oscar: destruyo la Trampa despues de voltearse | ROM `Lote (2026-10-11, antes de completar)`; `estados/v0.2/listas/reaper-of-the-cards.ss1`; `python3 scripts/probar_lote.py ROM "Reaper of the Cards"` |
| Reasoning | 0508 | funciona | sí | sí | sí (Oscar) | Con el nivel que declara el juego (4): revela Dian Keto the Cure Master, Call of the Haunted y Mechanicalchaser (nivel 4); el monstruo va al cementerio y el mazo pasa de 34 a 31. Con el nivel 4 escrito en memoria (4): revela Dian Keto the Cure Master, Call of the Haunted y Mechanicalchaser (nivel 4); el monstruo va al cementerio y el mazo pasa de 34 a 31. Con el nivel 3 escrito en memoria (3): revela Dian Keto the Cure Master, Call of the Haunted y Mechanicalchaser (nivel 4); el monstruo se invoca y el mazo pasa de 34 a 31. Ayuda de prueba: nivel declarado escrito en memoria para ver las dos ramas. Arreglada o completada el 2026-10-11. Jugada por capturas desde el estado de Oscar (coincide): evidencia/ronda6/32-reasoning. **Oscar:** Oscar 2026-10-18: perfecto, probado con nivel 4 y 3 | ROM `f5ea439a`; `estados/v0.2/listas/reasoning.ss1`; `python3 scripts/probar_lote.py ROM "Reasoning"` |
| Rigorous Reaver | 0524 | funciona | n/a | sí | sí (Oscar) | Colocada boca abajo y atacada: los dos jugadores descartan 1 carta y el atacante pierde 500 ATK. Probada tres veces. Revisada por capturas (coincide): evidencia/ronda1/01-rigorous-reaver. **Oscar:** Oscar: funciona perfecto | ROM `Lote (2026-10-11, antes de completar)`; `estados/v0.2/listas/rigorous-reaver.ss1`; `python3 scripts/repetir_sesion.py ROM evidencia/ronda1/01-rigorous-reaver` |
| Riryoku | 0487 | funciona | sí | sí | sí (capturas) | Se eligen dos monstruos boca arriba: el primero pierde la mitad del ATK y el segundo la gana hasta el fin del turno (750 a 375 y 1850 a 2225). Revisada por capturas (coincide): evidencia/ronda4/20-riryoku. **Capturas:** evidencia/ronda4/20-riryoku: sesion repetida en el ROM f5ea439 el 2026-10-18: IGUAL paso a paso | ROM `f5ea439a`; `estados/v0.2/listas/riryoku.ss1`; `python3 scripts/repetir_sesion.py ROM evidencia/ronda4/20-riryoku` |
| Riryoku Field | 0417 | funciona | n/a | sí | sí (capturas) | Contra Black Pendant del rival: el equipo se niega y se destruye. Revisada por capturas (coincide): evidencia/ronda1/10-riryoku-field. **Capturas:** evidencia/ronda1/10-riryoku-field: sesion repetida en el ROM f5ea439 el 2026-10-18: IGUAL paso a paso | ROM `f5ea439a`; `estados/v0.2/listas/riryoku-field.ss1`; `ESTADO_BASE=estados/duelo-equipo.ss1 python3 scripts/probar_cadena.py ROM "Riryoku Field"` |
| Seal of the Ancients | 0538 | funciona | n/a | sí | sí (capturas) | Paga 1000 LP y muestra que son las cartas boca abajo del rival, que quedan boca abajo. Se ven como destellos rapidos. Revisada por capturas (coincide): evidencia/ronda1/18-seal-of-the-ancients. **Capturas:** evidencia/ronda1/18-seal-of-the-ancients: sesion repetida en el ROM f5ea439 el 2026-10-18: IGUAL paso a paso | ROM `f5ea439a`; `estados/v0.2/listas/seal-of-the-ancients.ss1`; `python3 scripts/prueba_seal.py ROM` |
| Share the Pain | 0418 | funciona | sí | sí | sí (capturas) | Tributas un monstruo propio y el rival pierde su monstruo de menor ATK. Solo probada activandola el jugador. Revisada por capturas (coincide): evidencia/ronda3/19-share-the-pain. **Capturas:** evidencia/ronda3/19-share-the-pain: sesion repetida en el ROM f5ea439 el 2026-10-18: IGUAL paso a paso | ROM `f5ea439a`; `estados/v0.2/listas/share-the-pain.ss1`; `python3 scripts/repetir_sesion.py ROM evidencia/ronda3/19-share-the-pain` |
| Shooting Star Bow - Ceal | 0311 | funciona | n/a | sí | **pendiente** | Blazing Inpachi (1850 de ATK) equipado con Shooting Star Bow - Ceal: ATK por turno [850, 850]; esperado [850, 850]. Solo se midio la baja de ATK; el ataque directo, sin probar. | ROM `e8893dd2`; `estados/lote/equipo-shooting.st`; `python3 scripts/probar_lote.py ROM "Shooting Star Bow - Ceal"` |
| The Inexperienced Spy | 0084 | funciona | sí | sí | sí (capturas) | Al activarla muestra 1 carta AL AZAR de la mano del rival (cambio del 2026-10-13: el texto dice elegir y mirar 1, pero la lista del motor muestra el nombre de todas las candidatas, asi que elegir a ciegas no se puede; es lo que hace Inspection). Antes mostraba la mano entera. B cierra la lista, la carta va al cementerio y el duelo sigue. Arreglada el 2026-10-11: antes la lista no se podia cerrar (la funcion devolvia 0x80 fuera del estado de entrada y el motor la reabria). Revisada por capturas (coincide): evidencia/ronda2/15-the-inexperienced-spy. **Capturas:** evidencia/ronda9/15-the-inexperienced-spy: jugada el 2026-10-18 en el ROM f5ea439: muestra 1 carta al azar de la mano rival (ALL 1, Snatch Steal), B cierra y la carta va al cementerio | ROM `f5ea439a`; `estados/v0.2/listas/the-inexperienced-spy.ss1`; `python3 scripts/repetir_sesion.py ROM evidencia/ronda2/15-the-inexperienced-spy` |
| Twin Swords of Flashing Light - Tryce | 0320 | funciona | n/a | sí | **pendiente** | Blazing Inpachi (1850 de ATK) equipado con Twin Swords of Flashing Light - Tryce: ATK por turno [1350, 1350]; esperado [1350, 1350]. Solo se midio la baja de ATK y el descarte; atacar dos veces, sin probar. | ROM `e8893dd2`; `estados/lote/equipo-twin.st`; `python3 scripts/probar_lote.py ROM "Twin Swords of Flashing Light - Tryce"` |
| Two-Pronged Attack | 0488 | funciona | sí | sí | sí (capturas) | Con 2 monstruos propios y 1 del rival: se eligen los tres y van al cementerio. Revisada por capturas (coincide): evidencia/ronda1/13-two-pronged-attack. **Capturas:** evidencia/ronda1/13-two-pronged-attack: sesion repetida en el ROM f5ea439 el 2026-10-18: IGUAL paso a paso | ROM `f5ea439a`; `estados/v0.2/listas/two-pronged-attack.ss1`; `python3 scripts/probar_trampas.py ROM "Two-Pronged Attack"` |
| Wicked-Breaking Flamberge - Baou | 0317 | funciona | n/a | sí | **pendiente** | Blazing Inpachi (1850 de ATK) equipado con Wicked-Breaking Flamberge - Baou: ATK por turno [2350, 2350]; esperado [2350, 2350]. Solo se midio el bono de ATK y el descarte; otros efectos de la carta, sin probar. | ROM `e8893dd2`; `estados/lote/equipo-wicked-breaking.st`; `python3 scripts/probar_lote.py ROM "Wicked-Breaking Flamberge - Baou"` |
| Windstorm of Etaqua | 0489 | funciona | n/a | sí | sí (Oscar) | Activada cuando el rival invoca: sus monstruos boca arriba cambian de posicion. Con dos monstruos rivales boca arriba (variante pedida por Oscar): cambian de posicion los dos, no solo el que ataca. Revisada por capturas (coincide): evidencia/ronda1/29-windstorm-of-etaqua. **Oscar:** Oscar: cambio de posicion al monstruo rival; habia uno solo, falta verla con dos | ROM `Lote (2026-10-11, antes de completar)`; `estados/v0.2/listas/windstorm-of-etaqua.ss1`; `python3 scripts/repetir_sesion.py ROM evidencia/ronda1/29-windstorm-of-etaqua` |
| Stim-Pack | 0171 | funciona en parte | n/a | sí | **pendiente** | Blazing Inpachi (1850 de ATK) equipado con Stim-Pack: ATK por turno [2550, 2550, 2550]; esperado [2550, 2350, 2350]. **Falla:** ATK [2550, 2550, 2550], esperado [2550, 2350, 2350] | ROM `e8893dd2`; `estados/lote/equipo-stim-pack.st`; `python3 scripts/probar_lote.py ROM "Stim-Pack"` |
<!-- registro:fin -->

`build/... (Prueba3).gba`, la versión para jugar (sin cartas ni contraseñas de regalo), trae solo
Rigorous Reaver, Jowls of Dark Demise, Windstorm of Etaqua, Ready for Intercepting y Dark Necrofear.
Las piezas nuevas están en `build/... (Lote).gba`.

## Listas de selección ("Select card"): las teclas

Medido el 2026-10-12 con Aqua Dolphin, Dark Panther y Polymerization (`probar_lote.py`,
`probar_fusion.py`). Con el aviso abierto y el cursor en la pestaña ALL:

| Para | Teclas (70 cuadros entre una y otra) |
|---|---|
| Cerrar el aviso | `A` |
| Elegir **1** carta de una lista | `A` (ALL) `A` (la carta) `RIGHT` × 3 (DECIDE) `A` |
| Marcar **varias** (Fusion-Material) | `A` (ALL), y por cada carta: `A` (iconos, queda en CHECK) `A` (marca) `DOWN`; después `A` y `RIGHT` × 4 (DECIDE) `A` |
| Orden de los iconos de la lista | CHECK (solo si se marca), FILTER, SORT, CHANGE VIEW, DECIDE, SEE FIELD |
| Menú de una Mágica en la mano | arranca en Detail Screen: `UP` × 2 = Activate Effect, `UP` × 1 = Set |

Lo que **no** hay que hacer: pulsar `RIGHT` antes de abrir los iconos (cambia de pestaña de filtro y la
lista queda vacía). Las funciones: `elegir_en_lista_hasta` (`probar_lote.py`) repite la secuencia hasta
que el estado de la resolución (`0x020204C6`) llega al que se espera.

