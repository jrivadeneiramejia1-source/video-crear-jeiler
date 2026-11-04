#!/usr/bin/env python3
"""Dibuja un video 2D cuadro a cuadro (Chromium sin pantalla + ffmpeg) a partir de un PROYECTO.json.

  python render.py PROYECTO.json verificar                    errores de la página; escenas seguidas y sin huecos; subtítulos dentro del video
  python render.py PROYECTO.json stills 2 10 30.5 [--carpeta stills]   guarda imágenes sueltas para MIRARLAS antes de renderizar
  python render.py PROYECTO.json hoja SALIDA.png [--n 8]      hoja de cuadros repartidos por todo el video
  python render.py PROYECTO.json video SALIDA.mp4 [--fps 30]  video SIN sonido (la voz y la música se pegan después)
Opciones:  --ancho N --alto N (el mismo proyecto sirve horizontal 1280x720 y vertical 720x1280 o 1080x1920)
           --extra archivo.js (repetible: más tipos de escena, p. ej. los de video-explicativo)   --motor CARPETA (otro motor)
PROYECTO.json: ver ejemplo/proyecto.json. Los tiempos están en segundos. Usar el Python de la instalación:
~/.cache/video-jeiler/venv/bin/python (bash instalar_render.sh). No sobrescribe un video que ya existe."""
import asyncio, json, os, pathlib, shutil, subprocess, sys
from playwright.async_api import async_playwright

AQUI = pathlib.Path(__file__).resolve().parent

def chromium():
    for c in (os.environ.get("CHROMIUM_PATH"), "/opt/pw-browsers/chromium", shutil.which("chromium"), shutil.which("chromium-browser"), shutil.which("google-chrome")):
        if c and os.access(c, os.X_OK) and not os.path.isdir(c): return c
    return None

def opciones(a):
    o = {"ancho": None, "alto": None, "fps": 30, "extra": [], "motor": str(AQUI.parent / "motor"), "carpeta": "stills", "n": 8}; rest = []; i = 0
    while i < len(a):
        if a[i] in ("--ancho", "--alto", "--fps", "--n"): o[a[i][2:]] = int(a[i + 1]); i += 2
        elif a[i] == "--extra": o["extra"].append(a[i + 1]); i += 2
        elif a[i] in ("--motor", "--carpeta"): o[a[i][2:]] = a[i + 1]; i += 2
        else: rest.append(a[i]); i += 1
    return rest, o

async def abrir(p, proyecto, o):
    pr = json.loads(pathlib.Path(proyecto).read_text(encoding="utf-8"))
    if o["ancho"]: pr["ancho"] = o["ancho"]
    if o["alto"]: pr["alto"] = o["alto"]
    pr.setdefault("ancho", 1280); pr.setdefault("alto", 720)
    ruta = chromium(); b = await p.chromium.launch(**({"executable_path": ruta} if ruta else {}))
    pg = await b.new_page(viewport={"width": pr["ancho"], "height": pr["alto"]}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    await pg.add_init_script("window.PROYECTO=" + json.dumps(pr))
    await pg.goto("file://" + str(pathlib.Path(o["motor"]) / "index.html")); await pg.wait_for_function("window.READY===true")
    for ex in o["extra"]: await pg.add_script_tag(path=ex)
    await pg.evaluate("Promise.all([400,600,700,800].map(w=>document.fonts.load(w+' 20px Inter')))")
    return b, pg, errs, pr

async def verificar(proyecto, o):
    async with async_playwright() as p:
        b, pg, errs, pr = await abrir(p, proyecto, o); ok = True; es = pr["escenas"]; total = await pg.evaluate("window.TOTAL")
        for i, e in enumerate(es):
            if e["fin"] <= e["inicio"]: print(f"  escena {i}: fin <= inicio"); ok = False
            if i and abs(e["inicio"] - es[i - 1]["fin"]) > 0.01: print(f"  hueco o choque entre las escenas {i - 1} y {i}"); ok = False
        for c in pr.get("cues", []):
            if c["b"] > total + 0.01 or c["a"] < 0: print(f"  subtítulo fuera del video: {c['a']}-{c['b']}"); ok = False
        for t in (0.0, total / 2, total - 0.05):   # dibujar tres cuadros para atrapar errores de las escenas
            try: await pg.evaluate(f"render({t})")
            except Exception as ex: errs.append(str(ex)[:200])
        print(f"duración {total:.2f} s, {len(es)} escenas, {len(pr.get('cues', []))} subtítulos | errores de la página: {errs or 'ninguno'}")
        await b.close(); return ok and not errs

async def stills(proyecto, tiempos, o):
    carpeta = pathlib.Path(o["carpeta"]); carpeta.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b, pg, errs, pr = await abrir(p, proyecto, o)
        for t in tiempos:
            await pg.evaluate(f"render({t})"); await pg.screenshot(path=str(carpeta / f"t_{t:07.2f}.png"))
        print("imágenes en", carpeta, "| errores de la página:", errs or "ninguno"); await b.close()

async def video(proyecto, salida, o):
    if pathlib.Path(salida).exists(): sys.exit(f"{salida} ya existe: elige otro nombre (no se sobrescribe).")
    fps = o["fps"]
    async with async_playwright() as p:
        b, pg, errs, pr = await abrir(p, proyecto, o); total = await pg.evaluate("window.TOTAL"); n = int(round(total * fps)); tmp = salida + ".tmp.mp4"
        ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                               "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp], stdin=subprocess.PIPE)
        for i in range(n):
            await pg.evaluate(f"render({i / fps})"); ff.stdin.write(await pg.screenshot(type="png"))
        ff.stdin.close(); ff.wait()
        if ff.returncode == 0: pathlib.Path(tmp).rename(salida)
        print(f"{pr['ancho']}x{pr['alto']} | cuadros {n} | duración {total:.2f} s | errores de la página: {errs or 'ninguno'} | ffmpeg {ff.returncode} -> {salida}"); await b.close()
        sys.exit(ff.returncode or (1 if errs else 0))

if __name__ == "__main__":
    rest, o = opciones(sys.argv[1:])
    if len(rest) < 2: sys.exit(__doc__)
    pr, modo = rest[0], rest[1]
    if modo == "verificar": sys.exit(0 if asyncio.run(verificar(pr, o)) else 1)
    elif modo == "stills": asyncio.run(stills(pr, [float(x) for x in rest[2:]], o))
    elif modo == "video" and len(rest) == 3: asyncio.run(video(pr, rest[2], o))
    elif modo == "hoja" and len(rest) == 3:
        d = json.loads(pathlib.Path(pr).read_text(encoding="utf-8")); total = max(e["fin"] for e in d["escenas"]); n = o["n"]; carpeta = pathlib.Path(rest[2]).with_suffix("")
        o["carpeta"] = str(carpeta) + "_cuadros"; ts = [round(total * (i + .5) / n, 2) for i in range(n)]; asyncio.run(stills(pr, ts, o))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-pattern_type", "glob", "-i", f"{o['carpeta']}/t_*.png", "-vf", f"scale=640:-2,tile=4x{(n + 3) // 4}:padding=4:color=0x202020", "-frames:v", "1", rest[2]], check=True)
        shutil.rmtree(o["carpeta"]); print("hoja:", rest[2])
    else: sys.exit(__doc__)
