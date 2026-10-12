# Data Model: Cerrar las pruebas del lote de 30

## Carta del lote

Una fila del registro. Son exactamente 30.

| Campo | Qué es | Reglas |
|---|---|---|
| `carta` | Nombre en el juego | Único. Debe existir en el ROM bajo prueba |
| `indice` | Número de la carta en el juego (1–1200) | Único |
| `id_konami` | ID de Konami | Único |
| `clase` | Monstruo de volteo, Monstruo de efecto, Mágica, Trampa… | Informativo |
| `usa_piezas_nuevas` | `si` / `no` | `si` cuando tiene función propia en `efectos/` o parche. Decide si necesita evidencia de lógica aislada |

## Veredicto

Uno por carta.

| Campo | Qué es | Reglas |
|---|---|---|
| `veredicto` | `funciona`, `funciona en parte`, `no funciona`, o vacío | Vacío solo si `aparcada = si` |
| `aparcada` | `si` / `no` | Si es `si`, `motivo_aparcada` es obligatorio |
| `motivo_aparcada` | Por qué se dejó | Texto libre |
| `detalle` | Qué se observó, en números o cartas concretas | Obligatorio si hay veredicto |
| `falla` | Qué difiere del texto | Obligatorio si el veredicto no es `funciona` |
| `fecha` | Cuándo se obtuvo | `AAAA-MM-DD` |

Transiciones permitidas:

```text
(sin veredicto) ──prueba en duelo──▶ funciona | funciona en parte | no funciona
(sin veredicto) ──tope de piezas───▶ pendiente de probar con Oscar ──sesión──▶ veredicto | aparcada
cualquier veredicto ──Oscar ve otra cosa──▶ veredicto corregido (se anota la discrepancia)
```

No hay vuelta a "sin veredicto", salvo que una prueba que pasaba deje de pasar (regresión).

## Evidencia

Tres clases, las del Principio IV.

| Campo | Qué es | Reglas |
|---|---|---|
| `ev_logica` | Script de prueba de lógica aislada | Obligatorio para figurar como apta solo si `usa_piezas_nuevas = si`; si no, `n/a` |
| `ev_auto` | Comando que corre la prueba automática en duelo | Vacío si no se pudo automatizar |
| `ev_ojo` | `si`, `no` o `pendiente` | `si` solo cuando Oscar reportó haberla visto |
| `nota_ojo` | Qué reportó Oscar | Obligatorio si lo que vio difiere de la prueba automática |
| `rom_md5` | MD5 del ROM en que se obtuvo el veredicto | Obligatorio si hay `ev_auto` o `ev_ojo = si` |
| `estado` | Estado de partida para reproducir | Ruta dentro de `estados/` |

## Regla de aptitud

Una carta es **apta para una receta de juego** cuando se cumplen todas:

1. `veredicto = funciona`
2. `aparcada = no`
3. `ev_ojo = si`
4. `ev_auto` no está vacío, **o** se probó con Oscar porque no se pudo automatizar
5. si `usa_piezas_nuevas = si`, `ev_logica` no está vacío ni es `n/a`

Se calcula; no se guarda.

## Escenario

Vive en código (`scripts/probar_lote.py`), no en el registro.

| Campo | Qué es |
|---|---|
| Estado base | De qué estado parte |
| Mano del jugador | Qué cartas van en qué posiciones |
| Mano del rival | Lo mismo, con el tipo de cada carta |
| Extras | Tope del mazo, cementerio (solo si el estado lo admite) |
| Pasos | Qué hace el corredor: colocar, terminar turno, esperar, responder |
| Esperado | Comparación entre la instantánea de antes y la de después |

Reglas: antes de emitir un veredicto se comprueba que cada carta pedida está donde se pidió.
Dos cartas pueden compartir escenario (Electric Snake y Minar), pero cada una tiene su
propio "esperado" y su propio veredicto.

## Instantánea

Lo que se compara para decidir.

| Campo | De dónde sale |
|---|---|
| LP de los dos lados | `Duelo.lp()` |
| Cartas en mano, por lado | `Duelo.mano()` |
| Campo por controlador | listas de zonas (`probar_volteo.campo`) |
| Cementerio y retiradas, por lado | `Duelo.zona()` |
| Cantidad de cartas en el mazo, por lado | `Duelo.zona(lado, "c")` |
| Posición y ATK de cada monstruo | `ranura+0x33`, `ranura+0x28` |
