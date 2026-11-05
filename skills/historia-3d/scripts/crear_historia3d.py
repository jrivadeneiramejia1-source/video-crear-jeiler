#!/usr/bin/env python3
"""De una HISTORIA en JSON a un video 3D terminado: una voz por personaje, duración de cada toma según lo que dura cada frase, dibujo con Blender (escena3d.py),
música original, subtítulos y revisión. Los pasos largos se pueden continuar si se corta (los cuadros ya dibujados no se repiten).

Uso:  python3 crear_historia3d.py HISTORIA.json CARPETA [--solo-plan | --solo-fijas | --solo-voces] [--ancho 960 --alto 540 --muestras 16 --fps-render 12] [--sin-musica] [--sin-subtitulos]
  --solo-voces   solo hace las voces y dice cuánto dura cada frase y cada toma
  --solo-plan    voces + plan de tomas (escena_render.json) y revisa que todo lo que dice el cuento se vea (sin dibujar)
  --solo-fijas   una imagen fija por toma (para aprobar el encuadre ANTES de dibujar el video)
Necesita: el Python de voz (PYTHON_VOZ, por defecto ~/.cache/video-jeiler/venv/bin/python) y el Python de Blender (PYTHON_BLENDER, por defecto ~/.cache/video-jeiler/venv-blender/bin/python).
Formato: el de video-3d/scripts/escena3d.py más: "voces" {quien: {voz, velocidad}}, "musica" {animo, tono, lufs}, y en cada toma "lineas" [{quien, texto}], "pausa_inicio", "cola", "anim_habla".
Deja en CARPETA: voces/ | render/ | audio_final.wav | subs.srt | video_final.mp4 | hoja.png | informe.txt. Es voz SINTÉTICA: declararlo al publicar. Claude no oye ni ve el movimiento."""
import argparse, copy, json, math, os, pathlib, re, subprocess, sys, time, wave
import numpy as np

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
HOME = pathlib.Path.home() / ".cache" / "video-jeiler"
PY_VOZ = os.environ.get("PYTHON_VOZ", str(HOME / "venv" / "bin" / "python")); PY_BL = os.environ.get("PYTHON_BLENDER", str(HOME / "venv-blender" / "bin" / "python"))
def buscar(rel):
    for p in (RAIZ / rel, pathlib.Path.home() / ".claude" / "skills" / rel):
        if p.exists(): return p
    sys.exit(f"No encuentro {rel} (instalar el grupo historia3d).")
ESCENA3D = lambda: buscar("video-3d/scripts/escena3d.py"); COMPONER = lambda: buscar("musica-y-efectos/scripts/componer.py")
def ejecutar(cmd, **k):
    r = subprocess.run(cmd, **k)
    if r.returncode: sys.exit(f"Falló: {' '.join(str(c) for c in cmd[:3])} ... (código {r.returncode})")
def leer_wav(ruta):
    with wave.open(str(ruta)) as w: sr = w.getframerate(); n = w.getnchannels(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return (x.reshape(-1, n).mean(axis=1) if n > 1 else x), sr
def escribir_wav(ruta, x, sr=48000):
    x = np.clip(x, -1, 1); st = x if x.ndim == 2 else np.stack([x, x], 1)
    with wave.open(str(ruta), "wb") as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((st * 32767).astype(np.int16).tobytes())
def tiempo_srt(t): ms = int(round(t * 1000)); return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); p.add_argument("historia"); p.add_argument("salida")
    p.add_argument("--solo-plan", action="store_true"); p.add_argument("--solo-fijas", action="store_true"); p.add_argument("--solo-voces", action="store_true")
    p.add_argument("--ancho", type=int, default=960); p.add_argument("--alto", type=int, default=540); p.add_argument("--muestras", type=int, default=16); p.add_argument("--fps-render", type=int, default=12)
    p.add_argument("--sin-musica", action="store_true"); p.add_argument("--sin-subtitulos", action="store_true"); a = p.parse_args()
    ruta_h = pathlib.Path(a.historia).resolve(); H = json.load(open(ruta_h, encoding="utf-8")); out = pathlib.Path(a.salida).resolve(); out.mkdir(parents=True, exist_ok=True); L = []; fps = a.fps_render
    # 1) validar: cada voz existe y quien habla está en la toma
    errores = []
    for t in H["tomas"]:
        for l in t.get("lineas", []):
            if l["quien"] not in H.get("voces", {}): errores.append(f"toma {t['id']}: «{l['quien']}» no tiene voz en \"voces\".")
            elif l["quien"] != "narrador" and l["quien"] not in t.get("personajes", {}): errores.append(f"toma {t['id']}: habla «{l['quien']}» pero no aparece en esa toma.")
    if errores: sys.exit("\n".join(errores))
    # 2) voces
    lineas = [{"id": f"{t['id']}_{k + 1}", "quien": l["quien"], "texto": l["texto"]} for t in H["tomas"] for k, l in enumerate(t.get("lineas", []))]
    (out / "voces").mkdir(exist_ok=True); entrada = out / "voces" / "entrada.json"; datos = {"voces": H.get("voces", {}), "lineas": lineas}; viejo = json.load(open(entrada)) if entrada.exists() else None
    if viejo != datos or not (out / "voces" / "voces.json").exists():
        json.dump(datos, open(entrada, "w", encoding="utf-8"), ensure_ascii=False, indent=1); ejecutar([PY_VOZ, str(AQUI / "voces_historia.py"), str(entrada), str(out / "voces")])
    dur_l = {v["id"]: v for v in json.load(open(out / "voces" / "voces.json", encoding="utf-8"))}
    # 3) línea de tiempo: cada frase una tras otra; la toma dura lo que piden sus frases (o lo que diga "dur" si es más)
    cuadro = lambda x: round(x * fps) / fps; t0 = 0.0; plan = []; GAP = 0.3
    for t in H["tomas"]:
        c = t.get("pausa_inicio", 0.5); marcas = []
        for k, l in enumerate(t.get("lineas", [])):
            v = dur_l[f"{t['id']}_{k + 1}"]; marcas.append({"id": v["id"], "quien": l["quien"], "texto": l["texto"], "ini": c, "fin": c + v["dur"], "archivo": v["archivo"]}); c += v["dur"] + GAP
        dur = cuadro(max(t.get("dur", 0), (c - GAP + t.get("cola", 0.7)) if marcas else t.get("dur", 3)))
        plan.append({"toma": t, "t0": t0, "dur": dur, "marcas": marcas}); t0 += dur
    total = t0; L.append(f"{len(H['tomas'])} tomas, {len(lineas)} frases, duración total {total:.1f} s ({int(round(total * fps))} cuadros de dibujo a {fps} por segundo)")
    for q in plan: L.append(f"  toma {q['toma']['id']}: {q['dur']:.1f} s, frases {len(q['marcas'])}")
    print("\n".join(L), flush=True)
    if a.solo_voces: (out / "informe.txt").write_text("\n".join(L) + "\n", encoding="utf-8"); return
    # 4) tomas partidas por frase: quien habla usa la animación de hablar; la cámara no se corta
    R = copy.deepcopy(H); R["tomas"] = []; R.pop("voces", None); mitad = {}
    for q in plan:
        t = q["toma"]; cortes = [0.0]
        for m in q["marcas"]: cortes += [cuadro(m["ini"]), cuadro(m["fin"] + 0.08)]
        cortes = sorted({c for c in cortes if 0 <= c < q["dur"]}) + [q["dur"]]
        for k in range(len(cortes) - 1):
            ini, fin = cortes[k], cortes[k + 1]
            if fin - ini < 1 / fps - 1e-6: continue
            hablando = next((m["quien"] for m in q["marcas"] if cuadro(m["ini"]) <= ini + 1e-6 and ini < cuadro(m["fin"] + 0.08) - 1e-6), None)
            s = copy.deepcopy(t); s.pop("lineas", None); s["id"] = f"{t['id']}_{k + 1}"; s["dur"] = round(fin - ini, 4); s["t_ini"] = ini; s["dur_total"] = q["dur"]
            ah = t.get("anim_habla", "ual1:Idle_Talking_Loop")    # false = quien habla sigue con su animación (ej.: saltando de alegría)
            if ah and hablando and hablando in s.get("personajes", {}): s["personajes"][hablando]["anim"] = ah
            R["tomas"].append(s)
            if ini <= q["dur"] / 2 < fin + 1e-9 and t["id"] not in mitad: mitad[t["id"]] = f"{s['id']}:{q['dur'] / 2 - ini:.2f}"    # el tramo que contiene la mitad de la toma
    ruta_r = out / "escena_render.json"
    for pid, cfg in R["reparto"].items():
        if cfg.get("piel") and not os.path.isabs(cfg["piel"]): cfg["piel"] = str((ruta_h.parent / cfg["piel"]).resolve())
    json.dump(R, open(ruta_r, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    base = [PY_BL, str(ESCENA3D()), str(ruta_r), str(out / "render"), "--ancho", str(a.ancho), "--alto", str(a.alto), "--muestras", str(a.muestras), "--fps-render", str(fps)]
    if a.solo_plan:
        ejecutar(base + ["--solo-revisar"]); (out / "informe.txt").write_text("\n".join(L) + "\n", encoding="utf-8"); return
    if a.solo_fijas:
        ejecutar(base + sum([["--fija", v] for v in mitad.values()], [])); return
    # 5) dibujo (largo, se puede continuar)
    t_ini = time.time(); ejecutar(base); L.append(f"dibujo: {time.time() - t_ini:.0f} s"); muda = out / "render" / "escena_muda.mp4"
    if not muda.exists(): sys.exit("No salió escena_muda.mp4")
    # 6) audio: voces en su sitio + música baja con ducking + volumen final
    sr = 48000; N = int(round(total * sr)) + sr; voz = np.zeros(N, np.float32)
    for q in plan:
        for m in q["marcas"]:
            x, s0 = leer_wav(out / "voces" / m["archivo"]); x = np.interp(np.arange(int(len(x) * sr / s0)) * s0 / sr, np.arange(len(x)), x).astype(np.float32); i = int(round((q["t0"] + m["ini"]) * sr)); voz[i:i + len(x)] += x[:max(0, N - i)]
    voz /= max(np.abs(voz).max(), 1e-6); voz *= 0.7; mezcla = np.stack([voz, voz], 1)
    mus = H.get("musica", {}); L.append("música: " + ("sin música" if a.sin_musica else f"{mus.get('animo', 'calmo')} en {mus.get('tono', 'G')}"))
    if not a.sin_musica:
        mw = out / "musica.wav"; ejecutar([PY_VOZ, str(COMPONER()), str(mw), "--duracion", str(int(math.ceil(total)) + 1), "--animo", mus.get("animo", "calmo"), "--tono", mus.get("tono", "G")])
        with wave.open(str(mw)) as w: sm = w.getframerate(); nc = w.getnchannels(); y = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32).reshape(-1, nc) / 32768
        y = y[:N]; y = np.pad(y, ((0, N - len(y)), (0, 0))); y = y if y.shape[1] == 2 else np.repeat(y, 2, 1)
        env = np.convolve(np.abs(voz), np.ones(int(0.25 * sr)) / int(0.25 * sr), "same"); duck = 1 - 0.65 * np.clip(env / 0.06, 0, 1); duck = np.convolve(duck, np.ones(int(0.2 * sr)) / int(0.2 * sr), "same")
        mezcla = mezcla + y * duck[:, None] * (10 ** (mus.get("lufs_relativo", -20) / 20))
    escribir_wav(out / "mezcla.wav", mezcla[:int(round(total * sr))] if False else mezcla[:int(round(total * sr))]); 
    ejecutar(["ffmpeg", "-v", "error", "-y", "-i", str(out / "mezcla.wav"), "-af", f"loudnorm=I={mus.get('lufs', -14)}:TP=-1.5:LRA=11", "-ar", "48000", str(out / "audio_final.wav")])
    # 7) subtítulos (frases) y título
    srt = []; k = 0
    def poner(ini, fin, txt): nonlocal k; k += 1; srt.append(f"{k}\n{tiempo_srt(ini)} --> {tiempo_srt(fin)}\n{txt}\n")
    if H.get("titulo"): poner(0.3, min(3.6, plan[0]["dur"]), "{\\an8}{\\fs34}" + H["titulo"])
    for q in plan:
        for m in q["marcas"]: poner(q["t0"] + m["ini"], q["t0"] + m["fin"] + 0.15, (m["texto"] if m["quien"] == "narrador" else (f"{m['quien'].capitalize()}: {m['texto']}" if H.get("subtitulos_nombres") else f"«{m['texto']}»")))    # diálogos entre comillas (menos letras que con el nombre)
    (out / "subs.srt").write_text("\n".join(srt), encoding="utf-8")
    vf = "null" if a.sin_subtitulos else f"subtitles={(out / 'subs.srt').as_posix()}:force_style='FontName=Inter,FontSize=17,Outline=2,Shadow=0,MarginV=22,PrimaryColour=&H00FFFFFF&,OutlineColour=&H90000000&'"
    final = out / "video_final.mp4"; ejecutar(["ffmpeg", "-v", "error", "-y", "-i", str(muda), "-i", str(out / "audio_final.wav"), "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(final)])
    # 8) revisión: duración, volumen, hoja de cuadros
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(final)], capture_output=True, text=True).stdout or 0)
    e = subprocess.run(["ffmpeg", "-nostdin", "-i", str(final), "-af", "ebur128=peak=true", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr; I = re.findall(r"I:\s+(-?[\d.]+) LUFS", e); P = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e)
    L.append(f"video final: {d:.2f} s (esperado {total:.2f}); volumen {I[-1] if I else '?'} LUFS, pico {P[-1] if P else '?'} dBFS")
    subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-y", "-i", str(final), "-vf", f"fps=1/2.5,scale=320:-2,tile=6x{max(1, math.ceil(d / 2.5 / 6))}:padding=4:color=black", "-frames:v", "1", str(out / "hoja.png")])
    L.append("Es voz sintética: declararlo al publicar. Claude no oye el audio ni ve el movimiento: mirar hoja.png y escuchar antes de publicar.")
    (out / "informe.txt").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L[-3:]))

if __name__ == "__main__":
    main()
