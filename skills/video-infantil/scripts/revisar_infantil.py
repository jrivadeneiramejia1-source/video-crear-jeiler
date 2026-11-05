#!/usr/bin/env python3
"""Revisión MEDIBLE de un video para niños: destellos, cortes por minuto, sustos de volumen y velocidad de lectura/narración.
Lo que una máquina NO puede medir (si algo asusta, si es violento, si enseña algo bueno) lo revisa una persona adulta.

Uso:  python3 revisar_infantil.py VIDEO [--srt SUBTITULOS.srt]
Mide:
 1) destellos: cambios fuertes de brillo seguidos; más de 3 en un segundo es el límite de la guía de accesibilidad WCAG 2.3.1 (riesgo para niños y adultos
    sensibles a luces). Aquí es una estimación simplificada (brillo medio del cuadro): no reemplaza una prueba formal.
 2) ritmo visual: cortes SECOS de escena por minuto (los fundidos suaves no se cuentan; guía sin calibrar: más de 12 por minuto es muy movido para niños pequeños).
 3) sustos de sonido: el momento más fuerte contra el volumen típico (la mediana; más de 8 LU de diferencia = golpe de volumen) y el pico real (> -1 dBTP).
 4) con --srt: letras por segundo y palabras por minuto (guía sin calibrar: más de 15 letras por segundo o 140 palabras por minuto es rápido para niños;
    los más pequeños casi no leen: conviene narrar).
Sale con código 1 si algún punto avisa."""
import re, subprocess, sys
import numpy as np

def run(*c): return subprocess.run(c, capture_output=True, text=True)
def secs(h, m, s, ms): return h * 3600 + m * 60 + s + ms / 1000

a = sys.argv[1:]; srt = None
if "--srt" in a: i = a.index("--srt"); srt = a[i + 1]; del a[i:i + 2]
if len(a) != 1: sys.exit(__doc__)
video = a[0]; av = []
dur = float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video).stdout or 0)
print(f"Video: {video} | {dur:.1f} s")

# 1) destellos
raw = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-i", video, "-vf", "fps=30,scale=64:36,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
fr = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 36 * 64).astype(float) / 255 if raw else np.zeros((0, 2304))
lum = fr.mean(axis=1) if len(fr) else np.array([]); flashes = []   # una "destello" = subida y bajada de brillo de al menos 0,10 con el estado oscuro por debajo de 0,8
if len(lum) > 3:
    sentido = 0; ext = lum[0]; ext_i = 0
    for i in range(1, len(lum)):
        d = lum[i] - ext
        if sentido >= 0 and d <= -0.10: sentido = -1; ext = lum[i]; ext_i = i; flashes.append(i) if min(lum[ext_i], ext) < 0.8 else None
        elif sentido <= 0 and d >= 0.10: sentido = 1; ext = lum[i]; ext_i = i
        elif (sentido == 1 and lum[i] > ext) or (sentido == -1 and lum[i] < ext): ext = lum[i]; ext_i = i
peor = max((sum(1 for f in flashes if t <= f < t + 30) for t in range(0, max(len(lum), 1), 5)), default=0)
print(f"1) destellos: el peor segundo tiene {peor} (límite: 3)  {'OK' if peor <= 3 else '<-- AVISO: posible riesgo de destellos'}")
if peor > 3: av.append("destellos")

# 2) ritmo visual
sc = run("ffmpeg", "-nostdin", "-i", video, "-vf", "select='gt(scene,0.35)',showinfo", "-an", "-f", "null", "-")
cortes = len(re.findall(r"pts_time:", sc.stderr)); porminuto = cortes / dur * 60 if dur else 0
print(f"2) ritmo visual: {cortes} cortes secos de escena (fundidos no cuentan), {porminuto:.1f} por minuto (guía: hasta 12)  {'OK' if porminuto <= 12 else '<-- AVISO: muy movido'}")
if porminuto > 12: av.append("ritmo visual")

# 3) sonido
e = run("ffmpeg", "-nostdin", "-i", video, "-vn", "-af", "ebur128=framelog=info:peak=true", "-f", "null", "-").stderr
M = [float(x) for x in re.findall(r"M:\s*(-?\d+\.?\d*)", e) if float(x) > -70]; I = re.findall(r"I:\s+(-?[\d.]+) LUFS", e); P = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)
if M and I:
    li = float(I[-1]); tipico = float(np.median(M)); salto = max(M) - tipico; pico = float(P[-1]) if P else None
    print(f"3) sonido: volumen típico {tipico:.1f} LUFS (integrado {li:.1f}), momento más fuerte {max(M):.1f} (diferencia {salto:.1f} LU; guía: hasta 8), pico real {pico} dBFS  {'OK' if salto <= 8 and (pico is None or pico <= -1) else '<-- AVISO: golpe de volumen o pico alto'}")
    if salto > 8 or (pico is not None and pico > -1): av.append("sonido")
else: print("3) sonido: no tiene audio medible")

# 4) lectura y narración
if srt:
    cues = []
    for b in re.split(r"\n\s*\n", open(srt, encoding="utf-8").read().strip().replace("\r", "")):
        m = re.search(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", b)
        if m:
            g = [int(x) for x in m.groups()]; txt = " ".join(l for l in b.split("\n")[1:] if "-->" not in l and l.strip()); cues.append((secs(*g[:4]), secs(*g[4:]), txt))
    cps = [len(t.replace(" ", "")) / max(b - a_, .2) for a_, b, t in cues]; pal = sum(len(t.split()) for _, _, t in cues); hablado = sum(b - a_ for a_, b, _ in cues)
    wpm = pal / hablado * 60 if hablado else 0
    mal = max(cps, default=0) > 15 or wpm > 140
    print(f"4) lectura: máximo {max(cps, default=0):.1f} letras por segundo (guía: 15), narración {wpm:.0f} palabras por minuto (guía: 140)  {'OK' if not mal else '<-- AVISO: rápido para niños'}")
    if mal: av.append("lectura")
print("AVISOS: " + (", ".join(av) if av else "ninguno") + ". Falta lo que no se mide: que nada asuste ni sea violento, que enseñe algo bueno y que un adulto lo haya visto entero.")
sys.exit(1 if av else 0)
