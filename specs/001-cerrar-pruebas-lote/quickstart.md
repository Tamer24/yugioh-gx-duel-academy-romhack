# Quickstart: validar la feature de punta a punta

Todo se corre desde la raíz del proyecto.

## Requisitos

- Python 3 con `pillow`, `unicorn` y `capstone` (ya instalados).
- `nucleos/mgba_libretro.dylib`.
- El ROM bajo prueba:

```sh
ROM="build/Yu-Gi-Oh! GX - Duel Academy (Efectos).gba"
md5 -q "$ROM"     # esperado: 4ed08c04c7c3f5256ed7597200def613
```

## 1. El registro es uno solo (US2)

```sh
python3 scripts/registro.py verificar "$ROM"
```

Esperado: salida 0 y un resumen con 30 cartas. Para ver que la comprobación sirve, cambiar a
mano un veredicto en la tabla de `PRUEBAS.md` y volver a correr: tiene que fallar nombrando
la carta. Deshacer con `python3 scripts/registro.py tabla "$ROM"`.

## 2. Un escenario se arma y se comprueba

```sh
python3 scripts/escenario.py "$ROM" estados/duelo-inicio.ss1 /tmp/prueba.st \
    --yo 1:"Reaper of the Cards"
python3 scripts/escenario.py "$ROM" /tmp/prueba.st --mostrar
```

Esperado: la mano del jugador muestra Reaper of the Cards en la posición 1. Pedir una
posición que no existe (`--yo 9:...`) tiene que fallar sin escribir el archivo.

## 3. Las 9 cartas tienen prueba (US1)

```sh
python3 scripts/probar_lote.py --listar
python3 scripts/probar_lote.py "$ROM" "Electromagnetic Bagworm"
python3 scripts/probar_lote.py "$ROM"          # el lote entero, 3 corridas por carta
```

Esperado: cada carta termina en un veredicto, o figura en la lista para probar con Oscar con
el motivo. Ninguna queda en `INESTABLE`.

## 4. Nada quedó sin cerrar

```sh
python3 scripts/registro.py verificar "$ROM"
python3 scripts/registro.py aptas "$ROM"
python3 scripts/registro.py pendientes "$ROM"
```

Esperado: 0 cartas "sin probar", "sin confirmar" o "a medias" (SC-001). `aptas` no lista
ninguna carta con `ev_ojo` distinto de `si` (SC-006).

## 5. Oscar confirma una carta (US3)

1. Abrir `specs/001-cerrar-pruebas-lote/guia-oscar.md` y elegir una carta.
2. En mGBA, con el ROM `(Efectos)` abierto: *Archivo → Cargar estado desde archivo* y elegir
   el estado que indica la guía.
3. Seguir los pasos y comparar con "qué debería verse".
4. Registrar:

```sh
python3 scripts/registro.py ojo "$ROM" "Kunai with Chain" si
python3 scripts/registro.py tabla "$ROM"
```

Esperado: la carta pasa a `aptas`. Tiempo por carta: menos de 5 minutos (SC-005).
