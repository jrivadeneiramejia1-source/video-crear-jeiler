#!/usr/bin/env python3
"""¿Es el MISMO personaje en distintas escenas o clips? Compara los colores del centro de varias imágenes (cuadros o fijas).

Uso:  python3 comparar_cuadros.py REFERENCIA.png OTRA1.png OTRA2.png ... [--umbral 0.35]
Cada imagen se reduce y se mira la zona central (donde suele estar el personaje); se compara su paleta de colores con la de la referencia:
distancia 0 = mismos colores, 1 = ninguno en común. Si pasa del umbral (0,35 por defecto, una guía sin calibrar) avisa «posible cambio de personaje».
Es una ALARMA barata, no un juez: no ve la forma de la cara ni del pelo (eso lo revisa una persona con la hoja de personaje). Sale con 1 si algo avisa."""
import subprocess, sys
import numpy as np

def hist(png):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", png, "-vf", "scale=256:-2,crop=iw*0.4:ih*0.8:iw*0.3:ih*0.1,scale=64:64", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    if len(r.stdout) != 64 * 64 * 3: sys.exit(f"No pude leer {png}")
    px = np.frombuffer(r.stdout, dtype=np.uint8).reshape(-1, 3) // 32   # 8 niveles por canal = 512 casillas
    h = np.bincount(px[:, 0] * 64 + px[:, 1] * 8 + px[:, 2], minlength=512).astype(float); return h / h.sum()

a = sys.argv[1:]; umbral = 0.35
if "--umbral" in a: i = a.index("--umbral"); umbral = float(a[i + 1]); del a[i:i + 2]
if len(a) < 2: sys.exit(__doc__)
ref = hist(a[0]); mal = False
for f in a[1:]:
    d = 1 - float(np.minimum(ref, hist(f)).sum()); flag = d > umbral; mal |= flag
    print(f"{f}: distancia {d:.2f}  {'<-- posible cambio de personaje' if flag else 'igual'}")
sys.exit(1 if mal else 0)
