# Contrato: comandos

Los tres scripts nuevos. Todos se corren desde la raíz del proyecto, validan su entrada y
fallan antes de escribir (Principio VI). Ninguno escribe sobre un `.gba`.

`ROM` es la ruta del ROM bajo prueba.

## `scripts/escenario.py`

Arma un estado de duelo a partir de otro.

```text
python3 scripts/escenario.py ROM BASE.st SALIDA.st [--yo POS:CARTA ...] [--rival POS:CARTA ...]
python3 scripts/escenario.py ROM ESTADO.st --mostrar
```

- `POS` es la posición en la mano (0 en adelante). `CARTA` es un nombre exacto o un índice.
- Cambia el índice de la carta y su tipo, para que la IA y los menús la traten como lo que es.
- `--mostrar` imprime LP, manos, campo, cementerio y cantidad de cartas en el mazo de los dos
  lados, sin escribir.
- Falla si: la carta no existe en el ROM, la posición no existe en esa mano, `SALIDA` es el
  mismo archivo que `BASE`, o el archivo no es un estado de este juego.
- Después de escribir, vuelve a leer `SALIDA` y comprueba que las manos son las pedidas.

También se usa como módulo: `escenario.armar(...)` devuelve la ruta del estado y
`escenario.comprobar(duelo, esperado)` devuelve la lista de diferencias (vacía si está bien).

## `scripts/probar_lote.py`

Corre los casos de las cartas de los grupos A y B.

```text
python3 scripts/probar_lote.py ROM [CARTA ...] [--corridas 3] [--fotos CARPETA] [--registrar]
python3 scripts/probar_lote.py --listar
```

- Sin `CARTA` corre todos los casos definidos.
- Por cada corrida imprime: preparación (correcta o qué falta), instantánea de antes,
  instantánea de después, y el resultado.
- Resultado por corrida, uno de: `PREPARACION INVALIDA`, `NO SE DIO EL DISPARADOR`,
  `FUNCIONA`, `FUNCIONA EN PARTE`, `NO FUNCIONA`.
- Resultado por carta: el de las corridas si las 3 coinciden; si no, `INESTABLE`.
- `--registrar` escribe el veredicto en `datos/pruebas.csv` solo si el resultado por carta es
  uno de los tres veredictos. Sin esa opción no escribe nada.
- Código de salida: 0 si todas las cartas pedidas dieron un veredicto; 1 si alguna quedó en
  `PREPARACION INVALIDA`, `NO SE DIO EL DISPARADOR` o `INESTABLE`.

## `scripts/registro.py`

Opera sobre `datos/pruebas.csv`.

```text
python3 scripts/registro.py verificar ROM
python3 scripts/registro.py tabla ROM          # regenera la tabla en PRUEBAS.md
python3 scripts/registro.py aptas ROM
python3 scripts/registro.py pendientes ROM     # las que Oscar tiene que mirar
python3 scripts/registro.py ojo ROM "CARTA" si|no ["qué vio"]
```

- `verificar`: aplica las reglas de [registro-csv.md](./registro-csv.md) y comprueba que la
  tabla de `PRUEBAS.md` es la que se generaría hoy. Salida 0 si todo coincide.
- `tabla`: reemplaza en `PRUEBAS.md` lo que hay entre `<!-- registro:inicio -->` y
  `<!-- registro:fin -->`. Falla si faltan las marcas o si `verificar` falla.
- `aptas`: imprime las cartas que cumplen la regla de aptitud de `data-model.md`.
- `pendientes`: imprime las cartas con `ev_ojo = pendiente`, con su estado y qué mirar.
- `ojo`: registra el reporte de Oscar. Con `no`, exige el texto de lo que vio, corrige el
  veredicto a `funciona en parte` salvo que se indique otro, y deja la discrepancia en
  `nota_ojo`.
