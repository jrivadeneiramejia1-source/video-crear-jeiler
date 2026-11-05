#!/usr/bin/env python3
"""Saca la «receta» MEDIBLE de un video de referencia para copiar su ESTILO (nunca su contenido): formato, ritmo, tramos, colores, audio y una hoja de cuadros.

Uso:  python3 receta.py VIDEO [--salida CARPETA] [--hoja-cada 2.5]
Deja en CARPETA (por defecto receta_<nombre>/):  receta.md (para leer) | receta.json | hoja.png (cuadros para mirar)
Mide: duración y formato; cambios bruscos de imagen (cortes o destellos); actividad visual por segundo (cuánto cambia la imagen); tramos (cambios fuertes de color); paleta (6 colores);
      volumen (LUFS, pico), silencios y tempo aproximado de la música.
NO mide (lo mira o lo escucha una persona, o Claude sobre la hoja de cuadros): de qué trata, el texto en pantalla, si hay voz, la técnica, los derechos.
Los umbrales son guías sin calibrar. Solo usa ffmpeg y numpy; no sube nada a internet."""
import colorsys, json, os, re, subprocess, sys
import numpy as np

def run(*c): return subprocess.run(c, capture_output=True, text=True)

a = sys.argv[1:]; salida = None; hoja_cada = 2.5
if "--salida" in a: i = a.index("--salida"); salida = a[i + 1]; del a[i:i + 2]
if "--hoja-cada" in a: i = a.index("--hoja-cada"); hoja_cada = float(a[i + 1]); del a[i:i + 2]
if len(a) != 1 or not os.path.isfile(a[0]): sys.exit(__doc__)
video = a[0]; nombre = os.path.splitext(os.path.basename(video))[0]
salida = salida or f"receta_{nombre}"; os.makedirs(salida, exist_ok=True)

# ---- ficha ----
pj = json.loads(run("ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate", "-of", "json", video).stdout or "{}")
vs = [s for s in pj.get("streams", []) if s.get("codec_type") == "video"]; au = [s for s in pj.get("streams", []) if s.get("codec_type") == "audio"]
if not vs: sys.exit("El archivo no tiene imagen.")
dur = float(pj["format"]["duration"]); W0, H0 = vs[0]["width"], vs[0]["height"]
num, den = (vs[0].get("r_frame_rate") or "30/1").split("/"); fps0 = float(num) / float(den or 1) if float(den or 1) else 0
forma = "vertical (9:16)" if H0 > W0 * 1.5 else "vertical" if H0 > W0 else "horizontal" if W0 > H0 else "cuadrado"

# ---- imagen: cuadros pequeños ----
FPS = min(4.0, 2400.0 / max(dur, 1))
raw = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-i", video, "-vf", f"fps={FPS},scale=64:64:flags=area,format=rgb24", "-an", "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, 64, 64, 3) if raw else np.zeros((0, 64, 64, 3), np.uint8)
n = len(fr); seg = int(np.ceil(n / FPS)) if n else 0
act = np.abs(np.diff(fr.astype(np.int16), axis=0)).mean(axis=(1, 2, 3)) / 255 if n > 1 else np.zeros(0)
bri = fr.mean(axis=(1, 2, 3)) / 255 if n else np.zeros(0)
def nivel(x): return "quieto" if x < .01 else "suave" if x < .04 else "movido" if x < .10 else "muy movido"
por_seg = [float(act[int(s * FPS):int((s + 1) * FPS)].mean()) if len(act[int(s * FPS):int((s + 1) * FPS)]) else 0.0 for s in range(seg)]
barras = "▁▂▃▄▅▆▇█"; mx = max(por_seg + [1e-6]); spark = "".join(barras[min(7, int(v / mx * 7.999))] for v in por_seg)

# cambios bruscos de imagen entre dos cuadros (cortes secos o destellos); umbral 0,20 sin calibrar: con 0,30 se escapa un corte entre colores de brillo parecido
sc = run("ffmpeg", "-nostdin", "-i", video, "-vf", "select='gt(scene,0.20)',showinfo", "-an", "-f", "null", "-")
cortes = [round(float(t), 2) for t in re.findall(r"pts_time:([\d.]+)", sc.stderr)]

# firma de color por segundo (histograma 4x4x4) y tramos
def firma(bloque):
    q = (bloque.reshape(-1, 3) // 64).astype(int); idx = q[:, 0] * 16 + q[:, 1] * 4 + q[:, 2]
    h = np.bincount(idx, minlength=64).astype(float); return h / max(h.sum(), 1)
sig = [firma(fr[int(s * FPS):max(int((s + 1) * FPS), int(s * FPS) + 1)]) for s in range(seg)] if n else []
d = np.zeros(seg)
for s in range(2, seg - 1):
    izq = np.mean(sig[max(0, s - 2):s], axis=0); der = np.mean(sig[s:s + 2], axis=0); d[s] = 0.5 * np.abs(izq - der).sum()
lim = []; UM = 0.18
for s in range(2, seg - 1):
    if d[s] >= UM and d[s] == d[max(0, s - 2):s + 3].max() and (not lim or s - lim[-1] >= 3): lim.append(s)
for c in cortes:
    s = int(round(c))
    if 0 < s < seg and all(abs(s - l) >= 2 for l in lim): lim.append(s)
lim = sorted(lim); bordes = [0] + lim + [dur]

def nombre_color(rgb):
    r, g, b = [x / 255 for x in rgb]; h, s, v = colorsys.rgb_to_hsv(r, g, b); h *= 360
    if v < .15: return "negro"
    if s < .15: return "blanco" if v > .85 else "gris claro" if v > .6 else "gris" if v > .35 else "gris oscuro"
    base = ("rojo" if h < 15 or h >= 345 else "naranja" if h < 40 else "amarillo" if h < 70 else "verde" if h < 165 else "turquesa" if h < 200
            else "azul" if h < 255 else "violeta" if h < 290 else "rosa" if h < 345 else "rojo")
    if base == "naranja" and v < .55: base = "café"
    return base + (" oscuro" if v < .4 and base != "café" else "")
def hexa(rgb): return "#%02X%02X%02X" % tuple(int(x) for x in rgb)
def kmeans(px, k=6, it=12):
    rng = np.random.default_rng(0); c = px[rng.choice(len(px), k, replace=False)].astype(float)
    for _ in range(it):
        lab = ((px[:, None, :].astype(float) - c[None]) ** 2).sum(-1).argmin(1)
        for j in range(k):
            if (lab == j).any(): c[j] = px[lab == j].mean(0)
    cnt = np.bincount(lab, minlength=k); o = np.argsort(-cnt); return c[o], cnt[o] / cnt.sum()
paleta = []
if n:
    rng = np.random.default_rng(1); px = fr.reshape(-1, 3); px = px[rng.choice(len(px), min(15000, len(px)), replace=False)]
    cs, sh = kmeans(px); paleta = [{"hex": hexa(c), "nombre": nombre_color(c), "parte": round(float(p), 3)} for c, p in zip(cs, sh)]
tramos = []
for i in range(len(bordes) - 1):
    t0, t1 = bordes[i], bordes[i + 1]; i0, i1 = int(t0 * FPS), max(int(t1 * FPS), int(t0 * FPS) + 1)
    sub = fr[i0:i1]
    if not len(sub): continue
    c3, p3 = kmeans(sub.reshape(-1, 3)[::3], k=3, it=8)
    tramos.append({"de": round(float(t0), 1), "a": round(float(t1), 1), "actividad": nivel(float(act[max(i0 - 1, 0):max(i1 - 1, 1)].mean()) if len(act) else 0),
                   "brillo": round(float(bri[i0:i1].mean()), 2), "colores": [f"{hexa(c)} {nombre_color(c)}" for c in c3]})

# ---- audio ----
audio = {"tiene": bool(au)}
if au:
    e = run("ffmpeg", "-nostdin", "-i", video, "-af", "ebur128=peak=true", "-vn", "-f", "null", "-").stderr
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", e); L = re.findall(r"LRA:\s+([\d.]+) LU", e); P = re.findall(r"Peak:\s+(-?[\d.]+|-?inf) dBFS", e)
    s = run("ffmpeg", "-nostdin", "-i", video, "-af", "silencedetect=n=-50dB:d=0.3", "-vn", "-f", "null", "-").stderr
    sil = sum(float(x) for x in re.findall(r"silence_duration:\s*([\d.]+)", s))
    audio.update(lufs=float(I[-1]) if I else None, lra=float(L[-1]) if L else None, pico_dbfs=float(P[-1]) if P and "inf" not in P[-1] else None, silencio_pct=round(100 * sil / dur, 1))
    sr = 11025; pcm = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-i", video, "-vn", "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(pcm, np.float32); N, hop = 1024, 256
    if len(x) > N * 8:
        win = np.hanning(N); fl = (len(x) - N) // hop; M = np.abs(np.array([np.fft.rfft(x[i * hop:i * hop + N] * win) for i in range(fl)]))
        env = np.maximum(np.diff(np.log1p(10 * M), axis=0), 0).sum(1); env = env - env.mean(); ac = np.correlate(env, env, "full")[len(env) - 1:]
        lo, hi = int(60 / 180 * sr / hop), int(60 / 60 * sr / hop); 
        if hi < len(ac) and ac[0] > 0:
            k = lo + int(np.argmax(ac[lo:hi])); bpm = 60 * sr / hop / k; conf = min(float(ac[k] / max(ac[lo:hi].mean(), 1e-9)), 99.0)
            audio.update(tempo_bpm=round(float(bpm)), tempo_confianza=round(conf, 1))
    audio["aviso"] = "pico en 0 dBFS o más = sonido recortado (saturado)" if audio.get("pico_dbfs") is not None and audio["pico_dbfs"] >= -0.1 else None

# ---- hoja de cuadros ----
cols = 8; esc = 216 if H0 > W0 else 320
subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-i", video, "-vf", f"fps=1/{hoja_cada},scale={esc}:-2,tile={cols}x{max(1, int(np.ceil(dur / hoja_cada / cols)))}:padding=4:color=black", "-frames:v", "1", os.path.join(salida, "hoja.png")], capture_output=True)

# ---- salida ----
R = {"archivo": os.path.basename(video), "duracion_s": round(dur, 2), "tamano": f"{W0}x{H0}", "forma": forma, "fps": round(fps0, 1), "cortes_secos_s": cortes,
     "cortes_por_minuto": round(len(cortes) / dur * 60, 1), "actividad_por_segundo": [round(v, 3) for v in por_seg], "tramos": tramos, "paleta": paleta, "audio": audio,
     "hoja_cada_s": hoja_cada, "nota": "Medidas sin calibrar; texto en pantalla, voz, tema y derechos: los revisa una persona."}
json.dump(R, open(os.path.join(salida, "receta.json"), "w"), ensure_ascii=False, indent=1)
M = [f"# Receta de «{R['archivo']}» (solo para estudiar el estilo)", "",
     f"- **Formato:** {R['tamano']}, {forma}, {R['fps']} cuadros por segundo, {R['duracion_s']} s.",
     f"- **Cambios bruscos de imagen (cortes o destellos):** {len(cortes)} ({R['cortes_por_minuto']} por minuto)" + (f", en {', '.join(str(c) + ' s' for c in cortes)}." if cortes else ". El video cambia con movimiento continuo, no con cortes."),
     "", "## Ritmo visual (cuánto cambia la imagen cada segundo)", "```", spark, f"0 s{' ' * max(1, len(spark) - 8)}{R['duracion_s']:.0f} s", "```",
     "Barras altas = mucho cambio (algo se dibuja o se mueve); bajas = imagen casi quieta.", "", "## Tramos (donde cambian los colores o el movimiento)",
     "| De | A | Movimiento | Brillo | Colores dominantes |", "|---|---|---|---|---|"]
M += [f"| {t['de']} s | {t['a']} s | {t['actividad']} | {t['brillo']} | {', '.join(t['colores'])} |" for t in tramos]
M += ["", "## Paleta general", ", ".join(f"{p['hex']} {p['nombre']} ({round(p['parte'] * 100)} %)" for p in paleta), "", "## Audio"]
if audio["tiene"]:
    M.append(f"- Volumen {audio.get('lufs')} LUFS, rango {audio.get('lra')} LU, pico {audio.get('pico_dbfs')} dBFS; silencio {audio.get('silencio_pct')} %." + (f" **{audio['aviso']}.**" if audio.get("aviso") else ""))
    if "tempo_bpm" in audio: M.append(f"- Tempo aproximado: {audio['tempo_bpm']} pulsos por minuto (confianza {audio['tempo_confianza']}; menos de 2 = poco claro).")
else: M.append("- Sin audio.")
M += ["", "## Falta (se mira con `hoja.png` y se escucha)", "- De qué trata, texto en pantalla, si hay voz o solo música, y con qué técnica se hizo.",
      "- Marcas de agua y nombres de usuario: **no se copian** (son de otra persona).", "- Derechos del video, la música, las imágenes y el texto: son de su autor.", "",
      "_Medidas sin calibrar: sirven para comparar, no son verdades absolutas._"]
open(os.path.join(salida, "receta.md"), "w", encoding="utf-8").write("\n".join(M) + "\n")
print("\n".join(M))
print(f"\nArchivos en {salida}/: receta.md, receta.json, hoja.png")
