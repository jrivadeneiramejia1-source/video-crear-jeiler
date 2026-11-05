#!/bin/bash
# Instala Blender como módulo de Python (bpy) para renderizar 3D sin pantalla ni tarjeta gráfica (Cycles en CPU).
# Uso: bash instalar_blender.sh      (en $VIDEO_JEILER_MODELOS o ~/.cache/video-jeiler/venv-blender; baja unos 400 MB desde pypi.org)
# Necesita internet, python3 (el paquete bpy 5.x trae versiones para Python 3.11 y 3.13; con otro Python puede no instalarse) y ffmpeg.
set -euo pipefail
BASE="${VIDEO_JEILER_MODELOS:-$HOME/.cache/video-jeiler}"
command -v ffmpeg >/dev/null || { echo "Falta ffmpeg."; exit 1; }
if [ ! -x "$BASE/venv-blender/bin/python" ]; then python3 -m venv "$BASE/venv-blender"; fi
"$BASE/venv-blender/bin/pip" install --quiet bpy numpy 2>&1 | grep -v "notice" || true
"$BASE/venv-blender/bin/python" -c "import bpy; print('bpy', bpy.app.version_string)"
echo "LISTO. Python de Blender: $BASE/venv-blender/bin/python"
echo "Nota: EEVEE necesita una tarjeta gráfica (libEGL); este instalador usa Cycles en CPU, más lento pero sin tarjeta."
