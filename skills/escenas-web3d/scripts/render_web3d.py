#!/usr/bin/env python3
"""Dibuja una escena 3D (Three.js + GSAP en Chromium sin pantalla) cuadro a cuadro y la une con ffmpeg.

  python render_web3d.py PROYECTO.json verificar                  errores de la página y duración
  python render_web3d.py PROYECTO.json stills 0 2.5 7 [--carpeta stills]   imágenes sueltas para MIRAR antes del video
  python render_web3d.py PROYECTO.json hoja SALIDA.png [--n 8]    hoja de cuadros repartidos
  python render_web3d.py PROYECTO.json video SALIDA.mp4 [--fps 30]  video SIN sonido
Opciones: --ancho N --alto N (horizontal 1280x720 o vertical 720x1280)   --libs CARPETA (por defecto ~/.cache/video-jeiler/web)
          --recursos CARPETA (modelos .glb e imágenes; por defecto ~/.cache/video-jeiler/recursos3d; también se buscan junto al PROYECTO.json)
Usar el Python de la instalación (bash instalar_web3d.sh): ~/.cache/video-jeiler/venv/bin/python. No sobrescribe videos existentes."""
import asyncio, functools, http.server, json, os, pathlib, shutil, subprocess, sys, threading, urllib.parse
from playwright.async_api import async_playwright

AQUI = pathlib.Path(__file__).resolve().parent
ARGS_GL = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--no-sandbox"]

def chromium():
    for c in (os.environ.get("CHROMIUM_PATH"), "/opt/pw-browsers/chromium", shutil.which("chromium"), shutil.which("chromium-browser"), shutil.which("google-chrome")):
        if c and os.access(c, os.X_OK) and not os.path.isdir(c): return c

def opciones(a):
    o = {"ancho": None, "alto": None, "fps": 30, "n": 8, "carpeta": "stills", "libs": os.environ.get("VIDEO_JEILER_MODELOS", str(pathlib.Path.home() / ".cache/video-jeiler")) + "/web", "recursos": os.environ.get("VIDEO_JEILER_MODELOS", str(pathlib.Path.home() / ".cache/video-jeiler")) + "/recursos3d"}; r = []; i = 0
    while i < len(a):
        if a[i] in ("--ancho", "--alto", "--fps", "--n"): o[a[i][2:]] = int(a[i + 1]); i += 2
        elif a[i] in ("--carpeta", "--libs", "--recursos"): o[a[i][2:]] = a[i + 1]; i += 2
        else: r.append(a[i]); i += 1
    return r, o

def servir(libs, carpetas):
    """Sirve el motor, las librerías y los modelos/imágenes por http local (los módulos de Three.js no cargan desde file://).
    /m/RUTA se busca en las carpetas dadas (la del proyecto y la de recursos); nunca fuera de ellas."""
    motor, base = str(AQUI.parent / "motor"), pathlib.Path(libs)
    carpetas = [pathlib.Path(c).resolve() for c in carpetas]
    class H(http.server.SimpleHTTPRequestHandler):
        def translate_path(self, p):
            p = p.split("?")[0]
            if p.startswith(("/three/", "/gsap/")): return str(base / p.lstrip("/"))
            if p.startswith("/m/"):
                r = urllib.parse.unquote(p[3:])
                for c in carpetas:
                    f = (c / r).resolve()
                    if f.is_file() and f.is_relative_to(c): return str(f)
                return str(base / "no-existe")
            return str(pathlib.Path(motor) / (p.lstrip("/") or "index.html"))
        def log_message(self, *a): pass
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=s.serve_forever, daemon=True).start(); return s

async def abrir(p, proyecto, o):
    pr = json.loads(pathlib.Path(proyecto).read_text(encoding="utf-8"))
    if o["ancho"]: pr["ancho"] = o["ancho"]
    if o["alto"]: pr["alto"] = o["alto"]
    pr.setdefault("ancho", 1280); pr.setdefault("alto", 720)
    if not (pathlib.Path(o["libs"]) / "three/build/three.module.js").exists(): sys.exit("Faltan Three.js y GSAP: ejecutar bash instalar_web3d.sh")
    srv = servir(o["libs"], [pathlib.Path(proyecto).resolve().parent, o["recursos"]]); ruta = chromium()
    b = await p.chromium.launch(args=ARGS_GL, **({"executable_path": ruta} if ruta else {}))
    pg = await b.new_page(viewport={"width": pr["ancho"], "height": pr["alto"]}); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
    await pg.add_init_script("window.PROYECTO=" + json.dumps(pr))
    await pg.goto(f"http://127.0.0.1:{srv.server_port}/index.html"); await pg.wait_for_function("window.READY===true || window.FALLO", timeout=120000)
    fallo = await pg.evaluate("window.FALLO || null")
    if fallo: await b.close(); srv.shutdown(); sys.exit("Error en la escena: " + fallo)
    return b, pg, errs, pr, srv

async def cuadro(pg, t):
    await pg.evaluate(f"render({t})"); return await pg.screenshot(type="png")

async def main():
    r, o = opciones(sys.argv[1:])
    if len(r) < 2: sys.exit(__doc__)
    proyecto, modo = r[0], r[1]
    if modo == "video" and (len(r) < 3 or pathlib.Path(r[2]).exists()): sys.exit("Falta la salida o ya existe (no se sobrescribe).")
    async with async_playwright() as p:
        b, pg, errs, pr, srv = await abrir(p, proyecto, o); total = await pg.evaluate("window.TOTAL"); ok = True
        if modo == "verificar":
            for t in (0, total / 2, total - 0.05): await pg.evaluate(f"render({t})")
            print(f"duración {total:.2f} s, {len(pr.get('objetos', []))} objetos | errores de la página: {errs or 'ninguno'}"); ok = not errs
            info = await pg.evaluate("window.INFO")
            for ac in info.get("acciones", []):
                if "natural" in ac: print(f"  camina {ac['id']} {ac['a']}-{ac['b']} s: {ac['distancia']} m a {ac['velocidad']} m/s (animación natural {ac['natural']} m/s, ajuste x{ac['factor']})")
            for av in info.get("avisos", []): print("  AVISO:", av)
            for mo in info["modelos"]: print(f"  modelo {mo['id']} ({mo['modelo']}): alto natural {mo['alto_natural']}; clips = {', '.join(mo['clips']) or 'ninguno'}")
        elif modo == "stills":
            c = pathlib.Path(o["carpeta"]); c.mkdir(exist_ok=True)
            for t in r[2:]: (c / f"t{float(t):06.2f}.png").write_bytes(await cuadro(pg, float(t))); print("guardado", c / f"t{float(t):06.2f}.png")
        elif modo == "hoja":
            ts = [total * i / max(o["n"] - 1, 1) * 0.999 for i in range(o["n"])]; d = pathlib.Path(r[2]).with_suffix(".tmp"); d.mkdir(exist_ok=True)
            for i, t in enumerate(ts): (d / f"{i:02d}.png").write_bytes(await cuadro(pg, t))
            cols = 4 if o["n"] > 4 else o["n"]; rows = -(-o["n"] // cols)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(d / "%02d.png"), "-vf", f"scale=480:-1,tile={cols}x{rows}", "-frames:v", "1", r[2]], check=True)
            shutil.rmtree(d); print("hoja guardada en", r[2])
        elif modo == "video":
            n = int(round(total * o["fps"]))
            ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(o["fps"]), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", r[2]], stdin=subprocess.PIPE)
            for i in range(n): ff.stdin.write(await cuadro(pg, i / o["fps"]))
            ff.stdin.close(); ok = ff.wait() == 0 and not errs; print(f"{n} cuadros -> {r[2]} | errores de la página: {errs or 'ninguno'}")
        await b.close(); srv.shutdown()
    sys.exit(0 if ok else 1)

asyncio.run(main())
