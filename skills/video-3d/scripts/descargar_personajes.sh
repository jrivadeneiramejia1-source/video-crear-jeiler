#!/bin/bash
# Baja personajes 3D ya hechos (con esqueleto y animaciones) de licencia CC0 (Kenney, vía OpenGameArt) a una carpeta tuya.
# Uso: bash descargar_personajes.sh [animated-characters-1 | animated-characters-2 | blocky-characters]   (sin argumento: los tres)
# Cada paquete se baja a su propia carpeta ~/.cache/video-jeiler/personajes/<paquete>/ y NUNCA se copia al repo. Se comprueba que su licencia diga CC0.
set -euo pipefail
BASE="${VIDEO_JEILER_MODELOS:-$HOME/.cache/video-jeiler}/personajes"; mkdir -p "$BASE"
declare -A ZIP=( [animated-characters-1]=kenney_animated-characters-1.zip [animated-characters-2]=kenney_animated-characters-2.zip [blocky-characters]=kenney_blocky-characters_2.0.zip )
paquetes=("$@"); [ ${#paquetes[@]} -gt 0 ] || paquetes=(animated-characters-1 animated-characters-2 blocky-characters)
for p in "${paquetes[@]}"; do
  [ -n "${ZIP[$p]:-}" ] || { echo "Paquete desconocido: $p"; exit 1; }
  d="$BASE/$p"; [ -d "$d" ] && { echo "$p ya está en $d"; continue; }
  tmp=$(mktemp -d); curl -fsSL --retry 3 -o "$tmp/p.zip" "https://opengameart.org/sites/default/files/${ZIP[$p]}"
  unzip -q "$tmp/p.zip" -d "$tmp/c"
  if ! grep -rqiE "creative commons zero|CC0" "$tmp/c" --include="*.txt"; then echo "ATENCIÓN: $p no declara CC0 en su License.txt; no se instala."; rm -rf "$tmp"; exit 1; fi
  mv "$tmp/c" "$d"; rm -rf "$tmp"; echo "$p -> $d (CC0)"
done
echo "Créditos (voluntarios, se agradecen): «Personajes de Kenney (kenney.nl), CC0»."
