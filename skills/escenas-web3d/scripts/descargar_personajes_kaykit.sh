#!/bin/bash
# Baja 5 personajes con esqueleto y animaciones (KayKit Adventurers 1.0, CC0) a la carpeta de recursos; NADA entra al repo.
# Uso: bash descargar_personajes_kaykit.sh      Después, en el proyecto: "modelo": "kaykit/Knight.glb", "clip": "Walking_A"
# Comprueba que su LICENSE.txt diga CC0 antes de dejar los archivos. Necesita git e internet (GitHub).
set -euo pipefail
BASE="${VIDEO_JEILER_MODELOS:-$HOME/.cache/video-jeiler}"; DEST="$BASE/recursos3d/kaykit"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
git clone --depth 1 --quiet https://github.com/KayKit-Game-Assets/KayKit-Character-Pack-Adventures-1.0.git "$T/kk"
grep -qiE "Creative Commons Zero|CC0" "$T/kk/LICENSE.txt" || { echo "La licencia NO dice CC0: no se instala nada."; exit 1; }
mkdir -p "$DEST"
cp "$T"/kk/addons/*/Characters/gltf/*.glb "$DEST/"; cp "$T/kk/LICENSE.txt" "$DEST/LICENSE.txt"
echo "LISTO en $DEST: $(ls "$DEST"/*.glb | xargs -n1 basename | tr '\n' ' ')"
echo "Crédito sugerido: «Personajes de KayKit (kaylousberg.com), CC0»."
