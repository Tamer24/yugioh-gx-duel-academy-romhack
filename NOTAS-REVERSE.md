# Duel Academy: notas de ingeniería inversa

Sesión del 2026-10-09 sobre `Yu-Gi-Oh! GX - Duel Academy (USA).gba`
(MD5 `f62c47cbe08e1e3bcfcf9f1b84841a76`). Complementa a
`../DUEL-ACADEMY-ROMHACK.md`. Los offsets son de archivo; la dirección de GBA
es el offset + `0x08000000`.

Cada dato lleva una marca:

- **[ROM]** lo comprobé leyendo o ejecutando código de tu ROM.
- **[HIP]** hipótesis razonable, sin comprobar.

## Lo más importante

1. **El juego trae código de efecto para 172 cartas que no están en el juego.**
   Son restos del motor compartido con los World Championship: Crush Card
   Virus, Vampire Lord, Dark Necrofear, Creature Swap, De-Fusion, Mirror Wall,
   Royal Oppression, Blade Knight y otras. La lista completa está en
   `datos/cartas_recortadas.csv`. [ROM]
2. **El efecto de una carta se busca por su ID de Konami, no por su posición.**
   Si a un hueco del juego le cambio el ID por el de una carta recortada, el
   código del juego le encuentra la fila de efecto. Lo comprobé ejecutando las
   rutinas originales en un emulador de CPU. [ROM]
3. **Tener fila de efecto no garantiza que la carta funcione.** De 12 probadas
   en duelo, 4 andan completas y 5 no hacen nada. Hay que probar una por una.
4. **Hay dos parches de código funcionando:** uno libera la elección de huecos
   y otro permite la invocación especial por tipo (Dark Necrofear).

## Tabla de efectos por carta [ROM]

- Empieza en `0x17D9BEC` (no en `0x17DA800`, como dice la wiki de
  `yugiohgx-da`). Son **901 filas de 28 bytes**, hasta `0x17DFE78`.
- Está **ordenada por ID de Konami**: va de 4022 (Time Wizard) a 6467.
- Formato de la fila:

  | Offset | Campo |
  |---|---|
  | `+0x00` | u16 ID de Konami, u16 en cero |
  | `+0x04` | puntero a función. En 108 filas apunta a `0x08061629`, que solo devuelve 0 |
  | `+0x08` | u32 de flags. `FFFFFFFF` en 813 filas |
  | `+0x0C`, `+0x10`, `+0x14`, `+0x18` | cuatro punteros a función; cualquiera puede estar en cero |

- La busca `FUN_0806162C`: recibe el índice de carta, lo pasa a ID con la tabla
  de `0x7A8624` y hace búsqueda binaria. **El índice máximo (900) está fijo en
  el código** (`movs r4,#0xE1; lsls r4,#2`).
- Hay 13 lugares del código que usan la dirección base `0x097D9BEC`. Todos
  llegan a la fila por el índice que devuelve esa función. Mover o agrandar la
  tabla exige cambiar esos 13 punteros y el 900.
- Qué hace cada columna no está resuelto. [HIP] `+0x04` resuelve el efecto y
  las otras son condición, costo y disparadores, como en la decompilación de
  Eternal Duelist Soul.

Reparto de las 901 filas:

| | Con funciones | Fila vacía | Total |
|---|---|---|---|
| Cartas del juego | 687 | 42 | 729 |
| Cartas recortadas | 109 | 63 | 172 |

**Hay un segundo mecanismo de efectos.** 137 monstruos de efecto del juego no
tienen fila (Exodia, Kuriboh, Maha Vailo, Jinzo #7), y 42 cartas tienen una
fila vacía. Sus efectos se resuelven en otra parte del código. Por eso las 63
recortadas con fila vacía son más dudosas que las 109 que sí tienen funciones.

## Tabla de IDs [ROM]

- `0x7A8620`: u16 con la cantidad de cartas (1200). La búsqueda de ID a índice
  (`FUN_080DD72C`) **lee este valor**, no lo tiene fijo. Otros 40 lugares del
  código también lo leen.
- `0x7A8624`: índice a ID de Konami. **Tiene que estar ordenada**, porque la
  búsqueda inversa es binaria. La dirección aparece en 706 lugares del código.

## Mazos [ROM]

- Tabla en `0x17E1294`: 36 entradas de 12 bytes `{puntero, cantidad de
  renglones, 0}`. La entrada 0 está vacía y hay 29 mazos cargados.
- Cada renglón del mazo ocupa 8 bytes: `{u32 ID de Konami, u32 copias}`.
- La única referencia a la tabla está en `0x72990`.
- Volcado completo en `datos/mazos.csv`.
- Los mazos suman entre 13 y 47 cartas. [HIP] El juego completa los que tienen
  menos de 40, o algunas listas no son mazos de rival. El 13 (13 cartas
  sueltas) y el 34 (24 cartas sueltas) parecen otra cosa.
- No identifiqué qué número corresponde a qué duelista. Por contenido: el 1 es
  de héroes elementales, el 2 de "roids", el 3 de koalas, el 31 de Blue-Eyes.

## Otras tablas en la misma zona

- `0x17DFE78`: tríos de IDs, parecen recetas de fusión. [HIP]
- `0x17E1444`–`0x17E1700`: listas de IDs agrupadas por función (curación,
  campos, equipos, trampas). Parecen categorías para la IA. [HIP]
- Después vienen bloques con carta, posición y puntos de vida (2600, 5000,
  3600). Parecen los tableros de los exámenes prácticos. [HIP]
- `0x1430BE0`: tabla de offsets del examen escrito. Tiene **204** entradas, no
  1200 como dicen las notas de `yugiohgx-da`; los datos empiezan en
  `0x1430F10`. [ROM]

## Confirmado de `yugiohgx-da` [ROM]

- Arte: 80×80, 8bpp en tiles de 8×8, 64 colores. Extraje seis cartas y se ven
  bien.
- Contraseñas: el algoritmo da 89631139 para Blue-Eyes, que es la real.
- Nombres y descripciones: el código suma un offset de 32 bits a la base, sin
  límite. Un texto nuevo puede vivir en cualquier parte del ROM.

## Espacio libre

Desde `0x17FD89C` hasta el final (8 MB) la entropía es 7,997 y no hay
estructura. Las palabras del código que "apuntan" ahí son instrucciones que
coinciden por azar, no punteros. [ROM] La prueba definitiva sigue siendo jugar
con algo escrito ahí; el ROM de prueba guarda sus textos en `0x1800000`.

## Cómo se restaura una carta

`restaurar.py` convierte un monstruo Normal en una carta recortada: cambia ID,
estadísticas, nombre, descripción y contraseña, reemplaza el ID viejo en mazos,
listas y examen, y recoloca la carta en el orden alfabético (`0xF59558`).

Con el parche `busqueda_ids` sirve cualquier hueco. Sin él, el hueco tiene que
ser vecino del ID nuevo para no desordenar la tabla de IDs.

(Desde el 2026-10-11 la lista la calcula `scripts/huecos.py`: 47 seguros, 20 libres.)
Los huecos se eligen entre 46 monstruos Normales "seguros": no están en mazos
de rivales, ni en listas de la IA, ni son material de fusión, ni aparecen en el
código o en el examen, y salen en algún sobre. La carta restaurada hereda el
lugar del hueco en los sobres.

## Parches de código (`scripts/parches.py`) [ROM]

El código nuevo va al espacio libre desde `0x1900000`. Sobre el código
original solo hay ganchos de 4 u 8 bytes.

**`busqueda_ids`.** Reemplaza `FUN_080DD72C` (ID a índice) por una búsqueda
binaria sobre una tabla propia de pares `{ID, índice}`. Probado: una partida
nueva arma el mismo baúl inicial de 137 cartas que el ROM original.

**`invocacion_tipo`.** La invocación especial "retirando monstruos del
Cementerio" solo comparaba atributos y aceptaba 1 o 2 cartas. El parche:

- mueve la tabla de `0x17DFF44` al espacio libre y le suma entradas;
- amplía `FUN_0800DDC0`: un requisito con el bit `0x80` compara el **tipo**;
- reemplaza `FUN_0806FDD0` para que el tercer requisito repita el segundo;
- agrega el texto del pedido, la validación y el retiro de la tercera carta
  dentro de `FUN_0806FF54` (ganchos en `0x7004C`, `0x70228` y `0x7042E`);
- guarda la tercera ranura elegida en `0x020278BE`, un byte libre.

Probado con Dark Necrofear: aparece *Special Summon*, pide "Select 3 Fiend
monsters to remove from the Graveyard", la lista solo muestra Demonios, los
tres quedan retirados y la carta entra al campo. La IA no está contemplada:
no conviene poner estas cartas en mazos de rivales.

**`contrasenas_gratis`.** Un `nop` en `0xD5FA8`: la máquina de contraseñas no
descuenta los DP. Solo para ROMs de prueba.

**`baul_inicial`.** Gancho en el final de `FUN_080E15CC` (`0xE1632`), la rutina
que reparte los mazos iniciales: después llama a `FUN_080E58B8(índice, copias)`
por cada carta de la receta. Probado: una partida nueva arranca con 167 cartas
distintas en el baúl (las 137 de siempre más las 30, 3 copias de cada una).
Solo para ROMs de prueba.

## Resultados de las pruebas [ROM]

Detalle por carta en `PRUEBAS.md` y `datos/pruebas.csv`. De 12 cartas probadas
en duelo:

- **Funcionan (4):** Rigorous Reaver, Jowls of Dark Demise, Windstorm of
  Etaqua, Ready for Intercepting.
- **Funciona con parche, a medias (1):** Dark Necrofear. Se invoca; su
  posesión está vaciada (la función de su fila solo devuelve 0).
- **A medias o sin confirmar (2):** Hiro's Shadow Scout (el rival roba 1 en vez
  de 3), Dark-Eyes Illusionist (pide objetivo; el bloqueo no lo confirmé).
- **No funcionan (5):** Goddess of Whim, The Inexperienced Spy, Exchange,
  Share the Pain, Kunai with Chain.

Conclusión: tener una fila con funciones reales **no alcanza**. Quedan 103
recortadas con función real en `+0x04`, pero cada una hay que probarla. Las que
fallaron tienen en común que necesitan una interacción extra (mostrar la mano
rival, que el rival elija, un menú de activación). [HIP] Como pasó con la tabla
de invocación, a varias les deben faltar entradas en tablas de datos recortadas.

Un filtro previo que sí sirve: descartar las que tienen en `+0x04` una función
vacía (`movs r0,#0; bx lr`). Son 69 de las 172.

## Mazos iniciales [ROM]

`0x17F3D44` en adelante: 251 renglones `{u32 ID, u32 copias}`. La tabla que
los reparte está en `0x17F451C`: 4 entradas de 16 bytes `{ranura de mazo,
puntero a renglones, cantidad de renglones, puntero al nombre}`, para las
ranuras 0, 1, 2 y 7 (39, 39, 39 y 41 renglones). La recorre `FUN_080E15CC`, que
por cada renglón llama a `FUN_080E1574(ranura, ID, copias)`: completa el baúl
hasta esas copias y agrega la carta al mazo. Los 93 renglones que quedan en el
medio (`0x17F40EC`) no están en esa tabla. [HIP] `restaurar.py` también
reemplaza IDs ahí; si no, una partida nueva pediría una carta que ya no existe.

## Memoria durante el juego [ROM]

| Dirección | Qué hay |
|---|---|
| `0x02000000` | Baúl: 12 bytes por carta, índice − 1. En `+4`, u16 con bits 3–10 = copias, bit 1 = carta nueva, bit 2 = obtenida por contraseña. En `+8`, u32 copiado de los flags de la tabla de efectos |
| `0x02003848` | DP |
| `0x02003858` | Mazos del jugador: 8 de `0xC6` bytes, índices u16. Mazo de lado en `0x02003E88`, de fusión en `0x020044B8` |
| `0x02004B08` | Cabeceras de mazo, 36 bytes: bits 0–6 = cartas del mazo principal; después el nombre |
| `0x02022250` | Duelo, jugador: LP en `+0`; cartas en ranuras de `0x50` bytes |
| `0x02024D58` | Duelo, rival (misma estructura, `0x2B08` más adelante) |
| `0x02028188` | Cursor del duelo: x, y, índice en la mano. y = 0 mano, 1 mágicas/trampas, 2 monstruos, 3 y 4 lado rival |
| `0x0200BBB0` | Lista del baúl que arma el editor: u32 con índice en los 11 bits bajos; cantidad en `+0x70BE` |

Ranura de carta en duelo: `+0x24` índice, `+0x28` ATK, `+0x2C` DEF, `+0x30`
atributo (3 bits altos) y tipo (5 bajos), `+0x31` zona en el nibble alto
(`0` campo, `5` mágica/trampa, `A` campo mágico, `B` fusión, `C` mazo,
`D` cementerio, `E` retirada, `F` mano), `+0x33` posición (`10` ataque,
`30` defensa, `20` boca abajo), `+0x70` flags de efecto.

Listas por jugador: mano en `+0x2824`, mazo en `+0x28A4`, cementerio en
`+0x2924`, fusión en `+0x29A4` (una ranura por byte).

En el duelo contra Jaden el mazo real tuvo 55 cartas, y las primeras coinciden
con el mazo 1 de la tabla: la tabla da la base y el juego suma cartas de otra
lista. [HIP]

## Scripts

| Script | Para qué |
|---|---|
| `scripts/da_lib.py` | Offsets y lectura de tablas |
| `scripts/volcar.py` | Genera los CSV de `datos/` |
| `scripts/restaurar.py` | Aplica una receta de `recetas/` y deja un ROM nuevo |
| `scripts/parches.py` | Los parches de código. Necesita `keystone-engine` |
| `scripts/bps.py` | Crea y aplica parches `.bps` |
| `scripts/emular.py` | Ejecuta las búsquedas del juego sobre un ROM (`unicorn`) |
| `scripts/gba.py` | Emulador sin ventana manejado por script (núcleo `mgba_libretro`, Pillow) |
| `scripts/duelo_auto.py` | Sobre `gba.py`: partida nueva, mazo de prueba, cursor, menús y estado del duelo |
| `estados/sabado-cuarto.st` | Partida nueva guardada en el primer sábado, para no repetir la introducción |

```
python3 scripts/restaurar.py "ROM.gba" recetas/prueba3.json "build/salida.gba"
python3 scripts/bps.py --aplicar "ROM.gba" build/prueba3.bps "build/salida.gba"
```

Recetas: `prueba3.json` (las 5 que funcionan, para jugar), `test.json` (ROM
único de prueba: las 30 del lote, ya en el baúl al empezar, con contraseñas
gratis) y `candidatas-30.json` (lo mismo sin las cartas en el baúl).

## Motor de efectos: lo leído hasta ahora [ROM] / [HIP]

Investigación del 2026-10-09 con `scripts/desensamblar.py` (necesita `capstone`).

**Comprobado en el código [ROM]**

- Las funciones de una fila de efecto son chequeos, no la resolución. Ejemplo,
  The Inexperienced Spy: `fn_10` (`0x080320BC`) solo lee un contador del rival;
  `fn_04` (`0x0803E3AC`) verifica condiciones y devuelve `0x80`.
- Ese `0x80` es un **código de interacción** que el motor guarda en el byte
  `0x020204C6` (`0x0201FD00+0x7C6`). Tres funciones lo despachan con un
  `switch (código - 0x62)` de 31 casos: `0x080502FC` (tabla `0x0805034C`),
  `0x08050BEC` (tabla `0x08050C2C`) y `0x0805A754` (tabla `0x0805A79C`).
- En las tres solo hay casos para `0x62`, `0x63`, `0x7C`–`0x80` (y `0x78` en la
  tercera). Los 24 códigos `0x64`–`0x7B` caen al valor por defecto. El `switch`
  **no está indexado por carta**, así que no es donde se recortaron las
  cartas.
- El caso `0x80` llama a `0x080500F0` (selección de objetivos), guarda estado
  en `0x02019F00+0x24` y devuelve el siguiente estado (`0x7E` o `0x7F`).
- Los eventos se encolan con `0x08022084` y `0x08021FE8` en la cola de
  `0x020214E0`: entradas de 8 bytes, código en `+0xC` (bit 15 = lado del
  rival), argumento en `+0xE`, cantidad en `0x020214E0+0x90C`. Hay una
  segunda lista (cadena/disparos) con la cantidad en `+0xD64`.
- `0x08015E78` junta efectos disparados; no los resuelve.

**Hipótesis [HIP]**

- Los nombres de `ghidra_functions.json` de `yugiohgx-da` (3862 entradas, no
  241) dan candidatos: `state_machine_effect_resolution` `0x080577E8`,
  `effect_activation_gatekeeper` `0x080317E4`,
  `card_effect_handler_common_33cards` `0x0803991C`,
  `card_effect_handler_atk_def_change_24cards` `0x0803B334`,
  `card_effect_handler_draw_11cards` `0x08061A74`. Los nombres son de otro
  autor y no están verificados.
- La resolución real de una carta probablemente está en
  `state_machine_effect_resolution` o en los `card_effect_handler_*`
  compartidos por familias de cartas. Sin comprobar.
- La primera hipótesis de `PROYECTO.md` §8 (a las fallidas les faltan entradas
  en tablas) sigue en pie, pero no se encontró la tabla.

**Descartado**

- Que las cinco cartas que fallan tengan una fila de efecto distinta: la
  combinación `fn_04 + fn_10` sin `fn_0C` es la más común del juego (71
  mágicas y 58 trampas originales que funcionan).

## Cómo funciona una carta en el motor (Ghidra) [ROM] / [HIP]

Decompilado con `ghidra/` (ver más abajo). Resultados del 2026-10-09:

- Las funciones de una fila son **pasos de una máquina de estados de
  activación**. El estado vive en el byte `0x020204C6`; los valores que se ven
  son `0x7E`, `0x7F` y `0x80`. Cada función recibe la carta (`byte *`) y
  devuelve el estado siguiente (`0` = no hace nada).
  - Pot of Greed (`0x0803DFE4`): en `0x7F` pide confirmación y pasa a `0x7E`;
    en `0x80` roba (`FUN_0801B28C(lado, n)`) y pasa a `0x7F`.
  - Ancient Telescope (fila 185, `0x0803E458`): solo actúa si el estado es
    `0x80`: limpia la zona de efectos, registra las cartas del rival y abre el
    diálogo (`init_effect_dialogue`). Devuelve `10`.
- `fn_10` es una **condición de bloqueo/recursos**: la de Pot of Greed
  (`0x08031824`) revisa si el rival tiene una carta fija en juego; la de The
  Inexperienced Spy (`0x080320BC`) revisa que el rival tenga cartas en mano.
- `FUN_080616B8` (`0x080616B8`) toma una carta, busca su fila y **llama a
  `fn_0C` si no es cero**; si es cero devuelve 1 y no hace nada. La usan las
  funciones de disparo (`0x0803E400` y familia).
- Las funciones son **compartidas por familias** (por ejemplo `0x0803E401`
  la usan Reinforcements, Castle Walls y siete más).
- **The Inexperienced Spy:** `fn_04` (`0x0803E3AC`) solo comprueba que haya
  cartas en la mano rival y devuelve `0x80`. **Nada atiende ese `0x80` para
  esta carta**: no hay función que muestre la mano. Es la causa más probable de
  "se activa y no hace nada" [HIP]. Ancient Telescope es la plantilla de lo que
  falta.
- Descartado: "fn_0C vacío explica el fallo". Pot of Greed, Monster Reborn,
  Mirror Force y Trap Hole originales también lo tienen vacío y funcionan.

### Ghidra

- Carpeta `ghidra/`: `codigo.bin` (primeros `0x7A8000` bytes del ROM, base
  `0x08000000`), `proyecto/` (proyecto analizado, grande, regenerable),
  `scripts/` (`Preparar.java`, `Decompilar.java`), `salida/` (C decompilado).
- `nombres_yugiohgx-da.json` viene de yugiohgx-da (MIT) y trae 3862
  direcciones; la mayoría con nombre automático `FUN_...`.
- Regenerar: `analyzeHeadless ghidra/proyecto da -import ghidra/codigo.bin
  -loader BinaryLoader -loader-baseAddr 0x08000000 -processor ARM:LE:32:v4t
  -preScript Preparar.java <json>`.
- Decompilar: `-process codigo.bin -noanalysis -postScript Decompilar.java
  salida.c DIR1 DIR2 ...`. Necesita `JAVA_HOME` de `openjdk@21`.

## Menús de selección y códigos de resolución: qué está vacío [ROM] / [HIP]

Hallazgo del 2026-10-09. Es el mismo patrón que la invocación del Cementerio
(§5.4): **una tabla chica con casos borrados**.

- **Abrir un menú:** `FUN_08026970(lado, modo, p3, p4)` (`0x08026970`) guarda
  el modo en `0x02022250+0x5640` (bits 12–17) y arranca el submenú.
  `FUN_08026A3C(lado, n, 0, 0)` es su envoltorio para el modo 1.
- **Despachador de modos:** `FUN_08026614` (`0x08026614`), `modo - 1` con 29
  casos; tabla en `0x08026678` (entrada del modo N en `0x08026678 + (N-1)*4`).
  El valor por defecto es `0x08026628` (`movs r0,#0`).
- **Modos con manejo real:** 1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 15, 17, 18, 19,
  20, 21, 22, 23, 24, 29.
- **Modos vacíos (9):** 6, 7, 13, 14, 16, 25, 26, 27, 28.
- Modo 1 = elegir una carta de la mano propia y descartarla (Graceful Charity,
  Card Destruction). Lo atiende `FUN_0806B408` (`0x0806B408`), que recibe el
  lado, la cantidad y banderas.
- **Las cartas recortadas que usan modos vacíos son las que fallan:**
  Exchange (modo 6), Earthshaker (14), Magic Drain (26). Los modos 4, 11, 12,
  17, 21, 22 y 29 los usan cartas del juego.
- **Exchange** (`0x08043A08`): en `0x80` abre el modo 6 para el jugador, en
  `0x7F` lo abre para el rival, en `0x7E` guarda la elección y devuelve `0x64`.
  **Corrección (2026-10-10):** `0x64` no es un código vacío: lo devuelven 27
  cartas, muchas originales que funcionan (Thunder Dragon, Painful Choice,
  Hyena...), así que se atiende en otro lado. Lo que falta a Exchange es el
  modo 6 (vacío), no la resolución. `scripts/codigos_estado.py` y
  `datos/codigos_estado.csv`.
- **The Inexperienced Spy** no abre ningún menú: su `fn_04` devuelve `0x80` y
  nada más. Necesita su propio paso que muestre la mano rival.
- [HIP] Un modo nuevo que muestre la mano de un lado dado serviría para
  Exchange (6) y para la Spy.

## Cómo se muestran y eligen cartas: el registro de efectos [ROM] / [HIP]

Aclarado el 2026-10-09 leyendo **Spiritual Water Art - Aoi** (original, "mirá la
mano del rival, elegí 1 y mandala al cementerio") y **Ancient Telescope**.

- **No usa los menús de modos** (§anterior). Usa un **registro de efectos**:
  la lista de cartas candidatas.
  - `clear_zone_effects(6, 0)` vacía el registro.
  - `remove_card_from_effect_register(carta)` (`0x0800B640`, el nombre es de
    `yugiohgx-da` y engaña) agrega una carta como candidata.
  - `init_effect_dialogue(0, n, ptr, flag)` (`0x080875F4`) abre la pantalla de
    selección con lo registrado.
- Aoi (`fn_04` `0x0803F4A0`) recorre estados `0x80 → 0x7E → 0x7D`. Su función
  de candidatas (`FUN_0805CFB0`) registra **todas las cartas de la mano del
  rival** (recorre su lista de mano con el contador de mano) y sigue por la cola
  común `FUN_08061382`, que filtra protegidas y devuelve cuántas quedan.
- Ancient Telescope (`0x0803E458`) hace lo mismo con el **tope del mazo** del
  rival (hasta 5) y luego `init_effect_dialogue`, con estos ajustes
  posteriores: `*(p-5) &= 0x3f; *(p-4) &= 0xfc; *(p-0x24) = (*(p-0x24) & 0xf0) | 2`
  y devuelve `10`.
- Campos del lado (`0x02022250 + lado*0x2B08`): contador de mano = bits 7–13
  del u16 en `+0x1B`; contador de mazo = bits 6–12 del u16 en `+0x1C`.
- **Hipótesis [HIP] para The Inexperienced Spy:** en estado `0x80`, registrar la
  mano del rival (como Aoi) y abrir `init_effect_dialogue` (como Telescope),
  sin enviar nada al cementerio.
- `FUN_0805AEB0(lado, ID, 0)` (`0x0805AEB0`) es un despachador **por ID de
  carta** que llama a la función de candidatas. 160 de los 901 IDs tienen
  función propia (149 del juego, 11 recortadas); el resto cae en
  `FUN_08061382`. `datos/hojas_objetivo.csv`, generado con
  `scripts/hojas_objetivo.py` (Unicorn).
- **Descartado:** que el despachador explique los fallos. Reaver, Jowls,
  Windstorm y Ready for Intercepting funcionan y tampoco tienen función propia.

## Primera función propia: The Inexperienced Spy [PROBADO jugando]

- Fuente: `efectos/spy_mano.s`. Se ensambla con `arm-none-eabi-as`
  (`brew install arm-none-eabi-binutils`), no con keystone.
- Se engancha reemplazando `fn_04` de la fila 181 (ID 4848). Conserva la
  comprobación original (`ORIGINAL`) y solo en el estado `0x80` registra la mano
  del rival y abre `init_effect_dialogue`, ajustando los mismos tres bytes que
  Ancient Telescope. Devuelve `10`.
- Pruebas: `scripts/test_spy.py` (6 escenarios, pasan) y **jugada en mGBA el 2026-10-10: al activarla aparecen las cartas de la mano del rival.** El patrón (registrar candidatas + `init_effect_dialogue`) queda validado.
- Herramientas: `scripts/parche_efecto.py` (sobre un ROM ya generado) y la clave
  `efectos_nuevos` de las recetas (`restaurar.py`). El código nuevo va desde
  `0x1A00000` con la CLI y desde `0x1900000` con la receta.
- Error corregido: el byte de estado es `0x020204C6`, no `0x0201FEC6`.

## Seal of the Ancients (ID 5011): ya tiene la función completa [ROM] / [PROBADO jugando]

A diferencia de la Spy, **no le falta una función**: las tres de su fila existen.

- `fn_04` (`0x08041F04`): recorre las 11 zonas del rival; en cada carta que existe
  y no está boca arriba hace la animación de revelarla (`FUN_08022034`,
  `FUN_0800E6A0`, `FUN_0801AA64`) y la devuelve.
- `fn_10` (`0x08033DA8`): condición. Pide poder pagar 1000 LP
  (`FUN_08030280(lado, ranura, 1000)`) y que el rival tenga una carta boca abajo
  (`FUN_0800E874` existe, `FUN_0800E888` no está boca arriba).
- `fn_14` (`0x0802D6EC`): paga el costo. Cadena de comparaciones por ID que llama
  a `FUN_0801ABD0(lado, cantidad)`. **Para 5011 paga 1000 LP** (`scripts/test_seal.py`).
- **Jugada el 2026-10-10:** baja 1000 LP y muestra qué son las cartas boca abajo del rival (Nimble Momonga y Call of the Haunted, reconocidas), que quedan boca abajo. Se ven como destellos rápidos: el código no hace pausa ni abre diálogo.

## Reasoning (ID 5530) y Chosen One (ID 5101) [ROM] / [PROBADO jugando]

**Reasoning** necesita DOS piezas, más trabajo que la Spy:

- `fn_04` (`0x08046B80`): en `0x80` abre el modo 9 para el rival y devuelve
  `0x7F`; en `0x7F` **no hace nada**. Falta la resolución (revelar del mazo hasta
  un monstruo invocable, comparar con el nivel declarado, invocar o mandar al
  cementerio).
- El manejador del modo 9 (`FUN_0806A8D4`) es un **stub que devuelve 1** sin
  preguntar nada. El modo 10 (Reversal Quiz, `FUN_0806A8D8`) sí pregunta con
  `ask_multiple` (hasta 4 opciones): sirve de molde, pero un nivel 1–12 no entra
  en 4 opciones.
- `fn_10` (`0x08035244`): mazo no vacío, `effect_activation_gatekeeper` y al menos
  una zona de monstruo libre.
- Jugada: se activa, va al cementerio y no cambia nada (mazo, LP, campo).

**Chosen One** (verdicto corregido):

- `fn_10` (`0x08033FB0`) exige: una zona de monstruo libre, **1 monstruo invocable
  y al menos 2 Mágicas/Trampas en la mano** (sin contar la propia carta). Con una
  sola Mágica en la mano el menú no ofrece activarla: es la condición, no un fallo.
- Con una mano válida el menú **sí ofrece activarla**, pero al activarla la carta
  queda boca arriba en la zona de Mágicas sin pedir la selección: no se resuelve.
- `fn_04` (`0x08042404`) es una máquina de 9 estados (`0x78`–`0x80`) por tabla.
  Simulada con las funciones del motor en 0, desde `0x80` no devuelve nada: falta
  saber qué consulta primero.

**Riryoku**: con 2 monstruos propios se activa pero queda en el campo, sin pedir
elegir monstruos (mismo síntoma que Chosen One).

**Lecciones del corredor automático** (`scripts/probar_magicas.py`): un veredicto
solo vale si la preparación se comprobó (leyendo la RAM). Tras invocar, el juego
pregunta "You Summoned a monster. Activate...?" y hay que contestar No. El
corredor no sabe aún terminar el turno desde el campo.

## Chosen One (ID 5101): funciona [PROBADO jugando]

`efectos/chosen_one.s`; prueba de la rama de la IA en `scripts/test_chosen.py`. Texto de la carta:
"Select 1 Monster Card and 2 other cards from your hand. Your opponent picks 1 of them at
random. If it is the Monster Card, Special Summon it and send the other 2 to the Graveyard. If
not, send all 3 cards to the Graveyard."

**Lo que se descubrió** (la nota de arriba "falta `fn_18`" era cierta, pero no hacía falta
escribirla):

1. La `fn_04` original (`0x08042404`) ya trae el final: 0x7A sortea y muestra la carta (el
   índice elegido queda en `0x020204C8`, 0..2), 0x79 descarta las no elegidas con
   `FUN_080195A8(lado, POSICION EN LA MANO, 0, 0)` y 0x78 cierra. Le falta solo la selección.
   Espera en `p[9..11]` las **posiciones en la mano** (no ids de ranura) y en `p[8]` bajo = 3.
2. **Selección múltiple con la lista** (misma de Exchange, `init_effect_dialogue(0, 3, ...)`):
   el motor deja **tres u32 consecutivos desde `0x02019F24`**, cada uno con
   `(v & 0x7FFFF) >> 11` = id de ranura (0xFF = sin elegir), en orden de marcado. En pantalla:
   `A` sobre la carta → icono CHECK → `A`. Con 0 restantes aparece en el menú de iconos el de
   confirmar (la mano que apunta a una carta, 5º). La lista no incluye la propia carta.
3. **Mano propia como candidatas:** `FUN_0805AEB0(lado del RIVAL, 6440, 0)` registra la mano
   del lado opuesto; pasándole el lado contrario al propio sale la mano propia.
4. **Invocación especial desde la mano:** `record_monster_set(lado, id, 1, 0)` (`0x0806C7C4`)
   la pide; el juego sigue con "Select card position." (estado `0x0A`, como Monster Reborn).
   Mandar al cementerio: `FUN_08018518(lado, id, ranura de la carta)` (`0x08018518`), que
   limpia, envía y procesa en el acto.
5. **Trampa de los índices:** las posiciones de mano se corren al sacar una carta. Por eso
   la resolución propia (estado 0x79) convierte las posiciones a ids **antes** de mover nada
   y manda cada carta por id.
6. Tipo de carta en la ranura: `+0x30`, 5 bits bajos. `< 0x15` monstruo; Mágica/Trampa
   `0x15`..`0x16` (Salamandra, una Equip, es `0x16`).

**Estructura** (`chosen_one.s` reemplaza `fn_04` y delega en `ORIGINAL` solo el estado 0x7A):
`0x80` candidatas + aviso → `0x7F` lista de 3 → `0x7E` lee y valida (1 monstruo + 2 más; si
no vale, vuelve a `0x80`; cancelar con B = `0x64` sin efecto) y deja `p[9..11]` y `p[8]` →
`0x7A` (original: sorteo y animación) → `0x79` propio (descarta/invoca). IA: elige sola el
primer monstruo y las dos primeras Mágicas/Trampas de su mano.

Pendiente: que Oscar la mire; la rama de la IA solo se probó con Unicorn.

## El evento 0x4B y la lista de modificadores de ATK/DEF [ROM] / [PROBADO jugando]

Resuelto el 2026-10-10. Era lo que bloqueaba a Goddess of Whim y a Riryoku.

**Cola de eventos** (`0x020214E0`, ver arriba): `FUN_0801A5BC(lado, a1, a2, a3)` encola el evento
`0x4B` (bit 15 = lado). El consumidor es `FUN_08022124` (`switch` sobre `[cola] & 0xFFF`, tabla en
`0x08022154`); el caso `0x4B` llama a **`FUN_0800E9B8(lado, a3, a1, a2)`**, que **agrega un
modificador a la lista del monstruo destino** `a2`:

| Campo de la ranura | Qué es |
|---|---|
| `+0x3E` (nibble bajo) | cuenta de entradas (máx. 15) |
| `+0x40 + 2*i` (u16) | entrada: byte alto = tipo (`a3 & 0xFF`; nibble bajo = tipo 1..15, nibble alto = parámetro), byte bajo = ranura de la carta **origen** `a1` |
| `+0x3C`, `+0x3D` | último destino / tipo registrados (los usa el evento 0x4C, que quita un modificador) |

Entonces `FUN_0801A5BC(lado, ranura propia, ranura objetivo, tipo)`. Rush Recklessly (original) usa
`tipo = 4`.

**Calculador** (`FUN_08012460(ranura, &salida, mascara)`, salida: `+4` = ATK, `+8` = DEF; `mascara`
bit 0 = ATK, bit 1 = DEF): recorre la lista y despacha por tipo con una tabla de saltos en
`0x08012C58` (tipo `k` en `0x08012C58 + 4*(k-1)`). Tipos 5, 6 y 8 están vacíos. El tipo 4
(`0x08013B4C`) es un árbol de IDs de la carta origen (Rush Recklessly +700, etc.). **El motor
borra los tipos de "hasta el fin del turno" al terminar el turno** (medido: la cuenta pasa a 0 al
cerrar mi turno con Rush Recklessly), y el ATK que se muestra en `+0x28` sale de este cálculo: por
eso escribir `+0x28` a mano se revertía.

**Goddess of Whim**: su `fn_04` original llamaba a `FUN_0801A5BC` con `(lado, índice de carta,
ranura, (cara/cruz << 8) | 4)`, un formato anterior del evento. Ahora `efectos/goddess_whim.s`
sortea la moneda, avisa, y en el estado 0x7D llama a
`FUN_0801A5BC(lado, ranura, ranura, (1 o 2) << 4 | 4)`; `efectos/modificador_atk.s` reemplaza la
entrada del tipo 4 de la tabla (`T:08012C64:08013B4C`) con un envoltorio que, si la carta origen
es Goddess (ID 4435), multiplica ×2 (nibble 1) o divide ÷2 (nibble 2) y, si no, sigue al original.
Quedó probada en el juego: el ATK se mantiene el turno entero, vuelve a 950 al terminar el
turno y el efecto se puede usar de nuevo el turno siguiente (bit 14 de `+0x60`).

Además hubo que arreglar el menú de campo: `efectos/gancho_lista_campo.s` (`FUN_08015C78`: lista
de IDs de efectos de campo "una vez por turno") y `efectos/gancho_menu_campo.s` (`FUN_08079200`:
`switch` por ID que decide si el monstruo ofrece "Activate Effect"). Ambos con
`parche_efecto.py ... G:DIRECCION:archivo.s`; la entrada de tabla con
`T:DIRECCION:VALOR_ORIGINAL:archivo.s`; unos bytes sueltos con
`B:DIRECCION:BYTES_ORIGINALES:BYTES_NUEVOS` (2026-10-11).

## Riryoku (ID 5009): funciona [PROBADO jugando]

`efectos/riryoku.s` + el caso de Riryoku en `efectos/modificador_atk.s`; prueba con Unicorn
`scripts/test_modificadores.py` (usa `datos/volcado_goddess.*`, un volcado de RAM del duelo).

- El `fn_04` original (formato viejo del evento 0x4B) pasaba como "origen" la **cantidad** a
  restar (se truncaba a 8 bits) y leía `p[9]`, `p[10]` como (lado, zona). El motor actual
  espera modificadores en la lista de cada monstruo: el tipo 9 de la tabla no sirve (suma el id
  de la ranura origen).
- Ahora registra **dos modificadores tipo 4** con origen = la ranura de Riryoku (su ID, 5009, es lo
  que reconoce el calculador) y en el nibble alto la posición `(lado << 3) | zona` del monstruo que
  pierde. En el calculador (envoltorio del tipo 4): si la ranura que se calcula es la del que
  pierde, ATK / 2; si no, se le suma el ATK ya reducido del primero (llamando de nuevo a
  `FUN_08012460`, que vuelve a pasar por el primer caso; no hay ciclo).
- Probado en el juego: Needle Worm 750 → 375 y Blazing Inpachi 1850 → 2225; Riryoku va al
  cementerio. Como son modificadores de tipo 4, el motor los borra al terminar el turno (igual que
  Rush Recklessly y Goddess). El orden de elección es el de `fn_18`: primero el que pierde.
- Orden de teclas con el corredor: Activate Effect (UP, UP, A) → A cierra el aviso → A elige el
  primer monstruo → A cierra el 2.º aviso → LEFT/RIGHT al otro monstruo → A. Solo se puede
  invocar un monstruo por turno: para tener dos hay que pasar un turno.
- No probada: que la active la IA, ni un tributo/destrucción de alguno de los dos monstruos con el
  modificador activo (en ese caso la posición de la zona guardada en el nibble podría apuntar a
  otra ranura).

## Share the Pain (ID 4889): funciona si la activa el jugador [PROBADO jugando]

`efectos/share_the_pain.s`; prueba con Unicorn `scripts/test_share.py`; estado
`estados/duelo-share.st` (Share the Pain en la posición 5 de la mano).

Dos fallos, uno por cada parte del texto:

1. **Comprobación previa invertida.** El `fn_04` original llama a
   `FUN_08010FA4(rival, 0xFF, 3, ranura)`, que devuelve **cuántos monstruos del rival se pueden
   tributar**, y abandona si el resultado es **distinto de 0**: con monstruos rivales nunca
   hacía nada. Medido en el juego con un gancho (resultado 1 con un Nimble Momonga rival).
2. **El menú de modo 8 no elige nada para la IA.** Aunque pasara la comprobación, el original
   abre el menú "elegir monstruo a tributar" para el lado del rival; si es la IA, nadie lo
   contesta. La función propia, cuando la activa el jugador (lado 0), elige el monstruo del
   rival de **menor ATK** entre sus 5 zonas (`+0x5610 + 11*lado`) y lo manda al cementerio con
   `FUN_08018518(0, id, ranura propia)`.

El coste (tributo propio) ya funcionaba: lo resuelve `fn_14` (`0x0802D338`, compartida con
Catapult Turtle, Cannon Soldier...). Cuando la activa la IA (lado 1) se delega en el original,
cuyo menú de modo 8 sí funciona para el humano; **esa rama no está probada**.

## Kunai with Chain (ID 4657): funciona [PROBADO jugando]

`efectos/kunai_cadena.s` (fn_04), `efectos/kunai_condicion.s` (fn_10), `scripts/test_kunai.py`
(6 escenarios con Unicorn) y, en el juego, `scripts/probar_trampas.py`.

**Causa:** el código recortado lee al atacante como `(lado = p[4], posición de campo = p[5])`,
pero el motor deja en `p[4]` el **id de ranura** del atacante (bit 7 = lado), igual que
Sakuretsu Armor / Mirror Force (originales). Medido en el juego registrando `fn_10`: la
solicitud llega con tipo `0x10` (`(p >> 13) & 0x3F`, ataque declarado) y `[p+4] = 0x00FF009A`
(`0x9A` = ranura 26 del rival). El efecto de posición usa `FUN_0801A36C(lado, id, 0, 0)`, la
misma llamada que Block Attack. Las dos funciones nuevas usan el id de ranura.

**Prueba en el juego** (corredor de trampas, ver abajo): colocada boca abajo, el rival declara
el ataque con Des Wombat, el aviso aparece, se activa y la posición del atacante pasa de `0x10`
(ataque) a `0x30` (defensa). Mirror Force original, mismo escenario, destruye al atacante.

Solo implementa el primer efecto (cambio de posición); el equipamiento de +500 ATK no está
(ahora que existe la lista de modificadores se podría, ver "El evento 0x4B...").

## Trampas: la ventana de respuesta y cómo manejarla desde el corredor [PROBADO jugando]

Resuelto el 2026-10-10 (hacía falta para probar cualquier trampa; antes el corredor nunca
conseguía que el juego ofreciera una).

- **Solicitud de respuesta:** el motor guarda la última en `0x0202048C` (misma forma que `p`):
  tipo en los bits 13-18 (`0x10` = ataque declarado) y `[+4]` = id de ranura del atacante.
  `Duelo.tipo_evento()` la lee.
- **Aviso:** unos 100 cuadros después aparece "Your opponent declared an attack. Activate the
  effect of Spell/Trap/Effect Monster? Yes / No" y el duelo **espera sin límite**. No hay que
  apurarse; A = Yes (el cursor arranca en Yes; UP lo pasa a No).
- **Selección:** tras Yes sale "Select Spell/Trap Card to activate." (A para cerrarlo) y aparece
  una mano-cursor sobre el atacante. Las teclas la mueven por el campo; los datos del cursor de
  `0x02028188` y `0x02019F0C` **no** la siguen. Desde esa posición: `DOWN, DOWN` lleva al borde
  derecho de mi fila de magias/trampas y de ahí `LEFT` hasta la zona (zona 0 = cuatro `LEFT`;
  la zona sale de la lista `0x02022250 + 0x5610 + 5 + z`). `A` abre el menú de la carta
  (Activate Effect / Detail Screen, queda en Detail): `UP`, `A`.
- **Por qué antes fallaba:** el corredor pulsaba A cada tanto; el primer A contestaba Yes y
  los siguientes caían sobre el atacante sin efecto, o B cancelaba. Tampoco se veía bien porque
  la IA **no ataca si tengo monstruos y una trampa colocada** (sí ataca directo con el campo
  vacío, a partir de su 3.er turno).
- Implementado en `scripts/duelo_auto.py` (`tipo_evento`, `esperar_evento`,
  `responder_con_trampa`, `zona_magia`) y usado por `scripts/probar_trampas.py`.

### Trampas que se activan en mi propio turno (Acid Trap Hole, Two-Pronged Attack)

Mismo corredor (`correr_turno_propio` en `scripts/probar_trampas.py`): colocarla, pasar turnos
hasta que se dé la condición, y en mi fase principal:

- **Cursor sobre la carta:** en la fila de magias/trampas el cursor recorre `x = 1..7` y las
  cinco zonas están en `x = 2 + zona` (`Duelo.mover(y=1)` y luego `mover(x=...)`). El nombre de
  la carta bajo el cursor (`0x02019F0C`) **no** se actualiza en este modo: no usarlo.
- `A` abre el menú (Activate Effect / Detail Screen, queda en Detail): `UP`, `A`.
- **Acid Trap Hole:** aviso "Select 1 face-down Defense Position monster to destroy." y
  `A A A A A A` bastan (el cursor ya cae sobre el objetivo). Funciona: el monstruo boca abajo
  (Nimble Momonga) va al cementerio rival.
- **Two-Pronged Attack:** avisos "Select your 1st monster." / "2nd monster." / "Select
  opponent's monster to destroy."; teclas `A A A RIGHT A A UP A A A A`. Se activa y va al
  cementerio, **pero no destruye nada**: el `fn_04` original solo validaba las tres elecciones
  (leyendo `p[9..11]` como lado/zona, formato viejo) y recorría un bucle vacío; nunca destruía.
  Arreglada con `efectos/two_pronged_attack.s`: con `p[8] & 0xF = 3` comprueba que las dos primeras
  sean propias y distintas y la tercera del rival, y las manda al cementerio con
  `FUN_08018518`. Probada: los tres monstruos van al cementerio.
- Un monstruo por turno: para tener dos hay que dejar pasar un turno (`un_monstruo_por_turno`).

### Trampas que responden a una Mágica del rival (Magic Drain...) [PROBADO jugando]

Resuelto el 2026-10-10: **Magic Drain funciona sin tocar nada** (fn_10 y fn_04 originales, ROM
`Test`). El diagnóstico anterior ("el juego no genera ventana") era un error del corredor.

- La IA de `duelo-inicio` juega **Dian Keto the Cure Master** en su 2.º turno (~800 cuadros
  después de terminar el mío, con una A cada 90 cuadros para los diálogos).
- El juego pregunta **"Dian Keto the Cure Master has activated. Will you chain? Yes / No"** y
  espera sin límite. Esa solicitud **no** pasa por `0x0202048C` (la del ataque declarado): el
  motor llama a `fn_10(p_propia, evento)` con **dos** argumentos, y el evento es la estructura
  de `0x020204A4`, cuyo primer u16 es `(id de ranura de la carta activada << 1) | ...`
  (medido `0x033F` = ranura 31 del rival). `fn_10` de Magic Drain solo comprueba que esa carta
  sea de tipo Mágica y que no sea el ID 0x147E (carta fuera de las 1200).
- Las fn_10 de dos argumentos (empiezan con `cmp r1,#0`): Magic Drain, Seven Tools of the
  Bandit, Anti-Spell y la carta id5264. Riryoku Field y Mystical Refpanel usan la misma firma.
- Medido con un envoltorio de diagnóstico sobre fn_10 (contador en `0x0203F100`, anillo en
  `0x0203F110`): 3 llamadas previas con r0 = puntero de pila y r1 = 0, y la 4.ª con
  r1 = `0x020204A4`. Hay RAM libre en `0x0203F100`.
- Secuencia de botones: A (Yes), A ("Select Spell/Trap Card to activate."), DOWN, DOWN, LEFT
  x(4-zona), A (menú), UP, A. Resultado: cadena "BLOCK 1 Opponent Dian Keto / BLOCK 2 You Magic
  Drain", resuelve con *Destroy Negate*: Dian Keto va al cementerio del rival sin curar
  (LP 8000 → 8000) y Magic Drain al mío. La IA no tenía otra Mágica que descartar.
- Corredor: `scripts/probar_cadena.py ROM [NOMBRE]` (detecta que la IA deja una carta nueva en
  su fila de magias/trampas, espera, y usa `responder_con_trampa`).
- Flags de la fila (`+0x08`): son una **máscara de tipos de evento**, bit N = responde al tipo N
  (Mirror Force `0x10000` = tipo 0x10 ataque; Sebek's Blessing `0x100000` = 0x14 daño; Trap
  Hole `0xC0`; Michizure `0x4000`). `0xFFFFFFFF` (813 filas) = sin restricción. La rutina
  `FUN_0800F6E0` (flags de la ranura, `+0x70`) fuerza bits según una lista de IDs escrita en el
  código (0x13A7 Injection Fairy Lily, 0x1524 Sasuke Samurai) y `FUN_0800F7D8` otra.
- **Riryoku Field y Mystical Refpanel: funcionan** sin tocar (originales). Riryoku Field: con
  `estados/duelo-equipo.ss1` (mano rival con Black Pendant) niega y destruye el equipo.
  Refpanel: contra Dian Keto redirige la curación (LP 9000 / 8000). `ESTADO_BASE=` cambia el
  estado inicial de `probar_trampas.py` / `probar_cadena.py`.
- **Pendiente: Big Burn** (necesita una Mágica rival que apunte al cementerio, p. ej. Monster
  Reborn con un monstruo ya muerto; no se da en el 2.º turno de `duelo-inicio`).
- Tipos de evento medidos en el turno del rival: `0x01` inicio, `0x02` fin, `0x03` invocación,
  `0x04` cambio de fase, `0x05`, `0x0A` (arg = id de ranura), `0x10` ataque declarado, `0x11`
  siguiente paso del ataque, `0x14` daño.

## Selección de objetivos: cómo corre una carta con `fn_18` (Riryoku) [ROM] / [PROBADO jugando]

- Tres despachadores leen una columna de la fila cada uno y guardan el puntero en
  RAM: `FUN_08066088` (`fn_14`), `FUN_08066194` (`fn_18`, lo guarda en
  `0x020204E0`) y `FUN_0806629C` (`fn_04`). Se puede observar desde afuera: al
  activar Riryoku aparece `5D 42 05 08` en `0x020204E0` (= `0x0805425D`).
- El **contador de pasos** de la selección está en los bits 10–17 de la palabra de
  `0x020204C0`; avanza 0 → 1 → 2 → 3.
- `fn_18` es una máquina de pasos: muestra el aviso (`ask_question`, texto por ID),
  espera `A` sobre un objetivo válido y graba la elección en la carta (`p[9]`,
  `p[10]`) con `FUN_08051680`. `fn_04` se ejecuta cuando `p[8] & 0xF` llega a la
  cantidad de elegidos y aplica el efecto.
- **Riryoku** (`fn_18` `0x0805425C`): avisos "Select monster to halve its ATK." y
  "Select monster to increase ATK." (existen en el ROM). Con la entrada correcta
  (cerrar el aviso con `A`, elegir, cerrar el 2º aviso, mover el cursor al otro
  monstruo, elegir) **resuelve y va al cementerio, pero ninguna ranura de monstruo
  cambia** (comparación byte a byte de las 0x50 de cada una). `fn_04`
  (`0x08041E84`) termina con `FUN_080159E0(p[9], 0)` y encola un evento `0x4B` de
  tipo 9 (`FUN_0801A5BC`). [HIP] falta el manejo de ese tipo de evento o de
  `FUN_080159E0`; no está comprobado.
- **Chosen One** no tiene `fn_18`: la selección no existe. Se resolvió sin ella, con la lista
  de selección múltiple (ver "Chosen One (ID 5101): funciona").
- Corrección del corredor (`probar_magicas.py`): las cartas que piden elegir
  objetivos necesitan entrada guiada; con `A` repetida el veredicto "queda sin
  resolver" era un artefacto del corredor, no de la carta.

### Riryoku: el cambio se aplica y el motor lo revierte [PROBADO jugando]

Medido cuadro a cuadro con el núcleo automático (ROM `(Efectos)`):

- `fn_04` se llama **una vez**, tras la 2ª elección, con `p[8]=2`, `p[9]` y `p[10]` =
  las ranuras elegidas (`0x08`, `0x20`). Los supuestos de la función eran correctos.
- Una escritura directa del ATK en `ranura+0x28` **persiste** si el motor no hace
  nada (se comprobó 120 cuadros), pero tras resolver la cadena el motor la
  **restaura a la base 4 cuadros después** (cuadro 92 aplica, cuadro 96 revierte).
- El motor también devuelve el ATK a la base **al cambiar de turno**: "hasta el fin
  del turno" no necesita registro propio, pero sí hace falta sobrevivir al
  recálculo posterior a la cadena.
- Graceful Dice (original, permanente) deja `+0x3E = 1` y `+0x40..41 = 26 14`
  además de cambiar `+0x28` y `+0x2C`. En `FUN_080188AC` cada entrada se decodifica
  como `kind = entrada >> 8`, `ranura = entrada & 0xFF`: son **cartas asociadas a
  la ranura** (equipos, efectos), no cantidades. El cuenta está en el nibble bajo
  de `+0x3E`.
- El tipo de evento 9 que encola la `fn_04` original **solo lo usa Riryoku**; las
  originales usan 4, 6, 10, 13 y 15. [HIP] ese tipo no tiene manejador.
- Pendiente: qué `kind` representa "ATK propio modificado" y qué rutina recalcula
  el ATK desde la base (no es `FUN_08072378` ni `FUN_08003B5C`).

## Exchange (ID 5218): funciona [PROBADO jugando]

`efectos/exchange.s`, ensamblada con binutils. **Lo aprendido, que sirve a cualquier carta
que pida elegir de una lista:**

1. **El motor llama a `fn_04` con el estado que ella misma devolvió.** Tras `ask_question`
   hay que devolver un estado EXPLÍCITO (`0x7F`); si se devuelve lo que deja la función de
   la pregunta, el motor vuelve con un estado cualquiera (`0x4D`, `0x51`...). Se vio
   registrando Painful Choice (original): `0x80` pregunta → `0x7F` abre la lista →
   `0x7E` resuelve.
2. **Candidatas:** `FUN_0805AEB0(lado, ID, 0)` registra los candidatos *y* prepara la
   solicitud que consume el aviso. Pasándole **el ID de Aoi (6440)** registra la mano del
   rival. Con registros manuales (`REGISTRAR`) el aviso no aparece.
3. **Lista:** `init_effect_dialogue(0, n, 0x02019F24, 1)` más los tres ajustes de Telescope;
   `n` es **cuántas cartas elegir**. Con `n = 1` el menú de la carta trae un icono de
   **elegir** (la mano que apunta a una carta, 4º desde la izquierda); con `n > 1` trae
   CHECK y hay que marcar `n` cartas.
4. **Carta elegida:** `(u32 en 0x02019F24 & 0x7FFFF) >> 11` = id de ranura (bit 7 = lado).
5. **Mover una carta entre manos:** intercambiar las 0x50 bytes de las dos ranuras e
   invertir el bit de dueño (bit 19 del `u32` en `+0x30` = bit 3 de `+0x32`). Las listas de
   mano apuntan a ranuras y no se tocan.
6. **Azar:** `FUN_080E5740()`.
7. **Cierre:** `0x64` lo devuelven 27 cartas originales como estado final.

Rama de la IA (lado 1 activando): al azar en las dos manos, sin diálogo.
Pruebas: `scripts/test_exchange.py` (Unicorn), y el juego con `probar_magicas.py`.

## Qué sigue

Esta lista es la del 2026-10-09; el plan vigente está en `PLAN.md`, §4.

1. Probar las 18 candidatas que faltan (`PRUEBAS.md`).
2. ~~Escribir la posesión de Dark Necrofear~~ Hecha el 2026-10-11; ver
   "Bagworm −500 y la posesión de Dark Necrofear".
3. Buscar las tablas de datos que les faltan a las que fallan a medias, como
   se hizo con la de invocación.
4. Traer el dibujo de cada carta restaurada desde un PNG de 80×80.
5. Identificar qué mazo es de quién y de dónde salen las cartas que se suman.

## Fuentes

- [coolstuffinc/yugiohgx-da](https://github.com/coolstuffinc/yugiohgx-da): offsets base, nombres de funciones, formato de arte y contraseñas.
- [CosmicScribe64/eds-decomp](https://github.com/CosmicScribe64/eds-decomp): estructura de la tabla de efectos en el motor anterior.
- [DawnbrandBots/yaml-yugi](https://github.com/DawnbrandBots/yaml-yugi): ID de Konami a nombre, estadísticas y contraseña.

## Monstruos de volteo: corredor y primer caso (Electromagnetic Bagworm) [PROBADO jugando]

- `scripts/probar_volteo.py ROM NOMBRE` (con `ESTADO_BASE=estados/duelo-bagworm.ss1`): coloca el
  monstruo con `menu(1)` (Set), termina el turno y deja que el rival ataque; imprime zonas y
  estado (`+0x33`: 0x20 boca abajo, 0x30 cara arriba en defensa, 0x10 ataque).
- El estado `duelo-bagworm.ss1` cambia Needle Worm por Bagworm (mano propia, pos. 1) y toda la
  mano rival por Máquinas (`b30` bajo 5 bits = tipo 7). Hay que cambiar también el tipo en
  `+0x30` al cambiar de carta o la IA no la trata como esperas.
- La IA ataca al monstruo boca abajo con su Máquina (~1190 cuadros tras terminar mi turno). Se
  voltea (carta grande en pantalla) y sale el aviso de selección; después el cursor queda sobre la
  Máquina rival y las A siguientes no la eligen. **Cuidado**: mi corredor pulsaba A cada 90
  cuadros y respondía el aviso sin querer; para observar hay que dejar de pulsar.
- Bagworm queda con nibble de zona `1` (no es cementerio `d`) y ya no aparece en mi campo.
- **Causa real (resuelto):** la `fn_18` de Bagworm (0x0805436C) era una máquina de pasos
  recortada: el paso 0 buscaba la Máquina y avisaba, pero el paso siguiente solo detectaba A/B y
  devolvía 0 sin llamar a `FUN_08051680` (grabar la elección), a diferencia de la `fn_18` vecina
  0x0805446C. Además su `fn_04` usaba el formato viejo (p[9] = lado, zona fija 0).
- Arreglo: `efectos/bagworm_seleccion.s` (paso 0 = la original; luego B cancela y A graba el id
  bajo el cursor, byte `0x02022250 + 0x5668`, con `FUN_08051680(p, id)`) y
  `efectos/bagworm_control.s` (como Jowls: `FUN_0801A8A4(id, 0)` hace el traspaso de zona y
  `FUN_0801A5BC(lado, ranura propia, id, 4)` registra el efecto). Se enganchan con
  `parche_efecto.py ORIG BASE SALIDA 5040:fn_18:efectos/bagworm_seleccion.s 5040:fn_04:efectos/bagworm_control.s`.
- **El contador de pasos de la selección está en la palabra `0x020204C0`** (bits 10-17); se
  leyó mal dos veces (0x0201FD00 + 0x7C0 = 0x020204C0, no 0x0201FEC0).
- **Control = listas de zonas, no el bloque de memoria.** Un monstruo robado sigue en el bloque
  de su dueño (`J1 + n*0x50`) pero su id pasa a la lista `LISTA_ZONAS` del que lo controla y el
  bit 3 de `+0x32` se apaga. `Duelo.cartas()` / `zona()` agrupan por dueño: usar las listas
  (`probar_volteo.campo`) para saber quién controla.
- Resultado en el juego: la Máquina pasa a mi lista de zonas y Bagworm va al cementerio unos 40
  cuadros después (la batalla se resuelve igual). El modificador de -500 ATK/DEF de la Máquina
  que la destruye no se vio (ATK sigue 1850, 1 entrada en la lista de modificadores): pendiente.

## Cierre del lote de 30: cómo se provocó cada disparador (2026-10-10)

Feature `specs/001-cerrar-pruebas-lote`. Corredor: `scripts/probar_lote.py`; escenarios con
`scripts/escenario.py`; resultados en `datos/pruebas.csv`.

**El ROM `(Efectos)` de `build/` no traía las funciones de Bagworm** [ROM]. Se escribieron
después de armarlo. `(Efectos)` se reproduce byte a byte (mismo MD5) aplicando al `(Test)`,
en este orden, lo que lista `scripts/construir_lote.sh`; ese script arma además el ROM
`(Lote)` = `(Efectos)` + Bagworm (MD5 `dbbbab32ccc659ae077cf12fcf4c15c6`).

**Edición del estado de un duelo** [PROBADO]:

- Ranura de carta: `+0x24` índice, `+0x28` ATK, `+0x2C` DEF, `+0x30` atributo y tipo, y el
  **nibble bajo de `+0x31` es el nivel**. Escribir ahí un 4 deja colocar sin tributo un
  monstruo de nivel 5 (Reaper of the Cards).
- **El mazo también se edita**: lista de ranuras en `lado+0x28A4`, y **la primera entrada es
  la próxima carta que se roba**. Vale para los dos lados.
- Contadores por lado en `lado+0x1B`, u64 de a 7 bits: total, mano, mazo, cementerio.
- El motor recalcula ATK y DEF cada pocos cuadros y al voltear: una escritura suelta dura
  menos de 60 cuadros. Para sostener un valor hay que reescribirlo en cada cuadro.
- La posición (`+0x33`) escrita a mano sí persiste y la IA la toma en cuenta.

**Comportamiento de la IA** [PROBADO]:

- **Mira la DEF del monstruo boca abajo**: lo ataca solo si su ATK la supera. Con ATK apenas
  menor (1350 contra 1400) ataca algunas veces y otras no.
- Juega Card Destruction y Delinquent Duo en cuanto los tiene. **No juega Confiscation.**
- Juega Monster Reborn si hay un monstruo en algún cementerio.
- Coloca Magic Jammer en su primer turno y la usa contra la primera Mágica que activo.
- Con un monstruo propio más débil que el mío lo coloca boca abajo en defensa.
- Mano de relleno: Blue-Eyes White Dragon. No puede jugarlo, así que su turno es corto.

**Manejo del juego** [PROBADO]:

- Battle Phase: `B` abre "Will you end the Main Phase?" (*Enter Battle Phase* arriba), `A`.
  En la Battle Phase, `A` sobre mi monstruo → *Attack / Detail Screen* (queda en Detail):
  `UP`, `A`, `A` (cierra "Select your opponent's monster to attack."), `A`. Después `B` →
  *Go to Main Phase 2*.
- Encadenar a una Mágica del rival ("Will you chain?"): tras *Yes* y el aviso, **el cursor
  arranca en mi mano**, no sobre un atacante: `UP` lleva a la zona 4 de mi fila de trampas y
  de ahí `LEFT` × (4 − zona). El recorrido `DOWN, DOWN` de `responder_con_trampa` solo sirve
  cuando hay un ataque declarado.
- Lista "Select card" (descarte de Delinquent Duo): `A` sobre *ALL*, `A` sobre la carta,
  `RIGHT` × 3 hasta *DECIDE*, `A`.
- Avisos de volteo: aparecen unos 450 a 700 cuadros después de que la carta se da vuelta y
  esperan sin límite. Tras cerrarlos el cursor queda sobre el atacante; `UP` sube a la fila
  de magias y trampas del rival.
- **Dos emuladores en el mismo proceso no dan el mismo azar**: el núcleo guarda estado
  global. Las corridas repetidas no son idénticas aunque partan del mismo estado.

**Resultados** [PROBADO]:

- Funcionan: Dark-Eyes Illusionist (el objetivo no ataca; pasada de control borrando el
  modificador tipo 3), Reaper of the Cards, Big Burn.
- En parte: Electromagnetic Bagworm. El control es permanente (en la prueba anterior "volvía"
  porque el rival robaba Snatch Steal) y la Máquina no pierde 500.
- No funcionan Electric Snake, Minar y Penguin Knight: sus `fn_04` nunca se ven actuar. Las
  tres tienen solo `fn_04` y direcciones vecinas (`0x08039301`, `0x08039321`, `0x0803A48D`).
  [HIP] El motor no llama a nadie en "enviada al cementerio por efecto del rival": ninguna de
  las 1200 cartas del juego usa ese disparador.
- No funcionan Lady Panther ni Fairy Guardian: el menú del monstruo no trae *Activate Effect*.
  [HIP] Mismo síntoma que Goddess of Whim antes de `efectos/gancho_lista_campo.s` y
  `gancho_menu_campo.s`: falta su ID en la lista de efectos de campo.

## Revisión por capturas del 2026-10-11: tres defectos y una carta destrabada

Las 29 filas de la guía se jugaron de a pasos con `scripts/paso.py` (subagentes mirando capturas y
leyendo la memoria). Lo que salió:

- **The Inexperienced Spy: la lista no se cerraba [PROBADO].** `efectos/spy_mano.s` devolvía el
  resultado de la función original (`0x80`) en cualquier estado que no fuera `0x80`. Al cerrar la
  lista el motor llamaba otra vez, recibía `0x80`, volvía a entrar y la reabría. Ancient Telescope
  (`0x0803E458`), la original equivalente, devuelve `0` fuera de `0x80`, y con ella `B` y el icono
  *EXIT* cierran la lista. Arreglo: mirar el estado primero y devolver `0`. `test_spy.py` tenía el
  `0x80` como resultado esperado: una prueba que copia el código no detecta el error.
- **Chosen One: el monstruo no salía nunca [PROBADO].** El estado `0x7A` original
  (`0x080424CE`) hace `r = azar() % 3` hasta que `r != [0x020204C8]` (el "anterior"), lo guarda, y
  si el contador `[0x020204C7]` no es 0 lo decrementa y muestra la carta (una ruleta); con el
  contador en 0 esa es la elegida. La pieza nueva no inicializaba nada: anterior = 0 y contador = 0,
  o sea un solo tiro que nunca puede ser 0, y el monstruo es el índice 0. En 22 corridas salieron
  solo 1 y 2. Arreglo: contador = 0 y anterior = `0xFF` antes de pasar a `0x7A`. Después, en 24
  corridas: 10, 7 y 7.
- **Goddess of Whim: dos monedas [PROBADO].** El menú "Select heads or tails" (modo `0x15`) tira la
  moneda, muestra "Correct!" o "Miss!" y deja en `0x02022250 + 0x5656` **si acertó** (1) o no (0).
  La pieza nueva lo leía como "lo que llamó el jugador" y tiraba otra moneda con `AZAR`: el cartel y
  el efecto coincidían la mitad de las veces. Medido en 8 corridas: el byte coincide con el cartel
  las 8. Arreglo: usar ese byte.
- **Lady Panther funciona [PROBADO jugando].** Sus tres funciones existen; solo faltaba su ID (5193)
  en las listas de `gancho_lista_campo.s` y `gancho_menu_campo.s`. Condición (`fn_10`,
  `0x080343F4`): candidatas del ID 5109 (Return of the Doomed), que son los monstruos de mi
  cementerio con el bit 5 de `ranura+0x60` (destruidos en batalla este turno). Tras tributarse pide
  "Select monster to return to the Deck." con la lista "Your Graveyard".
- **Fairy Guardian sigue sin funcionar [PROBADO].** Misma forma que Lady Panther, pero sus
  candidatas (`0x0805D240`) piden una Mágica de mi cementerio con el **bit 6** de `ranura+0x60`.
  Cuando Magic Jammer niega y destruye mi Mágica ese bit queda en 0 (`+0x60 = 0`, `+0x64 = 2`).
  Ninguna llamada a `FUN_0800E0E0` (poner bandera) usa el 5 ni el 6 con valor constante: se ponen
  por otro camino, sin ubicar. Con el bit escrito a mano y el ID en las listas, el menú ofrece el
  efecto, se tributa y pide la Mágica, pero la Mágica no vuelve al mazo (una corrida). [HIP] La
  resolución (`fn_04`, `0x08043904`) tampoco está completa.
- **Banderas de `ranura+0x60`:** `FUN_0800E09C(lado, ranura, n)` lee el bit `n`; `FUN_0800E0E0` lo
  pone. Usos con valor constante en el ROM: lee 3, 4, 5, 6, 10, 11, 12, 14, 24, 25, 29, 31; pone 1,
  2, 3, 8, 10, 12, 14, 15, 16, 31.
- **Preguntas por fase:** con una Trampa colocada que se puede activar, el juego pregunta "It's the
  Draw Phase / Standby Phase... Activate the effect of Spell/Trap/Effect Monster?" en cada fase de
  los dos jugadores y cuando el rival invoca o coloca. El tipo de evento (`0x0202048C`) pasa por
  1, 2, 3, 5... Dos subagentes lo tomaron por un cuelgue.
- **Listas:** `A` sobre *ALL* entra; `A` sobre una carta abre los iconos. Para elegir una: 4.º
  icono. Para elegir varias: el 1.º es *CHECK* y con 0 restantes aparece un 5.º que confirma. En una
  lista de solo mirar el 4.º es *EXIT* y `B` cierra.
- **La IA y los monstruos boca abajo:** con un monstruo mío boca abajo, a veces invoca en ataque y
  ataca, a veces coloca boca abajo; depende del azar, y el azar de los cuadros transcurridos. Una
  espera distinta antes de terminar el turno cambia la jugada.
- **Magic Drain:** con 2 Mágicas en la mano, la IA no descartó para negarla (1 corrida). **Windstorm
  of Etaqua:** con dos monstruos rivales boca arriba cambian los dos.


## Completar y arreglar el lote (2026-10-11, tarde)

Ocho cartas cambiaron de estado en una tanda: Hiro's Shadow Scout, Kunai with Chain, Electromagnetic
Bagworm (duración del control), Electric Snake, Minar, Penguin Knight, Fairy Guardian y Reasoning.
Piezas en `efectos/`, orden de armado en `scripts/construir_lote.sh`, pruebas de lógica en
`scripts/test_hiro.py`, `test_kunai.py`, `test_bagworm.py`, `test_enviada_por_rival.py` y
`test_reasoning.py`, casos en duelo en `scripts/probar_lote.py`.

**Hiro's Shadow Scout** [PROBADO]. Su `fn_04` (`0x0803B6E4`) procesa una carta por llamada (contador
en `0x020204C7`) pero devuelve siempre 0, así que el motor no la volvía a llamar; además indexa el
mazo con `r7`, que nadie inicializa. `efectos/hiro_scout.s` la llama con `r7 = 0` y devuelve `0x7F`
mientras queden cartas. `FUN_08018570(lado, ranura, causante)` = del mazo a la mano (también Cyber Jar).

**Equipar una Trampa (Kunai with Chain)** [PROBADO]. Molde: Metalmorph (`0x0803991C`).

- `FUN_0801A600(lado, ranura del equipo, ranura del monstruo)` equipa. Pide el equipo boca arriba en
  la zona 5 y el monstruo boca arriba en la zona 0.
- El +500 **ya estaba** en el calculador: los tipos 1 y 2 de la lista de modificadores (`0x08012C94`)
  son equipos y se resuelven por ID de la carta origen (Metalmorph `0x1238` +300, Kunai `0x1231`
  +500). También `FUN_080296D0` (la `fn_0C` de los equipos: objetivo válido) y `FUN_0800DB44`
  contemplan a Kunai. Lo único recortado era la llamada que equipa.
- `FUN_080236C4(p)` = "esta carta ya activada (bandera `0x20`) va al cementerio": devuelve 1, salvo
  Mágicas de Equipo, Continuas y de Campo y una lista de IDs escrita en el código (`0x0FEE`, `0x1102`,
  `0x1238`, `0x13EA`, `0x1400`, `0x149B`, `0x1809`), para las que devuelve el bit 4 de `p[2]`.
  `efectos/gancho_queda_campo.s` agrega a Kunai cuando se equipó (`p[8] & 0xF != 0`).
- La `fn_10` original dejaba activarla también con un monstruo propio boca arriba
  (`FUN_08010C10(lado, 1, 0)` los cuenta): por eso el juego la ofrece en cada fase.
- Al dejar el campo el monstruo equipado, el motor manda el equipo al cementerio solo.

**Control temporal de un monstruo** [PROBADO].

- Change of Heart (`0x0803EB98`) hace tres cosas: `FUN_0801A8A4(ranura, 0)` (pasa el monstruo al lado
  contrario del que lo controla), el evento `0x3B` con argumento `0x15` y el modificador de tipo 4.
  **Lo que hace volver al monstruo es la bandera `0x15`**: la End Phase (`FUN_08065BF8`, consulta en
  `0x08065D20`) devuelve a todo monstruo que la tenga. El modificador de tipo 4 no interviene.
- **Eventos `0x3B` y `0x3C`** (`FUN_0801B9F4`, `FUN_0801BA28`): poner y quitar una bandera de
  `ranura+0x60`. Así pone el motor las banderas 4, 5, 8, `0xA`, `0xC`, `0xD`, `0xE`, `0x11`, `0x13`,
  `0x15`, `0x19`, `0x1B`, `0x1C`, `0x1E`, `0x1F`, `0x20` y `0x21`. Buscar solo llamadas a
  `FUN_0800E0E0` no las encuentra.
- Fin de turno: `FUN_0801D7DC` recorre las cartas de los dos lados; quita las banderas 5, 6 y `0x19`,
  pasa la `0x18` a `0x19`, descuenta el contador de `+0x34` (bits 2–4) y llama a
  `FUN_0800EED8(ranura)`, que quita los modificadores de tipo 4 y 10 (y el 13 según el dueño).
  `FUN_0800F050(ranura, tipo)` quita las entradas de un tipo.
- **Jugador del turno:** bit 1 de `0x0202787E` (`J0 + 0x562E`).
- Bagworm: `efectos/bagworm_control.s` deja una entrada de **tipo 5** (libre: el calculador y las
  tablas de quita lo tratan como a los tipos sin efecto) y `efectos/gancho_fin_control.s` contesta
  "vuelve" en la End Phase del turno siguiente de quien lo controla.
- **Bagworm −500:** hecho; ver "Bagworm −500 y la posesión de Dark Necrofear" más abajo. Es el segundo
  efecto de Slate Warrior (original, ID 5037), que el motor resuelve por ID en la rutina de destrucción
  en batalla (`FUN_08068C8C`).

**"Enviada al cementerio por un efecto del rival"** [PROBADO]. Destrabó cuatro cartas con un gancho.

- **Cola de acciones** (`send_card_to_graveyard(ranura, banderas, causante)` encola,
  `process_card_actions` ejecuta en `FUN_08016C36`): en `0x020214E0`, ranuras en `+0x964`, causantes
  en `+0xA64`, banderas (u16) en `+0xB64`, cantidad en `+0xD64`. Banderas de la acción: `0x1` al
  cementerio, `0x2` retirada, `0x4` a la mano, `0x10` al tope del mazo, `0x20` al fondo, `0x100` hace
  poner la bandera 4 y `0x800` (batalla) la bandera 5.
- `FUN_080188AC(ranura, destino)` mueve la carta: `destino = lado << 15 | zona << 10 | ...`
  (`0x3008` = al mazo). Al final tiene **el árbol de disparadores por ID** para "fue al cementerio"
  (Sangan, Witch of the Black Forest, Night Assailant...): mira la zona de origen y encola el efecto
  con `FUN_080314B4(lado << 31 | 0xE4 << 21 | ranura, zona_y_ranura duplicado)`. Es parte del
  "segundo mecanismo" de efectos de `PROYECTO.md` §5.3.
- Electric Snake, Minar y Penguin Knight no están en ese árbol, y **nada pone la bandera 6**, que es
  la que lee Fairy Guardian. `efectos/gancho_enviada_por_rival.s` (gancho en `0x0801706C`, después del
  movimiento) pone la bandera 6 y dispara a las tres.
- Los descartes de la mano y del mazo (`FUN_08019598`) **no anotan causante** (`0xFF`). Para ellos
  cuenta la carta que se está resolviendo: su cabecera está en **`0x020204A4`** (bit 0 = lado) y el
  motor la borra al terminar; el byte de estado `0x020204C6` vale 0 fuera de una resolución.
  Ghidra muestra esa base como `0x02020630 + 0x5A4`: es un error suyo, la dirección real se midió.
- La bandera 6 solo la lee `FUN_0805D240` (candidatas de Fairy Guardian) y se limpia al fin del turno.
- **Dos efectos disparados a la vez:** el juego pide "Select the order of effects to add to the
  chain." y espera. `A` cierra el aviso, `A` abre los iconos, `RIGHT` va a *DECIDE*, `A`.
- **Penguin Knight:** su `fn_04` solo encolaba el evento `0x24`, que es **barajar el mazo**. Lo de
  pasar el cementerio al mazo se escribió con el molde de Fiber Jar (`0x0804587C`).
- **Fairy Guardian:** su `fn_04` es la de Lady Panther sin el paso final. Banderas del envío en esa
  familia: Lady Panther `0x10`, Crimson Sentry `0x20`, Return of the Doomed `4`.

**Reasoning** [PROBADO]. Una sola pieza, `efectos/reasoning.s`, con el molde de Cyber Jar
(`0x0803FA8C`): `FUN_0801AB04(lado, ranura)` muestra una carta del mazo; `FUN_080DD328(índice)` = no
se puede Invocar de forma Normal (137 cartas: Fusión, Ritual...); `FUN_080DCE18(índice)` = Spirit
(9 cartas); `record_monster_set(lado, ranura, 1, 0)` invoca desde el mazo. El nivel lo declara el
juego (4 las más de las veces): no hay menú, así que no hizo falta el modo 9.
**`ask_question` acepta un texto propio** guardado en el espacio libre (ASCII terminado en 0).
El texto original "Declare monster Level." está en `0x146A882`, sin uso.

**Herramientas nuevas**

| Script | Para qué |
|---|---|
| `scripts/llamadores.py ROM DIR [nombres]` | Todos los `BL` del código que llaman a una dirección |
| `scripts/llamar_fn.py ROM DIR` | Ejecuta un predicado del ROM para las 1200 cartas y lista las que marca |
| `scripts/resolver_literales.py ROM x.c` | Cambia los `DAT_08...` de un C de Ghidra por su valor, con nombre de carta |
| `scripts/rejugar_sesion.py ROM VIEJA NUEVA` | Rehace una sesión de `paso.py` en otra carpeta (evidencia nueva) |

**Lo que NO funciona** (para no repetirlo)

- Leer en Ghidra una función que llama a `FUN_0800E158`, `ask_question` o
  `send_card_to_graveyard`: las tenía marcadas como "no retorna" y el decompilado se corta ahí.
  `Decompilar.java` ya quita la marca, pero el flujo que Ghidra analizó sigue cortado: para esos
  tramos, `scripts/desensamblar.py`.
- Buscar el ID de una carta solo en los literales: los árboles de comparación llegan a muchos IDs
  con `adds`/`subs` desde un vecino (Kunai = Metalmorph − 7).
- Comparar sesiones grabadas después de agregar un evento al motor: el azar se corre. La sesión
  `ronda1/28-magic-drain` difiere en una frase del rival; los estados finales son iguales.

## Bagworm −500 y la posesión de Dark Necrofear (2026-10-11, noche)

**Electromagnetic Bagworm, −500** [PROBADO].

- "The ATK and DEF of the monster that destroyed this card are decreased by 500 points" es el efecto de
  Slate Warrior (5037) y Rigorous Reaver (5044). La rutina de destrucción en batalla (`FUN_08068C8C`)
  los reconoce por ID en **dos árboles de comparaciones**, uno por cada carta del combate (`0x08068D00`
  y `0x08068FD0`), y encola el efecto de la destruida con **tipo 4** y el otro monstruo en `p[4]`.
- `efectos/gancho_destruida_batalla_a.s` y `_b.s` agregan el 5040 a esas dos ramas. `test_bagworm.py`
  comprueba, con el ROM original al lado, que ningún otro de los 1200 IDs cambió de destino.
- La `fn_04` de Bagworm recibe entonces dos pedidos distintos: el volteo (tipo 3) y este (tipo 4). El
  tipo 4 lo delega en la `fn_04` de Slate Warrior (`0x08042078`), como hace Rigorous Reaver: deja en el
  monstruo un modificador de tipo 10. La `fn_18` con tipo 4 no pide elegir nada.
- **En el juego el −500 se resuelve antes del aviso de elegir la Máquina**, que por eso sale unos
  segundos más tarde: las teclas grabadas de la sesión `ronda6/03` ya no calzan y se jugó de nuevo
  (`ronda7/03`).

**Dark Necrofear, posesión** [PROBADO]. Tres piezas y un cambio en un gancho que ya existía.

- **Lo que el ROM conserva:** la `fn_18` de su fila (`0x08052BE0`, compartida con Snatch Steal, Change
  of Heart y Jowls) trae el caso de Necrofear, con el texto "Select and gain control of 1 opponent's
  face-up monster." y la elección automática para la IA; la `fn_0C` (`0x0802A750`) es su par, la
  validación del objetivo [HIP: no la decompilé en esta tanda].
  La `fn_04` es un stub. La receta de prueba anulaba `fn_0C` y `fn_18`; `recetas/lote.json` las
  devuelve (`"anular_columnas": []`) y corrige el texto de la carta. La invocación retirando 3
  Demonios sigue andando con las dos activas (jugada en `evidencia/ronda7/33-dark-necrofear`).
- **El motor disparaba a Necrofear por su cuenta, pero en otro momento:** apenas era destruida **en
  batalla** encolaba su efecto con tipo 4 y momento `0xE` (por eso su carta se mostraba en la Battle
  Phase). Con la `fn_18` original a secas el aviso salía ahí y el control se tomaba en plena batalla.
  Destruida por un efecto no la disparaba.
- **Ese disparo se quitó** [PROBADO]. Sale del procesador de acciones, del árbol de IDs que empieza en
  `0x0801785E` (acción con banderas `& 0x4040`, destino cementerio, origen distinto del cementerio):
  la rama de Necrofear es `cmp r1, #0x1466 ; beq 0x080178C8` en `0x0801786E`, y `0x080178C8` encola
  con `0xE4 << 21`. El ID no está como literal: el árbol lo arma restando (`0x1544 - 1 - 0xDD`), por
  eso buscar el literal 5222 no lo encuentra. Cambiar ese `beq` por un `nop` (`2BD0` -> `C046`) solo
  afecta a Necrofear: con el `beq` sin tomar, el árbol sigue a la salida por defecto (`0x08017A98`).
  Ahora su carta se muestra una sola vez, en la End Phase. En la receta es una pieza de bytes
  sueltos, `B:DIRECCION:BYTES_ORIGINALES:BYTES_NUEVOS` (tipo nuevo de `parche_efecto.py`, que
  comprueba los bytes originales antes de escribir).
- Los otros usos del literal 5222 en el código no son disparadores: `0x0801E1AC` (bits por jugador en
  `J + 0x2AEB`), `0x0806E6A4` y `0x0806E81E` (predicados que devuelven 0 para Necrofear, [HIP] "se
  puede invocar de forma especial desde..."), `0x08052CA4`/`0x08052DD4` (la `fn_18` compartida). `efectos/necrofear_seleccion.s` y
  `efectos/necrofear_posesion.s` solo atienden el pedido con **momento 5**
  (`(cabecera & 0x7FE00) == 0xA800`) y contestan "nada que hacer" a cualquier otro.
- **End Phase:** `FUN_08064388` es la parte que atiende los efectos "en la End Phase". En su paso 1
  recorre las zonas del campo con un árbol de IDs (Goblin Attack Force, Swords of Revealing Light, los
  Spirit...) y después ejecuta las acciones encoladas. `efectos/gancho_fin_necrofear.s` (gancho en
  `0x08064920`, después del recorrido) busca un Necrofear en el **cementerio** con la bandera 5
  (destruida en batalla) o la 6 (por un efecto del rival), comprueba que el rival controle algún
  monstruo boca arriba (`FUN_08010C10(lado, 1, 0)`) y encola el efecto con
  `FUN_080314B4(lado << 31 | 0x54 << 21 | ranura, ...)`: tipo 4, momento 5. Apaga las dos banderas
  para no encolarlo dos veces.
- **Destruida por un efecto del rival:** la bandera 4 del motor no sirve (Raigeki y Dark Hole no la
  ponen: sus acciones no traen el bit `0x100`). Lo que distingue una destrucción de un descarte es el
  **bit `0x40` de las banderas de la acción**: medido `0x9041` con Raigeki del rival, `0x9001`
  descartada de la mano por Card Destruction del rival, `0x1041` con un Dark Hole propio, `0x8840` y
  `0x8041` en batalla (el bit `0x8000` acompaña a las del rival, el `0x1000` a las de efecto).
  `efectos/gancho_enviada_por_rival.s` le pone a Necrofear la bandera 6 solo si la acción trae el
  `0x40`; para las demás cartas no cambia nada.
- **Toma de control:** `FUN_0801A8A4(id, 0)`, la de Change of Heart, sin la bandera `0x15`: no vuelve.
- **Versión fiel** [PROBADO] (la primera, del mismo día, dejaba el control permanente y a Necrofear
  en el cementerio). Lo que se averiguó para hacerla:
  - **Equipar es solo un registro.** `FUN_0801A600(lado, equipo, monstruo)` encola el evento `0x48`,
    que llama a `FUN_0800E918(lado, 1, equipo, monstruo)`: `equipo+0x3C` = id del monstruo,
    `equipo+0x3D` = tipo, y una entrada `tipo << 8 | ranura del equipo` en la lista del monstruo. No
    comprueba zonas. El evento `0x49` es el de las Uniones (tipo 2; con su tercer argumento en 0
    desequipa, `FUN_0800EAC4`) y el `0x4A` registra el tipo que se le pase.
  - **La tabla del consumidor de eventos (`0x08022154`) está corrida en uno:** el evento `N` usa la
    entrada `N − 1` (`0x38` mover = `FUN_0801BDB4`, `0x3B`/`0x3C` banderas, `0x48` = `FUN_0801C4C8`).
  - **Un monstruo que pasa a ser equipo:** molde, los monstruos Unión (`0x08061A74`). Paso `0x80`:
    `FUN_08011120(lado)` da la casilla libre de Mágicas y Trampas (−1 si no hay) y
    `FUN_080188AC(id, lado << 15 | 0x1400 | casilla << 4 | 8)` lo mueve boca arriba; paso `0x7F`: equipa.
    Necrofear hace las dos cosas en una sola llamada y desde el cementerio (zona `0xD`): funciona.
  - **El efecto de Snatch Steal no toma el control** (`0x0803F2E8` solo equipa y marca la bandera
    `0x1F`). El control lo aplica el motor por ID: `FUN_0802F73C(carta, quitar, máscaras)` lo da o lo
    devuelve cuando el efecto continuo se activa o se anula (lo recorre `FUN_0802F9C4`), y **el
    procesador de acciones devuelve el monstruo cuando Snatch Steal deja el campo** (árbol en
    `0x080171B0`: carta en zona 5, `+0x3C` distinto de `0xFF`, monstruo en el campo y controlado por
    quien controla el equipo → `FUN_0801A8A4`; sin zona libre, al cementerio).
  - Necrofear toma el control ella misma (`FUN_0801A8A4`) y usa solo esa devolución:
    `efectos/gancho_necrofear_equipo.s` cambia su ID por el de Snatch Steal antes de ese árbol. No
    hereda la ganancia de LP del rival ni la bandera `0x1F`: si algo anulara las Mágicas, el control
    no se suspende [sin probar].
  - **Si el monstruo equipado deja el campo**, el motor manda sus equipos al cementerio
    (`FUN_08019BDC` → `FUN_08019884`, que recorre la lista de modificadores): no hizo falta nada.
  - **No se repite:** `efectos/gancho_enviada_por_rival.s` no le pone la bandera 6 si la zona de
    origen es la 5. Medido con Harpie's Feather Duster del rival: `ranura+0x60` queda en 0, el
    monstruo vuelve y la End Phase pasa sin aviso.
  - **Sin casilla libre de Mágicas y Trampas** no se encola el efecto (`efectos/gancho_fin_necrofear.s`).
  - Sin probar en duelo: sin casilla libre (solo lógica), Necrofear equipada devuelta a la mano o
    retirada, la del rival destruida estando equipada, el monstruo volteado boca abajo.
- **Herramientas que salieron de esta tanda:** `scripts/buscar_id.py` (todos los sitios donde el
  motor compara con un ID, literal o calculado, por función), `scripts/decompilar.py` (Ghidra por
  dirección, también interior), `efectos/plantilla_fn04.s` y el recetario `ACCIONES.md`.
- **Necrofear en manos del rival** [PROBADO]: ningún mazo rival la lleva, así que en la prueba el
  Mechanicalchaser que invoca el rival pasa a ser ella en memoria. Destruida en batalla o por mi
  Raigeki, en mi End Phase la IA elige sola a mi monstruo (la `fn_18` original), sin aviso ni espera,
  y en su turno ataca con él.
- **Sin posesión** [PROBADO en duelo, con un monstruo rival boca arriba en la End Phase]: descartada
  de mi mano por Card Destruction del rival, y destruida en mi campo por mi Offerings to the Doomed.
  En los dos casos `ranura+0x60` queda en 0. Si ahí se fuerza la bandera 6, el aviso sale: lo que
  impide la posesión es que la bandera no se pone.
- **Mágicas de juego rápido en la mano** (Offerings to the Doomed): el juego pregunta en cada fase
  "It's the Draw Phase. Activate the effect of Spell/Trap/Effect Monster?" y espera la respuesta,
  también en la End Phase. Una prueba automática con una de esas en la mano tiene que contestar No.
  El menú de la carta tiene tres opciones (Activate Effect, Set, Detail Screen), no dos.
- Pruebas: `scripts/test_necrofear.py` (28 casos) y 6 casos en `test_enviada_por_rival.py`;
  `probar_lote.py ROM "Dark Necrofear"` hace nueve sondas por corrida (3 corridas): mía destruida en
  batalla y con Raigeki del rival, del rival destruida en batalla y con mi Raigeki, las dos sin
  posesión, y tres con Necrofear ya equipada (mi Heavy Storm, mi Dark Hole, Harpie's Feather Duster
  del rival).

**El emulador no liberaba memoria** [PROBADO]. `scripts/gba.py` cargaba el núcleo y el ROM en cada
`GBA(...)` y nunca llamaba a `retro_unload_game` ni `retro_deinit`; además el objeto quedaba vivo por
un ciclo de referencias con sus propias funciones de respuesta. Unos 75 MB por instancia. `paso.jugar`
abre una por paso, así que `repetir_sesion.py` con las 49 sesiones (810 pasos) pedía decenas de gigas;
dos a la vez dejaron la Mac sin memoria. Ahora `GBA.cerrar()` descarga y suelta todo, y abrir un GBA
cierra el anterior (el núcleo es uno solo por proceso: dos GBA vivos nunca funcionaron). Medido: 42
pasos, de 3,1 GB a 0,9 GB; la regresión entera, 1,7 GB. Las 49 sesiones dan el mismo resultado.

## Armar todo en la Mac, sin keystone (2026-10-11)

- `parches.Espacio.asm` usa keystone si está y, si no, las binutils de ARM con la misma fuente. Para
  que el resultado sea **byte a byte** el de keystone: relleno `00 BF` (nop de Thumb-2) antes de las
  constantes (`.balignw 4, 0xbf00`) y ningún relleno cuando la fuente no tiene constantes.
  Comprobado: `test.json` → `d6fe444f…`, `prueba3.json` → `0122cad6…`, `candidatas-30.json` →
  `cb519dad…`, y `lote.json` → `990aefb8…` (el ROM de trabajo). [ROM]
- Una receta puede traer `"hereda"` (otra receta de la carpeta) y `"piezas"` (la lista de
  `parche_efecto.py`); las cartas pueden traer `"arte"`.
- **Arte:** índices de 0 a 63; la paleta puede traer el bit 15 puesto (se ignora). Las cartas del
  juego que no usan el índice 0 tienen ahí `0x83E0`. Un dibujo convertido con el índice 0 sin usar se
  ve bien en el duelo (probado con Reasoning en un ROM aparte). [PROBADO]

## La tienda y los sobres (2026-10-12) [ROM] / [PROBADO jugando]

Punto de partida: `estados/tienda.ss1`, estado de mGBA de Oscar sobre el ROM `(Lote)`, parado en la
tienda con 3000 DP y los sobres 0 a 3 en venta. Carga igual en el ROM `(Ampliado)`.

**Manejo de la pantalla** (para scripts): arriba y abajo cambian de sobre (esperar unos 55 cuadros
entre uno y otro), derecha suma uno al pedido, `A` pregunta "Are you sure?" con el cursor en Yes,
`A` confirma, cada `A` siguiente abre un sobre, y al final queda la lista de cartas. `B` saltea lo
que falte de la apertura y sale; **el baúl se actualiza recién al salir de la lista**. Con esperas
10 cuadros más cortas que las de `scripts/probar_sobres.py`, que hace todo eso, se perdieron teclas.

**Datos** (resumen en `PROYECTO.md` §5.5):

- Tabla de sobres `0x097F2844`, 48 × 16 bytes. Literales que la nombran (20): `0xBD7C8, 0xBD8FC,
  0xBDB18, 0xBDB84, 0xBDBD4, 0xBDBF8, 0xBDC2C, 0xBDD44, 0xBE3A4, 0xD2660, 0xD7550, 0xD7688, 0xD77C8,
  0xD89AC, 0xD8A44, 0xD8B18, 0xD8CC8, 0xD8D74, 0xD8F0C, 0xD9044`.
- Textos `0x097F2B44`, 48 × 3 offsets relativos a `0x094EDD78`. Literales (3): `0xBDC50, 0xBDC78,
  0xBDC90`.
- Las direcciones son `0x09…` porque el ROM pasa de 16 MB: offset de archivo + `0x08000000`.

**Funciones:**

| Dirección | Qué hace |
|---|---|
| `FUN_080BD89C(sobre, salida)` | Arma un sobre: baja en uno lo que hay en venta, tira 0 a 17999, elige la primera carta por rareza y completa con comunes. Guarda la rareza en los 3 bits altos de cada u16 |
| `FUN_080BD700` | Si una carta ya está en el sobre que se arma (por eso no se repiten) |
| `FUN_080BD72C` | El sobre 47: cartas de todo el juego; una parte la busca entre las que no se tienen |
| `FUN_080BDA90` | Reposición y merma de lo que hay en venta |
| `FUN_080BDC30`, `shop_show_packs` (`0x080BDC58`) | Los tres textos de un sobre |
| `FUN_080BDC9C` | El porcentaje "Comp." del sobre |
| `FUN_080BDD4C` | Grupo de un sobre por su número: 0 a 11 → 0, 12 a 21 → 1, 22 a 32 → 2, 33 a 46 → 3, 47 → 4, más → 5 |
| `FUN_080BE260` | Si el sobre está disponible: salta por grupo y, adentro, por sobre (`FUN_080BDD80`, `FUN_080BDE88`, `FUN_080BE090`, `FUN_080BE144`) |
| `FUN_080BE2F4` | Disponible y con alguno en venta |
| `FUN_080BE32C` | Lista de índices de las cartas de un sobre |
| `FUN_080D2574` | Compra: llama a `FUN_080BD89C` por cada sobre pedido y anota las cartas (el sobre va en 6 bits) |
| `FUN_080D84D0(actual, sentido)` | Sobre siguiente o anterior entre los ofrecidos |
| `FUN_080D1AD4(índice, lugar)` | Carga el dibujo chico de una carta al abrir el sobre |

El C de Ghidra de las primeras está en `ghidra/salida/sobres.c` y `sobres2.c`. La zona
`0x080D7000`–`0x080D9A00` (la pantalla de la tienda) no tiene funciones definidas en el proyecto de
Ghidra: hay que leerla desensamblada.

**El dibujo chico** [PROBADO]. `FUN_080D1AD4` carga 64 bytes de `0x08F61184 + índice × 64` (32
colores) y 1024 de `0x08F73DC4 + índice × 1024` (32×32, 4×4 tiles de 8×8, valores 0 a 31, con el
índice 0 como un color más). Cada tabla tiene 5 literales: `0x8C5E4/0x8C5E8`, `0x91878/0x9187C`,
`0xAD9A8/0xAD9A4`, `0xC79F0/0xC79F4`, `0xD1B8C/0xD1B94`. Cómo se encontró: las cartas 1201 en
adelante salían con ruido al abrir un sobre, y el ruido usaba pocos colores, o sea que el dibujo no
era el grande. `arte.py` lo arma reduciendo el grande a 32×32 y 32 colores (sale parecido al del
juego, no igual: diferencia media de 18 sobre 255 con Sangan).

**La última carta no sale.** En `0x080BD980` (`blo`) y `0x080BD9D4` (`bhs`) el sorteo pide índice
menor que la cantidad. En el juego original deja afuera a la 1200. `ampliar.py` los cambia a `bls`
y `bhi`; el ROM `(Lote)` queda como el original.

**Un sobre que cuelga el juego.** Con menos comunes que cartas por sobre, el bucle que completa el
sobre no termina (pasó con una lista de 3 para un sobre de 5: los DP se descuentan y la pantalla
queda en la apertura). `sobres.py` lo rechaza.

**Lo medido para un sobre número 49 (no se intentó).** Tres cosas atan la tienda a 48:

1. *La constante.* Lugares de las zonas `0x080BD600`–`0x080BE500` y `0x080D2000`–`0x080DA000` con un
   `cmp` o `movs` de `0x2F` o `0x30`, hallados por búsqueda y **sin revisar uno por uno**: `BD8F0`
   (este es el caso especial del sobre 47, no un tope), `BDB28, BDBC4, BDBE0, BDC06, BDC34, BDC62,
   BDCB0, BDD72, BE340, D204C, D2114, D2522, D2544, D2548, D2556, D2948, D2A46, D2C62, D2CC6, D2EAC,
   D2EC6, D2F6C, D2F86, D4284, D4CD0, D4CE4, D5E92, D711E, D75A4, D7D4C, D7D7E, D84E6, D84EA, D851A,
   D8528, D8560, D85B4, D86DC, D9842, D9A6C, D9A76, D9D54`. En `FUN_080BDD4C` el `0x2F` separa
   grupos. Todas caben en un byte: cambiar la cantidad sería reescribir constantes, sin ganchos.
2. *Lo que hay en venta, en la partida.* 4 bytes por sobre desde `0x02004C08`; en `0x02004CC8`
   empiezan otros datos. El juego solo lee y escribe el primer byte de cada uno (visto en los
   accesos de `0xBD8D8`, `0xBDAA6`, `0xBDB0E`–`0xBDB22`, `0xBDB9A`–`0xBDBBA`, `0xBE310` y `0xD85A6`;
   el literal `0x4C08` aparece en 12 lugares: `0xBD908, 0xBDAD4, 0xBDB80, 0xBE320, 0xD7558, 0xD77C4,
   0xD85C0, 0xD8A40, 0xD8B14, 0xD8D70, 0xD8F08, 0xD9110`; los seis de `0xD7…`–`0xD9…` no se
   leyeron). [HIP] Si los otros tres bytes están libres, el sobre `k ≥ 48` podría vivir en el
   segundo byte del sobre `k − 48`: la dirección que calcula el juego menos 191. No haría falta
   tocar el guardado. En el estado de la tienda esos bytes están en cero.
3. *La memoria de la tienda.* En `0x0203B546` hay un u16 por sobre (el pedido) y pegada atrás, en
   `0x0203B5A8`, la máscara de 64 bits de sobres ofrecidos: entra un sobre más en los 2 bytes de
   relleno, no dos. En `0x0203CD70` hay otro u16 × 48 (el bucle de `0x080D2928` escribe uno por
   sobre pedido); no se miró qué tiene atrás.

Además, cada sobre nuevo necesita su rama en `FUN_080BE260` (hoy un número mayor que 47 da "no
disponible") y un dibujo de sobre, que no se buscó.
