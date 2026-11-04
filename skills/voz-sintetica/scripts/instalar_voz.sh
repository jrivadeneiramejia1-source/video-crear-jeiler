#!/bin/bash
# Instala la voz sintética (Kokoro, sin internet después de instalar). Se corre UNA vez por computador o sesión.
# Uso: bash instalar_voz.sh      (todo en $VIDEO_JEILER_MODELOS o ~/.cache/video-jeiler; ~355 MB de modelos)
# Crea un Python propio (venv) en ese lugar para no tocar el del sistema. Necesita internet, python3 y curl.
# Descarga solo desde github.com (thewh1teagle/kokoro-onnx, archivos del modelo Kokoro 82M) y pypi.org (paquetes de Python).
set -euo pipefail
BASE="${VIDEO_JEILER_MODELOS:-$HOME/.cache/video-jeiler}"
M="$BASE/modelos-voz"; mkdir -p "$M"
if [ ! -x "$BASE/venv/bin/python" ]; then python3 -m venv "$BASE/venv"; fi
"$BASE/venv/bin/pip" install --quiet kokoro-onnx soundfile numpy 2>&1 | grep -v "notice" || true
R=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
dl(){ [ -s "$M/$2" ] || { echo "bajando $2 ..."; curl -fsSL --retry 3 -o "$M/$2.tmp" "$1" && mv "$M/$2.tmp" "$M/$2"; }; }
dl $R/kokoro-v1.0.onnx kokoro-v1.0.onnx
dl $R/voices-v1.0.bin voices-v1.0.bin
echo "LISTO. Python: $BASE/venv/bin/python | modelos: $M"
