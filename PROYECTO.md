# Duel Academy Romhack: documento de proyecto

Estado al **2026-10-09**. Reúne todo lo aprendido y dónde está el trabajo, para
usarlo como contexto de entrada de Spec Kit. El detalle byte a byte sigue en
`NOTAS-REVERSE.md`; las instrucciones de prueba, en `PRUEBAS.md`.

Marcas de confianza que se usan en todo el documento:

- **[ROM]** comprobado leyendo o ejecutando código del ROM.
- **[PROBADO]** comprobado jugando un duelo en emulador.
- **[HIP]** hipótesis razonable, sin comprobar.
- **[DECIDIR]** decisión de producto que todavía no se tomó.

> **Plan vigente y estado de las cartas: ver `PLAN.md`.** Este documento es el mapa del ROM y el backlog original.

## 1. Cómo usar este documento con Spec Kit

| Etapa de Spec Kit | Qué sección usar |
|---|---|
| Constitución (principios del proyecto) | §3 Principios y restricciones |
| Especificar una feature (qué y por qué) | §9 Backlog: cada ítem es una feature candidata. §2 da la visión |
| Aclarar | §10 Preguntas abiertas y §2 Decisiones pendientes |
| Plan técnico | §5 Mapa del ROM, §6 Cómo se modifica, §7 Herramientas |
| Tareas e implementación | §7 Herramientas y §8 Estado actual |

Los nombres exactos de los comandos cambiaron entre versiones de Spec Kit
(hoy el README los lista como `/speckit-constitution`, `/speckit-specify`,
`/speckit-plan`, `/speckit-tasks`, `/speckit-implement`): conviene mirar el
[repositorio](https://github.com/github/spec-kit) al instalarlo.

## 2. Visión

Hacer un **romhack o fangame que expanda Yu-Gi-Oh! GX Duel Academy** (GBA,
versión USA). La primera línea de trabajo elegida fue **recuperar cartas que
el juego trae en su código pero no en su lista de cartas**, y sumarles las
piezas que les falten.

### Decisiones pendientes [DECIDIR]

Estas definen el alcance y no están tomadas:

1. **Qué significa "expandir":** solo más cartas, o también rivales, mazos,
   historia y eventos de la academia.
2. **Cartas restauradas vs. cartas nuevas:** quedarse con las 172 recortadas,
   o escribir efectos de cero para cartas que el juego nunca tuvo.
3. **Reemplazar o ampliar:** hoy cada carta restaurada pisa un monstruo Normal.
   Pasar de 1200 cartas exige agrandar varias tablas y probablemente el
   guardado.
4. **Idioma:** dejar el inglés o traducir textos (los nombres y descripciones
   ya se pueden reubicar sin límite de largo).
5. **Cómo se consiguen las cartas nuevas:** sobres, contraseñas, premios.
6. **Plataforma de destino:** emulador en Mac y Retroid (`roms/gba/`).
7. **Distribución:** si se comparte, va como parche `.bps`, nunca el ROM.

## 3. Principios y restricciones

Lo que se respetó hasta ahora y conviene llevar a la constitución:

1. **El ROM original no se toca.** Vive en Descargas y es la base de todo.
   Cada versión se genera de cero a partir de él.
2. **Todo cambio es reproducible.** Una receta JSON más los scripts producen
   el ROM; nada se edita a mano con un editor hexadecimal.
3. **Se distribuye el parche `.bps`, no el ROM.**
4. **Nombre de archivo distinto por versión**, porque el emulador ata la
   partida guardada al nombre.
5. **Código original casi intacto.** El código nuevo va al espacio libre
   (desde `0x1900000`); sobre el original solo se escriben ganchos de 4 a 10
   bytes. Los datos nuevos van desde `0x1800000`.
6. **Cada dato lleva su marca de confianza** ([ROM], [PROBADO], [HIP]).
7. **Una carta no entra al hack sin prueba en duelo.** Tener fila de efecto no
   garantiza que funcione (§8).
8. **Las comprobaciones van dentro del script.** `restaurar.py` verifica IDs
   únicos, mazos sin IDs inexistentes y contraseñas sin repetir antes de
   escribir el ROM.
9. **Los ROMs de prueba y los de juego son recetas distintas.** Contraseñas
   gratis y cartas regaladas solo en los de prueba.
10. **Quién prueba:** Oscar juega y reporta; el emulador sin ventana queda para
    comprobaciones que se leen de la memoria (baúl, DP), no para jugar duelos.

Restricciones técnicas duras:

- Procesador ARM7TDMI, código en Thumb. Los efectos de las cartas son C
  compilado, no datos: un efecto nuevo es código ensamblador.
- 1200 cartas fijas; tabla de efectos de 901 filas con el tope escrito en el
  código.
- `keystone-engine` ya no hace falta: no tiene paquete para el Python de la Mac de Oscar (3.14) y
  `parches.py` ensambla las mismas fuentes con las binutils de ARM (`brew install
  arm-none-eabi-binutils`). Comprobado el 2026-10-11: las recetas dan los mismos MD5 que los ROMs
  armados con keystone.

## 4. El ROM

| Dato | Valor |
|---|---|
| Archivo | `Yu-Gi-Oh! GX - Duel Academy (USA).gba` |
| Título interno / código | `YUGIOHGXDA` / `BYGE` (Konami) |
| Tamaño | 32 MB (`0x2000000`) |
| MD5 | `f62c47cbe08e1e3bcfcf9f1b84841a76` |
| SHA-1 | `57d6bb789833b62b360072902982d5f1011b3640` |
| CRC32 | `3b8a00fe` |
| Guardado | SRAM |
| Cartas | 1200 (índices 1–1200; el 0 es una entrada vacía) |

Todos los offsets son **de archivo**. Dirección de GBA = offset + `0x08000000`
(el código también usa el espejo `0x09000000` para la segunda mitad).

Es pariente de los *World Championship* de GBA: comparte motor, rango de IDs
(4007 en adelante) y restos de código. Quedaron nombres de fuentes en el ROM:
`duel/kernel/d_duelmagic.c`, `duel/effects/d_magic_lock3.c`,
`duel/tutorial/d_tut_script.c`, `msg/msg_main.c`.

## 5. Mapa del ROM

### 5.1 Tablas por carta (índice 0–1200) [ROM]

| Offset | Qué hay | Formato |
|---|---|---|
| `0x7A8620` | Cantidad de cartas | u16 = 1200. La leen la búsqueda ID→índice y otros 40 lugares |
| `0x7A8624` | Índice → ID de Konami | 1201 × u16. Ordenada: la búsqueda inversa es binaria. Aparece en 706 lugares del código |
| `0x7A8F88` | Claves de contraseña | 1201 × u32 |
| `0x7AA24C` | Paletas del arte | 1201 × 128 bytes (64 colores BGR555) |
| `0x7CFACC` | Arte | 1201 × 6400 bytes: 80×80, 8bpp, en tiles de 8×8 |
| `0xF243CC` | Estadísticas | 1201 × u32 empaquetado |
| `0xF25690` / `0xF2A68C` | Nombres / offsets | ASCII con `00`; offsets u32 relativos a la base |
| `0xF2B950` / `0xF58294` | Descripciones / offsets | igual |
| `0xF59558` | Orden alfabético | 1201 × u16: puesto (0–1199) de cada índice. La usa el editor de mazos |

Los offsets de texto son de 32 bits sin límite: un texto nuevo puede vivir en
cualquier parte del ROM. Códigos dentro del texto: `@4`, `@5`, `@7` (colores),
`%s` (nombre en tiempo de ejecución).

### 5.2 Estadísticas: un u32 por carta [ROM]

| Bits | Campo |
|---|---|
| 0–8 | DEF ÷ 10 |
| 9–17 | ATK ÷ 10 |
| 18–19 | Clase: 0 Normal, 1 Efecto, 2 Fusión, 3 Ritual |
| 20–24 | Tipo |
| 25–28 | Nivel |
| 29–31 | Atributo: 1 Luz, 2 Oscuridad, 3 Agua, 4 Fuego, 5 Tierra, 6 Viento |

Tipos: 1 Dragon, 2 Zombie, 3 Fiend, 4 Pyro, 5 Sea Serpent, 6 Rock, 7 Machine,
8 Fish, 9 Dinosaur, 10 Insect, 11 Beast, 12 Beast-Warrior, 13 Plant, 14 Aqua,
15 Warrior, 16 Winged Beast, 17 Fairy, 18 Spellcaster, 19 Thunder, 20 Reptile,
21 Trap, 22 Spell.

Valores completos para mágicas y trampas:

| Clase | u32 | Clase | u32 |
|---|---|---|---|
| Spell | `01600000` | Spell Ritual | `016C0000` |
| Spell Field | `01640000` | Trap | `21500000` |
| Spell Equip | `01660000` | Trap Counter | `21520000` |
| Spell Continuous | `01680000` | Trap Continuous | `21580000` |
| Spell Quick-Play | `016A0000` | | |

### 5.3 Tabla de efectos [ROM]

- `0x17D9BEC`, **901 filas de 28 bytes**, ordenada por ID de Konami (4022 a
  6467).
- Fila: `u16 ID, u16 0`, función en `+0x04`, `u32 flags` en `+0x08`, funciones
  en `+0x0C`, `+0x10`, `+0x14`, `+0x18`.
- `0x08061629` es la función "sin efecto". Otro relleno habitual es un stub
  `movs r0,#0; bx lr`.
- La busca `FUN_0806162C(índice)`: pasa el índice a ID y hace búsqueda
  binaria. **El máximo (900) está fijo en el código.** La dirección base
  aparece en 13 lugares.
- **El efecto se encuentra por ID de Konami, no por posición.** Es lo que
  permite restaurar cartas cambiando un ID.
- Qué hace cada columna no está resuelto. [HIP] `+0x04` resuelve el efecto y
  las otras son condición, costo y disparadores, como en la decompilación de
  *Eternal Duelist Soul*.
- **Hay un segundo mecanismo de efectos**: 137 monstruos de efecto del juego
  no tienen fila (Exodia, Kuriboh, Jinzo #7) y 42 tienen fila vacía. Se
  resuelven en otra parte del código, todavía sin ubicar.

Reparto de las 901 filas: 729 son de cartas del juego y **172 de cartas
recortadas** (Crush Card Virus, Vampire Lord, Dark Necrofear, Creature Swap,
De-Fusion, Mirror Wall, Royal Oppression, Blade Knight, entre otras). Lista
completa en `datos/cartas_recortadas.csv`.

| Recortadas | Cantidad | En el lote de 30 | Sin tocar |
|---|---|---|---|
| Con función real en `+0x04` | 103 | 29 | 74 |
| Con stub en `+0x04` | 69 | 1 (Dark Necrofear) | 68 |

### 5.4 Invocación especial retirando del Cementerio [ROM]

- Tabla original en `0x17DFF44`: 12 entradas de 8 bytes `{u16 ID, u8
  requisito 0, u8 requisito 1, u8 cantidad}`. Solo atributos, 1 o 2 cartas.
- Funciones: `FUN_0806FD38` (búsqueda, con el tope 11 fijo), `FUN_0806FDD0`
  (¿la carta cumple el requisito?), `FUN_0806FE4C` (chequeo), `FUN_0806FF54`
  (ejecutor por pasos), `FUN_0806EA1C` (¿puede invocar?),
  `FUN_0800DDC0(ranura, atributo)`, `FUN_08077544` (máquina de invocaciones).
- Siete literales apuntan a la tabla: `0x6FD70, 0x6FDCC, 0x6FF44, 0x70054,
  0x70200, 0x7022C, 0x7039C`.

Es el modelo de lo que probablemente les falta a otras cartas: **una tabla de
datos chica, con el tope fijo en el código, de la que la carta fue borrada**.

### 5.5 Mazos, sobres y otras listas [ROM]

| Offset | Qué hay |
|---|---|
| `0x17E1294` | Mazos de rivales: 36 entradas de 12 bytes `{puntero, renglones, 0}`; 29 cargados. Renglón = `{u32 ID, u32 copias}`. Única referencia en `0x72990` |
| `0x17F3D44` | Mazos iniciales del jugador: 251 renglones `{u32 ID, u32 copias}` |
| `0x17F451C` | Tabla que los reparte: 4 entradas de 16 bytes `{ranura, puntero, renglones, nombre}` para las ranuras 0, 1, 2 y 7 |
| `0x17F0DCC` | Sobres: bloques de `0x78` bytes con 40 × u16 de IDs y 5 pares (puntero, cantidad) que parten las cartas por rareza. Los 12 primeros son de 40; después hay listas de 51 a 177 |
| `0x17D9678` | Fusiones: 80 entradas de 16 bytes |
| `0x17DFE78`–`0x17FD89C` | Zona de listas u16 de IDs: fusiones, categorías para la IA, tableros de examen, sobres |
| `0x1430BE0` | Examen escrito: 204 offsets; datos desde `0x1430F10` |
| `0x13F7000`–`0x1470000` aprox. | Diálogos y textos de interfaz |

- Los mazos de rivales suman entre 13 y 47 cartas. En un duelo contra Jaden
  el mazo real tuvo 55 y sus primeras cartas coinciden con el mazo 1. [HIP] La
  tabla da la base y el juego suma cartas de otra lista.
- No se sabe qué número de mazo es de qué duelista. Por contenido: 1 héroes
  elementales, 2 "roids", 3 koalas, 31 Blue-Eyes.
- Las listas usan **IDs de Konami, no índices**: al cambiar el ID de un hueco
  hay que reemplazarlo en todas.

### 5.6 Contraseñas [ROM]

Los 8 dígitos se leen como 8 nibbles de un u32. Se guarda
`valor XOR relleno(i)`, con
`relleno(i) = ((i × 0x343FD + 0x269EC3) >> 16) | 0x9EC30000`.
Comprobado: Blue-Eyes da 89631139. La compra está en `FUN_080D5EE0` (resta
1000 DP en `0xD5FA8`) y entrega con `FUN_080E58B8(índice, copias)`.

### 5.7 Funciones identificadas [ROM]

| Dirección | Qué hace |
|---|---|
| `0x080DD72C` | ID de Konami → índice (búsqueda binaria sobre la tabla de IDs) |
| `0x0806162C` | Índice → fila de la tabla de efectos, o −1 |
| `0x0800DCB4` | Índice → puntero al nombre |
| `0x080E58B8` | Agrega copias de una carta al baúl y la marca como nueva |
| `0x080E15CC` | Reparte los cuatro mazos iniciales al crear la partida |
| `0x080E1574` | `(ranura, ID, copias)`: completa el baúl y agrega al mazo |
| `0x080E5BA4` | Agrega una carta a un mazo del jugador |
| `0x080D5EE0` | Compra por contraseña |
| `0x0800F898` | Devuelve los flags que se copian al baúl |

`yugiohgx-da` trae un `ghidra_functions.json` con 241 funciones nombradas.

### 5.8 Memoria durante el juego [ROM]

| Dirección | Qué hay |
|---|---|
| `0x02000000` | Baúl: 12 bytes por carta (índice − 1). `+4` u16: bits 3–10 copias, bit 1 nueva, bit 2 por contraseña. `+8` u32 de flags |
| `0x02003848` | DP |
| `0x02003858` | Mazos del jugador: 8 de `0xC6` bytes, índices u16 |
| `0x02004B08` | Cabeceras de mazo (36 bytes): cantidad y nombre |
| `0x02022250` | Duelo, jugador: LP en `+0`, ranuras de `0x50` bytes |
| `0x02024D58` | Duelo, rival (misma estructura) |
| `0x02028188` | Cursor del duelo: x, y, índice en la mano |
| `0x02019F00` | Selección en curso (`+0x24`, `+0x28`, `+0x2C`) |
| `0x0200BBB0` | Lista del baúl que arma el editor de mazos |

Ranura de carta en duelo: `+0x24` índice, `+0x28` ATK, `+0x2C` DEF, `+0x30`
atributo (3 bits altos) y tipo (5 bajos), `+0x31` zona en el nibble alto
(`0` campo, `5` mágica/trampa, `A` campo mágico, `B` fusión, `C` mazo,
`D` cementerio, `E` retirada, `F` mano), `+0x33` posición (`10` ataque,
`30` defensa, `20` boca abajo), `+0x70` flags. Listas por jugador: mano
`+0x2824`, mazo `+0x28A4`, cementerio `+0x2924`, fusión `+0x29A4`.

### 5.9 Espacio libre [ROM]

Desde `0x17FD89C` hasta el final (unos 8 MB) hay relleno aleatorio sin
referencias. Los ROMs de prueba ya guardan ahí textos (`0x1800000`) y código
(`0x1900000`) y funcionan.

### 5.10 Sin ubicar

Lista de prohibidas y limitadas, motor de sonido, segundo mecanismo de
efectos, lógica de la IA, eventos y calendario de la academia, formato del
guardado.

## 6. Cómo se modifica el juego hoy

### 6.1 Restaurar una carta recortada

`restaurar.py` toma un monstruo Normal (el "hueco") y lo convierte:

1. Cambia el ID de Konami por el de la carta recortada.
2. Escribe estadísticas, nombre, descripción y contraseña.
3. Reemplaza el ID viejo en mazos de rivales, mazos iniciales, listas u16 y
   examen.
4. Recoloca la carta en el orden alfabético.
5. Aplica los parches de código pedidos y verifica el resultado.

**Huecos.** Un monstruo Normal es un hueco "seguro" si no está en mazos, listas de la IA, fusiones,
código ni examen, y sale en algún sobre. `python3 scripts/huecos.py ROM_ORIGINAL` los calcula: 47
seguros, 27 usados y **20 libres** (recalculado el 2026-10-11; la cuenta anterior decía 46 y 15, pero
la lista con que se hizo no se guardó). Tres de los 30 usados (Flying Fish, Mystical Shine Ball,
Fiend Scorpion) hoy no pasarían el criterio, que ahora también mira los IDs que el código arma con
sumas y restas; no se vio ningún efecto de eso. La carta
restaurada hereda el lugar del hueco en los sobres y también **su dibujo**.

### 6.2 Formato de receta

```json
{
  "parches": {
    "busqueda_ids": true,
    "invocacion_tipo": [{"id_konami": 5222, "tipo": "Fiend", "cantidad": 3}],
    "contrasenas_gratis": true,
    "baul_inicial": 3
  },
  "cartas": [{
    "hueco": 524, "hueco_nombre": "Boneheimer", "id_konami": 5044,
    "nombre": "Rigorous Reaver", "atk": 1600, "def": 100, "nivel": 3,
    "atributo": "FIRE", "tipo": "Plant", "clase": "Effect",
    "contrasena": "39180960", "descripcion": "FLIP: ...",
    "anular_columnas": ["fn_c", "fn_18"]
  }]
}
```

`clase` es Normal, Effect, Fusion o Ritual para monstruos, o una de la tabla
de §5.2 para mágicas y trampas. `anular_columnas` es opcional y pone en cero
columnas de la fila de efecto.

### 6.3 Parches de código existentes (`scripts/parches.py`)

| Parche | Qué hace | Estado |
|---|---|---|
| `busqueda_ids` | Reemplaza la búsqueda ID→índice por una sobre una tabla propia de pares. Cualquier hueco sirve para cualquier carta | Una partida nueva arma el mismo baúl que el original |
| `invocacion_tipo` | La invocación "retirando del Cementerio" acepta requisitos por tipo y de 3 cartas. Mueve la tabla, amplía `FUN_0800DDC0`, reemplaza `FUN_0806FDD0`, ganchos en `0x7004C`, `0x70228`, `0x7042E` | [PROBADO] con Dark Necrofear. La IA no lo contempla |
| `contrasenas_gratis` | `nop` en `0xD5FA8`: no descuenta DP | Solo para pruebas |
| `baul_inicial` | Gancho en `0xE1632`: al crear la partida agrega N copias de cada carta de la receta | Solo para pruebas. Baúl de 167 cartas comprobado |

Técnica de gancho: `ldr rN,[pc]; bx rN; .word destino` (8 bytes en dirección
alineada a 4, 10 si no) o un `BL` de 4 bytes hacia un trampolín cercano.

## 7. Herramientas y archivos

Carpeta: la raíz de este repositorio.

| Ruta | Para qué |
|---|---|
| `scripts/da_lib.py` | Offsets y lectura/escritura de tablas (clase `Rom`) |
| `scripts/volcar.py` | Genera los CSV de `datos/` |
| `scripts/restaurar.py` | Receta → ROM nuevo |
| `scripts/parches.py` | Parches de código (necesita `keystone-engine`) |
| `scripts/bps.py` | Crea y aplica `.bps` en Python puro, valida CRC |
| `scripts/emular.py` | Ejecuta rutinas sueltas del juego (`unicorn`) |
| `scripts/gba.py` | Emulador sin ventana (núcleo `mgba_libretro`, Pillow) |
| `scripts/duelo_auto.py` | Sobre `gba.py`: partida nueva, mazo de prueba, lectura del duelo |
| `datos/cartas.csv` | Las 1200 cartas con estadísticas, contraseña y texto |
| `datos/efectos.csv` | Las 901 filas de efecto |
| `datos/cartas_recortadas.csv` | Las 172 recortadas |
| `datos/mazos.csv` | Mazos de rivales |
| `datos/pruebas.csv` | Resultado por carta del lote de 30 |
| `datos/huecos.csv` | Registro de huecos: qué índice ocupa cada carta restaurada. `restaurar.py` lo hace cumplir |
| `scripts/parche_efecto.py`, `efectos/*.s` | Piezas propias (funciones de efecto, ganchos, entradas de tabla) |
| `scripts/construir_lote.sh` | Arma el ROM de trabajo `(Lote)` de cero, desde `recetas/lote.json` |
| `scripts/arte.py` | Dibujos: del ROM a PNG y de PNG al ROM (clave `"arte"` de una carta en la receta) |
| `scripts/armar_version.py` | Versión de juego con las cartas aptas: receta, ROM, `.bps` y notas |
| `recetas/*.json` | `prueba3` (para jugar), `test` (prueba, todo junto), `candidatas-30`, `prueba1`, `prueba2` |
| `build/*.bps`, `build/*.gba` | Parches y ROMs generados |
| `estados/sabado-cuarto.st` | Estado de mGBA libretro: partida nueva en el primer sábado |

```
python3 scripts/restaurar.py "ROM original.gba" recetas/test.json "build/salida.gba"
python3 scripts/bps.py "ROM original.gba" "build/salida.gba" build/salida.bps
python3 scripts/bps.py --aplicar "ROM original.gba" build/test.bps "build/salida.gba"
```

ROMs generados:

| ROM | Contenido | MD5 |
|---|---|---|
| `(Test).gba` | 30 cartas, los cuatro parches, 3 copias de cada una en el baúl | `d6fe444f169d3a1f92ec2c453b7ccc3a` |
| `(Candidatas).gba` | Igual, sin las cartas en el baúl | `cb519dad73a0b1cf70154369e8168547` |
| `(Prueba3).gba` | Las 4 que funcionan y Dark Necrofear, sin ayudas | `0122cad69328c075c66a6d0227a93f58` |
| `(Prueba1).gba`, `(Prueba2).gba` | Primeras pruebas, superadas | |

Proyectos externos:

- [coolstuffinc/yugiohgx-da](https://github.com/coolstuffinc/yugiohgx-da): herramienta Python para este mismo ROM, con wiki y nombres de funciones. Algunos offsets suyos estaban corridos (tabla de efectos, examen).
- [CosmicScribe64/eds-decomp](https://github.com/CosmicScribe64/eds-decomp): decompilación de *Eternal Duelist Soul*, motor anterior. Sirve para entender la tabla de efectos.
- [DawnbrandBots/yaml-yugi](https://github.com/DawnbrandBots/yaml-yugi): ID de Konami → nombre, estadísticas y contraseña reales.
- [Data Crystal, WC2006](https://datacrystal.tcrf.net/wiki/Yu-Gi-Oh!_Ultimate_Masters:_World_Championship_Tournament_2006/ROM_map): mapa del pariente más cercano.

## 8. Estado actual

**Hecho**

- Mapa de datos del ROM y volcado a CSV.
- Restauración de cartas por cambio de ID, automatizada y verificada.
- Cuatro parches de código (§6.3).
- Lote de 30 cartas restauradas, las 30 con veredicto y prueba en duelo.
- ROM único de prueba (`Test`), ROM de trabajo con las piezas nuevas (`Lote`) y ROM para jugar (`Prueba3`).

**Resultado del lote de 30**

| Carta | Índice | Reemplaza a | ID Konami | Contraseña | Clase | Resultado |
|---|---|---|---|---|---|---|
| Rigorous Reaver | 524 | Boneheimer | 5044 | 39180960 | Plant / Effect | funciona |
| Jowls of Dark Demise | 520 | Souleater | 5035 | 05257687 | Fiend / Effect | funciona |
| Windstorm of Etaqua | 489 | Flying Kamakiri #2 | 5001 | 59744639 | Trap | funciona |
| Ready for Intercepting | 534 | Shining Abyss | 5331 | 31785398 | Trap | funciona |
| Dark Necrofear | 968 | Gigobyte | 5222 | 31829185 | Fiend / Effect | funciona |
| Hiro's Shadow Scout | 532 | Lightning Conger | 4617 | 81863068 | Fiend / Effect | funciona |
| Dark-Eyes Illusionist | 57 | Fiend's Hand | 4736 | 38247752 | Spellcaster / Effect | funciona |
| Goddess of Whim | 525 | Flame Dancer | 4435 | 67959180 | Fairy / Effect | funciona |
| Kunai with Chain | 569 | Science Soldier | 4657 | 37390589 | Trap | funciona |
| The Inexperienced Spy | 84 | Doriado | 4848 | 81820689 | Spell | funciona |
| Share the Pain | 418 | Man-Eating Treasure Chest | 4889 | 56830749 | Spell | funciona |
| Exchange | 492 | Overdrive | 5218 | 05556668 | Spell | funciona |
| Electromagnetic Bagworm | 522 | Shapesnatch | 5040 | 07914843 | Insect / Effect | funciona |
| Reaper of the Cards | 971 | Pharaoh's Servant | 4090 | 33066139 | Fiend / Effect | funciona |
| Penguin Knight | 972 | Pharaonic Protector | 4205 | 36039163 | Aqua / Effect | funciona |
| Electric Snake | 936 | Mystical Shine Ball | 4469 | 11324436 | Thunder / Effect | funciona |
| Minar | 970 | Fiend Scorpion | 4540 | 32539892 | Insect / Effect | funciona |
| Lady Panther | 63 | Fire Reaper | 5193 | 38480590 | Beast-Warrior / Effect | funciona |
| Fairy Guardian | 530 | Flying Fish | 5202 | 22419772 | Fairy / Effect | funciona |
| Acid Trap Hole | 533 | Spherous Lady | 4691 | 41356845 | Trap | funciona |
| Mystical Refpanel | 657 | Lizard Soldier | 4826 | 35563539 | Trap | funciona |
| Two-Pronged Attack | 488 | Dark Bat | 4839 | 83887306 | Trap | funciona |
| Magic Drain | 536 | Grand Tiki Elder | 5133 | 59344077 | Trap Counter | funciona |
| Riryoku Field | 417 | Baron of the Fiend Sword | 5263 | 70344351 | Trap Counter | funciona |
| Big Burn | 564 | Skull Mariner | 5851 | 95472621 | Trap | funciona |
| Riryoku | 487 | Cyber Falcon | 5009 | 34016756 | Spell | funciona |
| Seal of the Ancients | 538 | Melchid the Four-Face Beast | 5011 | 97809599 | Spell | funciona |
| Chosen One | 70 | Spirit of the Harp | 5101 | 21888494 | Spell | funciona |
| Monster Recovery | 227 | Fire Kraken | 5152 | 93108433 | Spell Quick-Play | funciona |
| Reasoning | 508 | The Illusory Gentleman | 5530 | 58577036 | Spell | funciona |

El veredicto de cada carta, qué se observó, qué falla y cómo reproducirlo están en
`datos/pruebas.csv` (fuente única); la tabla de `PRUEBAS.md` se genera desde ahí. La columna
"Resultado" de arriba se copió de ese archivo el 2026-10-11 (noche).

**Estado al 2026-10-11 (noche):** las 30 funcionan. Las dos que estaban en parte se completaron:
Electromagnetic Bagworm (la Máquina que la destruye pierde 500) y Dark Necrofear (posesión en la End
Phase: queda equipada al monstruo elegido y el control dura mientras siga equipada). Ninguna quedó en
"no funciona" ni aparcada. El ROM de trabajo es `build/…(Lote).gba`
(`scripts/construir_lote.sh`, MD5 `c1b1289a1e0a3ca4c725272073c791db`). Falta la confirmación a ojo de
Oscar en 24 cartas; las que cambiaron el 2026-10-11 tienen partida por capturas en `evidencia/ronda6/`
y `evidencia/ronda7/`.

## 9. Backlog de features candidatas

Cada ítem puede ser una especificación propia. El orden es una sugerencia.

| # | Feature | Para qué | Qué se sabe | Dificultad |
|---|---|---|---|---|
| F1 | Cerrar las pruebas del lote de 30 | Saber qué cartas entran | ROM `Test` y `PRUEBAS.md` listos | Baja; es jugar |
| F2 | Diagnóstico de las cartas que fallan | Recuperar las que hoy no andan | Patrón de §5.4; hay que rastrear qué tablas consulta cada función de efecto | Media-alta |
| F3 | Posesión de Dark Necrofear | Carta completa | **Hecha el 2026-10-11, versión fiel:** queda equipada al monstruo elegido; el control termina si la destruyen | Hecho |
| F4 | Arte de las cartas restauradas | Que no muestren el dibujo del hueco | Formato conocido (80×80, 64 colores, tiles 8×8, paleta BGR555). Falta el conversor PNG → ROM | Baja-media |
| F5 | Más recortadas, por packs | Más cartas | El alta está hecha (`scripts/alta.py`). Clasificadas las 142 (`datos/triage_recortadas.csv`): 36 con el efecto compartido con cartas en juego, 38 con código propio, 2 vacías y 66 sin función de efecto. Quedan 20 huecos seguros | Baja por carta en el primer grupo |
| F6 | Más huecos o ampliar las 1200 | Sumar sin sacrificar cartas | La cantidad se lee de `0x7A8620`, pero hay 706 referencias a la tabla de IDs, arte y paletas por índice, tope 900 de efectos, baúl de 12 bytes por carta en RAM y guardado | Muy alta |
| F7 | Efectos escritos de cero | Las 68 con stub y cartas que el juego nunca tuvo | Requiere entender las columnas de la tabla de efectos y el segundo mecanismo | Muy alta |
| F8 | Identificar y editar mazos de rivales | Dificultad y variedad | Tabla y formato conocidos; falta saber quién usa cada mazo y de dónde salen las cartas extra | Media |
| F9 | IA para las cartas nuevas | Que los rivales las usen | Hay listas de categorías para la IA en `0x17E1444`–`0x17E1700` [HIP]; la lógica no está ubicada | Alta |
| F10 | Distribución de cartas (sobres, premios) | Que se consigan jugando | Formato de sobres conocido; hoy heredan el lugar del hueco | Baja-media |
| F11 | Rebalanceo y textos | Ajustes y traducción | Edición de datos pura; los textos ya se pueden reubicar | Baja |
| F12 | Historia, eventos y diálogos | El "fangame" | Diálogos ubicados en ASCII; eventos y calendario sin investigar | Sin estimar |
| F13 | Paquete de versión | Entregar | `bps.py` listo; falta definir nombre, versión y notas | Baja |

Dependencias: F2 necesita F1. F5 mejora mucho con F2. F3 y F7 comparten la
investigación de cómo se escribe un efecto. F9 depende de F8.

## 10. Preguntas abiertas

1. ¿Qué hace cada columna de la fila de efecto (`+0x04`, `+0x0C`…`+0x18`) y
   los flags de `+0x08`?
2. ¿Dónde está el segundo mecanismo de efectos (las 137 cartas sin fila)?
3. ¿Qué tablas consultan las funciones de las cartas que fallan?
4. ¿Qué mazo es de qué duelista y cómo se completan hasta 40 o más cartas?
5. ¿Qué son los 93 renglones de `0x17F40EC` que no están en la tabla de mazos
   iniciales?
6. ¿Cómo decide la IA qué jugar, y qué hace con una carta que no conoce?
7. ¿Qué formato tiene el guardado y cuánto se puede agrandar el baúl?
8. ¿Dónde está la lista de prohibidas y limitadas?

## 11. Riesgos

- **Cartas que parecen andar y fallan en un caso raro.** La prueba cubre el
  caso típico, no las cadenas ni las interacciones con otras cartas.
- **La IA frente a cartas nuevas.** No se sabe cómo reacciona; por ahora no
  van en mazos de rivales.
- **Partidas guardadas entre versiones.** Cambiar qué carta ocupa un índice
  cambia el baúl de una partida vieja. Conviene fijar los huecos pronto.
- **Huecos que se agotan.** 20 seguros para 142 recortadas pendientes (`scripts/huecos.py`).
- **Hardware real.** Todo se probó en emulador (mGBA); la Retroid también
  emula, así que el riesgo es bajo.

## 12. Glosario

- **Índice:** posición de la carta en el juego (1–1200). Es el "Nº" que
  muestra el baúl.
- **ID de Konami:** número global de la carta (4007 en adelante). El efecto
  se busca por este número.
- **Carta recortada:** tiene fila en la tabla de efectos pero no está entre
  las 1200.
- **Hueco:** monstruo Normal que se sacrifica para alojar una carta
  restaurada.
- **Receta:** JSON que describe un ROM: cartas y parches.
- **Fila de efecto:** entrada de 28 bytes con las funciones de una carta.
- **Stub:** función que solo devuelve 0.
- **Gancho:** salto corto escrito sobre el código original hacia código nuevo.
- **Baúl:** colección de cartas del jugador.
- **DP:** moneda del juego.
