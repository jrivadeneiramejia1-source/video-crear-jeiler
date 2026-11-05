#!/usr/bin/env python3
"""Compone música de fondo ORIGINAL con código (sin muestras ni melodías de nadie): acordes, arpegio, bajo y percusión suave.

Uso:  python componer.py SALIDA.wav [--duracion 60] [--animo alegre|calmo|misterio|epico] [--bpm N] [--tono C] [--semilla 1]
  --duracion  segundos (se redondea a compases enteros y se agrega un final suave)
  --animo     alegre (por defecto) | calmo | misterio | epico
  --tono      nota base: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
  --semilla   misma semilla = misma música (cambiarla da otra variación del arpegio)
Sale un .wav estéreo de 48 kHz, con el pico en -6 dBFS: pensado para ir DEBAJO de una voz (bajarlo y usar ducking al mezclar).
Solo usa numpy. Claude no puede oír: la calidad musical la juzga el oído de Jeiler; aquí se mide volumen y pico."""
import sys, wave
import numpy as np

SR = 48000
NOTAS = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
MAYOR = [0, 2, 4, 5, 7, 9, 11]; MENOR = [0, 2, 3, 5, 7, 8, 10]
ANIMOS = {   # escala, progresión (grados desde 0), bpm, notas del arpegio por compás, percusión, volumen del bajo
    "alegre": dict(escala=MAYOR, prog=[0, 4, 5, 3], bpm=112, arp=8, perc=True, bajo=.30),
    "calmo": dict(escala=MAYOR, prog=[0, 5, 3, 4], bpm=76, arp=4, perc=False, bajo=.22),
    "misterio": dict(escala=MENOR, prog=[0, 5, 2, 6], bpm=88, arp=4, perc=False, bajo=.25),
    "epico": dict(escala=MENOR, prog=[0, 6, 5, 4], bpm=100, arp=8, perc=True, bajo=.36),
}
hz = lambda semis: 261.6256 * 2 ** (semis / 12)   # 0 = do central

def acorde(escala, grado):
    n = lambda d: escala[d % 7] + 12 * (d // 7)
    return [n(grado), n(grado + 2), n(grado + 4)]

def poner(buf, x, inicio, canal=(1.0, 1.0)):
    i = int(inicio * SR); x = x[:max(0, buf.shape[0] - i)]
    if len(x): buf[i:i + len(x), 0] += x * canal[0]; buf[i:i + len(x), 1] += x * canal[1]

def pad(freq, dur):
    t = np.arange(int((dur + .6) * SR)) / SR; env = np.minimum(1, t / .35) * np.exp(-np.maximum(0, t - dur) * 7)
    return sum(np.sin(2 * np.pi * freq * (1 + d) * t) * a for d, a in ((0, 1), (.0017, .7), (-.0017, .7), (0, .0)) ) * env * .05

def pluck(freq, dur):
    t = np.arange(int(dur * SR)) / SR; env = np.exp(-t * 5.5) * np.minimum(1, t / .004)
    return (np.sin(2 * np.pi * freq * t) + .35 * np.sin(4 * np.pi * freq * t) + .12 * np.sin(6 * np.pi * freq * t)) * env * .16

def bajo(freq, dur):
    t = np.arange(int(dur * SR)) / SR; env = np.minimum(1, t / .01) * np.exp(-t * 2.2)
    return (np.sin(2 * np.pi * freq * t) + .3 * np.sin(4 * np.pi * freq * t)) * env

def bombo():
    t = np.arange(int(.28 * SR)) / SR; f = 110 * np.exp(-t * 14) + 42
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 11) * .55

def platillo(rng):
    t = np.arange(int(.07 * SR)) / SR; r = rng.standard_normal(len(t)); r = r - np.concatenate([[0], r[:-1]])   # ruido filtrado hacia agudos
    return r * np.exp(-t * 60) * .04

def componer(duracion, animo, bpm, tono, semilla):
    a = ANIMOS[animo]; bpm = bpm or a["bpm"]; rng = np.random.default_rng(semilla); beat = 60.0 / bpm; compas = 4 * beat
    n_comp = max(2, int(round(duracion / compas))); total = n_comp * compas + 1.5
    buf = np.zeros((int(total * SR) + SR, 2), dtype=np.float64); base = NOTAS[tono]
    for c in range(n_comp):
        t0 = c * compas; ac = acorde(a["escala"], a["prog"][c % len(a["prog"])])
        for s in ac: poner(buf, pad(hz(base + s - 12 + 12), compas), t0)                                  # colchón de acordes
        raiz = base + ac[0] - 24; golpes = 2 if a["perc"] else 1
        for b in range(0, 4, 4 // golpes if golpes > 1 else 4): poner(buf, bajo(hz(raiz + 12), beat * 1.9) * a["bajo"], t0 + b * beat)
        paso = compas / a["arp"]; orden = [0, 1, 2, 1] if a["arp"] == 8 else [0, 2, 1, 2]
        for k in range(a["arp"]):
            s = ac[orden[k % 4]] + 12 * (1 if (k % 8 == 5 and rng.random() < .5) else 0); p = k / max(a["arp"] - 1, 1)
            poner(buf, pluck(hz(base + s + 12), paso * 1.6), t0 + k * paso, (1 - .45 * p, .55 + .45 * p))   # el arpegio se mueve un poco de lado a lado
        if a["perc"]:
            for b in range(4):
                if b % 2 == 0: poner(buf, bombo(), t0 + b * beat, (1, 1))
                poner(buf, platillo(rng), t0 + b * beat + beat / 2, (.8, 1.0))
    final = int(total * SR); buf = buf[:final]
    fi = int(.8 * SR); fo = int(1.4 * SR); buf[:fi] *= np.linspace(0, 1, fi)[:, None]; buf[-fo:] *= np.linspace(1, 0, fo)[:, None]
    buf *= 10 ** (-6 / 20) / max(np.abs(buf).max(), 1e-9)
    return buf, n_comp, bpm, [acorde(a["escala"], g) for g in a["prog"]]

def guardar(ruta, buf):
    w = wave.open(ruta, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(buf, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

if __name__ == "__main__":
    a = sys.argv[1:]
    def opt(n, d):
        if n in a: i = a.index(n); v = type(d)(a[i + 1]); del a[i:i + 2]; return v
        return d
    dur = opt("--duracion", 60.0); animo = opt("--animo", "alegre"); bpm = opt("--bpm", 0); tono = opt("--tono", "C"); sem = opt("--semilla", 1)
    if len(a) != 1 or animo not in ANIMOS or tono not in NOTAS: sys.exit(__doc__)
    buf, n, bpm, prog = componer(dur, animo, bpm, tono, sem); guardar(a[0], buf)
    print(f"{a[0]}: {len(buf) / SR:.1f} s, {n} compases a {bpm} bpm, ánimo {animo}, tono {tono}. Composición original generada por código: sin muestras ni melodías de terceros.")
