# Guía para Oscar: qué mirar y cómo

Este archivo lo genera `scripts/armar_revision.py`; para cambiarlo se cambia ese script.

Las 30 cartas ya tienen veredicto. Las filas 1 a 29 se jugaron por script, con capturas
(`evidencia/index.html`); las filas 3, 23 a 26 y 30 a 33 son de cartas arregladas o completadas después de
esas capturas (y vueltas a jugar). Lo que queda es que confirmes vos las que quieras ver. Cada estado de `estados/revisar/` sale de **tu** estado (`build/Yu-Gi-Oh! GX - Duel Academy (Lote).ss1`): mismo duelo, mismo
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
- Tu mano conserva las cartas de tu estado salvo las que reemplacé: Darkfire Soldier #2 (1700) es el
  monstruo de apoyo en varios pasos.


## Monstruos de volteo

| N.º | Carta | Estado | Pasos | Qué deberías ver |
|---|---|---|---|---|
| 1 | Rigorous Reaver | `estados/revisar/01-rigorous-reaver.ss1` | Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival invoca a Mechanicalchaser y la ataca. | Los dos jugadores descartan 1 carta y Mechanicalchaser pierde 500 ATK. |
| 2 | Jowls of Dark Demise | `estados/revisar/02-jowls-of-dark-demise.ss1` | Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). Cuando Mechanicalchaser la ataque te pide elegir un monstruo rival: elegilo. | Mechanicalchaser pasa a tu campo ese turno. |
| 3 | Electromagnetic Bagworm | `estados/revisar/03-electromagnetic-bagworm.ss1` | Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). Aviso "Select opponent's Machine monster to gain control of.": `A`, `A` sobre Mechanicalchaser, `A`. | Antes del aviso Mechanicalchaser baja de 1850/800 a 1350/300: pierde 500 por destruir a Bagworm en batalla. Después pasa a tu campo, sigue siendo tuyo durante tu turno siguiente y vuelve al rival cuando terminás ese turno, siempre con 1350/300. |
| 4 | Dark-Eyes Illusionist | `estados/revisar/04-dark-eyes-illusionist.ss1` | Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). Tongyo (1350) la ataca y no la destruye (DEF 1400). Te pide un objetivo: elegí a Tongyo. Si el rival no ataca en su primer turno, terminá el tuyo otra vez. | Mientras Dark-Eyes siga boca arriba, Tongyo no vuelve a atacar. |
| 5 | Reaper of the Cards | `estados/revisar/05-reaper-of-the-cards.ss1` | Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival coloca una carta boca abajo. Terminá también tu segundo turno: el rival roba a Giant Orc y ataca. Aviso "Select Trap Card to destroy.": `A`, `ARRIBA` hasta la carta boca abajo, `A`. | La carta boca abajo era Call of the Haunted y se destruye. (Es de nivel 5; en este estado se coloca sin tributo porque le cambié el nivel dentro del estado.) |

## Trampas

| N.º | Carta | Estado | Pasos | Qué deberías ver |
|---|---|---|---|---|
| 6 | Windstorm of Etaqua | `estados/revisar/06-windstorm-of-etaqua.ss1` | Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival invoca a Mechanicalchaser y ataca: cuando el juego pregunte, *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*. | Mechanicalchaser cambia de posición. |
| 7 | Kunai with Chain | `estados/revisar/07-kunai-with-chain.ss1` | Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival ataca: cuando el juego pregunte, *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*. | El atacante pasa a defensa y, como no tenés monstruos, Kunai va al cementerio. El segundo efecto (equiparla) está en la fila 30. |
| 8 | Magic Drain | `estados/revisar/08-magic-drain.ss1` | Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival juega Dian Keto: "Will you chain?" → cuando el juego pregunte, *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*. | Dian Keto se niega y se destruye: el rival sigue en 8000 LP. |
| 9 | Mystical Refpanel | `estados/revisar/09-mystical-refpanel.ss1` | Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival juega Dian Keto: "Will you chain?" → cuando el juego pregunte, *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*. | Los 1000 LP los ganás vos: quedás en 9000 y el rival en 8000. |
| 10 | Riryoku Field | `estados/revisar/10-riryoku-field.ss1` | Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival invoca a Mechanicalchaser y le equipa Black Pendant: "Will you chain?" → cuando el juego pregunte, *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*. | Black Pendant se niega y se destruye. |
| 11 | Big Burn | `estados/revisar/11-big-burn.ss1` | Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival juega Card Destruction (los dos descartan la mano) y después Monster Reborn: `A` en el aviso del objetivo, "Will you chain?" → cuando el juego pregunte, *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*. | Todos los monstruos de los dos cementerios se retiran del juego y Monster Reborn no invoca nada. |
| 12 | Acid Trap Hole | `estados/revisar/12-acid-trap-hole.ss1` | Invocá a Darkfire Soldier #2, colocá la trampa y terminá el turno. El rival coloca a Tongyo boca abajo. En tu turno siguiente: cursor sobre la trampa, `A`, *Activate Effect*, y elegí ese monstruo. | Tongyo se voltea y se destruye. |
| 13 | Two-Pronged Attack | `estados/revisar/13-two-pronged-attack.ss1` | Turno 1: invocá a Darkfire Soldier #2 y colocá la trampa. Turno 2: invocá a The Thing in the Crater. Activá la trampa y elegí tus dos monstruos y el del rival. | Los tres van al cementerio. |
| 14 | Ready for Intercepting | `estados/revisar/14-ready-for-intercepting.ss1` | Turno 1: invocá a Sonic Maid (Guerrero) y colocá la trampa. Turno 2: activá la trampa sobre Sonic Maid. | Sonic Maid queda boca abajo en defensa. |

## Mágicas

| N.º | Carta | Estado | Pasos | Qué deberías ver |
|---|---|---|---|---|
| 15 | The Inexperienced Spy | `estados/revisar/15-the-inexperienced-spy.ss1` | Activala (menú de la carta, *Activate Effect*). | Se muestra 1 carta al azar de la mano del rival (una de Penguin Soldier, Dekoichi, Fusion Sage, Snatch Steal o Hane-Hane). `B` cierra la lista y la carta va al cementerio. |
| 16 | Exchange | `estados/revisar/16-exchange.ss1` | Activala. `A` en el aviso, `A` sobre *ALL*, `A` sobre una carta, icono de la mano que apunta (*DECIDE*, el 4.º), `A`. | Esa carta pasa a tu mano y una tuya, al azar, a la del rival. |
| 17 | Chosen One | `estados/revisar/17-chosen-one.ss1` | Activala y marcá 1 monstruo (Darkfire Soldier #2) y 2 Mágicas o Trampas (Trap Hole y Dian Keto). | El rival saca una al azar. Si es el monstruo, se invoca y las otras 2 van al cementerio; si no, las 3. |
| 18 | Seal of the Ancients | `estados/revisar/18-seal-of-the-ancients.ss1` | Turno 1: invocá a Darkfire Soldier #2 y terminá. El rival coloca cartas boca abajo. Turno 2: activala. | Pagás 1000 LP y ves, en destellos rápidos, qué son las cartas boca abajo del rival. |
| 19 | Share the Pain | `estados/revisar/19-share-the-pain.ss1` | Turno 1: invocá a Darkfire Soldier #2 y terminá. El rival coloca a Tongyo. Turno 2: activala y tributá a Darkfire Soldier #2. | El rival pierde a Tongyo. |
| 20 | Riryoku | `estados/revisar/20-riryoku.ss1` | Turno 1: invocá a Darkfire Soldier #2. Turno 2: invocá a The Thing in the Crater, activala y elegí los dos. | El primero pierde la mitad del ATK y el segundo la gana, hasta el fin del turno. |
| 21 | Monster Recovery | `estados/revisar/21-monster-recovery.ss1` | Invocá a Darkfire Soldier #2 y activala. | Darkfire Soldier #2 y las 4 cartas de tu mano vuelven al mazo, y robás 4 (las que tenías en la mano). |

## Monstruo con efecto en el campo

| N.º | Carta | Estado | Pasos | Qué deberías ver |
|---|---|---|---|---|
| 22 | Goddess of Whim | `estados/revisar/22-goddess-of-whim.ss1` | Invocala. Cursor sobre ella, `A`, *Activate Effect*, elegí cara o cruz. | Avisa si acertaste y el ATK pasa de 950 a 1900 o a 475 hasta el fin del turno. |

## Arregladas el 2026-10-11: "por un efecto del rival"

| N.º | Carta | Estado | Pasos | Qué deberías ver |
|---|---|---|---|---|
| 23 | Electric Snake | `estados/revisar/23-electric-snake.ss1` | Terminá el turno sin jugar nada. El rival juega Card Destruction y descarta tu mano. | Robás 2 cartas de más: quedás con 8 en la mano (las 6 que repone Card Destruction y las 2 de Electric Snake) en vez de 6. |
| 24 | Minar | `estados/revisar/24-minar.ss1` | Terminá el turno sin jugar nada. El rival juega Card Destruction y descarta tu mano. | El rival pierde 1000 LP (queda en 7000). |
| 25 | Penguin Knight | `estados/revisar/25-penguin-knight.ss1` | Turno 1: invocá a Darkfire Soldier #2 y terminá. El rival coloca a Needle Worm boca abajo. Turno 2: `B`, *Enter Battle Phase*, y atacalo. | Needle Worm manda 5 cartas de tu mazo al cementerio, Penguin Knight entre ellas, y enseguida todo tu cementerio vuelve al mazo, que se baraja: el cementerio queda vacío. |
| 26 | Fairy Guardian | `estados/revisar/26-fairy-guardian.ss1` | Turno 1: invocá a Fairy Guardian y terminá. El rival coloca Magic Jammer. Turno 2: activá Dian Keto; el rival la niega. En ese mismo turno: cursor sobre Fairy Guardian, `A`, *Activate Effect*. Aviso "Select Spell Card to return to the Deck.": `A`, `A` sobre *ALL*, `A` sobre Dian Keto, icono de la mano que apunta (el 4.º), `A`. | Fairy Guardian se tributa y Dian Keto sale de tu cementerio y vuelve al fondo de tu mazo. |

## Arreglada en la revisión por capturas

| N.º | Carta | Estado | Pasos | Qué deberías ver |
|---|---|---|---|---|
| 27 | Lady Panther | `estados/revisar/27-lady-panther.ss1` | Turno 1: colocá boca abajo a Giant Soldier of Stone (DEF 2000) y terminá. El rival invoca a Mechanicalchaser (1850) y lo ataca: rebota (el rival pierde 150) y Giant Soldier queda boca arriba en defensa. Turno 2: invocá a Lady Panther; en el menú de Giant Soldier of Stone elegí *Attack Position*; `B`, *Enter Battle Phase*, y atacá con él (1300) a Mechanicalchaser: pierde, va al cementerio y vos perdés 550 LP. Después `B`, *Go to Main Phase 2*, cursor sobre Lady Panther, `A`, *Activate Effect*. Unos segundos después sale el aviso "Select monster to return to the Deck.": `A`, `A` sobre *ALL*, `A` sobre Giant Soldier of Stone, icono de la mano que apunta (el 4.º), `A`. | Lady Panther se tributa y Giant Soldier of Stone vuelve al tope de tu mazo: lo robás en tu turno siguiente. Antes el menú no ofrecía *Activate Effect*. |

## Variantes que pidió Oscar

| N.º | Carta | Estado | Pasos | Qué deberías ver |
|---|---|---|---|---|
| 28 | Magic Drain | `estados/revisar/28-magic-drain.ss1` | Igual que el 8, pero el rival tiene además 2 Mágicas en la mano (Black Pendant, que no puede jugar porque no tiene monstruos). Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival juega Dian Keto: "Will you chain?" → cuando el juego pregunte, *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*. | El texto dice que el rival **puede** descartar 1 Mágica para negar a Magic Drain. Mirá si lo hace: si descarta, Dian Keto cura (rival en 9000) y le queda una Mágica menos; si no, Dian Keto se niega como en el 8. |
| 29 | Windstorm of Etaqua | `estados/revisar/29-windstorm-of-etaqua.ss1` | Igual que el 6, pero con dos monstruos rivales. Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). Mientras el rival tenga un solo monstruo, cada vez que el juego pregunte contestá *No* (te va a atacar directo). Terminá tu segundo turno: el rival invoca a Tongyo y ataca con los dos; ahí cuando el juego pregunte, *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*. | Los dos monstruos boca arriba del rival cambian de posición, no solo el que ataca. |

## Completadas el 2026-10-11

| N.º | Carta | Estado | Pasos | Qué deberías ver |
|---|---|---|---|---|
| 30 | Kunai with Chain | `estados/revisar/30-kunai-with-chain.ss1` | Segundo efecto. Turno 1: invocá a Darkfire Soldier #2 (1700), colocá Kunai boca abajo y terminá. Al empezar el turno del rival el juego pregunta "It's the Draw Phase. Activate the effect...?": *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*. Aviso "Select your monster to equip.": `A`, `A` sobre Darkfire Soldier #2. | Darkfire Soldier #2 pasa de 1700 a 2200 de ATK y Kunai queda boca arriba en el campo, equipada. Si después tributás o te destruyen ese monstruo, Kunai va al cementerio con él. |
| 31 | Hiro's Shadow Scout | `estados/revisar/31-hiro-s-shadow-scout.ss1` | Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival invoca a Mechanicalchaser y la ataca. | El rival roba 3 cartas (antes robaba 1) y se muestran: Dian Keto, que es Mágica, va a su cementerio; Blue-Eyes y Call of the Haunted quedan en su mano (después coloca la Trampa). |
| 32 | Reasoning | `estados/revisar/32-reasoning.ss1` | Activala (menú de la carta, *Activate Effect*). Aviso "Your opponent declares Level N.": `A`. | Se revelan Dian Keto, Call of the Haunted y Mechanicalchaser (nivel 4). Si el aviso decía 4, las tres van al cementerio. Si decía 3 o 2, Mechanicalchaser se invoca ("Select card position.") y las otras dos van al cementerio. El nivel lo elige el juego: 4 la mayoría de las veces. Probala un par de veces para ver las dos. |
| 33 | Dark Necrofear | `estados/revisar/33-dark-necrofear.ss1` | Activá Card Destruction: tus tres Demonios van al cementerio y robás a Dark Necrofear. Menú de Necrofear, *Special Summon*; aviso "Select 3 Fiend monsters to remove from the Graveyard.": `A`, `A` (entra a la lista), y en cada Demonio `A`, `A` (icono *CHECK*); con los tres marcados, `A`, `DERECHA` cuatro veces hasta *DECIDE*, `A`. Posición de ataque (`A`) y terminá el turno. El rival invoca a Goblin Attack Force (2300) y ataca a Necrofear (2200). Al final de su turno, aviso "Select and gain control of 1 opponent's face-up monster.": `A`, `A` sobre Goblin Attack Force. En tu turno robás Heavy Storm: terminá ese turno sin jugarla, dejá pasar el del rival y, en tu turno siguiente, activala. | Necrofear se invoca retirando los tres Demonios. Cuando la destruyen perdés 100 LP y va al cementerio; Goblin Attack Force sigue siendo del rival durante el resto de su turno y recién en la End Phase se muestra la carta de Necrofear y aparece el aviso. Al elegirlo pasa a tu campo y Necrofear queda boca arriba en tu zona de Mágicas y Trampas, equipada a él. Sigue siendo tuyo en tus turnos siguientes. Cuando Heavy Storm destruye a Necrofear, va a tu cementerio y Goblin Attack Force vuelve al campo del rival. |

## Para tener presente

Reasoning: el nivel lo declara siempre el juego (no hay menú para que lo declare una persona), también
si la carta la activara el rival.

Se edita el **estado de un duelo** (manos y mazo de los dos lados). El archivo `.sav` no lo
sé editar todavía: su formato no está ubicado.
