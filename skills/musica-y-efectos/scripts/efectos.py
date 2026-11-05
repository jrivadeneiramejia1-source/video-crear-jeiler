#!/usr/bin/env python3
"""Genera efectos de sonido sencillos con código (sin muestras de nadie): pop, ding, clic, whoosh, exito, error.
Uso:  python efectos.py CARPETA_SALIDA        -> CARPETA_SALIDA/pop.wav, ding.wav, clic.wav, whoosh.wav, exito.wav, error.wav (mono, 48 kHz, pico -3 dBFS)
Solo usa numpy. Para ponerlos en un video en un segundo exacto, mezclar con ffmpeg-skill (audio.py --effects) o con ffmpeg adelay+amix."""
import pathlib, sys, wave
import numpy as np
SR = 48000
def t(d): return np.arange(int(d * SR)) / SR
def env(x, a=.004, r=8): return np.minimum(1, t(len(x) / SR) / a) * np.exp(-t(len(x) / SR) * r)
def seno(f, d): return np.sin(2 * np.pi * f * t(d))
def pop(): x = seno(520, .12) * np.exp(-t(.12) * 28); return x * np.minimum(1, t(.12) / .002)
def ding(): x = (seno(1318, .9) + .4 * seno(2637, .9)) * np.exp(-t(.9) * 5); return x * np.minimum(1, t(.9) / .003)
def clic(): r = np.random.default_rng(3).standard_normal(int(.02 * SR)); return r * np.exp(-t(.02) * 220)
def whoosh():
    d = .6; r = np.random.default_rng(5).standard_normal(int(d * SR)); k = np.cumsum(r); k -= np.convolve(k, np.ones(400) / 400, "same")   # ruido que sube y baja
    return k / np.abs(k).max() * np.sin(np.pi * t(d) / d) ** 2
def exito(): return np.concatenate([seno(f, .16) * np.exp(-t(.16) * 7) for f in (523.25, 659.25, 783.99)] + [seno(1046.5, .5) * np.exp(-t(.5) * 6)])
def error(): d = .35; return (np.sign(seno(110, d)) * .5 + seno(165, d) * .5) * np.exp(-t(d) * 6)
def guardar(ruta, x):
    x = x / max(np.abs(x).max(), 1e-9) * 10 ** (-3 / 20); w = wave.open(str(ruta), "wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()
if __name__ == "__main__":
    if len(sys.argv) != 2: sys.exit(__doc__)
    c = pathlib.Path(sys.argv[1]); c.mkdir(parents=True, exist_ok=True)
    for n, fn in (("pop", pop), ("ding", ding), ("clic", clic), ("whoosh", whoosh), ("exito", exito), ("error", error)): guardar(c / f"{n}.wav", fn())
    print("Efectos en", c, ":", ", ".join(sorted(p.name for p in c.glob("*.wav"))), "(generados por código, sin muestras de terceros)")
