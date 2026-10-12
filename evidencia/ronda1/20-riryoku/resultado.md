carta: Riryoku (fila 20)
resultado: COINCIDE
esperado: Turno 1: invocar Darkfire Soldier #2. Turno 2: invocar The Thing in the Crater, activarla y elegir los dos. El primero pierde la mitad del ATK y el segundo la gana, hasta el fin del turno.
visto: Turno 1: Darkfire Soldier #2 invocado (ATK 1700). Turno 2: The Thing in the Crater invocado (ATK 1000). Riryoku activada desde la mano; el juego pidió "Select monster to halve its ATK." y elegí Darkfire: pasó a ATK 850 (en color de reducción en el panel). Luego pidió "Select monster to increase ATK." y elegí The Thing: pasó a ATK 1850 (en color de aumento en el panel). Riryoku fue al cementerio. Al terminar el turno y pasar al turno del rival, la salida muestra Darkfire en ATK 1700 y The Thing en ATK 1000 de nuevo (la vuelta a los valores originales se ve en la lectura de memoria; en la captura de ese paso no se distinguen los ATK).
antes: 013.png — paso 13: cursor sobre The Thing in the Crater, ATK 1000, Riryoku todavía en mi zona de magias.
despues: 014.png — paso 14: "monstruos ['Darkfire Soldier #2 (ataque, ATK 850, DEF 1100)', 'The Thing in the Crater (ataque, ATK 1850, DEF 1200)']", cementerio ['Riryoku'].
capturas clave:
- 006.png: menú de Riryoku en la mano con Activate Effect resaltado.
- 007.png: aviso "Select monster to halve its ATK." sobre el campo.
- 011-a.png: aviso "Select monster to increase ATK." tras elegir Darkfire.
- 016.png: panel con Darkfire Soldier #2 en ATK 850 (color de reducción).
- 017.png: panel con The Thing in the Crater en ATK 1850 (color de aumento).
- 020.png: Draw Phase del rival, sin ATK visibles en pantalla (la vuelta a 1700/1000 sale de la lectura de memoria del paso 20).
diferencias con la guía: ninguna en el resultado. Notas: (1) la captura 014 muestra de forma poco clara las dos zonas de monstruo (se ve sobre todo un sprite); los ATK sí quedan verificados en los pasos 16 y 17 con el cursor. (2) El comando cursor:X,Y no funciona con un aviso de selección abierto; hay que cerrar el aviso con A antes de moverlo, y con el aviso de selección hay que mover con LEFT/RIGHT. (3) El texto de los avisos ("halve" / "increase") no está en la guía; lo anoto por si quieren contrastarlo.
pasos usados: 21 (paso 0 a paso 20)
verificado: las lecturas de memoria del registro de la sesión coinciden con lo informado (comprobación por script) y miré las capturas clave
