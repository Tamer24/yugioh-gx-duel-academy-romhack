# Research: Cerrar las pruebas del lote de 30

Marcas: **[ROM]** leído del ROM o de los scripts, **[PROBADO]** visto en un duelo,
**[HIP]** hipótesis sin comprobar.

## 1. Cómo armar un escenario

- **Decision**: editar un estado de duelo ya empezado (`estados/duelo-inicio.ss1`), cambiando
  cartas de la mano de cualquiera de los dos lados y su byte de tipo.
- **Rationale**: es lo único que ya funciona [PROBADO]. `estado.py mano` cambia el índice en
  `ranura+0x24`; `probar_trampas.estado_con` además corrige el tipo en `+0x30` (5 bits bajos).
  El estado `duelo-bagworm.ss1` cambió así la mano rival entera y la IA jugó esas cartas.
- **Alternatives considered**:
  - Editar baúl o mazos del guardado o del estado: descartado, el editor de mazos usa listas
    que arma el juego [PROBADO, `PLAN.md` §2].
  - Editar el archivo `.sav`: descartado para lo automático, el formato del guardado no está
    ubicado [`PROYECTO.md` §5.10].
  - Jugar una partida real hasta que salga la carta: no es repetible.

Datos del estado base [ROM]:

| Lado | Mano |
|---|---|
| Jugador | Meteor Dragon, Needle Worm, Blazing Inpachi, Salamandra, Twin-Headed Fire Dragon, Monster Reincarnation |
| Rival | Nimble Momonga, Gyaku-Gire Panda, Dian Keto the Cure Master, Des Wombat, Call of the Haunted |

Comportamiento medido de la IA en ese estado [PROBADO]: juega Dian Keto en su 2.º turno;
ataca directo desde su 3.er turno si mi campo está vacío; no ataca si tengo monstruos y una
trampa colocada; ataca a un monstruo boca abajo con una Máquina.

## 2. Cómo provocar cada disparador

| Carta | Disparador | Escenario propuesto | Corredor base | Piezas nuevas | Riesgo |
|---|---|---|---|---|---|
| Reaper of the Cards | Volteo con una Trampa rival colocada | Reaper en mi mano; la mano rival ya trae Call of the Haunted. Colocar, terminar turno, dejar que ataque | `probar_volteo` | 0–1: esperar a que la IA coloque la Trampa | Bajo. [HIP] la IA coloca Call of the Haunted |
| Dark-Eyes Illusionist | Volteo; después el objetivo no ataca | Igual que Bagworm; tras el volteo, dejar pasar un turno rival y ver si el objetivo declara ataque | `probar_volteo` | 1: observar el turno siguiente | Bajo |
| Electromagnetic Bagworm | Volteo atacada por una Máquina | `estados/duelo-bagworm.ss1` ya existe | `probar_volteo` | 1: leer la lista de modificadores y la zona final | Bajo. Es observar, no armar |
| Electric Snake | Descartada de mi mano por efecto del rival | Snake en mi mano; una carta de descarte en la mano rival | nuevo, sobre `probar_cadena` | 1–2 | Medio. [HIP] la IA juega la carta de descarte |
| Minar | Igual que Electric Snake | Mismo escenario, otra carta | el mismo | 0 más | Medio |
| Big Burn | El rival apunta a un monstruo del cementerio | Big Burn colocada; un monstruo en algún cementerio; Monster Reborn o similar en la mano rival | `probar_cadena` | 1–2 | Medio. [HIP] la IA juega la carta y el motor abre la ventana de cadena |
| Lady Panther | Me destruyen un monstruo en batalla ese turno | Lady Panther y un monstruo débil en mi campo; atacar con el débil a uno más fuerte; abrir el menú de Lady Panther | nuevo | 2: declarar un ataque desde el campo, y abrir el menú de un monstruo | Alto. `PLAN.md`: manejar el campo con el corredor "aún no se reproduce" |
| Fairy Guardian | El rival manda una Mágica mía al cementerio ese turno | Fairy Guardian en mi campo, una Mágica mía colocada, y una carta rival que la destruya | nuevo | 2+: destrucción por la IA, y activar un efecto de monstruo en la ventana correcta | Alto. No se sabe si el efecto se ofrece en el turno rival |
| Penguin Knight | Va de mi mazo al cementerio por efecto del rival | Penguin Knight en el tope de mi mazo; el rival voltea un Needle Worm | nuevo | 2+: editar el orden del mazo, y hacer que la IA voltee | Alto. Editar el mazo dentro del estado no está probado |

- **Decision**: orden de ataque de menor a mayor riesgo: Bagworm, Dark-Eyes Illusionist,
  Reaper of the Cards, Electric Snake + Minar, Big Burn, Lady Panther, Fairy Guardian,
  Penguin Knight.
- **Rationale**: las tres primeras reutilizan un corredor que ya funciona. Electric Snake y
  Minar comparten escenario. Las tres últimas necesitan mecanismos que hoy no existen.
- **Qué carta de descarte usar** queda por resolver en la implementación: hay que buscar en
  `datos/cartas.csv` cuáles de las 1200 descartan de la mano rival y probar si la IA las
  juega. [HIP] Card Destruction está en el juego.

## 3. Qué pasa con las que no se pueden automatizar

- **Decision** (de Oscar, 2026-10-10): no se fuerzan. Cuando todo lo automatizable esté listo
  se le presenta una lista con cada carta, su efecto esperado y lo que haría falta poner en el
  guardado, y se prueban junto con él alterando el archivo.
- **Rationale**: Oscar prefiere una tanda de pruebas manuales al final. Coincide con el
  Principio VII (parar a tiempo) y con el Principio IV v1.0.1.
- **Tope**: una carta pasa a esa lista cuando necesita más de **dos piezas nuevas**. Una
  pieza es un mecanismo que hoy no existe en los corredores (por ejemplo, editar el orden del
  mazo o declarar un ataque desde el campo). Un mecanismo compartido cuenta una sola vez, para
  la primera carta que lo necesita.
- **Candidatas probables a la lista**: Lady Panther, Fairy Guardian y Penguin Knight.
- **Cómo se prueba con Oscar**: para cada una se entrega un estado en `estados/lote/` con las
  manos ya armadas, que él carga en mGBA con *Archivo → Cargar estado desde archivo*. [HIP]
  Si hace falta algo que la mano no cubre (orden del mazo, cementerio), se intenta editar en
  el estado durante la sesión, con Oscar mirando el resultado.
- **Alternatives considered**: llamar funciones del motor desde el script para forzar el
  disparador (`scripts/llamar_motor.py`). Se deja como último recurso: demuestra la lógica,
  pero no que el juego llegue solo a ese punto, así que no vale como prueba en duelo.

## 4. Cómo se decide el veredicto

- **Decision**: cada caso declara el efecto esperado como una comparación entre dos
  instantáneas del duelo (antes y después): LP, cantidad de cartas en mano, mazo, cementerio,
  campo, posiciones y ATK. El veredicto sale de esa comparación, no de la clasificación
  genérica "CAMBIA / NO HACE NADA" de los corredores actuales.
- **Rationale**: "CAMBIA" no distingue entre robar 2 y robar 1 (el caso de Hiro's Shadow
  Scout). FR-006 pide comparar con el texto.
- **La segunda instantánea se toma dos veces**: al resolver y unos 300 cuadros después. Ya
  pasó que un cambio de ATK se aplicaba y el motor lo revertía [PROBADO, Riryoku].
- **Preparación**: antes de la primera instantánea se comprueba que cada carta pedida está en
  la zona pedida. Si no, el resultado es `PREPARACION INVALIDA` y no hay veredicto (FR-004).
- **Repetición**: 3 corridas por caso; el veredicto solo se registra si las 3 coinciden
  (SC-004).

## 5. Cómo mantener un solo registro

- **Decision**: `datos/pruebas.csv` es la fuente única. La tabla de resultados de `PRUEBAS.md`
  se genera desde el CSV, entre dos marcas, y `registro.py verificar` falla si la tabla no
  está al día.
- **Rationale**: dos registros editados a mano ya divergieron una vez. Generar uno desde el
  otro hace que la coincidencia (FR-008) se cumpla por construcción y se compruebe con un
  comando.
- **Alternatives considered**: comparar dos archivos editados a mano con un script. Detecta
  la diferencia pero no la evita. Guardar todo solo en Markdown: los scripts tendrían que
  interpretar una tabla pensada para leer.
- El texto que hoy hay en `PRUEBAS.md` (instrucciones, experimentos) se conserva; solo se
  reemplazan las dos tablas de resultados ("Sin probar" y "Ya probadas por mí") por la
  generada.

## 6. Qué ROM se prueba

- **Decision**: `build/Yu-Gi-Oh! GX - Duel Academy (Efectos).gba`
  (MD5 `4ed08c04c7c3f5256ed7597200def613`) [ROM].
- **Rationale**: es el ROM de trabajo que trae las funciones propias (`PLAN.md` §3).
- **Por comprobar al empezar**: que contiene las 30 cartas del lote. [HIP] deriva de la
  receta `test`. Si falta alguna, esa carta se prueba en `(Test)` y se anota el ROM usado.
- **Riesgo**: no sale de una receta única (ver *Complexity Tracking* en `plan.md`). Cada
  veredicto guarda el MD5 del ROM.

### Actualización tras implementar (2026-10-10)

- `(Efectos)` trae las 30 cartas [ROM], pero **no** las dos funciones de Bagworm. Se armó el
  ROM `(Lote)` (MD5 `dbbbab32ccc659ae077cf12fcf4c15c6`) con `scripts/construir_lote.sh`, que
  reproduce `(Efectos)` byte a byte y agrega Bagworm. Los 9 veredictos nuevos son sobre `(Lote)`.
- Las cuatro dudas de abajo quedaron resueltas: la IA juega Card Destruction y Delinquent Duo
  (no Confiscation); juega Monster Reborn; el mazo se puede editar en el estado; el efecto de
  Fairy Guardian no se ofrece en ningún momento. Detalle en `NOTAS-REVERSE.md`.
- Ninguna carta superó el tope de dos piezas nuevas: las 9 tienen caso automático.

## Sin resolver (se resuelve implementando)

1. Qué carta de descarte juega la IA.
2. Si la IA juega Monster Reborn cuando hay un monstruo en un cementerio.
3. Si el estado admite cambiar el orden del mazo.
4. Si el efecto de Fairy Guardian se ofrece durante el turno del rival.

Ninguno bloquea el plan: si la respuesta es no, la carta pasa a la lista de Oscar.
