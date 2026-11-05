#!/usr/bin/env python3
"""Mide un guion de narración ANTES de producir: palabras, frases, duración estimada y avisos de estilo.
Uso:  python3 medir_guion.py GUION.txt [--voz sintetica|persona] [--duracion SEGUNDOS]
  GUION.txt   una frase por línea (o texto corrido; se parte en frases por . ? ! y saltos de línea). Las líneas que empiezan con # se ignoran.
  --voz       sintetica (Kokoro, ~0,40 s por palabra con pausas; por defecto) | persona (una persona leyendo, ~0,52 s por palabra con pausas)
  --duracion  duración buscada: dice cuántas palabras hacen falta y si el guion se pasa o se queda corto.
Los ritmos son medidas de pruebas anteriores; para tu voz o tu proyecto, medir una muestra real."""
import re, sys

a = sys.argv[1:]; voz = "sintetica"; dur = None
if "--voz" in a: i = a.index("--voz"); voz = a[i + 1]; del a[i:i + 2]
if "--duracion" in a: i = a.index("--duracion"); dur = float(a[i + 1]); del a[i:i + 2]
if len(a) != 1 or voz not in ("sintetica", "persona"): sys.exit(__doc__)
ritmo = 0.40 if voz == "sintetica" else 0.52
txt = " ".join(l.strip() for l in open(a[0], encoding="utf-8") if l.strip() and not l.strip().startswith("#"))
frases = [f.strip() for f in re.split(r"(?<=[.!?…])\s+", txt) if f.strip()]
if not frases: sys.exit("El guion está vacío.")
n = [len(f.split()) for f in frases]; total = sum(n); est = total * ritmo
print(f"{len(frases)} frases, {total} palabras | media {total / len(frases):.1f} palabras por frase, la más larga {max(n)}")
print(f"Duración estimada con voz {voz}: {est:.0f} s ({int(est // 60)}:{int(est % 60):02d})")
av = []
largas = [f for f, k in zip(frases, n) if k > 16]
if largas: av.append(f"{len(largas)} frase(s) de más de 16 palabras (difíciles de decir y de subtitular): «{largas[0][:60]}…»")
if total / len(frases) > 11: av.append("Frases largas en promedio (más de 11 palabras): partirlas con puntos.")
if txt.count(";"): av.append(f"{txt.count(';')} punto y coma: mejor puntos; la voz y los subtítulos los tratan mal.")
if txt.count(":") > 3: av.append(f"{txt.count(':')} dos puntos: dejar solo los que abren una cita.")
rep = [w for w in set(re.findall(r"[a-záéíóúñ]{5,}", txt.lower())) if len(re.findall(rf"\b{w}\b", txt.lower())) >= 6]
if rep: av.append("Palabras que se repiten mucho (6 veces o más): " + ", ".join(sorted(rep)[:6]))
if dur:
    meta = round(dur / ritmo); dif = est - dur
    print(f"Meta {dur:.0f} s -> unas {meta} palabras; el guion tiene {total} ({'sobran' if dif > 0 else 'faltan'} ~{abs(round(dif / ritmo))}).")
    if abs(dif) > dur * .15: av.append(f"La duración estimada se aleja más del 15 % de la meta ({est:.0f} s contra {dur:.0f} s).")
for x in av: print("AVISO:", x)
if not av: print("Sin avisos de estilo.")
