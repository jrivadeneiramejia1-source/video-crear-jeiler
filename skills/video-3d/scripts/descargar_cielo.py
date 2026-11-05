#!/usr/bin/env python3
"""Baja un cielo (HDRI) de Poly Haven (CC0) para usarlo de fondo y de luz en escena3d.py. Solo usa la librería estándar de Python.
Uso:  python3 descargar_cielo.py --listar [palabra]          # busca cielos (ej.: overcast, sunset, clouds)
      python3 descargar_cielo.py ID [ID ...] [--tam 1k]      # baja a $VIDEO_JEILER_MODELOS/recursos/cielos/ID_1k.hdr
Ejemplos de ID: overcast_soil_puresky (nublado, lluvia), kloofendal_48d_partly_cloudy_puresky (parcialmente nublado).
Poly Haven publica todo en CC0 (pide, sin obligar, dar crédito). No se copian al repo."""
import json, os, pathlib, sys, urllib.request
BASE = pathlib.Path(os.environ.get("VIDEO_JEILER_MODELOS", pathlib.Path.home() / ".cache" / "video-jeiler")) / "recursos" / "cielos"
def api(ruta):
    r = urllib.request.Request("https://api.polyhaven.com" + ruta, headers={"User-Agent": "video-crear-jeiler"}); return json.load(urllib.request.urlopen(r, timeout=30))
a = sys.argv[1:]
if not a or a[0] in ("-h", "--help"): sys.exit(__doc__)
if a[0] == "--listar":
    q = (a[1] if len(a) > 1 else "").lower(); d = api("/assets?t=hdris")
    for k, v in sorted(d.items(), key=lambda kv: -kv[1].get("download_count", 0)):
        t = " ".join(v.get("tags", []) + v.get("categories", []) + [v["name"]]).lower()
        if q in t: print(f"{k} | {v['name']} | {', '.join(v.get('categories', []))}")
    sys.exit(0)
tam = "1k"
if "--tam" in a: i = a.index("--tam"); tam = a[i + 1]; del a[i:i + 2]
BASE.mkdir(parents=True, exist_ok=True)
for ident in a:
    destino = BASE / f"{ident}_{tam}.hdr"
    if destino.exists(): print(f"{ident} ya está en {destino}"); continue
    f = api(f"/files/{ident}").get("hdri", {}).get(tam, {}).get("hdr")
    if not f: sys.exit(f"{ident}: no hay tamaño {tam} en formato .hdr")
    urllib.request.urlretrieve(f["url"], destino); print(f"{ident} -> {destino} ({destino.stat().st_size // 1024} KB, CC0)")
print("Crédito (voluntario): «Cielos de Poly Haven (polyhaven.com), CC0».")
