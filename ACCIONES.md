# Recetario de acciones

Cómo se hace cada cosa que puede hacer una carta en este motor: qué función se llama, con qué
argumentos, qué pieza ya lo hace y qué hay que cuidar. Sirve para implementar una carta nueva
armándola con acciones ya resueltas en vez de investigar de cero.

Complementa a `PLAN.md` (método y lecciones) y a `NOTAS-REVERSE.md` (el detalle de cómo se
averiguó cada cosa). Cuando una carta nueva obligue a resolver una acción que no está acá, **se
agrega su entrada** antes de dar la carta por terminada.

Marcas de certeza:

- **[PROBADO]**: lo usa una pieza nuestra y se jugó en duelo.
- **[ORIGINAL]**: se leyó en el código de una carta original que funciona, pero ninguna pieza
  nuestra lo usa todavía.
- **[HIP]**: hipótesis; verificar antes de apoyarse en ella.

## 1. Lo común a toda pieza

### Dónde va el código

Una carta tiene una fila en la tabla de efectos (`datos/efectos.csv`) con cinco columnas. Una pieza
(`efectos/*.s`) reemplaza una columna o engancha una función del motor. Se listan en
`recetas/lote.json`, siempre **al final** (el orden fija las direcciones).

| En la receta | Qué hace |
|---|---|
| `ID:fn_04:archivo.s` | El efecto: lo que pasa al resolverse |
| `ID:fn_0c:archivo.s` | ¿Este objetivo es válido? |
| `ID:fn_10:archivo.s` | Condición: ¿se puede activar ahora? Devuelve 1 o 0 |
| `ID:fn_14:archivo.s` | Coste |
| `ID:fn_18:archivo.s` | Selección: hace elegir objetivos y los deja en el pedido |
| `G:DIRECCION:archivo.s` | Gancho: pisa 8 bytes de una función del motor (dirección múltiplo de 4) y salta a código propio, que repite lo pisado y vuelve. El salto pisa `r3` |
| `T:DIRECCION:VALOR:archivo.s` | Reemplaza una entrada de una tabla de saltos; la anterior queda como `ORIGINAL` |
| `B:DIRECCION:ANTES:DESPUES` | Cambia unos bytes sueltos (comprueba los originales) |

En una columna, el valor anterior queda disponible como `ORIGINAL`: una pieza puede atender solo
unos casos y delegar el resto (`chosen_one.s`, `hiro_scout.s`).

### El pedido

Toda función de efecto recibe en `r0` un puntero `p` a 12 bytes.

| Campo | Qué es |
|---|---|
| `p[0]` bit 0 | Lado que activa (0 = jugador, 1 = rival) |
| cabecera bits 1–8, `(u16(p) & 0x1FF) >> 1` | Id de ranura de esta carta |
| `(p[1] >> 1) & 0xF` | Tipo de efecto: 3 = volteo, 4 = disparador |
| `(u32(p) >> 13) & 0x3F` | Momento: `0xE` = "fue al cementerio" (motor); 5 = End Phase (el que usa Necrofear) |
| `p[2]` bit 3 | Anulada: no hacer nada |
| `p[4]` | Dato del disparador: el atacante, o el monstruo que la destruyó (id de ranura) |
| `p[8] & 0xF` | Cuántos objetivos se eligieron |
| `p[9]`, `p[10]`, `p[11]` | Ids de ranura elegidos |

Una misma `fn_04` recibe pedidos distintos (volteo, disparador, End Phase): se distinguen por tipo y
momento. Para "tipo 4, momento 5": `(u32(p) & 0x7FE00) == 0xA800`.

### Estados: una `fn_04` puede ser una máquina de pasos

El motor llama a la `fn_04` con el byte de estado `0x020204C6` en `0x80`. **Lo que la función
devuelve es el estado siguiente**; con 0 termina. Entre un paso y otro el motor muestra avisos,
abre listas y ejecuta lo encolado. Secuencia típica con una lista: `0x80` registra candidatas y
pregunta → `0x7F` abre la lista → `0x7E` lee lo elegido y actúa. Después de `ask_question` hay
que devolver un estado explícito. Contador auxiliar libre: `0x020204C7`.

### Ranuras, zonas y banderas

Id de ranura: bit 7 = lado, 7 bits bajos = número (100 en adelante son fichas). Dirección:
`0x02022250 + lado * 0x2B08 + numero * 0x50`.

| Campo de la ranura | Qué es |
|---|---|
| `+0x24` (u16, 15 bits) | Índice de la carta. ID de Konami: `u16(0x087A8624 + indice * 2)` |
| `+0x28`, `+0x2C` (u32) | ATK y DEF actuales (los recalcula el motor: no escribirlos) |
| `+0x30` bits 0–4 | Tipo: menor que `0x15` monstruo; `0x15`, `0x16` Mágica o Trampa |
| `+0x30` bits 12–18 | Zona |
| `+0x30` bit 19 | Quién la controla |
| `+0x31` nibble bajo | Nivel |
| `+0x32` bit 3 | Dueño |
| `+0x33` | Posición: `0x10` ataque, `0x30` defensa boca arriba, `0x20` boca abajo (bit 4 = boca arriba) |
| `+0x3C`, `+0x3D` | Si es un equipo: id del monstruo equipado (`0xFF` = ninguno) y tipo |
| `+0x3E` nibble bajo, `+0x40…` (u16) | Lista de modificadores: byte alto = tipo, byte bajo = ranura de la carta que lo causa |
| `+0x60` (u32) | Banderas |

Zonas: 0 monstruos, 5 Mágicas y Trampas, `0xC` mazo, `0xD` cementerio, `0xE` retiradas, `0xF` mano.

Banderas de `+0x60` que se usan: 5 = destruida en batalla este turno (motor); 6 = enviada al
cementerio por un efecto del rival (la pone `gancho_enviada_por_rival.s`); 14 = efecto de campo de
"una vez por turno" disponible; `0x15` = vuelve a su dueño en la End Phase. La 5 y la 6 se borran
al terminar el turno. Se ponen y quitan con `EVENTO(0x3B o 0x3C, id, bandera)`; se leen con
`TIENE_BANDERA(id, bandera)`.

Datos del lado (`0x02022250 + lado * 0x2B08`): LP en `+0`; mano en `+0x2824`. Zonas del campo:
`0x02022250 + 0x5610 + lado * 11` (5 de monstruos, 5 de Mágicas, 1 de campo; `0xFF` = vacía).
Fase: `0x0202787E >> 2` (2 = Main Phase 1, 3 = Battle, 4 = Main Phase 2, 5 = End); bit 1 = de
quién es el turno.

### Funciones del motor con nombre

Las piezas reciben estas direcciones como constantes (`MOTOR` en `scripts/parches.py`): en el `.s`
se escribe `ldr r3, =NOMBRE` y `bl .Lllamar` (con `.Lllamar: bx r3`). Molde listo para copiar:
`efectos/plantilla_fn04.s`.

## 2. Acciones

### Ver y mostrar

| Acción | Cómo | Ejemplo | Certeza |
|---|---|---|---|
| Mostrar la mano del rival | Estado `0x80`: `CLEAR_ZONE`, registrar con `REGISTRAR` cada carta de la mano rival (lista en `+0x2824` del lado), `DIALOGO` | `spy_mano.s` (molde: Ancient Telescope `0x0803E458`) | [PROBADO] |
| Revelar una carta del mazo | `REVELAR(lado, ranura)` por cada carta, desde el tope | `reasoning.s` (molde: Cyber Jar `0x0803FA8C`) | [PROBADO] |
| Mostrar un texto propio | `ASK_QUESTION(texto)`; el texto va en el espacio libre de textos. Después, devolver un estado explícito | `reasoning.s`, `goddess_whim.s` | [PROBADO] |
| Tirar una moneda | El menú original "heads or tails" (modo `0x15`) tira y muestra el resultado; queda en `0x02022250 + 0x5656` (1 = acertó) | `goddess_whim.s` | [PROBADO] |
| Número al azar | `AZAR()` | `exchange.s` | [PROBADO] |

### Elegir

| Acción | Cómo | Ejemplo | Certeza |
|---|---|---|---|
| Elegir un monstruo del campo | Usar en `fn_18` la selección de una carta original parecida. Deja la cantidad en `p[8] & 0xF` y los ids en `p[9…]`. La IA elige sola. `0x08052BE0` = "1 monstruo rival boca arriba" (Snatch Steal, Change of Heart) | `necrofear_seleccion.s` | [PROBADO] |
| Restringir la selección a un caso | Envolver la `fn_18`: dejarla correr solo para el pedido que corresponde y devolver 1 en los demás | `necrofear_seleccion.s` | [PROBADO] |
| Selección propia en el campo | Paso 0 = la original (avisa); después B cancela y A graba el id bajo el cursor (`0x02022250 + 0x5668`) con `FUN_08051680(p, id)` | `bagworm_seleccion.s` | [PROBADO] |
| Elegir de una lista (mano, cementerio) | `0x80`: `CANDIDATAS(lado, ID de una carta original que liste eso, 0)` + `ASK_QUESTION` → `0x7F`: `DIALOGO` abre la lista → `0x7E`: leer lo elegido en `0x02019F24` (y `…28`, `…2C`): `(v & 0x7FFFF) >> 11` = id de ranura | `exchange.s`, `chosen_one.s` | [PROBADO] |
| Que elija la IA | Si `p[0] & 1` es el rival, no abrir menú: elegir en el código (al azar, el de menor ATK…) | `exchange.s`, `share_the_pain.s` | [PROBADO] |
| Validar un objetivo | `fn_0C(p, id)`: devuelve 1 si sirve. Ej.: en el campo, del rival y boca arriba | original `0x0802A750` | [ORIGINAL] |

### ATK y DEF

El motor **recalcula** el ATK y la DEF recorriendo la lista de modificadores de la ranura. Escribir
`+0x28` a mano no sirve. Todo cambio es una entrada en esa lista.

| Acción | Cómo | Ejemplo | Certeza |
|---|---|---|---|
| Sumar, restar, duplicar o dividir el ATK hasta el fin del turno | `EVENTO_MOD(lado, ranura origen, ranura destino, (dato << 4) \| 4)`: agrega un modificador de tipo 4, que el motor borra al terminar el turno. El cálculo va por ID de la carta origen: agregar el caso de la carta en `modificador_atk.s` | `goddess_whim.s`, `riryoku.s`, `modificador_atk.s` | [PROBADO] |
| Pasar ATK de un monstruo a otro | Dos modificadores de tipo 4, uno en cada monstruo, con el `dato` señalando al que pierde | `riryoku.s` | [PROBADO] |
| −500 ATK y DEF permanente | Modificador de tipo 10: delegar en la `fn_04` de Slate Warrior (`0x08042078`) con el monstruo en `p[4]` | `bagworm_control.s` (tipo de efecto 4) | [PROBADO] |
| Bono por estar equipada | Modificadores de tipo 1 (equipo) y 2 (Unión): el bono va por ID de la carta origen en el calculador (`0x08012C94`). Kunai (+500) y Metalmorph ya estaban; una carta nueva necesita su caso ahí | `kunai_cadena.s` | [PROBADO] para Kunai; agregar un caso nuevo, sin hacer |
| Marcar un monstruo sin tocar sus números | Modificador de tipo 5 (libre: el calculador no hace nada con él). `FUN_0800F050(ranura, tipo)` lo quita | `bagworm_control.s`, `gancho_fin_control.s` | [PROBADO] |

### Puntos de vida

| Acción | Cómo | Ejemplo | Certeza |
|---|---|---|---|
| Pagar LP (coste) | `PAGAR_LP(lado, cantidad)` (`FUN_0801ABD0`) | Seal of the Ancients (original; `test_seal.py`) | [PROBADO] |
| Daño | `DANIO(lado que lo recibe, cantidad)` (`FUN_0801ABF0`) | familia Ookazi, Tremendous Fire, Minar (`0x0803A48C`) | [ORIGINAL] |
| Ganar LP | `GANAR_LP(lado, cantidad)` (`FUN_0801AD6C`) | familia Dian Keto (`0x0803A20C`) | [ORIGINAL] |

Estas familias son una sola función con un árbol de IDs (cada ID, su cantidad). Una carta recortada
que ya comparte la función suele traer su caso (Minar funcionó sin tocar su `fn_04`).

### Mover cartas

| Acción | Cómo | Ejemplo | Certeza |
|---|---|---|---|
| Destruir o mandar al cementerio | `A_CEMENTERIO(lado, id, ranura de la carta que lo causa)` | `two_pronged_attack.s`, `share_the_pain.s` | [PROBADO] |
| Mandar a otro lado (mano, tope o fondo del mazo) | `LIMPIAR_ACCIONES()`; `ENVIAR(id, banderas, causante)`; `PROCESAR_ACCIONES()`. Banderas: `0x41` cementerio (destruida), `0x4` mano, `0x10` tope del mazo, `0x20` fondo | `fairy_guardian.s` (molde: Lady Panther `0x080430AC`) | [PROBADO] |
| Cambiar de zona directamente | `MOVER_CARTA(id, lado << 15 \| zona << 10 \| casilla << 4 \| 8 si boca arriba)`. `0x3008` = al mazo | `penguin_knight.s`, `necrofear_posesion.s` | [PROBADO] |
| Robar | `ROBAR(lado, cantidad)` (`FUN_0801B28C`) | Pot of Greed (`0x0803DFE4`); familia Electric Snake (`0x08039320`) | [ORIGINAL] |
| Robar del mazo del rival revisando cada carta | Una carta por llamada: devolver `0x7F` mientras queden, con el contador en `0x020204C7` | `hiro_scout.s` | [PROBADO] |
| Intercambiar dos cartas de mano entre jugadores | Intercambiar los `0x50` bytes de las dos ranuras e invertir el bit de dueño (`+0x32` bit 3). Las listas de mano no se tocan | `exchange.s` | [PROBADO] |
| Cementerio al mazo | Copiar la lista del cementerio y mover cada carta con `MOVER_CARTA(…, 0x3008)`; después barajar (evento `0x24`) | `penguin_knight.s` (molde: Fiber Jar `0x0804587C`) | [PROBADO] |
| Tributar un monstruo del rival | `FUN_08010FA4(rival, 0xFF, 3, ranura)` dice cuántos se pueden tributar; después `A_CEMENTERIO` | `share_the_pain.s` | [PROBADO] |

Antes de mover varias cartas de una misma lista (mazo, cementerio), **copiar la lista**: el motor la
compacta al sacar.

### Invocar y posición

| Acción | Cómo | Ejemplo | Certeza |
|---|---|---|---|
| Invocar un monstruo de forma especial | `INVOCAR(lado, id, 1, 0)` y devolver `0x0A`, como Monster Reborn | `reasoning.s` | [PROBADO] |
| Que un monstruo se invoque retirando N de un tipo del cementerio | No es una pieza: parche `invocacion_tipo` de la receta (`{"id_konami", "tipo", "cantidad"}`) | Dark Necrofear (3 Demonios) | [PROBADO] |
| Saber si un monstruo admite Invocación Normal o especial | `SOLO_ESPECIAL(indice)`, `ES_SPIRIT(indice)` | `reasoning.s` | [PROBADO] |
| Cambiar de posición a un monstruo | `CAMBIAR_POSICION(lado, id, 0, 0)`, como Block Attack | `kunai_cadena.s` | [PROBADO] |

### Tomar el control

Todas usan `TOMAR_CONTROL(id, 0)` (`FUN_0801A8A4`): pasa el monstruo al lado contrario del que lo
controla; devuelve 0 si no se pudo (sin zona libre). Lo que cambia es cómo y cuándo vuelve.

| Duración | Cómo | Ejemplo | Certeza |
|---|---|---|---|
| Hasta la End Phase de este turno | Además, bandera `0x15` (evento `0x3B`): la End Phase lo devuelve | Change of Heart (original, `0x0803EB98`) | [ORIGINAL] |
| Hasta el fin de mi turno siguiente | Modificador de tipo 5 con origen en la carta; un gancho en la End Phase contesta "vuelve" | `bagworm_control.s` + `gancho_fin_control.s` | [PROBADO] |
| Mientras otra carta siga equipada | Equipar la carta al monstruo (ver abajo) y hacer que, al dejar el campo, el motor la trate como a Snatch Steal: devuelve el monstruo | `necrofear_posesion.s` + `gancho_necrofear_equipo.s` | [PROBADO] |
| Permanente | Solo la llamada | La primera versión de Necrofear (reemplazada el 2026-10-11) | [PROBADO] |

### Equipar

Equipar es un registro: el equipo guarda al monstruo en `+0x3C` y el monstruo gana una entrada de
tipo 1 en su lista. Si el monstruo deja el campo, el motor manda sus equipos al cementerio.

| Acción | Cómo | Ejemplo | Certeza |
|---|---|---|---|
| Equipar una Mágica o Trampa que ya está boca arriba en el campo | `EQUIPAR(lado, id del equipo, id del monstruo)` | `kunai_cadena.s` (molde: Metalmorph `0x0803991C`) | [PROBADO] |
| Que una Trampa equipada no se vaya al cementerio al resolverse | Agregar su ID a `gancho_queda_campo.s` | Kunai with Chain | [PROBADO] |
| **Equipo con bono fijo de ATK** (recortada del grupo A, p. ej. Stim-Pack, Butterfly Dagger - Elma, Shooting Star Bow - Ceal) | Solo darla de alta: su caso sigue en el calculador (`0x08012BD8`, un `case` por ID en el árbol de `0x08012F00` a `0x08013090`; `scripts/buscar_id.py ROM ID` lo muestra). Los bonos medidos: Stim-Pack +700, Elma +300, Murasame +800 (solo Warrior), Baou +500, Ceal −1000, Tryce −500 | `recetas/packs/pack-2.json`, `_caso_equipo` en `scripts/probar_lote.py` | [PROBADO] el bono; los efectos extra (devolver a la mano, ataque directo, atacar dos veces), sin probar |
| Equipo que pide **descartar una carta** al activarlo (Baou, Tryce) | Lo hace la función del motor, sin pieza propia: aparece "Discard hand." y la lista de selección (`elegir_en_lista` en `probar_lote.py`) | Wicked-Breaking Flamberge - Baou | [PROBADO] |
| Bono de un equipo que **baja con los turnos** (Stim-Pack: 700 − 200 × contador en `ranura + 0x3A` del equipo) | El calculador ya resta; falta quien suba el contador cada turno (no ubicado). Hoy el bono queda en +700 | Stim-Pack | [ROM] |
| Que un monstruo pase a ser equipo | `CASILLA_MAGIAS(lado)` (−1 = sin lugar); `MOVER_CARTA(id, lado << 15 \| 0x1408 \| casilla << 4)`; `EQUIPAR`. Funciona también desde el cementerio | `necrofear_posesion.s` (molde: monstruos Unión, `0x08061A74`) | [PROBADO] |

### Disparadores: cuándo se activa sola

| Cuándo | Cómo | Ejemplo | Certeza |
|---|---|---|---|
| Al voltearse | Lo dispara el motor: llega a la `fn_04` con tipo de efecto 3 | `bagworm_control.s`, `hiro_scout.s` | [PROBADO] |
| Al ser destruida en batalla, con efecto sobre quien la destruyó | Agregar el ID a los dos árboles de la rutina de batalla; llega con tipo 4 y el otro monstruo en `p[4]` | `gancho_destruida_batalla_a.s` y `_b.s` | [PROBADO] |
| Al ir al cementerio por un efecto del rival | `gancho_enviada_por_rival.s`: pone la bandera 6 y encola el efecto según ID y zona de origen. Las banderas de la acción dicen cómo fue: `0x40` destruida, `0x800` en batalla | Electric Snake, Minar, Penguin Knight | [PROBADO] |
| En la End Phase del turno en que pasó algo | Un gancho en la End Phase busca la carta con su bandera y encola el efecto con un momento propio | `gancho_fin_necrofear.s` | [PROBADO] |
| Encolar un efecto a mano | `ENCOLAR_EFECTO(lado << 31 \| (momento << 4 \| tipo) << 21 \| id, d \| d << 16)` con `d = (zona y controlador) << 8 \| id` | `gancho_fin_necrofear.s` | [PROBADO] |

### Activación y permanencia

| Acción | Cómo | Ejemplo | Certeza |
|---|---|---|---|
| Decidir si se puede activar | `fn_10`: devuelve 1 o 0. `CONTAR_MONSTRUOS(lado, 1, 0)` cuenta los boca arriba | `kunai_condicion.s` | [PROBADO] |
| Efecto de un monstruo en el campo, una vez por turno, desde el menú | Agregar el ID a las listas de `gancho_lista_campo.s` y `gancho_menu_campo.s` | Goddess of Whim, Fairy Guardian, Lady Panther | [PROBADO] |
| Coste | `fn_14`; para tributar, el menú de modo 8 funciona con el jugador | Share the Pain (original) | [PROBADO] |

### Tocar el motor por ID

Mucho de lo que hace el motor está en árboles de comparación por ID. Tres maneras de meter una
carta en uno, de menos a más código:

| Quiero | Cómo | Ejemplo |
|---|---|---|
| Que el motor **deje de hacer** algo con una carta | Pieza `B:`: cambiar su `beq` por un `nop` | El aviso de Necrofear al ser destruida (`B:0801786E:2BD0:C046`) |
| Que trate a una carta **como a otra** en un árbol | Gancho que, antes del árbol, cambia el ID leído por el de la otra | `gancho_necrofear_equipo.s` |
| **Agregar** una carta a un árbol o lista | Gancho que resuelve la rama antes y vuelve | `gancho_destruida_batalla_a.s`, `gancho_lista_campo.s` |

### Cartas que el juego nunca tuvo

| Quiero | Cómo | Ejemplo | Certeza |
|---|---|---|---|
| Un **monstruo Normal** nuevo | Cargar sus datos en `scripts/cartas_nuevas.csv` (mismas columnas que `nombres_konami.csv`; el ID es el `cid` de la base oficial de Konami, que es la numeración que usa el juego) y darlo de alta con `scripts/alta.py`. No lleva fila de efecto: el motor busca el ID, no lo encuentra y lo trata como Normal. Un ID mayor que 6467 (el último del juego) no rompe nada | Elemental Hero Neos (ID 6653, hueco 7) | [PROBADO] |
| Su **dibujo** | PNG de cualquier tamaño en `arte/` y la clave `"arte": "arte/x.png"` en el borrador del pack. Sale también el dibujo chico (32×32), el que se ve al abrir un sobre | `arte/elemental-hero-neos.png` | [PROBADO] |
| Que **salga en un sobre** de la tienda | Clave `"sobres"` de la receta: `{"sobre": "Basic 1-A", "agregar": {"comunes": ["Carta"]}}`. Una restaurada ya sale en los sobres del monstruo que reemplazó. `scripts/sobres.py ver ROM SOBRE` muestra cómo queda | `recetas/sobres-demo.json` | [PROBADO] en pantalla |
| Que cuente como **"Elemental Hero"** para otras cartas | No hay una lista: cada carta que pide un "Elemental Hero" compara contra los IDs uno por uno en su propio árbol (6310 a 6313, 6344, 6345, 6393 y 6467). Hace falta un gancho "como a otra" por árbol: `0x08015200` (la cuenta de Shining Flare Wingman), `0x08010060`, `0x080205E0`, `0x08050B52`, `0x08060770` (dos sitios), `0x08060AA0`, `0x08060D04`, `0x08060FF0`. Falta identificar cuál es de cada carta | Sin hacer: Neos hoy **no** cuenta como Elemental Hero | [ROM] |
| Una carta nueva **con efecto** | No entra todavía: no tiene fila en la tabla de efectos (901 filas, tope fijo). Ver `PROYECTO.md`, F6 | Los Neo-Spacian | Sin hacer |

## 3. Cómo encontrar lo que falta

0. **Dar de alta y clasificar antes de empezar.** Un pack entra con `scripts/alta.py` (`preparar` y
   `aplicar`; ver `PLAN.md`, "Método que funciona"), que usa el clasificador:
   `python3 scripts/triage.py ROM_ORIGINAL "Nombre" …` (o `--archivo pack.txt`, una carta por línea) dice de cada carta si ya está en el juego, si está
   recortada o si no existe en el ROM, y para las recortadas qué trae su fila:

   | Grupo | Qué significa | Qué pasó con las 30 restauradas |
   |---|---|---|
   | A | El efecto comparte función con cartas que están en el juego | 7 de 7 anduvieron con su función original |
   | C | Función propia que ninguna carta en juego usa | 9 anduvieron tal cual; a 13 hubo que reescribírsela |
   | D | Función vacía: escribir el efecto de cero | 1 (Dark Necrofear) |
   | E | Sin función de efecto: efecto continuo que el motor resuelve por ID | ninguna era de este grupo: sin calibrar |

   Aparte avisa cuando un monstruo con efecto de campo no está en las listas del menú (acertó las 3
   que lo necesitaban, con 1 aviso de más). No ve si falta un disparador: para eso, la columna
   `motor`. Las 142 recortadas que quedan están clasificadas en `datos/triage_recortadas.csv`
   (36 A, 38 C, 2 D, 66 E; de las E, a 22 las nombra el motor y a 44 no).
   `--calibrar` repite la medición contra las cartas ya restauradas.
1. **¿Qué hace ya el motor con la carta?** `python3 scripts/buscar_id.py ROM_ORIGINAL "Nombre"`:
   lista todos los sitios del código que comparan con su ID, aunque el ID no esté como literal, y
   la función de cada uno. Una carta recortada suele conservar su caso en varios árboles.
2. **¿Quién hace algo parecido?** El mismo comando con una carta original que funcione. Las
   funciones donde aparece son el molde y los puntos donde enganchar.
3. **Leerlas:** `python3 scripts/decompilar.py ROM_ORIGINAL NOMBRE DIRECCION…` deja el C en
   `ghidra/salida/NOMBRE.c`. Acepta direcciones interiores. Para los tramos que Ghidra corta,
   `scripts/desensamblar.py ROM DESDE HASTA`.
4. **Mirar una original en marcha:** un registrador como `fn_04` de envoltorio (anota la cabecera
   y `p[8…10]` en `0x0203F000` y delega en `ORIGINAL`) muestra qué recibe y en qué estados.
5. Escribir la pieza desde `efectos/plantilla_fn04.s`, probar la lógica con Unicorn
   (`scripts/test_necrofear.py` es el modelo: se enganchan las direcciones del motor y se anotan las
   llamadas), y después en duelo (`scripts/probar_lote.py`, `scripts/paso.py`).

## 4. Lo que todavía no tiene receta

- Agregar un caso nuevo al calculador para el bono de un equipo (tipos 1 y 2).
- Anular efectos (el motor tiene banderas `0x1F` y `0x20` de "efecto continuo activo"; [HIP]).
- Retirar del juego como acción propia (bandera de acción `0x2`; sin usar por una pieza nuestra).
- Fichas, contadores, Fusión y Ritual.
- Cualquier decisión de la IA sobre cuándo jugar una carta (sin ubicar).
