# Cómo revisar una carta por capturas

Vas a jugar un duelo de *Yu-Gi-Oh! GX Duel Academy* (GBA) por script, sin ventana, para comprobar
si una carta hace lo que dice su fila de la guía. Jugás de a pasos: cada paso aprieta botones,
saca capturas y te muestra el duelo leído de la memoria. **Mirá la captura antes de decidir el
paso siguiente.**

Todo se corre desde la raíz del proyecto.

## Tu carta

Te pasan un número `N` y una carpeta de sesión. La fila `N` de
`specs/001-cerrar-pruebas-lote/guia-oscar.md` dice el estado a cargar, los pasos y qué debería
verse. Leé esa fila (y la sección "Para tener en cuenta" de arriba). La guía está escrita para
una persona con el emulador; vos hacés lo mismo con la herramienta.

## La herramienta

```
ROM="build/Yu-Gi-Oh! GX - Duel Academy (Lote).gba"
python3 scripts/paso.py "$ROM" SESION --desde ESTADO           # empieza la sesión
python3 scripts/paso.py "$ROM" SESION "ORDEN" ["ORDEN" ...]    # sigue desde el último paso
python3 scripts/paso.py "$ROM" SESION --volver K "ORDEN"       # retoma desde el paso K
```

Órdenes (cada una entre comillas):

- `"A w60 DOWN*2 f A"`: botones (`A B UP DOWN LEFT RIGHT L R START SELECT`), esperas en cuadros
  (`w60` = 1 segundo), repeticiones (`DOWN*2`) y `f` = sacar una captura en ese momento.
- `"mano:Nombre exacto"`: lleva el cursor a esa carta de tu mano. Solo sin menús abiertos.
- `"cursor:X,Y"`: lleva el cursor a la columna X de la fila Y. Filas: 0 tu mano, 1 tus magias y
  trampas, 2 tus monstruos, 3 monstruos del rival, 4 magias y trampas del rival. En las filas del
  campo la zona 0 es la columna 2, la zona 1 la columna 3, y así.

Cada paso imprime LP, cursor, manos, campo (con posición, ATK y DEF), cementerios, retiradas,
cantidad de cartas en cada mazo, y las rutas de las capturas (`NNN.png` al final del paso,
`NNN-a.png`, `NNN-b.png`... las pedidas con `f`). Las capturas se miran con la herramienta Read.

Si un paso sale mal (apretaste de más, se abrió otra cosa), no sigas encima: retomá con
`--volver K` desde el último paso bueno.

## Cómo se maneja el juego (medido)

- **Menú de una carta:** `A` sobre la carta lo abre. El cursor arranca en la **última** opción
  (*Detail Screen*). `UP` sube; `DOWN` desde la última da la vuelta a la primera. `B` lo cierra.
  - Monstruo en la mano: *Summon* / *Set* / *Detail Screen*.
  - Mágica en la mano: *Activate Effect* / *Set* / *Detail Screen*.
  - Trampa en la mano: *Set* / *Detail Screen*.
  - Trampa o Mágica colocada, o monstruo en el campo: *Activate Effect* (si se puede) y otras.
- **Invocar:** `"mano:Carta" "A w50 DOWN A w240"`. La animación dura unos 3 segundos: no aprietes
  nada mientras tanto. Un monstruo por turno.
- **Colocar boca abajo (Set):** monstruo `"mano:Carta" "A w50 UP A w120"`; trampa igual.
  Comprobá en la salida que quedó en el campo.
- **Terminar el turno:** sin menús abiertos, `"B w50 f A w120"`. En el primer turno pregunta
  *Will you end your turn?* con *Yes* marcado. Desde el segundo turno `B` ofrece *Enter Battle
  Phase* arriba y *End Turn* abajo: para terminar es `"B w50 DOWN f A w120"`. Mirá la captura.
- **Turno del rival:** avanzá con `"w120 f A w90 f A w90 f"`, de a poco. `A` cierra los diálogos.
  Cuando el juego **pregunta** algo (*Activate...?*, *Will you chain?*) hay *Yes* arriba y *No*
  abajo: pará, mirá, y contestá lo que dice la guía. Cuando vuelve a ser tu turno (tu mano tiene
  una carta más y se ve *Main Phase 1*) **dejá de apretar `A`**: abriría menús de tus cartas.
- **Activar una trampa cuando el juego pregunta:** *Yes* (`A`), sale el aviso *Select Spell/Trap
  Card to activate.* (`A` lo cierra), llevá el cursor a tu trampa con las flechas (mirá la
  captura para ver dónde quedó), `A` abre su menú, `UP` hasta *Activate Effect*, `A`.
- **Atacar:** `"B w80 A w170"` entra a la Battle Phase; cursor sobre tu monstruo, `A` abre su
  menú, `UP` hasta *Attack*, `A`; avisos con `A`; `A` sobre el objetivo.
- **Listas de cartas** (pantalla *Select card* / *Hand*, para descartar o elegir): primero el
  cursor está arriba, sobre el filtro *ALL*: `A` entra a la lista. `UP`/`DOWN` mueven entre las
  cartas. `A` sobre una carta abre una fila de 5 iconos con el cursor en el primero (*FILTER*):
  el que **elige** la carta es el 4.º, la mano que apunta a una carta: `"RIGHT*3 f A w120"`.
  Los otros iconos filtran u ordenan; `B` cierra la fila. Cuando hay que elegir **varias** cartas
  el 4.º icono es *CHECK* y las marca de a una (mirá la captura después de cada una); cuando el
  contador llega a "0 cards remaining", `A` sobre cualquier carta muestra un **5.º icono** (la
  mano que apunta): ese confirma la selección: `"A w40 RIGHT*4 f A w120"`.
  En una lista que es solo para **mirar** (sin elegir), `B` la cierra.
- **El juego pregunta en cada fase:** con una Trampa tuya colocada, el juego pregunta *It's the
  Draw Phase / Standby Phase... Activate the effect of Spell/Trap/Effect Monster?* en las fases
  del rival y en las tuyas, y también cuando el rival invoca o coloca. Tiene *Yes* marcado: para
  seguir de largo es `"DOWN w20 f A w150 f"` (No), una vez por pregunta. Si la pantalla parece
  congelada y la salida dice `evento` distinto de `0x0`, hay una pregunta esperando: sacá una
  captura y contestala. Si contestaste *Yes* sin querer, retomá con `--volver`.
- **Si el rival no hace lo que dice la guía** (por ejemplo coloca boca abajo en vez de atacar): su
  jugada depende del azar, y el azar depende de cuántos cuadros pasaron. Retomá con `--volver K`
  desde el paso anterior a terminar tu turno y agregá una espera distinta antes (`"w13"`, `"w29"`,
  `"w47"`, `"w71"`...). Probá hasta 6 esperas distintas antes de rendirte.
- No aprietes `A` varias veces seguidas sin mirar: en las listas marca y desmarca.
- Los efectos y avisos tardan: después de activar algo, esperá (`w120`) y sacá capturas con `f`
  repartidas (`"A w40 f w40 f w40 f w120"`) para no perderte los que duran poco.

## Reglas

1. De a pocos botones por paso, y mirá la captura. No encadenes diez acciones a ciegas.
2. Escribí **solo** dentro de tu carpeta de sesión. No toques scripts, estados, CSV ni documentos.
   No uses `w8:` (escribir memoria).
3. Un resultado vale solo si lo respaldan **la captura y los números** de la salida (LP, ATK,
   zonas). Si la captura y la memoria no coinciden, decilo.
4. No supongas. Si no llegaste a ver el efecto, el resultado es "no llegué", no "funciona".
5. Tope: unos 60 pasos. Si no llegás, pará e informá hasta dónde llegaste y qué te trabó.
6. No lances otros agentes.

## Qué entregar

Al terminar escribí `resultado.md` en tu carpeta de sesión y devolvé ese mismo texto:

```
carta: <nombre> (fila N)
resultado: COINCIDE | NO COINCIDE | NO LLEGUE
esperado: <lo que dice la guía>
visto: <qué pasó, con números: LP, ATK, qué carta fue a qué zona>
antes: <NNN.png> — <línea de la salida de ese paso que importa>
despues: <NNN.png> — <línea de la salida de ese paso que importa>
capturas clave: <3 a 6 archivos, cada uno con qué muestra>
diferencias con la guía: <pasos que no fueron como dice, textos distintos, o "ninguna">
pasos usados: <cantidad>
```

`COINCIDE` = se vio exactamente lo de "Qué deberías ver". Para las filas que dicen "**Debería**
... En mis pruebas ..." el resultado compara con lo que **debería** pasar: si pasó lo de "en mis
pruebas", es `NO COINCIDE` y lo aclarás en "visto".
