#!/usr/bin/env python3
"""Hace la voz de cada frase de una historia, con una voz distinta por personaje (Kokoro, sin internet; voz SINTÉTICA).
Uso:  python voces_historia.py ENTRADA.json CARPETA [--propias CARPETA_GRABACIONES] [--limpiar auto|ia|ffmpeg|no] [--completo]
  --propias   usa grabaciones propias (ver voces_propias.py) donde las haya; el resto se hace con voz sintética (--completo: si falta alguna, parar)
ENTRADA.json: {"voces": {"narrador": {"voz": "em_santa", "velocidad": 0.95}, "lila": {"voz": "ef_dora"}}, "lineas": [{"id": "1_1", "quien": "narrador", "texto": "..."}]}
Deja en CARPETA: linea_<id>.wav (sin silencio al inicio) y voces.json [{id, quien, texto, archivo, dur, origen}].
Cada voz puede traer "pausa" (segundos de silencio al final de cada coma/punto; 0 = como sale) (la puntuación manda en el ritmo de Kokoro: ver mejorar_texto()).
Usar el Python de la instalación de voz (~/.cache/video-jeiler/venv/bin/python, ver voz-sintetica/scripts/instalar_voz.sh)."""
import importlib.util, json, os, pathlib, re, sys
import numpy as np, soundfile as sf
import argparse
ap = argparse.ArgumentParser(); ap.add_argument("entrada"); ap.add_argument("carpeta"); ap.add_argument("--propias", default=""); ap.add_argument("--limpiar", default="auto"); ap.add_argument("--completo", action="store_true"); A = ap.parse_args()
aqui = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(aqui))
E = json.load(open(A.entrada, encoding="utf-8")); out = pathlib.Path(A.carpeta); out.mkdir(parents=True, exist_ok=True); res = []; propias = {}
if A.propias:
    import voces_propias; propias, avisos = voces_propias.preparar(E, A.propias, out, A.limpiar, A.completo)
    for z in avisos: print("AVISO", z, flush=True)
k = narrar = None; piper_cache = {}
def mejorar_texto(t, v):
    """Kokoro respira donde hay puntuación: una coma extra o «...» agrega pausa; sin puntuación corre. Con "pausas": true se agrega una coma tras «Y», «Pero», «Entonces», «Luego» al inicio."""
    t = t.strip()
    if v.get("pausas"): t = re.sub(r"^(Y|Pero|Entonces|Luego|Así|Bueno)\s+(?=[a-záéíóúñA-ZÁÉÍÓÚÑ¿¡])", lambda m: m.group(1) + ", ", t)
    return t
for l in E["lineas"]:
    if l["id"] in propias:
        p = propias[l["id"]]; res.append({"id": l["id"], "quien": l["quien"], "texto": l["texto"], "archivo": p["archivo"], "dur": p["dur"], "origen": p["origen"]})
        print(f"{l['id']} {l['quien']:9s} {p['dur']:.2f} s  PROPIA  {l['texto'][:50]}", flush=True); continue
    v = E["voces"][l["quien"]]
    if v.get("motor") == "piper":     # Piper: "voz" es el nombre del modelo (es_MX-claude-high, es_MX-ald-medium, es_ES-davefx-medium); "velocidad" 1.0 = normal (menos = más lento)
        from piper import PiperVoice, SynthesisConfig
        base = pathlib.Path(os.environ.get("VIDEO_JEILER_MODELOS", pathlib.Path.home() / ".cache" / "video-jeiler")) / "modelos-voz" / "piper"; mod = base / f"{v.get('voz', 'es_MX-claude-high')}.onnx"
        if not mod.exists(): sys.exit(f"Falta la voz de Piper {mod.name}: corre voz-sintetica/scripts/instalar_piper.sh")
        pv = piper_cache.setdefault(mod.name, PiperVoice.load(str(mod))); trozos = list(pv.synthesize(mejorar_texto(l["texto"], v), syn_config=SynthesisConfig(length_scale=1 / max(v.get("velocidad", 1.0), 0.3), noise_scale=0.8, noise_w_scale=0.9)))
        audio = np.concatenate([c.audio_float_array for c in trozos]); sr = trozos[0].sample_rate
        if sr != 24000: audio = np.interp(np.arange(int(len(audio) * 24000 / sr)) * sr / 24000, np.arange(len(audio)), audio)
        i0 = np.where(np.abs(audio) > 0.01)[0]; audio = audio[max(0, (i0[0] if len(i0) else 0) - int(0.05 * 24000)):]; i1 = np.where(np.abs(audio) > 0.01)[0]; audio = audio[:(i1[-1] + int(0.1 * 24000)) if len(i1) else len(audio)]
        f = out / f"linea_{l['id']}.wav"; sf.write(str(f), audio.astype(np.float32), 24000, subtype="PCM_16")
        res.append({"id": l["id"], "quien": l["quien"], "texto": l["texto"], "archivo": f.name, "dur": round(len(audio) / 24000, 3), "origen": "sintetica (piper)"}); print(f"{l['id']} {l['quien']:9s} {res[-1]['dur']:.2f} s  PIPER  {l['texto'][:50]}", flush=True); continue
    if narrar is None:
        ruta = next((p for p in (aqui.parent.parent / "voz-sintetica" / "scripts" / "narrar.py", pathlib.Path.home() / ".claude" / "skills" / "voz-sintetica" / "scripts" / "narrar.py") if p.exists()), None)
        if ruta is None: sys.exit("No encuentro voz-sintetica/scripts/narrar.py (instalar el grupo historia3d).")
        spec = importlib.util.spec_from_file_location("narrar_voz", ruta); narrar = importlib.util.module_from_spec(spec); spec.loader.exec_module(narrar); k = narrar.cargar()
    audio, t = narrar.sintetizar([mejorar_texto(l["texto"], v)], v.get("voz", "ef_dora"), v.get("velocidad", 1.0), 0.0, k)
    audio = audio[int(0.3 * 24000):]; audio = audio[:int(t[0]["fin"] * 24000) - int(0.3 * 24000)]   # sin el silencio de arranque que agrega narrar.py
    f = out / f"linea_{l['id']}.wav"; sf.write(str(f), audio.astype(np.float32), 24000, subtype="PCM_16")
    res.append({"id": l["id"], "quien": l["quien"], "texto": l["texto"], "archivo": f.name, "dur": round(len(audio) / 24000, 3), "origen": "sintetica"}); print(f"{l['id']} {l['quien']:9s} {res[-1]['dur']:.2f} s  {l['texto'][:50]}", flush=True)
json.dump(res, open(out / "voces.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
