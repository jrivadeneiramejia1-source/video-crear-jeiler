#!/usr/bin/env python3
"""Cambia colores (pelo, ropa, piel) o quita dibujos de la piel de un personaje de Kenney, a partir de su archivo SVG de origen, y la dibuja de nuevo como PNG.
Uso:
  python3 personalizar_piel.py SKIN.svg --listar                       # muestra los colores y los elementos (para saber qué cambiar)
  python3 personalizar_piel.py SKIN.svg SALIDA.png [--color "#ORIG=#NUEVO" ...] [--degradado gradientN=#A,#B ...] [--rellenar N=#COLOR ...] [--quitar N ...] [--agregar '<circle .../>'] [--comparar ORIGINAL.png]
--color    cambia TODAS las apariciones de ese color (también en los degradados). Se puede repetir.
--degradado gradientN=#A,#B  cambia los colores de un degradado concreto (por ejemplo solo la camiseta, sin tocar el pantalón).
--rellenar N=#COLOR  cambia el relleno del elemento número N (para piezas sueltas, como la franja del frente de una camiseta).
--quitar   quita el elemento número N (de la lista de --listar), por ejemplo un dibujo que no va (una calavera en un cuento infantil).
--agregar  pone un trozo de SVG nuevo (en coordenadas de la textura 1024x1024) encima.
--comparar mide cuánto se parece el dibujo (sin cambios) al PNG original de Kenney, para saber que el dibujado es fiel.
Necesita python con playwright (el de `animacion-2d/scripts/instalar_render.sh`)."""
import collections, os, re, shutil, sys

a = sys.argv[1:]
def opts(n):
    r = []
    while n in a:
        i = a.index(n); r.append(a[i + 1]); del a[i:i + 2]
    return r
colores = opts("--color"); degradados = opts("--degradado"); rellenos = opts("--rellenar"); quitar = [int(x) for x in opts("--quitar")]; agregar = opts("--agregar"); comparar = (opts("--comparar") or [None])[0]
listar = "--listar" in a; a = [x for x in a if x != "--listar"]
if not a or not os.path.isfile(a[0]): sys.exit(__doc__)
svg = open(a[0], encoding="utf-8").read()
ELEM = re.compile(r"<(?:path|rect|circle|ellipse)\b[^>]*?/?>", re.S)
if listar:
    cnt = collections.Counter(c.upper() for c in re.findall(r"#[0-9a-fA-F]{6}", svg))
    print("Colores (color: veces):", ", ".join(f"{c}: {n}" for c, n in cnt.most_common()))
    for i, e in enumerate(ELEM.findall(svg)):
        f = re.search(r'fill="([^"]*)"', e); d = re.search(r' d="([^"]*)"', e); nums = [float(x) for x in re.findall(r"-?\d+\.?\d*", d.group(1))] if d else []
        xs, ys = nums[0::2], nums[1::2]
        print(f"{i:3d} relleno={f.group(1) if f else '-':18s} zona x[{min(xs):.0f},{max(xs):.0f}] y[{min(ys):.0f},{max(ys):.0f}]" if xs and ys else f"{i:3d} relleno={f.group(1) if f else '-'}")
    sys.exit(0)
if len(a) < 2: sys.exit(__doc__)
salida = a[1]
for c in colores:
    o, n = c.split("="); svg = re.sub(re.escape(o), n, svg, flags=re.I)
for d in degradados:
    gid, cols = d.split("="); cols = cols.split(",")
    def _cambia(m, cols=cols):
        it = iter(cols); return re.sub(r'stop-color="#[0-9A-Fa-f]{6}"', lambda _: f'stop-color="{next(it, cols[-1])}"', m.group(0))
    svg = re.sub(r'<linearGradient[^>]*id="%s"[^>]*>.*?</linearGradient>' % re.escape(gid), _cambia, svg, flags=re.S)
if rellenos:
    ms = list(ELEM.finditer(svg)); cambios = []
    for r in rellenos:
        n, c = r.split("="); m = ms[int(n)]; nuevo = re.sub(r'fill="[^"]*"', f'fill="{c}"', m.group(0), count=1) if 'fill="' in m.group(0) else m.group(0).replace("<path", f'<path fill="{c}"', 1)
        cambios.append((m.start(), m.end(), nuevo))
    for st, en, nuevo in sorted(cambios, reverse=True): svg = svg[:st] + nuevo + svg[en:]
if quitar:
    ms = list(ELEM.finditer(svg)); fuera = [(m.start(), m.end()) for i, m in enumerate(ms) if i in quitar]
    for s, e in sorted(fuera, reverse=True): svg = svg[:s] + svg[e:]
if agregar: svg = svg.replace("</svg>", "".join(agregar) + "</svg>")
svg = re.sub(r"<svg\b", '<svg width="1024" height="1024" viewBox="0 0 1024 1024"', svg, count=1)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    ruta = next((c for c in (os.environ.get("CHROMIUM_PATH"), "/opt/pw-browsers/chromium", shutil.which("chromium"), shutil.which("chromium-browser"), shutil.which("google-chrome")) if c and os.path.exists(c)), None)
    nav = p.chromium.launch(**({"executable_path": ruta} if ruta else {})); pg = nav.new_page(viewport={"width": 1024, "height": 1024})
    pg.set_content(f"<html><body style='margin:0;background:transparent'>{svg}</body></html>")
    pg.screenshot(path=salida, omit_background=True, clip={"x": 0, "y": 0, "width": 1024, "height": 1024}); nav.close()
print("escrito", salida)
if comparar:
    from PIL import Image; import numpy as np
    A = np.asarray(Image.open(salida).convert("RGBA")).astype(float); B = np.asarray(Image.open(comparar).convert("RGBA")).astype(float)
    m = (A[..., 3] > 250) & (B[..., 3] > 250); dif = np.abs(A[..., :3] - B[..., :3]).mean(axis=2)[m]
    print(f"parecido: {m.sum()} píxeles comparados; diferencia media {dif.mean():.2f} de 255; {100 * (dif > 24).mean():.2f} % con diferencia grande")
