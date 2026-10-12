# Implementation Plan: Cerrar las pruebas del lote de 30 cartas restauradas

**Branch**: `001-cerrar-pruebas-lote` (sin rama git) | **Date**: 2026-10-10 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-cerrar-pruebas-lote/spec.md`

## Summary

Dar un veredicto respaldado por prueba en duelo a las 9 cartas sin probar o a medias, dejar
un único registro de resultados para las 30 y entregarle a Oscar una guía para confirmar a
ojo.

Enfoque: no se escribe un banco de pruebas nuevo. Se reutilizan los cuatro corredores que ya
existen y se agrega una sola pieza común, un **armador de escenarios** que edita un estado de
duelo (manos de los dos lados, y si hace falta el tope del mazo) y comprueba que quedó como
se pidió. `datos/pruebas.csv` pasa a ser la fuente única y la tabla de `PRUEBAS.md` se genera
a partir de él, de modo que no puedan divergir.

Las cartas cuyo disparador no se logre automatizar **no se fuerzan**: se juntan en una lista
con su efecto esperado y se prueban con Oscar, con un estado armado para cada una.

## Technical Context

**Language/Version**: Python 3.14 (el del sistema, sin entorno virtual)

**Primary Dependencies**: núcleo `mgba_libretro.dylib` (`nucleos/`) vía `scripts/gba.py`; Pillow; Unicorn y Capstone (solo para cartas con piezas nuevas). Todo instalado y comprobado.

**Storage**: archivos. `datos/pruebas.csv` (registro), `estados/*.st` (escenarios), `PRUEBAS.md` (lectura).

**Testing**: los propios corredores (`scripts/probar_*.py`) son las pruebas; cada veredicto se repite 3 veces. Sin framework de tests.

**Target Platform**: macOS (Mac de Oscar) para las pruebas automáticas; mGBA con ventana para la confirmación a ojo.

**Project Type**: herramientas de línea de comandos sobre un ROM (scripts sueltos).

**Performance Goals**: una corrida de una carta en menos de 2 minutos; el lote completo (9 cartas × 3 corridas) en menos de 1 hora.

**Constraints**: el ROM bajo prueba no se modifica; los escenarios se arman en el estado, no en el ROM. Las ayudas de prueba no pasan a recetas de juego.

**Scale/Scope**: 30 cartas en el registro; 9 con prueba nueva; 13 en la guía para Oscar.

**ROM bajo prueba**: `build/Yu-Gi-Oh! GX - Duel Academy (Efectos).gba`, MD5 `4ed08c04c7c3f5256ed7597200def613` [ROM]. Cada veredicto se registra con el MD5 del ROM en que se obtuvo.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Puertas de `.specify/memory/constitution.md` (v1.0.1).

- [x] **I. ROM original intacto**: ✅ la feature no genera ROMs ni parches; lee el ROM `(Efectos)` y nunca escribe sobre un `.gba`.
- [x] **II. Reproducible**: ⚠ desviación heredada, ver *Complexity Tracking*. Los escenarios sí son reproducibles: salen de un estado base más una definición en código.
- [x] **III. Intervención mínima**: ✅ N/A, no se escribe código en el ROM. Si un diagnóstico pide un envoltorio, se arma en un ROM aparte que no se registra.
- [x] **IV. Prueba en duelo**: ✅ es el objeto de la feature. El armador comprueba la preparación antes de todo veredicto (FR-004). Las no automatizables van a la lista para probar con Oscar.
- [x] **V. Marcas de confianza**: ✅ el registro distingue evidencia automática de confirmación a ojo; `research.md` marca cada supuesto sobre la IA como `[HIP]`.
- [x] **VI. Comprobaciones en el script**: ✅ `registro.py` valida el CSV (30 cartas, veredictos del vocabulario, sin repetidas) y falla antes de escribir `PRUEBAS.md`.
- [x] **VII. Alcance acotado**: ✅ no se arregla ninguna carta. Tope de dos piezas nuevas por carta; pasado ese tope, a la lista de Oscar.

**Re-evaluación tras el diseño (Phase 1)**: sin cambios. El diseño agrega dos scripts y
ninguno toca el ROM.

## Project Structure

### Documentation (this feature)

```text
specs/001-cerrar-pruebas-lote/
├── plan.md              # Este archivo
├── research.md          # Cómo provocar cada disparador; decisiones
├── data-model.md        # Registro, escenario, evidencia
├── quickstart.md        # Cómo validar la feature de punta a punta
├── contracts/
│   ├── registro-csv.md  # Columnas y reglas de datos/pruebas.csv
│   └── cli.md           # Comandos de escenario.py, probar_lote.py y registro.py
└── tasks.md             # Lo genera /speckit-tasks
```

### Source Code (repository root)

```text
scripts/
├── gba.py               # existente: emulador sin ventana
├── duelo_auto.py        # existente: manejo del duelo y lectura de RAM
├── estado.py            # existente: lectura y edición de estados
├── probar_magicas.py    # existente
├── probar_trampas.py    # existente
├── probar_cadena.py     # existente
├── probar_volteo.py     # existente
├── escenario.py         # NUEVO: arma un estado de duelo y comprueba la preparación
├── probar_lote.py       # NUEVO: un caso por carta de los grupos A y B, 3 corridas, veredicto
└── registro.py          # NUEVO: valida el CSV, genera la tabla, la lista de aptas y la guía

datos/
└── pruebas.csv          # fuente única del registro (se reescribe con el formato nuevo)

estados/
└── lote/                # NUEVO: un estado por carta, para las pruebas y para Oscar

PRUEBAS.md               # la tabla de resultados pasa a generarse desde el CSV
specs/001-cerrar-pruebas-lote/
└── guia-oscar.md        # NUEVO (entregable): qué mirar y cómo, carta por carta
```

**Structure Decision**: se mantiene la estructura plana de `scripts/` que ya usa el proyecto.
Tres scripts nuevos, cada uno con una responsabilidad; los corredores existentes se importan,
no se reescriben.

## Fases de trabajo

1. **Base común**: `escenario.py` (editar manos de los dos lados con su tipo, comprobar la
   preparación) y `registro.py` con el CSV en formato nuevo. Bloquea todo lo demás.
2. **US2, registro confiable**: migrar los 30 veredictos actuales al CSV, generar la tabla de
   `PRUEBAS.md`, verificar coincidencia. Se puede entregar sola.
3. **US1, las 9 cartas**: un caso por carta en `probar_lote.py`, de la más barata a la más
   cara según `research.md`. Cada caso que supere el tope pasa a la lista de Oscar.
4. **US3, guía y sesión con Oscar**: `guia-oscar.md` con las 13 del grupo C más las que no se
   pudieron automatizar; estados listos en `estados/lote/`; registrar lo que Oscar reporte.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principio II: el ROM `(Efectos)` no sale de una receta única; se armó con `parche_efecto.py` sobre un ROM base | Es el único ROM que trae las funciones propias ya escritas, y unificar la receta es la Fase 2 de `PLAN.md` | Unificar la receta primero retrasa los veredictos y no cambia el resultado. Mitigación: cada veredicto guarda el MD5 del ROM, y las pruebas son repetibles, así que el lote se vuelve a correr cuando exista la receta única |
