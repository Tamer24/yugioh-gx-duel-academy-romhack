# Duel Academy romhack: punto de partida para Claude Code

Romhack de *Yu-Gi-Oh! GX Duel Academy* (GBA, USA). Estado al **2026-10-20**. Este archivo es el
resumen para retomar; el detalle está en los documentos de abajo. Se escribe en español.

## Leer primero

| Archivo | Qué tiene |
|---|---|
| `PLAN.md` | Plan vigente, historia por tandas y estado de cada versión (la entrada más nueva va arriba) |
| `PROYECTO.md` | Mapa del ROM (tablas, memoria, funciones), backlog original y glosario |
| `NOTAS-REVERSE.md` | Detalle técnico byte a byte de cada hallazgo, por fecha |
| `ACCIONES.md` | Recetario: cómo se implementa cada acción de una carta (destruir, robar, equipar, anular…) |
| `PRUEBAS.md` | Tabla de resultados por carta (se genera desde `datos/pruebas.csv`) |
| `.specify/memory/constitution.md` | Constitución 2.0.0 (Spec Kit; local, no está en git) |

## Dónde estamos

- **v0.3 armada y rehecha el 2026-10-19:** 43 cartas aptas (las 30 restauradas, Elemental Hero Neos,
  los 6 equipos del pack 2 y los 6 Neo-Spacian del pack 3). Parche `build/hack-v0.3.bps`, ROM MD5
  `2734e173b21b9ba0defb1dc95ebf6d5e`. **No se compartió todavía.** Notas: `build/hack-v0.3.md`.
- ROM de trabajo `(Lote)` (todo, con ayudas de prueba): `build/lote.bps`, MD5 `11095a77db4dfdbd3d63614d78b06658`.
- v0.2 (31 cartas): `build/hack-v0.2.bps`, MD5 `9c45523e563cc42d478fea029e06eea1`.
- Último commit: `f6e6563` (Baou anula el efecto del monstruo que destruye en batalla).
- `datos/pruebas.csv`: 43 aptas, 0 no aptas, ninguna aparcada.

## Cómo se trabaja (constitución 2.0.0)

- **Claude verifica; Oscar juega libre.** Una carta es apta con tres evidencias: lógica (prueba con
  Unicorn, `scripts/test_*.py`), duelo automático (`scripts/probar_lote.py`, 3 corridas) y confirmación
  por capturas (`registro.py capturas`) o a ojo de Oscar (`registro.py ojo`). Oscar ya no prueba
  carta por carta: juega las versiones y cuenta lo raro.
- El ROM original **no se toca**: vive en `../Downloads/Yu-Gi-Oh! GX - Duel Academy (USA).gba`
  (MD5 `f62c47cbe08e1e3bcfcf9f1b84841a76`). Todo ROM sale de una receta (`recetas/*.json`) + scripts.
  Los `.gba`, `.sav` y `estados/lote/` no van a git; se comparte solo el `.bps`.
- Código nuevo en el espacio libre (`efectos/*.s` desde `0x1A00000`); sobre el original, solo ganchos.

## Comandos de todos los días (desde la raíz)

```sh
ORIG="../Downloads/Yu-Gi-Oh! GX - Duel Academy (USA).gba"
LOTE="build/Yu-Gi-Oh! GX - Duel Academy (Lote).gba"
sh scripts/construir_lote.sh "$ORIG"                         # rearma el (Lote) desde recetas/lote.json
python3 scripts/probar_lote.py "$LOTE" "Nombre de carta" --fotos evidencia/rondaN/slug --registrar
python3 scripts/probar_lote.py --listar                      # los 25 casos con escenario propio
python3 scripts/registro.py capturas "$LOTE" "Carta" evidencia/rondaN/slug "nota"
python3 scripts/registro.py aptas "$LOTE"                    # qué entra en una versión
python3 scripts/armar_version.py "$ORIG" 0.4                 # versión de juego (--rehacer para pisar)
python3 scripts/repetir_sesion.py ROM $(cat scripts/sesiones_regresion.txt)   # regresión: 30 partidas grabadas
python3 scripts/bps.py --aplicar "$ORIG" build/X.bps "build/X.gba"
```

Los estados de partida de esas sesiones están en `estados/regresion/`. Regresión esperada: 28 de 30 sesiones `IGUAL`; Exchange (azar) y Magic Drain variante 28 (cursor)
difieren siempre. Pruebas de lógica: `test_stim_pack.py`, `test_tryce.py`, `test_baou.py`,
`test_gancho_batalla.py` (ROM); `test_neo_spacian.py` (ROM y original); `test_atk_cuenta.py` (ROM sin
el gancho, ROM con él, `datos/volcado_goddess`).

Entorno en la Mac: Python 3 con `unicorn capstone pillow`; `brew install arm-none-eabi-binutils`;
núcleo `nucleos/mgba_libretro.dylib` (no está en git, se baja de libretro).

## Lo técnico que más se usa

- Duelo en RAM: jugador `0x02022250`, rival `+0x2B08`; ranuras de `0x50` (id de ranura = lado<<7 | n).
  `+0x24` índice (bit 15 se conserva), `+0x28` ATK, `+0x2C` DEF, `+0x31` zona en el nibble alto
  (`0` monstruo, `5` Mágica/Trampa, `D` cementerio, `F` mano, `C` mazo), `+0x33` posición
  (`10` ataque, `30` defensa, `20` boca abajo), `+0x3A` contador, `+0x3C` objetivo del equipo,
  `+0x60` banderas (bandera 5 = destruida en batalla este turno). Índice → ID: `0x087A8624`.
- Entrada de efecto `p`: bits 1-8 de `u16(p)` = id de ranura, bit 0 lado; bit 3 de `p[2]` = anulada.
  Byte de estado de la resolución `0x020204C6`.
- Batalla `0x02020C20`: atacante en bits 13-20 de `u32(+0)`, defensor en bits 5-12 de `u16(+2)`.
- **Resolvedor de cadenas:** la fn_04 de cada eslabón se llama en `0x080245D6` (eslabones 0-1) y
  `0x080245B6` (2+); entrada `r8 + 24 x índice`. Marcar ahí `p[2] |= 8` anula el efecto (Baou).
- Ganchos: `ldr r3,[pc]; bx r3; .word destino` en dirección alineada a 4; la pieza repite lo pisado y
  vuelve. Si la pieza usa `bl`, guardar `lr`. En Thumb, `ldrb` con offset > 31 no ensambla: usar base+0x30.
- Fin de turno `FUN_0801D7DC`; entrada a Battle Phase `FUN_0801B724`; `0x020214E0` bit 15 = lado de la
  acción en curso (no el jugador del turno).

## Lo que sigue

1. **Oscar juega la v0.3 libre** y cuenta lo raro (o la v0.2). Es lo único pendiente para cerrarla.
2. Elegir el próximo pack (`PLAN.md`, backlog; `datos/triage_recortadas.csv`): quedan 7 huecos seguros
   en el `(Lote)`; el ROM ampliado `(Neo Space)` no necesita huecos y falta decidir si la versión de
   juego pasa a esa base.
3. Abiertos de antes: confirmar a ojo el baúl ampliado con el ROM corregido; la IA no usa las cartas
   nuevas; Grand Mole se activa sola.

Spec Kit: la feature `specs/001-cerrar-pruebas-lote` quedó cerrada en los hechos (las 30 funcionan y
están en la v0.2/v0.3); para trabajo nuevo, empezar otra con `/speckit-specify`.
