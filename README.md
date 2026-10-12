# Yu-Gi-Oh! GX Duel Academy (GBA): romhack de cartas restauradas

Proyecto de ingeniería inversa y romhack de *Yu-Gi-Oh! GX Duel Academy* (Game Boy Advance, versión
USA). El ROM trae 172 cartas "recortadas": tienen su fila en la tabla de efectos, pero no se pueden
conseguir en el juego. Este proyecto las devuelve al juego y les escribe el efecto cuando falta o
está incompleto.

**Este repositorio no incluye el ROM ni ningún archivo que lo contenga.** Para usarlo hace falta una
copia propia del ROM USA (MD5 `f62c47cbe08e1e3bcfcf9f1b84841a76`). Lo que se comparte son parches
`.bps` (`build/`) y las herramientas para generarlos.

## Estado

- 30 cartas restauradas y funcionando en el ROM de trabajo; 6 confirmadas para una versión de juego
  (`build/hack-v0.1.bps`). La tabla completa, con la evidencia de cada una, está en `PRUEBAS.md`.
- Las 142 recortadas restantes están clasificadas por cuánto trabajo piden
  (`datos/triage_recortadas.csv`).
- Hay un sistema para sumar cartas por packs y un recetario de cómo se implementa cada acción.

## Por dónde empezar

| Documento | Para qué |
|---|---|
| `PLAN.md` | Dónde está el proyecto, lo aprendido, el método para implementar una carta y qué sigue |
| `ACCIONES.md` | Recetario: cómo se hace cada acción de una carta (ver la mano del rival, sumar o restar ATK, mover cartas, tomar el control, equipar, dispararse sola…) |
| `PROYECTO.md` | Mapa del ROM, formato de las recetas y backlog |
| `NOTAS-REVERSE.md` | El detalle técnico de cómo se averiguó cada cosa |
| `PRUEBAS.md` | Cómo se prueba y el resultado de cada carta |

## Cómo se arma el ROM de trabajo

```sh
sh scripts/construir_lote.sh "Yu-Gi-Oh! GX - Duel Academy (USA).gba"
```

Deja `build/Yu-Gi-Oh! GX - Duel Academy (Lote).gba` y el parche `build/lote.bps`. El ROM original no
se modifica.

## Cómo se suma un pack de cartas

```sh
python3 scripts/alta.py ROM_ORIGINAL preparar pack-2 "Carta" "Otra carta"
# completar la descripción de cada carta en recetas/packs/pack-2.json
python3 scripts/alta.py ROM_ORIGINAL aplicar pack-2
sh scripts/construir_lote.sh ROM_ORIGINAL
```

`scripts/triage.py` clasifica cartas sin darlas de alta, `scripts/huecos.py` lista los lugares libres
y `scripts/buscar_id.py` muestra dónde trata el motor a una carta.

## Qué hace falta

- Python 3, con `unicorn`, `capstone` y `Pillow` (`pip install unicorn capstone pillow`).
- Las binutils de ARM (`brew install arm-none-eabi-binutils`), para ensamblar las piezas de `efectos/`.
- Para las pruebas en duelo: el núcleo de mGBA para libretro (`mgba_libretro.dylib`, `.so` o `.dll`)
  dentro de `nucleos/`. No se incluye; se baja del buildbot de libretro.
- Opcional, para decompilar: Ghidra y OpenJDK 21. El proyecto de Ghidra se rehace desde el ROM propio
  (ver `NOTAS-REVERSE.md`, "Regenerar"); `ghidra/salida/` trae las funciones ya decompiladas.

## Qué hay en cada carpeta

| Carpeta | Contenido |
|---|---|
| `scripts/` | Herramientas: armado del ROM, alta de packs, pruebas de lógica (Unicorn) y en duelo (emulador sin ventana) |
| `efectos/` | Las piezas de código (ensamblador Thumb) que se agregan al juego |
| `recetas/` | Qué cartas y qué piezas lleva cada ROM |
| `datos/` | Tablas extraídas del juego y los registros de huecos y de pruebas |
| `estados/` | Estados de emulador para probar cada carta (`estados/revisar/` son los de mGBA) |
| `evidencia/` | Partidas jugadas por script, con capturas; `evidencia/index.html` es la galería |
| `build/` | Parches `.bps` |
| `ghidra/` | Scripts y funciones decompiladas |
| `specs/` | La especificación con que se cerró el primer lote |

## Créditos y aviso

- Los nombres de funciones de `ghidra/nombres_yugiohgx-da.json` vienen del proyecto yugiohgx-da
  (licencia MIT).
- Las pruebas en duelo usan el emulador mGBA.

Proyecto de aficionados, sin relación con Konami. *Yu-Gi-Oh!* y *Yu-Gi-Oh! GX Duel Academy* son
propiedad de sus dueños; acá no se distribuye el juego.
