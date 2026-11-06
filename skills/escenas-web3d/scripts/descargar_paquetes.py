#!/usr/bin/env python3
"""Baja paquetes de personajes, casas, muebles y ciudad con licencia CC0 a la carpeta de recursos (NADA entra al repo).

  python3 descargar_paquetes.py --lista                 paquetes disponibles
  python3 descargar_paquetes.py kaykit-muebles quaternius-casa     baja esos paquetes
  python3 descargar_paquetes.py --todo                  baja todos (unos 150 MB)
Destino: $VIDEO_JEILER_MODELOS/recursos3d o ~/.cache/video-jeiler/recursos3d. En el proyecto: "modelo": "kaykit-muebles/couch.gltf".
Antes de dejar cualquier archivo comprueba que la licencia diga CC0 (LICENSE.txt en los de GitHub; la página de OpenGameArt en los otros)."""
import io, os, pathlib, re, shutil, subprocess, sys, tempfile, urllib.parse, urllib.request, zipfile

BASE = pathlib.Path(os.environ.get("VIDEO_JEILER_MODELOS", pathlib.Path.home() / ".cache" / "video-jeiler")) / "recursos3d"
GH = "https://github.com/KayKit-Game-Assets/"
OGA = "https://opengameart.org/"
PAQUETES = {
 # nombre: (tipo, origen, qué copiar, carpeta destino, descripción)
 "kaykit-aventureros": ("git", GH + "KayKit-Character-Pack-Adventures-1.0.git", "Characters/gltf", "kaykit", "5 personajes con cara, esqueleto y 76 animaciones (caminar, sentarse, saludar...)"),
 "kaykit-muebles": ("git", GH + "KayKit-Furniture-Bits-1.0.git", "Assets/gltf", "kaykit-muebles", "camas, sofás, sillas, mesas, estantes, lámparas, alfombras, cuadros, plantas"),
 "kaykit-cocina": ("git", GH + "KayKit-Restaurant-Bits-1.0.git", "Assets/gltf", "kaykit-cocina", "cocina y restaurante: mesones, estufa, nevera, platos, comida"),
 "kaykit-prototipo": ("git", GH + "KayKit-Prototype-Bits-1.0.git", "Assets/gltf", "kaykit-prototipo", "paredes, ventanas, puertas, pisos, escaleras, cajas, barriles"),
 "kaykit-ciudad": ("git", GH + "KayKit-City-Builder-Bits-1.0.git", "Assets/gltf", "kaykit-ciudad", "edificios, calles, carros, semáforos, bancas, árboles"),
 "quaternius-personajes": ("oga", "content/animated-characters-pack", ("FBX", ".fbx"), "quaternius/personajes", "50 personas y criaturas (casual, chef, doctor, obrero, abuelos...) con 11 animaciones; la cara es negra con ojos blancos (usar «piel»)"),
 "quaternius-casa": ("oga", "content/lowpoly-house-interior-pack", ("FBX", ".fbx"), "quaternius/casa", "123 piezas de interior: camas, sofás, cocina, baño, puertas, ventana, lámparas, plantas"),
 "quaternius-edificios": ("oga", "content/lowpoly-buildings", ("FBX", ".fbx"), "quaternius/edificios", "10 edificios: casas, tienda, hospital, banco, apartamentos"),
 "quaternius-calle": ("oga", "content/lowpoly-modular-street-pack", ("FBX", ".fbx"), "quaternius/calle", "25 piezas de calle: tramos, esquinas, puentes, semáforos, señales, postes"),
 "quaternius-granja": ("oga", "content/lowpoly-animated-farm-animal-pack", ("FBX", ".fbx"), "quaternius/granja", "7 animales de granja con animación"),
}

def licencia_ok_oga(html):
    m = re.search(r'field-name-field-art-licenses.*?</div>\s*</div>', html, re.S)
    zona = m.group(0) if m else html
    return bool(re.search(r"CC0", zona)) and not re.search(r"CC-BY|GPL|OGA-BY", zona)

def bajar_git(nombre, url, sub, dest):
    t = pathlib.Path(tempfile.mkdtemp())
    try:
        subprocess.run(["git", "clone", "--depth", "1", "--quiet", url, str(t / "r")], check=True)
        lic = next(iter((t / "r").glob("LICENSE*")), None)
        if not lic or not re.search(r"Creative Commons Zero|CC0", lic.read_text(errors="ignore")): sys.exit(f"{nombre}: la licencia NO dice CC0; no se instala nada.")
        carpeta = next((t / "r").glob(f"**/{sub}")); dest.mkdir(parents=True, exist_ok=True)
        for f in carpeta.iterdir():
            if f.is_file(): shutil.copy2(f, dest / f.name)
        shutil.copy2(lic, dest / "LICENSE.txt")
    finally: shutil.rmtree(t, ignore_errors=True)

def bajar_oga(nombre, pagina, que, dest):
    html = urllib.request.urlopen(urllib.request.Request(OGA + pagina, headers={"User-Agent": "video-jeiler"}), timeout=60).read().decode("utf-8", "ignore")
    if not licencia_ok_oga(html): sys.exit(f"{nombre}: la página no dice solo CC0; no se instala nada.")
    zips = re.findall(r'href="(https://opengameart\.org/sites/default/files/[^"]+\.zip)"', html)
    if not zips: sys.exit(f"{nombre}: no se encontró el archivo .zip.")
    datos = urllib.request.urlopen(urllib.request.Request(zips[0], headers={"User-Agent": "video-jeiler"}), timeout=300).read()
    zf = zipfile.ZipFile(io.BytesIO(datos)); carpeta, ext = que; dest.mkdir(parents=True, exist_ok=True); n = 0
    for i in zf.infolist():
        if i.is_dir() or f"/{carpeta}/" not in i.filename or not i.filename.lower().endswith(ext): continue
        (dest / pathlib.Path(i.filename).name).write_bytes(zf.read(i)); n += 1
    (dest / "LICENSE.txt").write_text(f"CC0 1.0 (dominio público). Verificado en {OGA}{pagina} el día de la descarga.\n")
    if not n: sys.exit(f"{nombre}: el zip no traía archivos {ext} en {carpeta}.")

def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"): sys.exit(__doc__)
    if a[0] == "--lista":
        for k, v in PAQUETES.items(): print(f"{k:24} {v[4]}")
        return
    pedir = list(PAQUETES) if a[0] == "--todo" else a
    for nombre in pedir:
        if nombre not in PAQUETES: sys.exit(f"No existe «{nombre}». Usar --lista.")
        tipo, origen, que, carpeta, desc = PAQUETES[nombre]; dest = BASE / carpeta
        print(f"== {nombre}: {desc}")
        (bajar_git if tipo == "git" else bajar_oga)(nombre, origen, que, dest)
        print(f"   listo en {dest} ({sum(1 for f in dest.iterdir() if f.suffix.lower() in ('.glb', '.gltf', '.fbx'))} modelos)")
    print("Créditos sugeridos: KayKit (kaylousberg.com) y Quaternius (quaternius.com), CC0.")
main()
