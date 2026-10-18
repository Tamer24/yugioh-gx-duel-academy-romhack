# Pruebas para la v0.2

1. Abrí en mGBA el ROM `build/Yu-Gi-Oh! GX - Duel Academy (Lote).gba`.
2. *Archivo → Cargar estado desde archivo…* y elegí el archivo de `estados/v0.2/faltan/` que empieza con el número.
3. Hacé los pasos y fijate si pasa lo de "Qué tenés que ver".
4. Escribile a Claude, por ejemplo: "1 bien, 2 bien, 3: vi tal cosa". Claude lo anota y pasa el archivo a `listas/`.

Para terminar el turno: `B`, `A`. Las cartas restauradas muestran el dibujo del monstruo que reemplazan: es normal.
Kunai with Chain aparece dos veces (6 y 10) porque tiene dos efectos.

## Faltan

### Primero: las 9 que cambiaron el 11/10

**1. Electromagnetic Bagworm**: lista (17/10). Faltan dos variantes con un monstruo que no es Máquina:

**1b. Bagworm atacada por un no Máquina**: `faltan/01b-bagworm-atacada-por-no-maquina.ss1`

- Pasos: Colocá Bagworm boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival invoca a Blazing Inpachi (Pyro, 1850/0) y la ataca.
- Qué tenés que ver: Bagworm se voltea y se destruye. **No** te deja tomar el control de Blazing Inpachi: no aparece el aviso para elegir, o aparece sin nada para elegir. Blazing Inpachi baja de 1850 a 1350 de ATK (el −500 vale para cualquier monstruo que la destruya, no solo Máquinas).

**1c. Bagworm volteada con solo un no Máquina del rival**: `faltan/01c-bagworm-solo-rival-no-maquina.ss1`

- Pasos: Colocá Bagworm boca abajo y terminá el turno. El rival invoca a Tongyo (Pez, 1350): si la ataca, rebota (DEF 1400) y Bagworm se voltea. Si no ataca, en tu turno siguiente volteala vos (menú de la carta, *Flip Summon*).
- Qué tenés que ver: al voltearse **no** te deja tomar el control de Tongyo. Bagworm sigue en el campo y Tongyo sigue siendo del rival.

**2. Electric Snake**: `faltan/02-electric-snake.ss1`

- Pasos: Terminá el turno sin jugar nada. El rival juega Card Destruction y descarta tu mano.
- Qué tenés que ver: Robás 2 cartas de más: quedás con 8 en la mano (las 6 que repone Card Destruction y las 2 de Electric Snake) en vez de 6.

**3. Minar**: `faltan/03-minar.ss1`

- Pasos: Terminá el turno sin jugar nada. El rival juega Card Destruction y descarta tu mano.
- Qué tenés que ver: El rival pierde 1000 LP (queda en 7000).

**4. Penguin Knight**: `faltan/04-penguin-knight.ss1`

- Pasos: Turno 1: invocá a Darkfire Soldier #2 y terminá. El rival coloca a Needle Worm boca abajo. Turno 2: `B`, *Enter Battle Phase*, y atacalo.
- Qué tenés que ver: Needle Worm manda 5 cartas de tu mazo al cementerio, Penguin Knight entre ellas, y enseguida todo tu cementerio vuelve al mazo, que se baraja: el cementerio queda vacío.

**5. Fairy Guardian**: `faltan/05-fairy-guardian.ss1`

- Pasos: Turno 1: invocá a Fairy Guardian y terminá. El rival coloca Magic Jammer. Turno 2: activá Dian Keto; el rival la niega. En ese mismo turno: cursor sobre Fairy Guardian, `A`, *Activate Effect*. Aviso "Select Spell Card to return to the Deck.": `A`, `A` sobre *ALL*, `A` sobre Dian Keto, icono de la mano que apunta (el 4.º), `A`.
- Qué tenés que ver: Fairy Guardian se tributa y Dian Keto sale de tu cementerio y vuelve al fondo de tu mazo.

**6. Kunai with Chain**: `faltan/06-kunai-with-chain.ss1`

- Pasos: Segundo efecto. Turno 1: invocá a Darkfire Soldier #2 (1700), colocá Kunai boca abajo y terminá. Al empezar el turno del rival el juego pregunta "It's the Draw Phase. Activate the effect...?": *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*. Aviso "Select your monster to equip.": `A`, `A` sobre Darkfire Soldier #2.
- Qué tenés que ver: Darkfire Soldier #2 pasa de 1700 a 2200 de ATK y Kunai queda boca arriba en el campo, equipada. Si después tributás o te destruyen ese monstruo, Kunai va al cementerio con él.

**7. Hiro's Shadow Scout**: `faltan/07-hiro-s-shadow-scout.ss1`

- Pasos: Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival invoca a Mechanicalchaser y la ataca.
- Qué tenés que ver: El rival roba 3 cartas (antes robaba 1) y se muestran: Dian Keto, que es Mágica, va a su cementerio; Blue-Eyes y Call of the Haunted quedan en su mano (después coloca la Trampa).

**8. Reasoning**: `faltan/08-reasoning.ss1`

- Pasos: Activala (menú de la carta, *Activate Effect*). Aviso "Your opponent declares Level N.": `A`.
- Qué tenés que ver: Se revelan Dian Keto, Call of the Haunted y Mechanicalchaser (nivel 4). Si el aviso decía 4, las tres van al cementerio. Si decía 3 o 2, Mechanicalchaser se invoca ("Select card position.") y las otras dos van al cementerio. El nivel lo elige el juego: 4 la mayoría de las veces. Probala un par de veces para ver las dos.

**9. Dark Necrofear**: `faltan/09-dark-necrofear.ss1`

- Pasos: Activá Card Destruction: tus tres Demonios van al cementerio y robás a Dark Necrofear. Menú de Necrofear, *Special Summon*; aviso "Select 3 Fiend monsters to remove from the Graveyard.": `A`, `A` (entra a la lista), y en cada Demonio `A`, `A` (icono *CHECK*); con los tres marcados, `A`, `DERECHA` cuatro veces hasta *DECIDE*, `A`. Posición de ataque (`A`) y terminá el turno. El rival invoca a Goblin Attack Force (2300) y ataca a Necrofear (2200). Al final de su turno, aviso "Select and gain control of 1 opponent's face-up monster.": `A`, `A` sobre Goblin Attack Force. En tu turno robás Heavy Storm: terminá ese turno sin jugarla, dejá pasar el del rival y, en tu turno siguiente, activala.
- Qué tenés que ver: Necrofear se invoca retirando los tres Demonios. Cuando la destruyen perdés 100 LP y va al cementerio; Goblin Attack Force sigue siendo del rival durante el resto de su turno y recién en la End Phase se muestra la carta de Necrofear y aparece el aviso. Al elegirlo pasa a tu campo y Necrofear queda boca arriba en tu zona de Mágicas y Trampas, equipada a él. Sigue siendo tuyo en tus turnos siguientes. Cuando Heavy Storm destruye a Necrofear, va a tu cementerio y Goblin Attack Force vuelve al campo del rival.

### Después: las demás

**10. Kunai with Chain**: `faltan/10-kunai-with-chain.ss1`

- Pasos: Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival ataca: cuando el juego pregunte, *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*.
- Qué tenés que ver: El atacante pasa a defensa y, como no tenés monstruos, Kunai va al cementerio. El segundo efecto (equiparla) está en la fila 30.

**11. Mystical Refpanel**: `faltan/11-mystical-refpanel.ss1`

- Pasos: Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival juega Dian Keto: "Will you chain?" → cuando el juego pregunte, *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*.
- Qué tenés que ver: Los 1000 LP los ganás vos: quedás en 9000 y el rival en 8000.

**12. Riryoku Field**: `faltan/12-riryoku-field.ss1`

- Pasos: Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival invoca a Mechanicalchaser y le equipa Black Pendant: "Will you chain?" → cuando el juego pregunte, *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*.
- Qué tenés que ver: Black Pendant se niega y se destruye.

**13. Big Burn**: `faltan/13-big-burn.ss1`

- Pasos: Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival juega Card Destruction (los dos descartan la mano) y después Monster Reborn: `A` en el aviso del objetivo, "Will you chain?" → cuando el juego pregunte, *Yes*, `A`, llevá el cursor a tu trampa, `A`, *Activate Effect*.
- Qué tenés que ver: Todos los monstruos de los dos cementerios se retiran del juego y Monster Reborn no invoca nada.

**14. Acid Trap Hole**: `faltan/14-acid-trap-hole.ss1`

- Pasos: Invocá a Darkfire Soldier #2, colocá la trampa y terminá el turno. El rival coloca a Tongyo boca abajo. En tu turno siguiente: cursor sobre la trampa, `A`, *Activate Effect*, y elegí ese monstruo.
- Qué tenés que ver: Tongyo se voltea y se destruye.

**15. Two-Pronged Attack**: `faltan/15-two-pronged-attack.ss1`

- Pasos: Turno 1: invocá a Darkfire Soldier #2 y colocá la trampa. Turno 2: invocá a The Thing in the Crater. Activá la trampa y elegí tus dos monstruos y el del rival.
- Qué tenés que ver: Los tres van al cementerio.

**16. Ready for Intercepting**: `faltan/16-ready-for-intercepting.ss1`

- Pasos: Turno 1: invocá a Sonic Maid (Guerrero) y colocá la trampa. Turno 2: activá la trampa sobre Sonic Maid.
- Qué tenés que ver: Sonic Maid queda boca abajo en defensa.

**17. The Inexperienced Spy**: `faltan/17-the-inexperienced-spy.ss1`

- Pasos: Activala (menú de la carta, *Activate Effect*).
- Qué tenés que ver: Se muestra 1 carta al azar de la mano del rival (una de Penguin Soldier, Dekoichi, Fusion Sage, Snatch Steal o Hane-Hane). `B` cierra la lista y la carta va al cementerio.

**18. Exchange**: `faltan/18-exchange.ss1`

- Pasos: Activala. `A` en el aviso, `A` sobre *ALL*, `A` sobre una carta, icono de la mano que apunta (*DECIDE*, el 4.º), `A`.
- Qué tenés que ver: Esa carta pasa a tu mano y una tuya, al azar, a la del rival.

**19. Chosen One**: `faltan/19-chosen-one.ss1`

- Pasos: Activala y marcá 1 monstruo (Darkfire Soldier #2) y 2 Mágicas o Trampas (Trap Hole y Dian Keto).
- Qué tenés que ver: El rival saca una al azar. Si es el monstruo, se invoca y las otras 2 van al cementerio; si no, las 3.

**20. Seal of the Ancients**: `faltan/20-seal-of-the-ancients.ss1`

- Pasos: Turno 1: invocá a Darkfire Soldier #2 y terminá. El rival coloca cartas boca abajo. Turno 2: activala.
- Qué tenés que ver: Pagás 1000 LP y ves, en destellos rápidos, qué son las cartas boca abajo del rival.

**21. Share the Pain**: `faltan/21-share-the-pain.ss1`

- Pasos: Turno 1: invocá a Darkfire Soldier #2 y terminá. El rival coloca a Tongyo. Turno 2: activala y tributá a Darkfire Soldier #2.
- Qué tenés que ver: El rival pierde a Tongyo.

**22. Riryoku**: `faltan/22-riryoku.ss1`

- Pasos: Turno 1: invocá a Darkfire Soldier #2. Turno 2: invocá a The Thing in the Crater, activala y elegí los dos.
- Qué tenés que ver: El primero pierde la mitad del ATK y el segundo la gana, hasta el fin del turno.

**23. Monster Recovery**: `faltan/23-monster-recovery.ss1`

- Pasos: Invocá a Darkfire Soldier #2 y activala.
- Qué tenés que ver: Darkfire Soldier #2 y las 4 cartas de tu mano vuelven al mazo, y robás 4 (las que tenías en la mano).

**24. Goddess of Whim**: `faltan/24-goddess-of-whim.ss1`

- Pasos: Invocala. Cursor sobre ella, `A`, *Activate Effect*, elegí cara o cruz.
- Qué tenés que ver: Avisa si acertaste y el ATK pasa de 950 a 1900 o a 475 hasta el fin del turno.

**25. Lady Panther**: `faltan/25-lady-panther.ss1`

- Pasos: Turno 1: colocá boca abajo a Giant Soldier of Stone (DEF 2000) y terminá. El rival invoca a Mechanicalchaser (1850) y lo ataca: rebota (el rival pierde 150) y Giant Soldier queda boca arriba en defensa. Turno 2: invocá a Lady Panther; en el menú de Giant Soldier of Stone elegí *Attack Position*; `B`, *Enter Battle Phase*, y atacá con él (1300) a Mechanicalchaser: pierde, va al cementerio y vos perdés 550 LP. Después `B`, *Go to Main Phase 2*, cursor sobre Lady Panther, `A`, *Activate Effect*. Unos segundos después sale el aviso "Select monster to return to the Deck.": `A`, `A` sobre *ALL*, `A` sobre Giant Soldier of Stone, icono de la mano que apunta (el 4.º), `A`.
- Qué tenés que ver: Lady Panther se tributa y Giant Soldier of Stone vuelve al tope de tu mazo: lo robás en tu turno siguiente. Antes el menú no ofrecía *Activate Effect*.

## Ya confirmadas (están en `listas/`)

- Electromagnetic Bagworm (con Mechanicalchaser)
- Rigorous Reaver
- Jowls of Dark Demise
- Dark-Eyes Illusionist
- Reaper of the Cards
- Windstorm of Etaqua
- Magic Drain
