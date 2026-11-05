#!/usr/bin/env python3
"""Hace la voz de cada frase de una historia, con una voz distinta por personaje (Kokoro, sin internet; voz SINTÉTICA).
Uso:  python voces_historia.py ENTRADA.json CARPETA
ENTRADA.json: {"voces": {"narrador": {"voz": "em_santa", "velocidad": 0.95}, "lila": {"voz": "ef_dora"}}, "lineas": [{"id": "1_1", "quien": "narrador", "texto": "..."}]}
Deja en CARPETA: linea_<id>.wav (mono, 24 kHz, sin silencio al inicio) y voces.json [{id, quien, texto, archivo, dur}].
Usar el Python de la instalación de voz (~/.cache/video-jeiler/venv/bin/python, ver voz-sintetica/scripts/instalar_voz.sh)."""
import importlib.util, json, pathlib, sys
import numpy as np, soundfile as sf
if len(sys.argv) != 3: sys.exit(__doc__)
aqui = pathlib.Path(__file__).resolve().parent
ruta = next((p for p in (aqui.parent.parent / "voz-sintetica" / "scripts" / "narrar.py", pathlib.Path.home() / ".claude" / "skills" / "voz-sintetica" / "scripts" / "narrar.py") if p.exists()), None)
if ruta is None: sys.exit("No encuentro voz-sintetica/scripts/narrar.py (instalar el grupo historia3d).")
spec = importlib.util.spec_from_file_location("narrar_voz", ruta); narrar = importlib.util.module_from_spec(spec); spec.loader.exec_module(narrar)
E = json.load(open(sys.argv[1], encoding="utf-8")); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); k = narrar.cargar(); res = []
for l in E["lineas"]:
    v = E["voces"][l["quien"]]; audio, t = narrar.sintetizar([l["texto"]], v.get("voz", "ef_dora"), v.get("velocidad", 1.0), 0.0, k)
    audio = audio[int(0.3 * 24000):]; audio = audio[:int(t[0]["fin"] * 24000) - int(0.3 * 24000)]   # sin el silencio de arranque que agrega narrar.py
    f = out / f"linea_{l['id']}.wav"; sf.write(str(f), audio.astype(np.float32), 24000, subtype="PCM_16")
    res.append({"id": l["id"], "quien": l["quien"], "texto": l["texto"], "archivo": f.name, "dur": round(len(audio) / 24000, 3)}); print(f"{l['id']} {l['quien']:9s} {res[-1]['dur']:.2f} s  {l['texto'][:50]}", flush=True)
json.dump(res, open(out / "voces.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
