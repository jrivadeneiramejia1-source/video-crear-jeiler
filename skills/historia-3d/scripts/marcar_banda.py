#!/usr/bin/env python3
"""Pone sobre cada imagen fija (o cuadro) la BANDA de subtítulos (rojo) y la línea del margen de pies (amarillo) para ver a tamaño completo si algo importante queda tapado.
Uso:  python marcar_banda.py IMAGEN.png [IMAGEN2.png ...] [--carpeta SALIDA] [--banda 0.20] [--pies 0.16] [--arriba]
  --arriba  marca la banda de subtítulos arriba (para tomas con "subs": "arriba")
Escribe IMAGEN_banda.png (junto a la original o en --carpeta). Con --hoja ARCHIVO.png junta todas en una sola imagen (miniaturas, solo para ubicarse: la revisión se hace a tamaño completo)."""
import argparse, pathlib
from PIL import Image, ImageDraw
ap = argparse.ArgumentParser(); ap.add_argument("imagenes", nargs="+"); ap.add_argument("--carpeta", default=""); ap.add_argument("--banda", type=float, default=0.20); ap.add_argument("--pies", type=float, default=0.16); ap.add_argument("--arriba", action="store_true"); a = ap.parse_args()
for f in a.imagenes:
    im = Image.open(f).convert("RGBA"); w, h = im.size; ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    if a.arriba: d.rectangle([0, 0, w, a.banda * h], fill=(255, 0, 0, 70)); d.line([0, a.banda * h, w, a.banda * h], fill=(255, 0, 0, 255), width=2)
    else: d.rectangle([0, h * (1 - a.banda), w, h], fill=(255, 0, 0, 70)); d.line([0, h * (1 - a.banda), w, h * (1 - a.banda)], fill=(255, 0, 0, 255), width=2); d.line([0, h * (1 - a.pies), w, h * (1 - a.pies)], fill=(255, 220, 0, 255), width=2)
    sal = pathlib.Path(a.carpeta or pathlib.Path(f).parent); sal.mkdir(parents=True, exist_ok=True); o = sal / (pathlib.Path(f).stem + "_banda.png"); Image.alpha_composite(im, ov).convert("RGB").save(o); print(o)
