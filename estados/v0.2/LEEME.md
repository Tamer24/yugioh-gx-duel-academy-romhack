# Pruebas para la v0.2

1. Abrí en mGBA el ROM `build/Yu-Gi-Oh! GX - Duel Academy (Lote).gba`.
2. *Archivo → Cargar estado desde archivo…* y elegí en `estados/v0.2/faltan/` el archivo que empieza con el número.
3. Hacé los pasos y fijate si pasa lo de "Qué tenés que ver".
4. Escribile a Claude, por ejemplo: "4 bien, 7: vi tal cosa". Claude lo anota y pasa el archivo a `listas/`.

Para terminar el turno: `B`, `A`. Las cartas restauradas muestran el dibujo del monstruo que reemplazan: es normal.

## Faltan

**11b. Mystical Refpanel contra Hinotama**: `faltan/11b-refpanel-hinotama.ss1`

- Pasos: Colocá Mystical Refpanel boca abajo (menú de la carta, *Set*) y terminá el turno (`B`, `A`). El rival juega Hinotama (500 de daño a vos): cuando pregunte "Will you chain?", *Yes*, `A`, cursor a tu trampa, `A`, *Activate Effect*.
- Qué tenés que ver: el daño lo recibe el rival. Quedás en 8000 y el rival en 7500.

**11c. Mystical Refpanel contra Ookazi**: `faltan/11c-refpanel-ookazi.ss1`

- Pasos: igual que 11b; el rival juega Ookazi (800 de daño).
- Qué tenés que ver: quedás en 8000 y el rival en 7200.

**11d. Mystical Refpanel contra Pot of Greed**: `faltan/11d-refpanel-pot-of-greed.ss1`

- Pasos: igual que 11b; el rival juega Pot of Greed (roba 2).
- Qué tenés que ver: es el caso dudoso. Según el texto, Refpanel cambia el jugador de una Mágica que apunta a uno solo: si el juego la deja activar, robás vos 2 y el rival ninguna. Si no te pregunta "Will you chain?" o no te deja activarla, contame qué pasó: puede ser lo correcto para este juego.

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
- Bagworm sin Máquina (1b y 1c), Penguin Knight, Hiro's Shadow Scout, Reasoning (niveles 4 y 3), Dark Necrofear, Mystical Refpanel con Dian Keto, 18/10
