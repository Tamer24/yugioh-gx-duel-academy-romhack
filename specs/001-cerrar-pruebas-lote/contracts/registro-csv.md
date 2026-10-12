# Contrato: `datos/pruebas.csv`

Fuente única del registro de resultados. La leen `registro.py`, y más adelante la receta de
`Candidatas v1`. Detalle de cada campo en [data-model.md](../data-model.md).

## Formato

CSV con encabezado, UTF-8, separador coma, comillas dobles cuando el texto lleva comas.
Una fila de datos por cada carta de `datos/huecos.csv` (eran exactamente 30 hasta el 2026-10-11; con el alta de packs, `scripts/alta.py`, se suman).

## Columnas (en este orden)

```text
carta,indice,id_konami,clase,usa_piezas_nuevas,veredicto,aparcada,motivo_aparcada,
detalle,falla,ev_logica,ev_auto,ev_ojo,nota_ojo,rom_md5,estado,fecha
```

## Valores permitidos

| Columna | Valores |
|---|---|
| `usa_piezas_nuevas` | `si`, `no` |
| `veredicto` | `funciona`, `funciona en parte`, `no funciona`, vacío |
| `aparcada` | `si`, `no` |
| `ev_logica` | ruta de un script, `n/a`, vacío |
| `ev_ojo` | `si`, `no`, `pendiente` |
| `rom_md5` | 32 hexadecimales en minúscula, o vacío |
| `fecha` | `AAAA-MM-DD`, o vacío |

## Reglas que `registro.py verificar` hace cumplir

1. Hay una fila por cada carta de `datos/huecos.csv`, con el mismo índice, y no se repiten `carta`, `indice` ni `id_konami`.
2. Cada `carta` coincide con el nombre del `indice` en el ROM bajo prueba.
3. `veredicto` vacío solo si `aparcada = si`, o si la carta acaba de darse de alta y todavía no tiene evidencia (`ev_auto` vacío y `ev_ojo` distinto de `si`).
4. `aparcada = si` exige `motivo_aparcada`.
5. Un veredicto exige `detalle`; si no es `funciona`, exige además `falla`.
6. `ev_ojo = si` o `ev_auto` no vacío exigen `rom_md5`.
7. `estado`, si no está vacío, es un archivo que existe.
8. `ev_logica` y `ev_auto`, si nombran un script, nombran uno que existe.

Cualquier incumplimiento: salida distinta de cero y un mensaje que nombra la carta y la
columna. No se escribe nada.

## Compatibilidad

El CSV anterior tenía las columnas `carta,clase,resultado,detalle,en_prueba3`. Se reemplaza
entero. `en_prueba3` desaparece: qué cartas trae cada ROM lo dice su receta.
