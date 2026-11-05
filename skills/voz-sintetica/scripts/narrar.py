#!/usr/bin/env python3
"""Convierte un texto en voz (Kokoro, sin internet) y guarda el tiempo exacto de cada frase.

Uso:  python narrar.py TEXTO.txt SALIDA.wav [--voz ef_dora] [--velocidad 1.0] [--pausa 0.45] [--tiempos tiempos.json]
      python narrar.py --voces            (lista las voces; las de español empiezan con e: ef_dora, em_alex, em_santa)
TEXTO.txt: una frase por línea (las líneas vacías o que empiezan con # se ignoran). Cada línea se dice como una unidad.
SALIDA.wav: mono, 24 kHz, sin normalizar (ver audio-limpio o ffmpeg-skill para el volumen final).
tiempos.json: [{"texto": ..., "inicio": s, "fin": s}] -> sirve para subtítulos y para la duración de cada escena SIN reconocer la voz.
Es una VOZ SINTÉTICA: declararlo al publicar. No imita a ninguna persona; clonar una voz exige permiso escrito (no está en esta skill).
Usar el Python de la instalación: ~/.cache/video-jeiler/venv/bin/python"""
import json, os, pathlib, sys
import numpy as np

BASE = pathlib.Path(os.environ.get("VIDEO_JEILER_MODELOS", pathlib.Path.home() / ".cache" / "video-jeiler"))
M = BASE / "modelos-voz"

def cargar():
    if not (M / "kokoro-v1.0.onnx").exists(): sys.exit("Faltan los modelos de voz. Corre primero: bash instalar_voz.sh")
    from kokoro_onnx import Kokoro
    return Kokoro(str(M / "kokoro-v1.0.onnx"), str(M / "voices-v1.0.bin"))

def sintetizar(frases, voz="ef_dora", velocidad=1.0, pausa=0.45, k=None):
    """-> (audio float32 24 kHz, [{texto, inicio, fin}])"""
    k = k or cargar(); sr = 24000; partes = [np.zeros(int(0.3 * sr), dtype=np.float32)]; t = 0.3; tiempos = []
    for f in frases:
        a, sr_ = k.create(f, voice=voz, speed=velocidad, lang="es")
        assert sr_ == sr
        tiempos.append({"texto": f, "inicio": round(t, 3), "fin": round(t + len(a) / sr, 3)})
        partes += [a.astype(np.float32), np.zeros(int(pausa * sr), dtype=np.float32)]; t += len(a) / sr + pausa
    return np.concatenate(partes), tiempos

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--voces"]:
        print(" ".join(sorted(cargar().get_voices()))); sys.exit(0)
    def opt(n, d):
        if n in a: i = a.index(n); v = type(d)(a[i + 1]); del a[i:i + 2]; return v
        return d
    voz = opt("--voz", "ef_dora"); vel = opt("--velocidad", 1.0); pausa = opt("--pausa", 0.45); tj = opt("--tiempos", "")
    if len(a) != 2: sys.exit(__doc__)
    frases = [l.strip() for l in open(a[0], encoding="utf-8") if l.strip() and not l.strip().startswith("#")]
    if not frases: sys.exit("El texto está vacío.")
    audio, tiempos = sintetizar(frases, voz, vel, pausa)
    import soundfile as sf
    sf.write(a[1], audio, 24000)
    if tj: json.dump(tiempos, open(tj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pal = sum(len(f.split()) for f in frases)
    print(f"{len(frases)} frases, {pal} palabras, {len(audio) / 24000:.1f} s con la voz {voz} (≈{(tiempos[-1]['fin'] - 0.3) / pal:.2f} s por palabra) -> {a[1]}")
    print("Recordatorio: es una voz sintética; declararlo al publicar.")
