#!/bin/sh
# Arma el ROM "(Lote)" de cero a partir del ROM original: las 30 cartas restauradas con los
# parches de prueba (recetas/test.json) mas todas las piezas propias de efectos/, que estan
# listadas, en orden, en recetas/lote.json. Tambien deja el parche build/lote.bps.
#
# Uso: sh scripts/construir_lote.sh "ROM original.gba"
# Necesita arm-none-eabi-binutils (no hace falta keystone). No toca el ROM original.
set -e
cd "$(dirname "$0")/.."
ORIGINAL="$1"
[ -f "$ORIGINAL" ] || { echo "uso: sh scripts/construir_lote.sh \"ROM original.gba\"" >&2; exit 1; }
SALIDA="build/Yu-Gi-Oh! GX - Duel Academy (Lote).gba"

python3 scripts/restaurar.py "$ORIGINAL" recetas/lote.json "$SALIDA" | grep -v "^indice \|^   referencias"
python3 scripts/bps.py "$ORIGINAL" "$SALIDA" build/lote.bps
md5 -q "$SALIDA" 2>/dev/null || md5sum "$SALIDA"
