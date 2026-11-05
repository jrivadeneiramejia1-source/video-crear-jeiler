#!/bin/bash
# Instala Piper (otra voz sintética GRATIS y sin internet después de instalar) con voces en español. Opcional: sirve para comparar con Kokoro.
# Uso: bash instalar_piper.sh      (modelos en $VIDEO_JEILER_MODELOS/modelos-voz/piper o ~/.cache/video-jeiler/modelos-voz/piper; ~250 MB)
# Descarga solo desde huggingface.co/rhasspy/piper-voices (voces: es_MX claude = Apache-2.0, es_MX ald = dominio público, es_ES davefx = CC0) y pypi.org.
set -euo pipefail
BASE="${VIDEO_JEILER_MODELOS:-$HOME/.cache/video-jeiler}"; M="$BASE/modelos-voz/piper"; mkdir -p "$M"
if [ ! -x "$BASE/venv/bin/python" ]; then python3 -m venv "$BASE/venv"; fi
"$BASE/venv/bin/pip" install --quiet piper-tts soundfile numpy 2>&1 | grep -v "notice" || true
R=https://huggingface.co/rhasspy/piper-voices/resolve/main/es
for v in es_MX/claude/high/es_MX-claude-high es_MX/ald/medium/es_MX-ald-medium es_ES/davefx/medium/es_ES-davefx-medium; do
  n=$(basename $v); for e in onnx onnx.json; do [ -s "$M/$n.$e" ] || { echo "bajando $n.$e ..."; curl -fsSL --retry 3 -o "$M/$n.$e.tmp" "$R/$v.$e" && mv "$M/$n.$e.tmp" "$M/$n.$e"; }; done
done
echo "LISTO. En la historia: \"voces\": {\"lila\": {\"motor\": \"piper\", \"voz\": \"es_MX-claude-high\", \"velocidad\": 0.95}}"
