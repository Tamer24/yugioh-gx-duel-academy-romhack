# Feature Specification: Cerrar las pruebas del lote de 30 cartas restauradas

**Feature Branch**: `001-cerrar-pruebas-lote` (sin rama: la carpeta no es un repositorio git)

**Created**: 2026-10-10

**Status**: Draft

**Input**: User description: "Cerrar las pruebas del lote de 30 cartas restauradas (Fase 1, punto 3 de PLAN.md; F1 de PROYECTO.md)."

## Contexto

El hack restauró 30 cartas que el juego traía en su código pero no en su lista. Hoy no se
sabe con certeza cuáles pueden entrar al ROM `Candidatas v1`: siete nunca se probaron en un
duelo, dos quedaron a medias, trece pasan una prueba automática pero nadie las miró, y los
dos registros de resultados se contradicen.

Esta feature cierra esa incertidumbre. **No arregla cartas**: produce un veredicto por
carta, respaldado por una prueba en duelo, y deja a Oscar una lista corta de lo que le falta
mirar.

### Estado de partida

Según `PRUEBAS.md` y `PLAN.md` al 2026-10-10. Marcas de confianza según el Principio V.

| Grupo | Cantidad | Cartas | Marca |
|---|---|---|---|
| A. Sin ninguna prueba en duelo | 7 | Reaper of the Cards, Penguin Knight, Electric Snake, Minar, Lady Panther, Fairy Guardian, Big Burn | [HIP]: se desconoce si funcionan |
| B. Probadas a medias | 2 | Electromagnetic Bagworm, Dark-Eyes Illusionist | [PROBADO] una parte del efecto |
| C. Prueba automática que pasa, sin mirar | 13 | Acid Trap Hole, Mystical Refpanel, Two-Pronged Attack, Riryoku Field, Magic Drain, Monster Recovery, Goddess of Whim, Chosen One, Riryoku, Exchange, Share the Pain, Kunai with Chain, The Inexperienced Spy | [PROBADO] en prueba automática |
| D. Con veredicto cerrado | 8 | Rigorous Reaver, Jowls of Dark Demise, Windstorm of Etaqua, Ready for Intercepting, Seal of the Ancients (funcionan); Dark Necrofear (funciona en parte); Hiro's Shadow Scout (falla en parte); Reasoning (no funciona, aparcada) | [PROBADO] |

Qué debería hacer cada carta del grupo A, según su texto:

| Carta | Cuándo se dispara | Qué debería pasar |
|---|---|---|
| Reaper of the Cards | Al voltearse, con una Trampa del rival colocada | Elegís una carta; si es Trampa, se destruye |
| Penguin Knight | Va del mazo al cementerio por un efecto del rival | El cementerio propio vuelve al mazo |
| Electric Snake | El rival la descarta de tu mano con un efecto | Robás 2 cartas |
| Minar | El rival la descarta de tu mano con un efecto | El rival pierde 1000 LP |
| Lady Panther | El turno en que te destruyen un monstruo en batalla | Ofrece el efecto y devuelve ese monstruo al tope del mazo |
| Fairy Guardian | El turno en que el rival manda una Mágica tuya al cementerio | Ofrece el efecto y devuelve esa Mágica al fondo del mazo |
| Big Burn | El rival activa algo que apunta a un monstruo en el cementerio | Se retiran todos los monstruos de ambos cementerios |

Qué falta observar en el grupo B:

- **Electromagnetic Bagworm**: toma el control de la Máquina atacante [PROBADO]. Falta
  explicar por qué termina en el cementerio poco después, si el ataque debería cancelarse y
  si se aplica la reducción de 500 ATK.
- **Dark-Eyes Illusionist**: pide un objetivo al voltearse [PROBADO]. Falta ver si ese
  monstruo deja de poder atacar mientras ella siga boca arriba.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Veredicto para las cartas que nunca se probaron (Priority: P1)

Oscar quiere saber, para cada una de las nueve cartas de los grupos A y B, si hace lo que
dice su texto. Para eso cada carta se pone en un duelo armado de modo que su disparador
ocurra, se observa qué cambia y se compara con el texto.

**Why this priority**: es la única parte del lote donde no hay información. Sin estos
veredictos no se puede decidir el contenido de `Candidatas v1`.

**Independent Test**: se puede dar por cumplida mirando una sola carta: existe una prueba
repetible que arma el escenario, provoca el disparador y muestra un resultado que coincide
o no con el texto de la carta.

**Acceptance Scenarios**:

1. **Given** una carta del grupo A y un duelo donde su disparador puede ocurrir, **When**
   se provoca el disparador, **Then** queda registrado qué cambió en el duelo (LP, mano,
   mazo, cementerio, campo) y un veredicto que surge de comparar eso con el texto.
2. **Given** una prueba que terminó, **When** el escenario no quedó armado como se pidió
   (falta una carta en la mano, el campo o el cementerio no es el esperado), **Then** la
   prueba se declara inválida y no produce veredicto.
3. **Given** una carta del grupo B, **When** se observa la parte del efecto que faltaba,
   **Then** su veredicto pasa a ser uno de los tres valores definidos y deja de figurar
   como "a medias" o "sin confirmar".
4. **Given** una carta cuyo disparador no se logra provocar dentro del esfuerzo acordado,
   **When** se agota ese esfuerzo, **Then** la carta queda aparcada con el registro de lo
   que se intentó y por qué no funcionó.

---

### User Story 2 - Un solo registro de resultados, confiable (Priority: P2)

Oscar abre el registro de resultados y ve, para las 30 cartas, el mismo veredicto en el
documento que lee una persona (`PRUEBAS.md`) y en la tabla que leen los scripts
(`datos/pruebas.csv`). Hoy la tabla dice "no funciona" o "sin probar" para cartas que ya
funcionan.

**Why this priority**: con registros contradictorios, cualquier decisión sobre qué cartas
incluir puede tomarse sobre un dato viejo. Vale por sí sola aunque no se pruebe ninguna
carta nueva.

**Independent Test**: se compara carta por carta el veredicto de ambos registros; no debe
haber ninguna diferencia ni ninguna carta faltante.

**Acceptance Scenarios**:

1. **Given** los dos registros, **When** se comparan las 30 cartas, **Then** el veredicto
   coincide en todas.
2. **Given** una carta cualquiera del registro, **When** se la consulta, **Then** se ve su
   veredicto, qué se observó, con qué evidencia cuenta y cómo repetir la prueba.
3. **Given** el registro completo, **When** se pide la lista de cartas aptas para una
   receta de juego, **Then** solo aparecen las que funcionan y tienen todas las evidencias
   que exige el Principio IV.

---

### User Story 3 - Oscar confirma a ojo lo que solo se probó en automático (Priority: P3)

Oscar recibe una guía breve con las cartas que ya pasan una prueba automática pero que él
todavía no vio. Para cada una la guía dice desde dónde empezar, qué hacer y qué debería
verse. Oscar juega, reporta, y su reporte queda en el registro.

**Why this priority**: es el último paso que exige el Principio IV. Depende de Oscar y no
bloquea las otras dos historias, pero sin él ninguna de esas cartas puede ir a un ROM de
juego.

**Independent Test**: Oscar toma una carta de la guía y, sin pedir ayuda, llega a ver el
efecto y puede decir si coincide con lo descrito.

**Acceptance Scenarios**:

1. **Given** la guía y una carta pendiente, **When** Oscar sigue sus pasos, **Then** llega
   al momento en que la carta actúa sin tener que armar el escenario por su cuenta.
2. **Given** que Oscar reporta que vio lo esperado, **When** se registra el reporte,
   **Then** la carta figura como confirmada a ojo y pasa a la lista de aptas.
3. **Given** que Oscar reporta algo distinto de lo que dio la prueba automática, **When**
   se registra el reporte, **Then** prevalece lo que vio Oscar, el veredicto se corrige y
   la discrepancia queda anotada.

---

### Edge Cases

- **La carta hace algo, pero no lo que dice el texto** (por ejemplo, roba 1 en vez de 2):
  el veredicto es "funciona en parte" y el detalle dice exactamente qué difiere.
- **El disparador nunca ocurre** porque el rival no juega la carta necesaria: no cuenta
  como "no funciona". Hay que forzar el escenario o aparcar la carta.
- **La prueba automática pasa pero el resultado se revierte enseguida** (ya ocurrió con un
  cambio de ATK): el veredicto debe considerar el estado unos instantes después, no solo en
  el momento de activar.
- **La carta se comporta distinto según quién la activa** (el jugador o el rival): solo se
  juzga el lado del jugador; el otro se anota como no probado.
- **Una carta del grupo C deja de pasar su prueba** al volver a correrla: vuelve al grupo
  sin veredicto firme y se anota la regresión.
- **Dos cartas necesitan el mismo escenario** (Electric Snake y Minar se disparan igual):
  se pueden probar con el mismo armado, pero cada una lleva su propio veredicto.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Cada una de las 30 cartas del lote DEBE terminar con exactamente un veredicto:
  *funciona*, *funciona en parte* o *no funciona*. "Sin probar", "sin confirmar" y "a
  medias" no son veredictos finales.
- **FR-002**: Una carta PUEDE quedar además marcada como *aparcada*, con el motivo. Aparcada
  es una decisión sobre el esfuerzo, no un veredicto: se suma a él o, si el disparador no se
  pudo provocar, lo reemplaza dejando constancia de lo intentado.
- **FR-003**: Todo veredicto DEBE estar respaldado por una prueba en duelo, es decir, la
  carta actuando dentro del juego y no solo su lógica aislada.
- **FR-004**: Toda prueba DEBE comprobar que el escenario quedó armado como se pidió antes de
  emitir un veredicto. Si no lo está, la prueba es inválida.
- **FR-005**: Para cada carta de los grupos A y B DEBE existir una forma repetible de
  provocar su disparador: descarte de la mano por efecto del rival, envío del mazo al
  cementerio por efecto del rival, destrucción de un monstruo propio en batalla, envío de
  una Mágica propia al cementerio por el rival, efecto del rival que apunta al cementerio, y
  volteo con una Trampa rival colocada.
- **FR-006**: El veredicto DEBE surgir de comparar lo observado con el texto de la carta, y
  el registro DEBE decir qué se observó en números o en cartas concretas (por ejemplo, "LP
  del rival 8000 → 7000").
- **FR-007**: El registro de cada carta DEBE incluir: veredicto, detalle de lo observado,
  evidencias con que cuenta (prueba automática, confirmación a ojo), desde qué punto de
  partida se reproduce y fecha.
- **FR-008**: `PRUEBAS.md` y `datos/pruebas.csv` DEBEN coincidir en el veredicto de las 30
  cartas, y esa coincidencia DEBE poder comprobarse sin revisarla a mano.
- **FR-009**: DEBE existir una lista de cartas aptas para una receta de juego. Una carta
  solo entra si su veredicto es *funciona* y tiene todas las evidencias del Principio IV,
  incluida la confirmación a ojo.
- **FR-010**: DEBE existir una guía para Oscar con las cartas pendientes de mirar. Por carta:
  punto de partida, pasos y qué debería verse.
- **FR-011**: Cuando Oscar reporte lo que vio, el reporte DEBE quedar en el registro. Si
  contradice a la prueba automática, prevalece lo que vio Oscar.
- **FR-012**: Una carta que resulte *no funciona* o *funciona en parte* DEBE quedar con una
  descripción de la falla suficiente para abrir después una feature de arreglo. Esta
  feature NO arregla la carta.
- **FR-013**: Si probar una carta exige más de dos piezas nuevas, la carta DEBE aparcarse y
  anotarse (Principio VII).
- **FR-014**: Lo aprendido sobre cómo provocar cada disparador, y lo que se intentó sin
  éxito, DEBE quedar anotado con su marca de confianza (Principio V).
- **FR-015**: Las ayudas de prueba (cartas regaladas, contraseñas gratis, escenarios
  armados) NO DEBEN pasar a ninguna receta de juego (Principio II).

### Key Entities

- **Carta del lote**: una de las 30 restauradas. Tiene nombre, número en el juego, qué
  debería hacer según su texto y cuándo se dispara.
- **Veredicto**: *funciona*, *funciona en parte* o *no funciona*, con el detalle de lo
  observado. Uno por carta.
- **Evidencia**: lo que respalda un veredicto. Hay tres clases: lógica aislada, prueba
  automática en duelo y confirmación a ojo de Oscar.
- **Escenario**: el duelo armado para que el disparador de una carta ocurra: qué hay en
  cada mano, campo, mazo y cementerio, y de quién es el turno. Varias cartas pueden
  compartir uno.
- **Registro de resultados**: el conjunto de veredictos y evidencias, en sus dos formas
  (para leer y para scripts).
- **Guía de confirmación**: la lista de cartas que Oscar tiene que mirar, con los pasos.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Las 30 cartas tienen un veredicto final o están aparcadas con motivo; quedan 0
  cartas "sin probar", "sin confirmar" o "a medias".
- **SC-002**: Las 9 cartas de los grupos A y B tienen al menos una prueba en duelo
  registrada, o el registro de por qué no se pudo provocar su disparador.
- **SC-003**: Los dos registros de resultados coinciden en las 30 cartas: 0 diferencias.
- **SC-004**: Cualquier prueba registrada se puede repetir desde su punto de partida y da el
  mismo veredicto en 3 de 3 corridas.
- **SC-005**: Oscar puede confirmar una carta de la guía en menos de 5 minutos, sin armar el
  escenario a mano ni pedir aclaraciones.
- **SC-006**: La lista de cartas aptas no contiene ninguna carta a la que le falte una
  evidencia del Principio IV.
- **SC-007**: Cada carta que no funciona o funciona en parte tiene una descripción de la
  falla que permite abrir su feature de arreglo sin volver a probarla.

## Assumptions

- **Qué cuenta como cerrado**: la feature se da por cumplida cuando las 30 cartas tienen
  veredicto respaldado por prueba en duelo, los registros coinciden y la guía está
  entregada. La confirmación a ojo se registra a medida que Oscar reporta; mientras falte,
  la carta tiene veredicto pero no figura como apta.
- **Dark-Eyes Illusionist entra en el grupo B**: observar si el bloqueo de ataque se aplica
  es terminar su prueba, no diagnosticarla. Si no se aplica, el veredicto es "funciona en
  parte" y el arreglo queda fuera.
- **The Inexperienced Spy entra en el grupo C**: `PLAN.md` la lista entre las que Oscar
  todavía tiene que mirar.
- **Solo se juzga el lado del jugador**. Qué pasa cuando la carta la usa el rival queda
  fuera y se anota como no probado.
- **Se prueba el caso típico de cada carta**, no sus cadenas ni interacciones con otras
  cartas (riesgo ya aceptado en `PROYECTO.md` §11).
- **Las cartas del grupo D conservan su veredicto**: no se vuelven a probar; solo se
  verifica que los dos registros lo reflejen igual.
- **El texto de referencia** de cada carta es su descripción en la receta del lote.
- **La prueba de lógica aislada** que pide el Principio IV aplica solo a las cartas con
  piezas nuevas (constitución 1.0.1). Las que usan la función original sin modificar
  necesitan la prueba automática en duelo y la confirmación a ojo.
- **Cartas que no se puedan comprobar en automático** (pedido de Oscar, 2026-10-10): no se
  sigue insistiendo. Cuando todo lo automatizable esté listo, se le presenta a Oscar una
  lista con esas cartas y su efecto esperado, y se prueban una por una junto con él,
  alterando el archivo de guardado para armar cada escenario.
- [HIP] Los disparadores que faltan se pueden provocar armando el escenario en un duelo ya
  empezado, como se hizo con las trampas y los monstruos de volteo.

### Fuera de alcance

- Arreglar cualquier carta que falle. Cada arreglo es una feature propia.
- Reasoning (aparcada: le faltan la pregunta de nivel y la resolución).
- La posesión de Dark Necrofear.
- Diagnosticar por qué Hiro's Shadow Scout hace robar 1 carta en vez de 3.
- El comportamiento de las cartas cuando las usa el rival.
- El arte de las cartas.
- Armar y publicar el ROM `Candidatas v1`.
