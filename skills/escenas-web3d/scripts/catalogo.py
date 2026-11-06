#!/usr/bin/env python3
"""Lista los modelos 3D bajados (con su ruta lista para poner en «modelo») y busca por palabra, también en español.

  python3 catalogo.py                       resumen por paquete
  python3 catalogo.py cama sofa             busca (español o inglés); muestra rutas
  python3 catalogo.py --paquete kaykit-muebles    todo lo de un paquete
Lee $VIDEO_JEILER_MODELOS/recursos3d o ~/.cache/video-jeiler/recursos3d (los baja descargar_paquetes.py)."""
import os, pathlib, re, sys, unicodedata
BASE = pathlib.Path(os.environ.get("VIDEO_JEILER_MODELOS", pathlib.Path.home() / ".cache" / "video-jeiler")) / "recursos3d"
SIN = {"cama": "bed", "sofa": "couch", "silla": "chair", "mesa": "table", "ventana": "window", "puerta": "door", "nevera": "fridge", "refrigerador": "fridge",
       "estufa": "stove oven", "cocina": "kitchen stove", "lampara": "lamp light", "alfombra": "rug carpet", "cuadro": "pictureframe", "planta": "plant houseplant cactus",
       "estante": "shelf bookshelf", "libro": "book", "bano": "bathroom toilet bathtub shower", "casa": "house building", "edificio": "building", "carro": "car", "calle": "street road",
       "semaforo": "trafficlight", "banca": "bench", "arbol": "tree", "pared": "wall", "piso": "floor", "escalera": "stairs", "caja": "box crate", "plato": "plate", "cortina": "curtains",
       "cajon": "drawer", "banco": "stool bank", "vaca": "cow", "perro": "pug", "doctor": "doctor", "chef": "chef cocinero", "obrero": "worker", "abuelo": "old oldclassy", "abuela": "old oldclassy",
       "mujer": "female", "hombre": "male", "nino": "casual", "personaje": "character", "mago": "mage", "caballero": "knight", "ladron": "rogue", "bruja": "witch"}
def norm(s): return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")
def modelos():
    for f in sorted(BASE.rglob("*")):
        if f.suffix.lower() in (".glb", ".gltf", ".fbx"): yield f.relative_to(BASE).as_posix()
a = sys.argv[1:]
if not BASE.exists(): sys.exit(f"No hay recursos en {BASE}. Ejecutar: python3 descargar_paquetes.py --todo")
todos = list(modelos())
if a and a[0] == "--paquete":
    for m in todos:
        if m.startswith(a[1] + "/") or m.startswith("quaternius/" + a[1].replace("quaternius-", "") + "/"): print(m)
elif a:
    claves = [set(re.split(r"\s+", norm(SIN.get(norm(p), p)))) | {norm(p)} for p in a]
    for m in todos:
        if any(any(k in norm(m) for k in ks) for ks in claves): print(m)
else:
    cuenta = {}
    for m in todos: cuenta.setdefault(m.rsplit("/", 1)[0], 0); cuenta[m.rsplit("/", 1)[0]] += 1
    for k, v in cuenta.items(): print(f"{k:28} {v:4} modelos")
