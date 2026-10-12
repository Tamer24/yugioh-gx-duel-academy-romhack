carta: Mystical Refpanel (fila 9)
resultado: COINCIDE
esperado: Los 1000 LP los ganás vos: quedás en 9000 y el rival en 8000.
visto: Al activar Mystical Refpanel en la cadena contra Dian Keto the Cure Master, el rival queda en 8000 LP y yo pasé de 8000 a 9000 LP (+1000 para mí). Dian Keto the Cure Master va al cementerio del rival; Mystical Refpanel va a mi cementerio. Captura 013-a muestra "Chain: Activating" con BLOCK 1 Opponent (Dian Keto) y BLOCK 2 You (Mystical Refpanel); 014-a muestra el +1000 del lado del jugador.
antes: 011.png — paso 11: LP yo 8000 | rival 8000; mis magias y trampas ['Mystical Refpanel'] (boca abajo); menú de la carta con "Activate Effect" y "Detail Screen".
despues: 014.png — paso 14: LP yo 9000 | rival 8000; cementerio yo ['Mystical Refpanel'], cementerio rival ['Dian Keto the Cure Master']; captura en End Phase.
capturas clave:
- 007.png: "Dian Keto the Cure Master has activated. Will you chain?" con Yes marcado (pregunta de cadena).
- 008.png: aviso "Select Spell/Trap Card to activate." tras contestar Yes.
- 011.png: menú de mi trampa en el campo con "Activate Effect".
- 013-a.png: "Chain: Activating", BLOCK 1 Opponent (Dian Keto), BLOCK 2 You (Mystical Refpanel).
- 014-a.png: +1000 sobre mi LP (lado del jugador), todavía en la cadena.
- 014.png: End Phase, LP 9000 (mío, barra inferior) y 8000 (rival, barra superior).
diferencias con la guía: ninguna en el resultado. En los pasos: el rival juega Dian Keto y hace falta un "A" extra para avanzar el diálogo "This Spell Card is gonna do wonders!" antes de que aparezca "Will you chain?" (la guía no lo menciona). Para llegar a la trampa usé "cursor:2,1" (zona de mis magias y trampas) en lugar de flechas. No vi el texto de negación de Dian Keto: la captura muestra la cadena resolviéndose y el cambio de LP, que es lo que pide la guía.
pasos usados: 15 (paso 0 de inicio + 14 pasos de juego; ver salida de paso.py en la sesión)
verificado: las lecturas de memoria del registro de la sesión coinciden con lo informado (comprobación por script) y miré las capturas clave
