#!/bin/bash
# Crea las pieles de Lila y Tito (personalizadas desde las de Kenney «Animated Characters 2», CC0) en ./pieles/
# Uso: bash crear_pieles.sh      (necesita el python con playwright de animacion-2d/scripts/instalar_render.sh y descargar_personajes.sh animated-characters-2)
set -euo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"; PY="${PYTHON_RENDER:-$HOME/.cache/video-jeiler/venv/bin/python}"
SK="${VIDEO_JEILER_MODELOS:-$HOME/.cache/video-jeiler}/personajes/animated-characters-2/Skins/Source"; mkdir -p "$AQUI/pieles"; P="$AQUI/../scripts/personalizar_piel.py"
"$PY" "$P" "$SK/skaterFemaleA.svg" "$AQUI/pieles/lila.png" --color "#38BB96=#F26B8A" --degradado gradient6=#F6C945,#F2B632 --degradado gradient7=#F6C945,#F2B632 --rellenar 18=#F6C945 --rellenar 16=#F2B632 --rellenar 2=#E0A62A --rellenar 46=#E0A62A
"$PY" "$P" "$SK/skaterMaleA.svg" "$AQUI/pieles/tito.png" --quitar 34 --agregar '<circle cx="321" cy="843" r="22" fill="#FFD23F"/>' --color "#EA3031=#2E7D4F" --degradado gradient6=#3C9D63,#4CB574 --degradado gradient7=#3C9D63,#4CB574 --rellenar 24=#4CB574
