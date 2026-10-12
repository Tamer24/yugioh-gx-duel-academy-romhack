# Duel Academy romhack: plan de trabajo

Estado al **2026-10-11** (noche). Complementa a `PROYECTO.md` (mapa del ROM y backlog),
`NOTAS-REVERSE.md` (detalle técnico), `PRUEBAS.md` (cómo probar y resultados) y `ACCIONES.md` (el
recetario: cómo se implementa cada acción de una carta).

## 1. Dónde estamos

**Las 30 cartas del lote tienen veredicto** y, desde el 2026-10-11 por la noche, **las 30 funcionan**.
La tabla completa se genera en `PRUEBAS.md` desde `datos/pruebas.csv`.

| Veredicto | Cartas |
|---|---|
| Funcionan (30) | Rigorous Reaver, Jowls of Dark Demise, Windstorm of Etaqua, Ready for Intercepting, Seal of the Ancients, The Inexperienced Spy, Exchange, Chosen One, Share the Pain, Goddess of Whim, Riryoku, Monster Recovery, Acid Trap Hole, Mystical Refpanel, Two-Pronged Attack, Magic Drain, Riryoku Field, Dark-Eyes Illusionist, Reaper of the Cards, Big Burn, Lady Panther, Hiro's Shadow Scout, Kunai with Chain, Electric Snake, Minar, Penguin Knight, Fairy Guardian, Reasoning, **Electromagnetic Bagworm, Dark Necrofear** |
| En parte (0) | |
| No funcionan (0) | |

**Tanda del 2026-10-11 por la noche** (detalle en `NOTAS-REVERSE.md`, "Bagworm −500 y la posesión de
Dark Necrofear"):

- **Electromagnetic Bagworm, −500:** la Máquina que la destruye en batalla queda con 500 menos de ATK y
  DEF, de forma permanente. Dos ganchos la suman a la lista del motor que ya tenía a Slate Warrior.
- **Dark Necrofear, posesión:** destruida en batalla o por un efecto del rival, en la End Phase de ese
  turno pide elegir un monstruo rival boca arriba y toma su control. **Versión fiel:** Necrofear pasa
  del cementerio a la zona de Mágicas y Trampas, boca arriba, equipada a ese monstruo; si la destruyen,
  el monstruo vuelve al rival; si destruyen al monstruo, ella va al cementerio; destruida estando
  equipada no vuelve a activarse. (La primera versión, del mismo día, dejaba el control permanente.)
- Las dos tienen prueba de lógica, tres corridas en duelo y partida por capturas (`evidencia/ronda7/`).
  La de Necrofear incluye la invocación retirando 3 Demonios, que sigue andando.
- Necrofear quedó probada también **en manos del rival** (la IA elige sola a mi monstruo en mi End
  Phase) y en los dos casos **sin posesión** (descartada por el rival; destruida por una Mágica mía).
  Con las tres de Necrofear ya equipada (mi Heavy Storm, mi Dark Hole, Harpie's Feather Duster del
  rival) son nueve sondas en `probar_lote.py ROM "Dark Necrofear"`.
- La carta de Necrofear ya no se muestra al ser destruida en batalla (era un aviso del motor, sin
  efecto): ahora se ve una sola vez, en la End Phase. Son 2 bytes (`B:0801786E:2BD0:C046` en la receta).

**Tanda del 2026-10-11 por la tarde** (detalle en `NOTAS-REVERSE.md`, "Completar y arreglar el lote"):

- **Hiro's Shadow Scout:** el rival roba 3 (robaba 1).
- **Kunai with Chain:** se puede equipar (+500 ATK) y queda en el campo.
- **Electromagnetic Bagworm:** el control termina al final de mi turno siguiente (era permanente).
- **Electric Snake, Minar, Penguin Knight, Fairy Guardian:** un solo gancho agrega al motor el
  "enviada al cementerio por un efecto del rival", que no existía. Penguin Knight y Fairy Guardian
  necesitaron además el final de su resolución.
- **Reasoning:** dejó de estar aparcada. El nivel lo declara el juego; revela, invoca o manda al
  cementerio.

Cada una pasó la prueba de lógica, tres corridas en duelo (`scripts/probar_lote.py`) y una partida
por capturas desde el estado de Oscar (`evidencia/ronda6/`, galería en `evidencia/index.html`).

**Revisión por capturas (2026-10-11, mañana).** Las 29 filas de la guía se jugaron por script
(`evidencia/COMO-REVISAR.md`, `scripts/paso.py`). Encontró tres defectos que la prueba automática no
veía (The Inexperienced Spy, Chosen One, Goddess of Whim), ya arreglados, y destrabó a Lady Panther.

Aptas para un ROM de juego: 6 (Rigorous Reaver, Jowls of Dark Demise, Reaper of the Cards,
Dark-Eyes Illusionist, Windstorm of Etaqua, Magic Drain). **A las otras 24 les falta
solo la confirmación a ojo de Oscar**: la revisión por capturas no la reemplaza (Principio IV). Kunai
with Chain la tenía y volvió a pendiente porque ahora hace algo más.

ROM de trabajo: `build/…(Lote).gba` (MD5 `c1b1289a1e0a3ca4c725272073c791db`), armado con
`scripts/construir_lote.sh`. Después de rearmarlo: las pruebas `scripts/test_*.py`
(`test_modificadores.py` pide además `datos/volcado_goddess`), `probar_lote.py`, `probar_trampas.py` y
`scripts/repetir_sesion.py ROM evidencia/ronda*/*`, **de a un proceso por vez** (ver "Lo que NO
funciona"). Las cuatro se corrieron sobre este ROM: todo igual que antes salvo las dos cartas nuevas.

## 2. Lo aprendido (lo que no hay que redescubrir)

**Cómo funciona una carta en el motor**

1. Las funciones de la fila de efecto son **pasos de una máquina de estados** de
   activación. El estado vive en `0x020204C6`; cada función recibe la carta y
   devuelve el estado siguiente (`0` = nada). Códigos típicos: `0x80` (entrada),
   `0x7F`, `0x7E`, `0x7D`, `0x7C`; `0x64` es un cierre habitual.
2. `fn_10` es la **condición** (recursos, objetivos). Pot of Greed, Chosen One y la
   Spy lo demuestran.
3. Mostrar y elegir cartas usa el **registro de efectos**: `clear_zone_effects(6,0)`,
   `remove_card_from_effect_register(carta)` (agrega) e `init_effect_dialogue(...)`.
   Aoi (mano rival) y Ancient Telescope (mazo) son los moldes.
4. Los **menús de selección** son 29 modos (`FUN_08026970`, despachador
   `FUN_08026614`, tabla `0x08026678`). Vacíos: 6, 7, 13, 14, 16, 25, 26, 27, 28.
   El 9 es un stub. Las cartas recortadas que usan modos vacíos fallan.
5. Una carta recortada falla por **una razón propia**: no existe una causa única.
   Se descartó que fueran "códigos vacíos" (`0x64`–`0x7B`) o la forma de la fila.

6. **Estado devuelto = estado siguiente.** El motor vuelve a llamar a `fn_04` con el estado
   que ella misma devolvió. Después de `ask_question` hay que devolver un estado EXPLÍCITO
   (`0x7F`); si no, llega un valor cualquiera (`0x4D`, `0x51`). Secuencia de las originales
   con lista (Painful Choice, Aoi): `0x80` pregunta → `0x7F` abre la lista → `0x7E` resuelve
   → `0x64` cierre.
7. **Candidatas:** `FUN_0805AEB0(lado, ID, 0)` registra los candidatos *y* prepara la
   solicitud que consume el aviso. Con el **ID de Aoi (6440)** registra la mano del rival.
   Con registros manuales el aviso no aparece.
8. **Lista de selección:** `init_effect_dialogue(0, n, 0x02019F24, 1)` más los tres ajustes de
   Telescope. `n` = cuántas cartas elegir. Con `n = 1` el menú de la carta trae un icono de
   **elegir** (mano que apunta a una carta); con `n > 1`, CHECK. La elegida queda en
   `(u32@0x02019F24 & 0x7FFFF) >> 11`.
9. **Mover una carta entre manos:** intercambiar las 0x50 bytes de las dos ranuras e invertir el
   bit de dueño (bit 3 de `+0x32`). Las listas de mano no se tocan.
10. **ATK:** una escritura en `ranura+0x28` persiste hasta que el motor recalcula; el motor
    restaura la base al cambiar de turno y también tras resolver una cadena (4 cuadros
    después). Sobrevivir exige registrar el cambio como modificador (`+0x3E`/`+0x40`).
11. **Cartas por ranura:** `0x02022250 + (id & 0x7F) * 0x50 + (id >> 7) * 0x2B08`; ATK `+0x28`,
    DEF `+0x2C`, índice `+0x24`, dueño bit 3 de `+0x32`. Manos: lista en `+0x2824`, cantidad
    `((b[+0x1C] & 0x3F) << 1) | (b[+0x1B] >> 7)`.
12. **Evento `0x4B`:** `FUN_0801A5BC(lado, a, b, tipo)`. Las originales usan tipos 4, 6, 10, 13
    y 15; el 9 solo lo usa Riryoku.

13. **Fuera del estado de entrada una función de efecto devuelve 0.** Si devuelve `0x80` el motor
    vuelve a entrar: así se reabría sin fin la lista de la Spy. Telescope es el molde.
14. **Sorteo de Chosen One** (estado `0x7A` original): tira hasta sacar un índice distinto del
    "anterior" (`0x020204C8`) y repite `0x020204C7` veces. Hay que dejar el anterior en `0xFF`.
15. **Moneda** (menú "Select heads or tails", modo `0x15`): el motor ya tira la moneda, muestra
    "Correct!" o "Miss!" y deja el resultado en `0x02022250 + 0x5656` (1 = acertó). No es lo que
    llamó el jugador.
16. **Banderas por carta** en `ranura + 0x60` (`FUN_0800E09C(lado, ranura, bit)` las lee): bit 5 =
    destruido en batalla este turno (Lady Panther), bit 14 = efecto de campo de una vez por turno,
    bit 6 = lo que pide Fairy Guardian (no se encontró quién lo pone).
17. **Efectos que se activan desde el menú del campo:** el ID tiene que estar en las dos listas de
    `efectos/gancho_lista_campo.s` y `efectos/gancho_menu_campo.s`.
18. **Con una Trampa colocada el juego pregunta en cada fase** si la activás (también en las del
    rival). No es un cuelgue: `evento` distinto de 0 y pantalla quieta = pregunta esperando.

19. **Bandera puesta por evento:** el motor pone casi todas las banderas de `ranura+0x60` con el evento
    `0x3B` (y las quita con el `0x3C`), no llamando a la función que las pone. La `0x15` es "vuelve a
    su dueño en la End Phase" (Change of Heart).
20. **Disparadores "fue al cementerio":** están por ID al final de `FUN_080188AC`, con la zona de
    origen a la vista. Un efecto disparado se encola con `FUN_080314B4`.
21. **Quién causó un envío al cementerio:** la acción trae la ranura causante, salvo los descartes de
    mano y mazo; para esos vale la carta que se está resolviendo (`0x020204A4`, bit 0 = lado).
22. **Antes de escribir un efecto, buscar si el motor ya lo tiene a medias:** el +500 de Kunai estaba
    en el calculador y solo faltaba la llamada que equipa; a Fairy Guardian le faltaba una línea.
23. **`ask_question` muestra un texto propio** guardado en el espacio libre.

24. **Un pedido de efecto trae tipo y momento** en su cabecera: tipo `(p[1] >> 1) & 0xF`, momento
    `(cabecera >> 13) & 0x3F`. El motor usa el momento `0xE` para los disparadores "fue al cementerio";
    la posesión de Necrofear se encola con el `5`. Así una misma `fn_04`/`fn_18` distingue quién la llama.
25. **Destruida o solo enviada:** lo dice el bit `0x40` de las banderas de la acción (`0x9041` Raigeki
    del rival, `0x9001` descarte por Card Destruction, `0x1041` Dark Hole propio). La bandera 4 de la
    carta ("destruida por un efecto") no sirve: Raigeki y Dark Hole no la ponen.
26. **Un disparador que el motor ya hace por ID puede caer en otro momento que el del texto:** a
    Necrofear la llamaba apenas era destruida en batalla (por eso se veía su carta ahí), no en la End
    Phase. Ese disparo se quitó: es un solo salto del árbol de IDs (`0x0801786E`).
27. **Con un monstruo mío de 2200 enfrente y Mechanicalchaser en la mano, la IA no jugó Fissure,
    Smashing Ground, Hammer Shot, Tribute to the Doomed, Offerings to the Doomed ni Lightning Vortex**
    (una corrida cada una); **Raigeki y Dark Hole sí**. Ataca a un 2200 con Goblin Attack Force (2300).

**Método que funciona** (una carta, de punta a punta)

0. **Dar de alta el pack** (solo cartas recortadas):
   `python3 scripts/alta.py ROM_ORIGINAL preparar PACK "Carta" …` clasifica cada carta
   (`scripts/triage.py`: qué trae el ROM y cuánto falta), le asigna un hueco seguro libre
   (`scripts/huecos.py`) y deja el borrador `recetas/packs/PACK.json`. Se completa la descripción de
   cada carta y `python3 scripts/alta.py ROM_ORIGINAL aplicar PACK` la suma al registro de huecos, a
   la receta y al registro de pruebas (sin veredicto). `sh scripts/construir_lote.sh` arma el ROM.
   Probado en seco el 2026-10-11 con Stim-Pack, Night Assailant y Double Snare sobre una copia del
   proyecto: el ROM armó, las 30 anteriores siguieron andando y Stim-Pack funcionó sin tocar nada
   (+700 ATK, equipada). Las 142 recortadas ya están clasificadas en `datos/triage_recortadas.csv`.
   **Quedan 20 huecos seguros** para esas 142: es el límite real de cuántas cartas más entran sin
   decidir qué monstruos Normales se sacrifican o ampliar las 1200. Después, por cada carta,
   descomponer el texto de la carta en acciones y buscarlas en **`ACCIONES.md`** (el recetario: qué se
   llama para ver la mano del rival, sumar o restar ATK, mover una carta, tomar el control, equipar,
   dispararse sola...). Lo que ya está ahí se copia; solo se investiga lo que falta, y al terminar
   **se agrega su entrada al recetario**.
1. Leer la fila (`datos/efectos.csv`) y ver qué hace ya el motor con la carta:
   `python3 scripts/buscar_id.py ROM_ORIGINAL "Nombre"` lista todos los sitios del código que comparan
   con su ID. Decompilar lo que haga falta con `python3 scripts/decompilar.py ROM_ORIGINAL NOMBRE DIR…`.
2. Buscar una carta **original** que haga algo parecido y usarla de molde (los mismos dos comandos).
3. Escribir la pieza que falta en `efectos/*.s` a partir de `efectos/plantilla_fn04.s` (binutils de
   ARM) y engancharla en `recetas/lote.json`, al final.
4. Probar la lógica con Unicorn (`scripts/test_*.py`).
5. Probarla en el juego, de forma automática y jugándola de a pasos con capturas (`scripts/paso.py`):
   llegar hasta el final del efecto (cerrar la lista, ver las dos ramas de un sorteo, pasar el turno).
6. Registrar el resultado en `PRUEBAS.md` y `PROYECTO.md`.

**Prácticas que ahorraron tiempo hoy**

- **Observar sin tocar** (cuadro a cuadro, leyendo la RAM) antes de pulsar teclas a ciegas.
- **Registrador de estados:** una `fn_04` de envoltorio (`ORIGINAL` + escribir estado y
  `p[8..10]` en `0x0203F000`) muestra qué recibe una carta original. Así se resolvió Exchange.
- **Comprobar la preparación** (campo, mano, LP) antes de dar un veredicto automático.
- **Comparar con una original** que haga lo mismo; es más barato que decompilar el motor.
- **Parar a tiempo:** si una carta necesita más de dos piezas nuevas, se aparca y se anota.

**Herramientas en pie**: Ghidra (`ghidra/`), Unicorn, Capstone, binutils de ARM,
núcleo libretro de mGBA (`nucleos/`) con `gba.py` y `duelo_auto.py`, estados de
duelo en `estados/` y `estado.py` para editar la mano.

**Lo que NO funciona** (para no repetirlo)

- Dar por buena una carta porque "aparece la lista" o "cambia algo": los tres defectos del 2026-10-11
  estaban después de ese punto (cerrar la lista, la otra rama del sorteo, el cartel contra el efecto).
- Una prueba de lógica que copia lo que hace el código: `test_spy.py` esperaba el `0x80` que era el error.
- Usar `probar_magicas.py` con cartas que piden elegir (Chosen One, Riryoku): queda "sin resolver".

- Editar baúl o mazos dentro de un estado: el editor usa listas que arma el juego.
- Simular una carta con las funciones del motor reemplazadas por `0`: no es
  concluyente cuando la carta depende de ellas.
- Un veredicto automático sin comprobar la preparación: se leyó mal dos veces.
- Terminar el turno desde el campo con el corredor: aún no se reproduce.
- Buscar el consumidor del evento `0x4B` o la rutina de recálculo de ATK a ciegas: se
  mezcla con funciones de gráficos y de IA; conviene hacerlo con el registrador.
- Escanear el ROM completo como si fuera código: más allá de `0x7A8000` hay datos.
- Pulsar `A` repetido en las listas: marca y desmarca.
- Dar por bueno el ROM de `build/` sin mirar su fila de efectos: `(Efectos)` no traía Bagworm.
- Escribir ATK o DEF una sola vez en memoria: el motor lo recalcula en menos de 60 cuadros.
- Hacer que la IA ataque a un monstruo boca abajo con DEF mayor que su ATK: no ataca.
- Usar `responder_con_trampa` para encadenar a una Mágica: el cursor arranca en la mano.
- **Correr dos regresiones a la vez.** El 2026-10-11 dos `repetir_sesion.py` en paralelo llegaron a
  unos 24 GB cada uno y dejaron la Mac sin memoria más de una hora: cada paso abría un emulador nuevo
  sin cerrar el anterior (unos 75 MB por paso, 810 pasos). Arreglado en `scripts/gba.py` (abrir un GBA
  cierra el anterior): la regresión entera usa ahora 1,7 GB. Igual, de a un proceso por vez.
- Probar una secuencia de teclas grabada después de cambiar un efecto que agrega una animación: los
  avisos llegan más tarde y las teclas caen en otro lado (`ronda6/03` de Bagworm). Se juega de nuevo.

## 3. El rumbo

Los cuatro objetivos de Oscar, en el orden en que se destraban:

### Fase 1: cerrar las cartas (objetivo 1)

Meta: un ROM con todas las cartas restauradas que se puedan hacer funcionar, cada una probada.

Hecho: las 30 tienen veredicto y las 30 funcionan (Bagworm −500 y la posesión de Necrofear se
hicieron el 2026-10-11 por la noche). Queda, en orden:

1. **Confirmación a ojo de Oscar** de las 24 pendientes (`python3 scripts/registro.py pendientes ROM`;
   estados y pasos en `specs/001-cerrar-pruebas-lote/guia-oscar.md`, capturas en `evidencia/index.html`).
2. Entregable: la versión de juego con las cartas aptas (`scripts/armar_version.py`; hoy v0.1 con 6).

Regla: una carta que necesita más de dos piezas nuevas se **aparca** y se anota.

### Fase 2: estructura de trabajo (objetivo 2)

Hecho el 2026-10-11 (tarde):

1. **Receta única, un solo comando.** `sh scripts/construir_lote.sh "ROM original.gba"` arma el ROM
   `(Lote)` de cero desde `recetas/lote.json` (que hereda las cartas de `test.json` y lista las piezas
   de `efectos/`). **Ya no hace falta keystone ni la nube:** `parches.py` ensambla sus fuentes con las
   binutils de ARM cuando keystone no está, y las recetas `test`, `prueba3` y `candidatas-30` dan los
   mismos MD5 de siempre.
2. **Registro de huecos:** `datos/huecos.csv` (qué índice ocupa cada carta). `restaurar.py` rechaza una
   receta que mueva una carta de hueco, use el hueco de otra o traiga una carta sin registrar. Para un
   lote nuevo: primero la fila en el registro.
3. **Arte:** `scripts/arte.py` extrae un dibujo del ROM a PNG y convierte un PNG al formato del juego
   (80×80, 63 colores más el índice 0 reservado); en una receta, la clave `"arte": "arte/x.png"` de una
   carta lo escribe en su hueco. Probado ida y vuelta (`scripts/test_arte.py`) y a la vista dentro del
   juego. **Faltan los 30 PNG:** no los puedo conseguir yo; cualquier tamaño sirve.
4. **Paquete de versión:** `python3 scripts/armar_version.py "ROM original.gba" 0.2` arma un ROM de
   juego solo con las cartas aptas del registro, sin ayudas de prueba, con su `.bps` y sus notas.
   Existe la **v0.1** con las 6 aptas de hoy (`build/hack-v0.1.bps`, notas en `build/hack-v0.1.md`);
   las partidas grabadas de esas 6 cartas se repiten iguales en ese ROM. El nombre "Hack vN" es
   provisorio. [DECIDIR]

Queda: los dibujos, y decidir nombre y cómo se consiguen las cartas (hoy heredan el lugar del hueco en
los sobres y se compran con su contraseña).

### Fase 3: mazos e IA (objetivos 3 y 4)

1. **Identificar el mazo de cada duelista** (F8): con el núcleo automático, entrar a
   cada duelo y leer el mazo real del rival.
2. **Rediseñar mazos representativos** (la personalidad más barata y visible).
3. **Investigar la IA** con Ghidra: dónde decide qué jugar; hoy sin ubicar.
4. **Personalidades** como tabla de parámetros por rival, enganchada a esa decisión.
5. **Rivales y eventos nuevos**: último, porque no se conoce el calendario ni los
   eventos (F12). Hay 7 entradas libres en la tabla de mazos de rivales.

### Decisiones tomadas

- Seguir **reemplazando** monstruos Normales; no ampliar las 1200 cartas por ahora.
- El ROM original no se toca; se distribuye `.bps`.
- Una carta no entra al hack sin prueba en duelo.

## 4. Para retomar

1. **Oscar:** abrir `evidencia/index.html` y `specs/001-cerrar-pruebas-lote/guia-oscar.md`, y confirmar
   o corregir carta por carta; las que quiera jugar, con su estado de `estados/revisar/` en el ROM
   `(Lote)`. Primero las nueve que cambiaron el 2026-10-11: filas 3, 23, 24, 25, 26, 30, 31, 32 y 33
   (la 33 es Dark Necrofear: invocación y posesión). Cada confirmación se registra con
   `python3 scripts/registro.py ojo ROM "CARTA" si|no "qué vio"`.
2. Con las confirmaciones: `python3 scripts/armar_version.py "ROM original.gba" 0.2` arma la versión de
   juego con todas las que queden aptas (Fase 1, punto 4).
3. Después, a elección: un lote nuevo de cartas (con `ACCIONES.md` como punto de partida), los dibujos
   de las cartas (Fase 2) o la Fase 3 (mazos e IA).

ROM de trabajo `build/…(Lote).gba` + `build/lote.bps` (el del 2026-10-10 quedó en
`build/lote-2026-10-10.bps`). Estados para revisar en `estados/revisar/`.
