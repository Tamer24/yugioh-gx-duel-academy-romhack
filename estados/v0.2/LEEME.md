# Pruebas para la v0.2

1. Abrí en mGBA el ROM `build/Yu-Gi-Oh! GX - Duel Academy (Lote).gba`.
2. *Archivo → Cargar estado desde archivo…* y elegí en `estados/v0.2/faltan/` el archivo que empieza con el número.
3. Hacé los pasos y fijate si pasa lo de "Qué tenés que ver".
4. Escribile a Claude, por ejemplo: "4 bien, 7: vi tal cosa". Claude lo anota y pasa el archivo a `listas/`.

Para terminar el turno: `B`, `A`. Las cartas restauradas muestran el dibujo del monstruo que reemplazan: es normal.

## Faltan

**1b. Electromagnetic Bagworm atacada por un no Máquina**: `faltan/01b-bagworm-atacada-por-no-maquina.ss1`

- Pasos: Colocá Bagworm boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival invoca a Blazing Inpachi (Piro, 1850/0) y la ataca.
- Qué tenés que ver: Bagworm se da vuelta y se destruye. **No** te deja quedarte con Blazing Inpachi (no aparece el aviso para elegir, o aparece sin nada para elegir). Blazing Inpachi baja de 1850 a 1350 de ATK: el −500 vale para cualquier monstruo que la destruya.

**1c. Electromagnetic Bagworm con solo un no Máquina del rival**: `faltan/01c-bagworm-solo-rival-no-maquina.ss1`

- Pasos: Colocá Bagworm boca abajo y terminá el turno. El rival invoca a Tongyo (Pez, 1350). Si la ataca, no la destruye y Bagworm queda boca arriba. Si no ataca, en tu turno siguiente dala vuelta vos (menú de la carta, *Flip Summon*).
- Qué tenés que ver: al darse vuelta **no** te deja tomar a Tongyo. Bagworm sigue en tu campo y Tongyo sigue siendo del rival.

**4. Penguin Knight**: `faltan/04-penguin-knight.ss1`

- Pasos: Penguin Knight **no** está en tu mano ni la vas a robar: está entre las 5 primeras cartas de tu mazo, y la prueba es que la mande al cementerio un efecto del rival. Turno 1: invocá a Darkfire Soldier #2 y terminá el turno. El rival coloca a Needle Worm boca abajo. Turno 2: `B`, *Enter Battle Phase*, y atacá a Needle Worm.
- Qué tenés que ver: Needle Worm se da vuelta y manda 5 cartas de tu mazo al cementerio, Penguin Knight entre ellas. Enseguida todo tu cementerio vuelve al mazo y se baraja: el cementerio queda vacío y el mazo con la misma cantidad que antes del ataque.

**7. Hiro's Shadow Scout**: `faltan/07-hiro-s-shadow-scout.ss1`

- Pasos: Colocala boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival invoca a Mechanicalchaser y la ataca.
- Qué tenés que ver: El rival roba 3 cartas (antes robaba 1) y se muestran: Dian Keto, que es Mágica, va a su cementerio; Blue-Eyes y Call of the Haunted quedan en su mano (después coloca la Trampa).

**8. Reasoning**: `faltan/08-reasoning.ss1`

- Pasos: Activala (menú de la carta, *Activate Effect*). Aviso "Your opponent declares Level N.": `A`.
- Qué tenés que ver: Se revelan Dian Keto, Call of the Haunted y Mechanicalchaser (nivel 4). Si el aviso decía 4, las tres van al cementerio. Si decía 3 o 2, Mechanicalchaser se invoca ("Select card position.") y las otras dos van al cementerio. El nivel lo elige el juego: 4 la mayoría de las veces. Probala un par de veces para ver las dos.

**9. Dark Necrofear**: `faltan/09-dark-necrofear.ss1`

- Pasos: Activá Card Destruction: tus tres Demonios van al cementerio y robás a Dark Necrofear. Menú de Necrofear, *Special Summon*; aviso "Select 3 Fiend monsters to remove from the Graveyard.": `A`, `A` (entra a la lista), y en cada Demonio `A`, `A` (icono *CHECK*); con los tres marcados, `A`, `DERECHA` cuatro veces hasta *DECIDE*, `A`. Posición de ataque (`A`) y terminá el turno. El rival invoca a Goblin Attack Force (2300) y ataca a Necrofear (2200). Al final de su turno, aviso "Select and gain control of 1 opponent's face-up monster.": `A`, `A` sobre Goblin Attack Force. En tu turno robás Heavy Storm: terminá ese turno sin jugarla, dejá pasar el del rival y, en tu turno siguiente, activala.
- Qué tenés que ver: Necrofear se invoca retirando los tres Demonios. Cuando la destruyen perdés 100 LP y va al cementerio; Goblin Attack Force sigue siendo del rival durante el resto de su turno y recién en la End Phase se muestra la carta de Necrofear y aparece el aviso. Al elegirlo pasa a tu campo y Necrofear queda boca arriba en tu zona de Mágicas y Trampas, equipada a él. Sigue siendo tuyo en tus turnos siguientes. Cuando Heavy Storm destruye a Necrofear, va a tu cementerio y Goblin Attack Force vuelve al campo del rival.

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

**26. Elemental Hero Neos** (opcional, carta nueva): `faltan/26-elemental-hero-neos.ss1`

- Pasos: Poné el cursor sobre Neos en tu mano y mirá su detalle. Si querés invocarla: bajá un monstruo por turno (por ejemplo Clayman y Mystical Elf), y en el tercer turno invocá a Neos tributando los dos.
- Qué tenés que ver: el detalle muestra nombre, dibujo, LIGHT, 7 estrellas, Warrior, texto y 2500/2000. Invocada, ataca con 2500.

## Ya confirmadas (en `listas/`)

- Rigorous Reaver, Jowls of Dark Demise, Dark-Eyes Illusionist, Reaper of the Cards, Windstorm of Etaqua, Magic Drain
- Electromagnetic Bagworm (con Máquina), 17/10
- Electric Snake, Minar, Fairy Guardian, Kunai with Chain (los dos efectos), 18/10
