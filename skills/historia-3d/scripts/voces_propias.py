#!/usr/bin/env python3
"""Usa GRABACIONES PROPIAS (voces de personas) en vez de la voz sintética, para que la duración real de cada frase mande en la línea de tiempo.
Lo usa crear_historia3d.py con  --voces-propias CARPETA  (no se corre solo).

Dos formas de entregar las grabaciones (se pueden mezclar; lo que falte se completa con voz sintética):
  1) UNA POR FRASE:    CARPETA/1_1.wav, 1_2.wav, 2_1.wav ...   (el número es «toma_frase»: sale en el guion que crea  crear_historia3d.py HISTORIA.json X --guion)
  2) UNA POR PERSONAJE: CARPETA/lila.wav, tito.wav, narrador.wav  (la persona lee todas sus frases de corrido, en orden).
     Se alinea con subtitulos/alinear_guion.py (de video-editar-jeiler): se transcribe, se compara con el guion y se corta cada frase. Revisar la tabla que imprime.
Formatos: wav, mp3, m4a, ogg, flac, opus, aac, mp4, mov (se usa el primer audio). Nunca se modifica el original: todo se escribe en SALIDA/voces/.
Limpieza (--limpiar): ia = audio-limpio (quita ruido con IA; necesita instalar_modelos.sh de video-editar-jeiler), ffmpeg = filtro simple, no = sin limpiar. Por defecto: ia si está instalada, si no ffmpeg.
PRIVACIDAD: las grabaciones de personas se quedan en una carpeta LOCAL. Nunca al repo público ni a servicios externos, y solo con permiso de su dueño
(si graba un niño o niña, con permiso de su mamá o papá). Este módulo se niega a leer de, o escribir en, una carpeta que Git rastrearía."""
import json, os, pathlib, re, subprocess, sys, tempfile, wave
import numpy as np

EXT = (".wav", ".mp3", ".m4a", ".ogg", ".flac", ".opus", ".aac", ".mp4", ".mov", ".webm", ".mkv")
SR = 48000
HOME = pathlib.Path.home() / ".cache" / "video-jeiler"
PY = os.environ.get("PYTHON_VOZ", str(HOME / "venv" / "bin" / "python"))

def carpeta_publica(ruta):
    """True si la carpeta está dentro de un repo de Git y alguno de los tipos de archivo de audio/video no está ignorado (Git podría subirlo)."""
    ruta = pathlib.Path(ruta).resolve(); ruta.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["git", "-C", str(ruta), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if r.returncode: return False
    return any(subprocess.run(["git", "-C", str(ruta), "check-ignore", "-q", str(ruta / ("x" + e))], capture_output=True).returncode != 0 for e in EXT + (".json", ".srt"))    # si algún tipo de archivo no está ignorado, Git podría subirlo

def buscar_herramienta(rel):
    cand = []
    if os.environ.get("EDITAR_SKILLS"): cand.append(pathlib.Path(os.environ["EDITAR_SKILLS"]) / rel)
    aqui = pathlib.Path(__file__).resolve()
    cand += [aqui.parents[3] / "video-editar-jeiler" / "skills" / rel, aqui.parents[4] / "jrivadeneiramejia1-source" / "video-editar-jeiler" / "skills" / rel, pathlib.Path.home() / ".claude" / "skills" / rel]
    return next((c for c in cand if c.exists()), None)

def decodificar(ruta, destino):
    r = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-i", str(ruta), "-vn", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(destino)], capture_output=True, text=True)
    if r.returncode: sys.exit(f"No pude leer el audio {ruta}: {r.stderr.strip()[:200]}")

def leer(ruta):
    with wave.open(str(ruta)) as w: x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return x

def escribir(ruta, x):
    with wave.open(str(ruta), "wb") as w: w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())

def limpiar(entrada, salida, modo):
    """entrada -> salida (wav mono 48 kHz). Devuelve el modo realmente usado."""
    if modo == "no": subprocess.run(["cp", str(entrada), str(salida)], check=True); return "no"
    if modo in ("ia", "auto"):
        s = buscar_herramienta("audio-limpio/scripts/limpiar_audio.py"); modelos = HOME / "modelos"
        if s and (modelos / "dpdfnet_baseline.onnx").exists():
            r = subprocess.run([PY, str(s), str(entrada), str(salida), "--lufs", "-20"], capture_output=True, text=True)
            if r.returncode == 0 and pathlib.Path(salida).exists(): return "ia"
            print("  (la limpieza con IA falló, uso el filtro simple)", r.stderr.strip()[-150:], flush=True)
        elif modo == "ia": print("  (no está instalada la limpieza con IA: corre video-editar-jeiler/skills/audio-limpio/scripts/instalar_modelos.sh; uso el filtro simple)", flush=True)
    subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-i", str(entrada), "-af", "highpass=f=80,afftdn=nf=-28,loudnorm=I=-20:TP=-2:LRA=11", "-ar", str(SR), "-ac", "1", str(salida)], check=True); return "ffmpeg"

def recortar_silencio(x, margen=0.12):
    """Quita el silencio del inicio y del final (deja un margen) y parejo el volumen de la voz."""
    if len(x) < SR // 10: return x
    v = int(0.01 * SR); n = len(x) // v; env = np.sqrt((x[:n * v].reshape(n, v) ** 2).mean(axis=1)); pico = env.max()
    if pico < 1e-4: return x
    act = np.where(env > max(pico * 0.05, 4 * np.percentile(env, 10)))[0]
    if not len(act): return x
    i = max(0, (act[0] * v) - int(margen * SR)); j = min(len(x), (act[-1] + 1) * v + int(margen * SR)); y = x[i:j]
    # volumen parejo entre frases: la parte con voz queda con el mismo nivel (RMS 0,08); el pico se limita a 0,9
    rms = np.sqrt((x[act[0] * v:(act[-1] + 1) * v] ** 2).mean()) + 1e-9; y = y * (0.08 / rms); p = np.abs(y).max()
    return y * (0.9 / p) if p > 0.9 else y

def entrada_de(carpeta, nombre):
    for e in EXT:
        for n in (nombre, nombre.upper()):
            f = carpeta / (n + e)
            if f.exists(): return f
    return None

def preparar(E, carpeta, out, limpieza="auto", completo=False):
    """E: {"voces": {...}, "lineas": [{id, quien, texto}]}. Escribe out/linea_<id>.wav de las frases con grabación propia. Devuelve {id: {archivo, dur, origen}} y una lista de avisos."""
    carpeta = pathlib.Path(carpeta).resolve(); out = pathlib.Path(out).resolve()
    if not carpeta.is_dir(): sys.exit(f"No existe la carpeta de voces propias: {carpeta}")
    if carpeta_publica(carpeta): sys.exit(f"La carpeta {carpeta} está dentro de un repo de Git y NO está ignorada: ahí no pongas grabaciones de personas (repo público). Usa una carpeta fuera del repo, por ejemplo ~/voces-propias.")
    if carpeta_publica(out): sys.exit(f"La carpeta de salida {out} está dentro de un repo de Git y NO está ignorada: con voces de personas, la salida debe quedar fuera del repo.")
    res = {}; avisos = []; tmp = pathlib.Path(tempfile.mkdtemp(prefix="voces_propias_"))
    def guardar(i, x, modo):
        x = recortar_silencio(x); f = out / f"linea_{i}.wav"; escribir(f, x); res[i] = {"archivo": f.name, "dur": round(len(x) / SR, 3), "origen": f"propia ({modo})"}
    # 1) una grabación por frase
    por_personaje = {}
    for l in E["lineas"]:
        f = entrada_de(carpeta, l["id"])
        if f:
            d = tmp / f"{l['id']}_bruto.wav"; decodificar(f, d); c = tmp / f"{l['id']}_limpio.wav"; modo = limpiar(d, c, limpieza); guardar(l["id"], leer(c), modo); print(f"  {l['id']:6s} {l['quien']:9s} {res[l['id']]['dur']:.2f} s  grabación propia ({f.name}, limpieza: {modo})", flush=True)
        else: por_personaje.setdefault(l["quien"], []).append(l)
    # 2) una grabación por personaje: transcribir, alinear con el guion y cortar
    for quien, ls in por_personaje.items():
        f = entrada_de(carpeta, quien)
        if not f: continue
        tr = buscar_herramienta("subtitulos/scripts/transcribir.py"); al = buscar_herramienta("subtitulos/scripts/alinear_guion.py")
        if not (tr and al): sys.exit("Para usar una grabación por personaje hace falta el repo video-editar-jeiler (subtitulos/scripts/transcribir.py y alinear_guion.py). Clónalo junto a este repo o pon EDITAR_SKILLS=/ruta/a/video-editar-jeiler/skills.")
        d = tmp / f"{quien}_bruto.wav"; decodificar(f, d); c = tmp / f"{quien}_limpio.wav"; modo = limpiar(d, c, limpieza)
        pj = tmp / f"{quien}_palabras.json"; r = subprocess.run([PY, str(tr), str(c), str(pj)], capture_output=True, text=True)
        if r.returncode: sys.exit(f"No pude transcribir {f.name} (¿está instalado video-editar-jeiler/skills/audio-limpio/scripts/instalar_modelos.sh?): {r.stderr.strip()[-300:]}")
        cues = tmp / f"{quien}_cues.txt"; cues.write_text("\n".join(re.sub(r"\s+", " ", l["texto"]).strip() for l in ls) + "\n", encoding="utf-8")
        sj = tmp / f"{quien}_tiempos.json"; r = subprocess.run([PY, str(al), str(cues), str(pj), str(sj)], capture_output=True, text=True, cwd=str(al.parent))
        if r.returncode: sys.exit(f"Falló alinear_guion.py con {quien}: {r.stderr.strip()[-300:]}")
        print(f"  --- {quien}: {f.name} ({len(ls)} frases), alineación con el guion ---\n" + "\n".join("  " + z for z in r.stdout.strip().splitlines()), flush=True)
        T = json.load(open(sj, encoding="utf-8")); x = leer(c)
        for l, t in zip(ls, T):
            if len(T) != len(ls): break
            guardar(l["id"], x[max(0, int((t["a"] - 0.12) * SR)):min(len(x), int((t["b"] + 0.05) * SR))], modo + ", cortada")
        for z in r.stdout.splitlines():
            if "REVISAR" in z: avisos.append(f"{quien}: {z.strip()}")
    faltan = [l["id"] for l in E["lineas"] if l["id"] not in res]
    if faltan and completo: sys.exit("Faltan grabaciones para las frases: " + ", ".join(faltan))
    if faltan: print(f"  Sin grabación (se hará con voz sintética): {', '.join(faltan)}", flush=True)
    return res, avisos
