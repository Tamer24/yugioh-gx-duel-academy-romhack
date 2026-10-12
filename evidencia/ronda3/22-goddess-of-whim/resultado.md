carta: Goddess of Whim (fila 22)
resultado: COINCIDE (con una discrepancia de texto en el aviso de la moneda, ver "diferencias")
esperado: Invocala. Cursor sobre ella, `A`, *Activate Effect*, elegí cara o cruz. Avisa si acertaste y el ATK pasa de 950 a 1900 o a 475 hasta el fin del turno.
visto: Invocada en Main Phase 1 con ATK 950 / DEF 700 (salida paso 1, 001.png). Menú de campo: *Activate Effect* arriba y *Detail Screen* abajo (002.png). Al elegir *Activate Effect* sale "Select heads or tails." (004.png).
  Rama cara (Heads): el aviso dice "You called it wrong... ATK halved." y el ATK baja a 475 (paso 6: "ATK 475"; 006.png). LP sin cambios (8000 / 8000).
  Rama cruz (Tails, tras --volver 4): el aviso dice "You called it right! ATK doubled." y el ATK sube a 1900 (paso 9: "ATK 1900"; 009.png). LP sin cambios.
  Una vez usado el efecto, en el mismo turno el menú de Goddess of Whim muestra solo *Detail Screen* (006-b, 007-a/b, 009.png). No aparece *Activate Effect* otra vez.
  Terminé el turno (Yes en "Will you end your turn?", 011-a.png). Durante el turno del rival el ATK se mantiene 950 (paso 12: "ATK 950"). Al volver mi turno (Main Phase 1, paso 14: 014.png) ATK 950, DEF 700.
antes: 004.png — paso 4: "Select heads or tails." (ATK 950, evento 0x0)
despues: 006.png — paso 6: "ATK 475, DEF 700" tras el aviso "You called it wrong... ATK halved." (rama cara). Rama cruz: 009.png — paso 9: "ATK 1900, DEF 700" tras "You called it right! ATK doubled."
capturas clave:
  - 002.png: menú de campo con *Activate Effect* / *Detail Screen*.
  - 005-b.png: "You called it wrong... ATK halved." (Heads).
  - 008-c.png: "You called it right! ATK doubled." (Tails).
  - 009.png: ATK 1900 y menú reabierto con solo *Detail Screen*.
  - 014.png: mi Main Phase 1 con ATK 950 al volver el turno.
diferencias con la guía: Ninguna en el flujo. Discrepancia de texto: en la pantalla de la moneda aparece "Correct!" en la rama cara (005-a.png) y "Miss!" en la rama cruz (008-b.png), pero el aviso siguiente dice lo contrario ("called it wrong" / "called it right"). El ATK sí sigue al aviso (475 / 1900). Conviene que lo mires en mGBA para decidir si el rótulo de la moneda está mal. Además, en ambas ramas el menú de la carta se abrió con un `A` de más después del aviso (no con un paso pensado para eso); igual mostró solo *Detail Screen*.
pasos usados: 15 (pasos 0 a 14; el paso 8 es la rama cruz tras --volver 4)
verificado: el ATK y el una-vez-por-turno están bien, pero el subagente notó que el cartel de la moneda y el aviso se contradecían: era un defecto real (dos sorteos independientes). Arreglado; ver la ronda 4.
