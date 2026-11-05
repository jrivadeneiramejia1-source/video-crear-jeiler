#!/bin/bash
# Baja los muebles y la naturaleza de Kenney (CC0, vía OpenGameArt) para armar escenarios 3D con escena3d.py. Nunca se copian al repo.
# Uso: bash descargar_recursos.sh        (a $VIDEO_JEILER_MODELOS/recursos o ~/.cache/video-jeiler/recursos)
set -euo pipefail
BASE="${VIDEO_JEILER_MODELOS:-$HOME/.cache/video-jeiler}/recursos"; mkdir -p "$BASE"
bajar() {  # nombre carpeta url
  [ -d "$BASE/$2" ] && { echo "$1 ya está en $BASE/$2"; return; }
  tmp=$(mktemp -d); curl -fsSL --retry 3 -o "$tmp/r.zip" "$3"; unzip -q "$tmp/r.zip" -d "$tmp/c"
  if ! grep -rqiE "creative commons zero|CC0" "$tmp/c" --include="*.txt"; then echo "ATENCIÓN: $1 no declara CC0; no se instala."; rm -rf "$tmp"; exit 1; fi
  mv "$tmp/c" "$BASE/$2"; rm -rf "$tmp"; echo "$1 -> $BASE/$2 (CC0)"
}
bajar "Furniture Kit" muebles "https://opengameart.org/sites/default/files/kenney_furniturePack.zip"
bajar "Nature Kit" naturaleza "https://opengameart.org/sites/default/files/Nature%20Kit%20%282.1%29.zip"
bajar "Universal Animation Library (Quaternius)" ual1 "https://opengameart.org/sites/default/files/universal_animation_librarystandard.zip"
bajar "Universal Animation Library 2 (Quaternius)" ual2 "https://opengameart.org/sites/default/files/universal_animation_library_2standard.zip"
echo "Créditos (voluntarios, se agradecen): «Muebles y naturaleza de Kenney (kenney.nl) y animaciones de Quaternius (quaternius.com), CC0»."
