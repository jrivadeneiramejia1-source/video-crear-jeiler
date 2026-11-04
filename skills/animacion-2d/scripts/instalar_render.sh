#!/bin/bash
# Prepara lo necesario para dibujar videos 2D con render.py: Playwright (Python) y un Chromium.
# Uso: bash instalar_render.sh      (en $VIDEO_JEILER_MODELOS o ~/.cache/video-jeiler; comparte el Python con voz-sintetica)
# Necesita internet, python3 y ffmpeg. Si ya hay un Chromium (en las sesiones en la nube viene uno en /opt/pw-browsers), no baja otro.
set -euo pipefail
BASE="${VIDEO_JEILER_MODELOS:-$HOME/.cache/video-jeiler}"
command -v ffmpeg >/dev/null || { echo "Falta ffmpeg."; exit 1; }
if [ ! -x "$BASE/venv/bin/python" ]; then python3 -m venv "$BASE/venv"; fi
"$BASE/venv/bin/pip" install --quiet playwright numpy 2>&1 | grep -v "notice" || true
ya_hay() { for c in "${CHROMIUM_PATH:-}" /opt/pw-browsers/chromium "$(command -v chromium 2>/dev/null || true)" "$(command -v chromium-browser 2>/dev/null || true)" "$(command -v google-chrome 2>/dev/null || true)"; do [ -n "$c" ] && [ -x "$c" ] && { echo "$c"; return 0; }; done; return 1; }
if c=$(ya_hay); then echo "Chromium encontrado: $c"; else echo "Bajando Chromium (~150 MB) con Playwright ..."; "$BASE/venv/bin/python" -m playwright install chromium; fi
echo "LISTO. Python: $BASE/venv/bin/python"
