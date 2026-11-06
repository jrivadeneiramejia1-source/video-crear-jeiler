#!/bin/bash
# Prepara lo necesario para escenas 3D de navegador: Playwright (Python), un Chromium, Three.js (MIT) y GSAP (licencia gratuita de GSAP).
# Uso: bash instalar_web3d.sh   (guarda en $VIDEO_JEILER_MODELOS o ~/.cache/video-jeiler; NADA se copia al repo, que es público)
# Necesita internet, python3, node/npm y ffmpeg. Si ya hay un Chromium (en la nube viene uno en /opt/pw-browsers), no baja otro.
set -euo pipefail
BASE="${VIDEO_JEILER_MODELOS:-$HOME/.cache/video-jeiler}"
WEB="$BASE/web"
for c in ffmpeg npm python3; do command -v "$c" >/dev/null || { echo "Falta $c."; exit 1; }; done
mkdir -p "$WEB"
if [ ! -x "$BASE/venv/bin/python" ]; then python3 -m venv "$BASE/venv"; fi
"$BASE/venv/bin/pip" install --quiet playwright 2>&1 | grep -v "notice" || true
if [ ! -f "$WEB/three/build/three.module.js" ]; then
  T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
  (cd "$T" && npm pack three@0.187.0 gsap@3.15.1 --silent >/dev/null)
  for f in "$T"/*.tgz; do tar -xzf "$f" -C "$T" --one-top-level="$(basename "$f" .tgz)"; done
  rm -rf "$WEB/three" "$WEB/gsap"
  mkdir -p "$WEB/three" "$WEB/gsap"
  cp -r "$T"/three-*/package/build "$WEB/three/build"; cp "$T"/three-*/package/LICENSE "$WEB/three/LICENSE"
  cp "$T"/gsap-*/package/dist/gsap.min.js "$WEB/gsap/"; cp "$T"/gsap-*/package/LICENSE.md "$WEB/gsap/" 2>/dev/null || true
fi
head -c 300 "$WEB/three/LICENSE" | head -3
ya_hay() { for c in "${CHROMIUM_PATH:-}" /opt/pw-browsers/chromium "$(command -v chromium 2>/dev/null || true)" "$(command -v chromium-browser 2>/dev/null || true)" "$(command -v google-chrome 2>/dev/null || true)"; do [ -n "$c" ] && [ -x "$c" ] && [ ! -d "$c" ] && { echo "$c"; return 0; }; done; return 1; }
if c=$(ya_hay); then echo "Chromium encontrado: $c"; else echo "Bajando Chromium (~150 MB) ..."; "$BASE/venv/bin/python" -m playwright install chromium; fi
echo "LISTO. Python: $BASE/venv/bin/python   Librerías: $WEB"
