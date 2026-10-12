# Tasks: Cerrar las pruebas del lote de 30 cartas restauradas

**Input**: documentos de diseño en `specs/001-cerrar-pruebas-lote/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: la feature *es* probar cartas, así que no hay tareas de test aparte: cada caso de
`scripts/probar_lote.py` es la prueba automática en duelo que pide el Principio IV. Esta
feature no agrega ni cambia cartas, así que no aplica el paso de lógica con Unicorn.

**Organization**: por historia de usuario. `ROM` es
`build/Yu-Gi-Oh! GX - Duel Academy (Efectos).gba`.

**Regla del tope** (research.md §3): si un caso de US1 necesita más de dos piezas nuevas, se
deja de insistir, la tarea se cierra anotando qué se intentó, y la carta pasa a la lista para
probar con Oscar (T029).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: se puede hacer en paralelo (otro archivo, sin dependencias pendientes)
- **[Story]**: historia de usuario a la que pertenece

---

## Phase 1: Setup

**Purpose**: confirmar que el punto de partida es el que supone el plan.

- [X] T001 Comprobar el entorno: MD5 de `build/Yu-Gi-Oh! GX - Duel Academy (Efectos).gba` igual a `4ed08c04c7c3f5256ed7597200def613`, que carga con `scripts/gba.py` y `nucleos/mgba_libretro.dylib`, y que `estados/duelo-inicio.ss1` abre con `scripts/estado.py duelo`
- [X] T002 Comprobar que el ROM `(Efectos)` trae las 30 cartas del lote: cruzar los nombres de `recetas/test.json` con `Rom.nombre(indice)` de `scripts/da_lib.py`; anotar en `specs/001-cerrar-pruebas-lote/research.md` §6 las que falten y en qué ROM se probarán
- [X] T003 Crear la carpeta `estados/lote/` para los estados por carta

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: las dos piezas comunes. Sin ellas no se puede armar un escenario ni registrar un veredicto.

**⚠️ CRITICAL**: ninguna historia empieza antes de terminar esta fase.

- [X] T004 [P] Crear `scripts/escenario.py` según `contracts/cli.md`: `armar(rom, base, salida, yo={pos: carta}, rival={pos: carta})` que cambia índice (`ranura+0x24`) y tipo (5 bits bajos de `ranura+0x30`) reutilizando `estado.abrir`, `estado.comprobar` y `estado.ranura_mano`; valida carta, posición y que `salida != base`; relee la salida y comprueba las manos
- [X] T005 Agregar a `scripts/escenario.py` la instantánea y la comprobación: `instantanea(duelo)` con los campos de `data-model.md` (LP, manos, campo por controlador con posición y ATK, cementerio, retiradas, cantidad de mazo por lado) y `comprobar(duelo, esperado)` que devuelve la lista de diferencias
- [X] T006 Agregar a `scripts/escenario.py` el modo de línea de comandos (`--yo`, `--rival`, `--mostrar`) y probarlo con los pasos 2 de `quickstart.md`, incluido el caso que debe fallar sin escribir
- [X] T007 [P] Crear `scripts/registro.py` con la lectura de `datos/pruebas.csv` y el comando `verificar ROM` que aplica las 8 reglas de `contracts/registro-csv.md`, nombrando carta y columna en cada error
- [X] T008 Reescribir `datos/pruebas.csv` con las 17 columnas de `contracts/registro-csv.md` y las 30 cartas, tomando veredicto, detalle y evidencias de `PRUEBAS.md`, `PLAN.md` §1 y `PROYECTO.md` §8; `usa_piezas_nuevas = si` para las que tienen archivo en `efectos/`; `ev_ojo = si` solo para las que Oscar jugó (las 4 del lote anterior, Dark Necrofear, Hiro's Shadow Scout, Seal of the Ancients si consta), `pendiente` para el resto con prueba automática
- [X] T009 Correr `python3 scripts/registro.py verificar ROM` hasta que pase con las 30 filas de `datos/pruebas.csv`

**Checkpoint**: se puede armar un estado, comprobarlo, y el registro tiene las 30 cartas en formato válido.

---

## Phase 3: User Story 1 - Veredicto para las cartas que nunca se probaron (Priority: P1) 🎯 MVP

**Goal**: las 9 cartas de los grupos A y B terminan con un veredicto respaldado por prueba en duelo, o en la lista para probar con Oscar.

**Independent Test**: `python3 scripts/probar_lote.py ROM "Electromagnetic Bagworm"` arma el escenario, comprueba la preparación, provoca el disparador y da el mismo veredicto en 3 de 3 corridas.

### Implementation for User Story 1

- [X] T010 [US1] Crear `scripts/probar_lote.py` según `contracts/cli.md`: tabla de casos (carta → función), `--listar`, bucle de corridas (por defecto 3), los cinco resultados por corrida, `INESTABLE` si las corridas difieren, `--fotos`, y código de salida
- [X] T011 [US1] Agregar a `scripts/probar_lote.py` la opción `--registrar`: escribe veredicto, detalle, falla, `ev_auto`, `rom_md5`, `estado` y fecha en `datos/pruebas.csv` solo si las corridas coinciden en un veredicto, y corre `registro.verificar` antes de guardar
- [X] T012 [US1] Caso **Electromagnetic Bagworm** en `scripts/probar_lote.py`, sobre `probar_volteo` y `estados/duelo-bagworm.ss1`: tras el volteo y la toma de control, registrar zona final de Bagworm, si el ataque se resolvió, y la lista de modificadores de ATK/DEF de la Máquina; comparar con el texto de la carta en `recetas/test.json`
- [X] T013 [US1] Caso **Dark-Eyes Illusionist** en `scripts/probar_lote.py`: armar `estados/lote/dark-eyes.st` con la carta en la mano, colocarla, dejar que la ataquen, elegir objetivo, y observar durante el turno rival siguiente si el objetivo declara ataque (evento `0x10` con su id de ranura)
- [X] T014 [US1] Caso **Reaper of the Cards** en `scripts/probar_lote.py`: armar `estados/lote/reaper.st`; esperar a que la IA coloque Call of the Haunted (comprobarlo en la preparación), dejar que ataque al monstruo boca abajo, elegir la Trampa y verificar que va al cementerio rival
- [X] T015 [US1] Buscar en `datos/cartas.csv` las cartas del juego que descartan de la mano del rival y medir cuál juega la IA al tenerla en la mano (armar el estado con `scripts/escenario.py --rival`); anotar el resultado con su marca en `NOTAS-REVERSE.md` y en `research.md` §2
- [X] T016 [US1] Caso **Electric Snake** en `scripts/probar_lote.py`, con la carta de descarte de T015: armar `estados/lote/descarte-snake.st`; esperado: Electric Snake al cementerio y mi mano +2 respecto de después del descarte
- [X] T017 [US1] Caso **Minar** en `scripts/probar_lote.py`, mismo escenario que T016 con `estados/lote/descarte-minar.st`; esperado: Minar al cementerio y LP del rival −1000
- [X] T018 [US1] Caso **Big Burn** en `scripts/probar_lote.py`, sobre `probar_cadena`: armar `estados/lote/big-burn.st` con Big Burn en mi mano y una carta que apunte al cementerio en la mano rival; conseguir un monstruo en algún cementerio antes; esperado: todos los monstruos de ambos cementerios pasan a retiradas
- [X] T019 [US1] Caso **Lady Panther** en `scripts/probar_lote.py`: invocar Lady Panther y un monstruo débil, atacar con el débil a uno más fuerte, abrir el menú de Lady Panther en el campo; esperado: ofrece el efecto y el monstruo destruido vuelve al tope del mazo. Aplica la regla del tope
- [X] T020 [US1] Caso **Fairy Guardian** en `scripts/probar_lote.py`: Fairy Guardian en el campo, una Mágica mía colocada y una carta rival que la destruya; esperado: ofrece el efecto y la Mágica vuelve al fondo del mazo. Aplica la regla del tope
- [X] T021 [US1] Caso **Penguin Knight** en `scripts/probar_lote.py`: probar si el estado admite poner una carta en el tope del mazo (lista en `lado+0x28A4`); si lo admite, hacer que el rival voltee Needle Worm; esperado: mi cementerio vuelve al mazo. Aplica la regla del tope
- [X] T022 [US1] Correr el lote entero con `python3 scripts/probar_lote.py ROM --registrar` y resolver cualquier `INESTABLE` o `PREPARACION INVALIDA` (o pasar la carta a la lista de Oscar)
- [X] T023 [US1] Anotar en `NOTAS-REVERSE.md` lo aprendido sobre cada disparador y lo que se intentó sin éxito, con marcas `[PROBADO]` / `[HIP]`; agregar a `PLAN.md` §2 "Lo que NO funciona" lo que corresponda

**Checkpoint**: las 9 cartas tienen veredicto en `datos/pruebas.csv` o están identificadas para probar con Oscar.

---

## Phase 4: User Story 2 - Un solo registro de resultados, confiable (Priority: P2)

**Goal**: `PRUEBAS.md` y `datos/pruebas.csv` dicen lo mismo de las 30 cartas, y se puede pedir la lista de aptas.

**Independent Test**: `python3 scripts/registro.py verificar ROM` pasa; cambiar a mano un veredicto en la tabla de `PRUEBAS.md` lo hace fallar nombrando la carta.

### Implementation for User Story 2

- [X] T024 [US2] Agregar a `scripts/registro.py` el comando `tabla ROM`: genera la tabla de resultados (carta, Nº, veredicto, evidencias, detalle, cómo reproducir) entre `<!-- registro:inicio -->` y `<!-- registro:fin -->` en `PRUEBAS.md`; falla si faltan las marcas o si `verificar` falla
- [X] T025 [US2] Editar `PRUEBAS.md`: reemplazar las tablas "Sin probar" y "Ya probadas por mí" por las marcas y la tabla generada; conservar el resto del texto; mover a `detalle` del CSV lo que las tablas viejas decían y la nueva no
- [X] T026 [US2] Extender `verificar` en `scripts/registro.py` para comprobar que la tabla de `PRUEBAS.md` es la que se generaría hoy, e imprimir el resumen (cuántas en cada veredicto, aparcadas, pendientes de ojo)
- [X] T027 [US2] Agregar a `scripts/registro.py` el comando `aptas ROM` con la regla de aptitud de `data-model.md`, y comprobar el paso 1 de `quickstart.md` (incluida la falla provocada)

**Checkpoint**: un comando dice si el registro es coherente y cuáles cartas pueden ir a una receta de juego.

---

## Phase 5: User Story 3 - Oscar confirma a ojo (Priority: P3)

**Goal**: Oscar tiene una guía y un estado por carta, y lo que reporta queda registrado.

**Independent Test**: Oscar toma una carta de `guia-oscar.md`, carga su estado en mGBA y llega a ver el efecto sin armar nada a mano.

### Implementation for User Story 3

- [X] T028 [US3] Agregar a `scripts/registro.py` los comandos `pendientes ROM` y `ojo ROM "CARTA" si|no ["qué vio"]` según `contracts/cli.md` (con `no`, exige el texto, corrige el veredicto y deja la discrepancia en `nota_ojo`)
- [X] T029 [US3] Armar con `scripts/escenario.py` un estado en `estados/lote/` para cada carta pendiente de ojo que no tenga uno (las 13 del grupo C más las que dieron veredicto en US1), y comprobar cada uno con `--mostrar`
- [X] T030 [US3] Escribir `specs/001-cerrar-pruebas-lote/guia-oscar.md`: por carta, estado a cargar, pasos y qué debería verse; primero las que ya pasan en automático, y en una sección aparte **las que no se pudieron comprobar**, cada una con su efecto esperado y qué habría que poner en el guardado para probarla
- [X] T031 [US3] Presentarle a Oscar la lista de las que no se pudieron comprobar (nombre, efecto esperado, qué se intentó) y acordar la sesión de prueba
- [X] T032 [US3] Sesión con Oscar: para cada carta de la lista, alterar el estado o el guardado, que Oscar la juegue, y registrar lo que vio con `python3 scripts/registro.py ojo`; las que tampoco se puedan provocar quedan `aparcada = si` con el motivo
- [ ] T033 [US3] Registrar con `registro.py ojo` las confirmaciones de Oscar para las cartas del grupo C a medida que las reporte, y regenerar la tabla con `registro.py tabla`

**Checkpoint**: toda carta mirada por Oscar figura como confirmada; las aptas son las que tienen todas las evidencias.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T034 [P] Actualizar `PLAN.md` §1 y §4 y `PROYECTO.md` §8 con los veredictos finales, apuntando a `datos/pruebas.csv` como fuente
- [X] T035 [P] Para cada carta con veredicto `no funciona` o `funciona en parte`, comprobar que `falla` en `datos/pruebas.csv` alcanza para abrir su feature de arreglo (SC-007) y listarlas en `PLAN.md` §3
- [ ] T036 Correr `quickstart.md` completo y verificar SC-001 a SC-007 de `spec.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: sin dependencias.
- **Foundational (Phase 2)**: depende de Setup. Bloquea todas las historias.
- **US1 (Phase 3)**: depende de Foundational.
- **US2 (Phase 4)**: depende de Foundational. No depende de US1, y conviene hacerla primero: es corta y deja el registro listo para recibir los veredictos.
- **US3 (Phase 5)**: T028–T030 dependen de Foundational; T031–T032 dependen de que US1 termine (hay que saber cuáles no se pudieron automatizar).
- **Polish (Phase 6)**: depende de las tres.

### Dentro de US1

- T010 y T011 antes que cualquier caso.
- T012, T013 y T014 no dependen entre sí, pero editan el mismo archivo: van en serie.
- T015 antes que T016 y T017. T017 después de T016 (comparten escenario).
- T019, T020 y T021 al final; son las candidatas a la lista de Oscar.
- T022 después de todos los casos.

### Parallel Opportunities

- T004 y T007 (archivos distintos).
- T034 y T035.
- Los casos de US1 comparten `scripts/probar_lote.py`, así que no se paralelizan.

---

## Implementation Strategy

### MVP First

1. Phase 1 y Phase 2.
2. US2 (T024–T027): el registro queda coherente aunque no se pruebe nada nuevo.
3. US1 hasta T014: las tres cartas de bajo riesgo con veredicto.
4. **Parar y validar** con `registro.py verificar`.

### Incremental Delivery

1. Base + US2 → registro confiable de las 30.
2. US1 en orden de riesgo → un veredicto más por carta; cada una que supere el tope se anota y se sigue.
3. US3 → guía entregada, lista de no comprobables presentada, sesión con Oscar.
4. Polish.

---

## Notes

- **2026-10-11:** Oscar no podía probar y pidió que las pruebas a ojo las jugara Claude por script con
  subagentes y capturas. T031 y T032 se hicieron así (`evidencia/COMO-REVISAR.md`, `scripts/paso.py`,
  galería en `evidencia/index.html`). T033 sigue abierta: son las confirmaciones de Oscar, que nadie
  puede registrar por él. T036 queda abierta hasta entonces (SC-005 depende de T033).

- **2026-10-11 (tarde):** fuera de esta feature (que solo probaba), se completaron o arreglaron ocho
  cartas (`PLAN.md` §1). Sus veredictos se volvieron a registrar con `probar_lote.py --registrar` y sus
  filas de la guía se jugaron por capturas (`evidencia/ronda6/`). T033 ahora abarca 23 cartas.

- Ninguna tarea escribe sobre un `.gba`.
- Los estados de `estados/lote/` son ayudas de prueba: no pasan a recetas de juego.
- T031 y T032 necesitan a Oscar; el resto se puede hacer sin él.
