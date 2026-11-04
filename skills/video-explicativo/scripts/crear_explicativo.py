#!/usr/bin/env python3
"""Crea un video explicativo completo a partir de un guion.json: voz sintética, escenas animadas, subtítulos y música; en horizontal y vertical.

Uso:  python crear_explicativo.py GUION.json CARPETA [--formatos horizontal,vertical] [--sin-musica] [--lufs -14] [--solo-plan] [--reusar] [--hd]
  --solo-plan  arma proyecto.json y los tiempos con la voz, pero NO dibuja el video (para revisar antes de gastar tiempo de dibujo)
  --hd         tamaño completo: horizontal 1920x1080 y vertical 1080x1920 (lo que piden Shorts y YouTube); dibuja unas 2 veces más lento
  --reusar     si en CARPETA ya están los silencio_*.mp4 de una corrida anterior con el MISMO guion y voz, no los dibuja otra vez (solo rehace audio y pegado)
Deja en CARPETA:  voz.wav | musica.wav | audio_final.wav | proyecto.json | silencio_*.mp4 (imagen sin sonido) | video_horizontal.mp4 | video_vertical.mp4 | hoja_*.png (cuadros para mirar) | informe.txt
Necesita las skills vecinas voz-sintetica (+ instalar_voz.sh), animacion-2d (+ instalar_render.sh) y musica-y-efectos. Usar el Python de la instalación
(~/.cache/video-jeiler/venv/bin/python). Formato del guion: ver ejemplo/guion.json y SKILL.md. Es voz sintética: declararlo al publicar."""
import importlib.util, json, os, pathlib, re, subprocess, sys, base64, mimetypes
import numpy as np

RAIZ = pathlib.Path(__file__).resolve().parents[2]
NARRAR = RAIZ / "voz-sintetica" / "scripts" / "narrar.py"; RENDER = RAIZ / "animacion-2d" / "scripts" / "render.py"
COMPONER = RAIZ / "musica-y-efectos" / "scripts" / "componer.py"; ESCENAS_JS = RAIZ / "video-explicativo" / "motor" / "escenas_explicativo.js"
FORMATOS = {"horizontal": (1280, 720), "vertical": (720, 1280)}

def cargar(ruta, nombre):
    if not ruta.exists(): sys.exit(f"Falta la skill vecina: {ruta}. Instala el grupo explicativo.")
    sp = importlib.util.spec_from_file_location(nombre, ruta); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m

def a_datauri(ruta):
    mime = mimetypes.guess_type(ruta)[0] or "image/png"; return f"data:{mime};base64," + base64.b64encode(pathlib.Path(ruta).read_bytes()).decode()

def volumen(ruta):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-nostdin", "-i", str(ruta), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", e); p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", e); return (float(i[-1]) if i else None), (float(p[-1]) if p else None)

def main():
    a = sys.argv[1:]; formatos = ["horizontal", "vertical"]; musica_on = "--sin-musica" not in a; solo_plan = "--solo-plan" in a; reusar = "--reusar" in a; hd = "--hd" in a; lufs = -14.0
    a = [x for x in a if x not in ("--sin-musica", "--solo-plan", "--reusar", "--hd")]
    for n in ("--formatos", "--lufs"):
        if n in a:
            i = a.index(n); v = a[i + 1]; del a[i:i + 2]
            if n == "--formatos": formatos = v.split(",")
            else: lufs = float(v)
    if len(a) != 2 or any(f not in FORMATOS for f in formatos): sys.exit(__doc__)
    g = json.load(open(a[0], encoding="utf-8")); out = pathlib.Path(a[1]); out.mkdir(parents=True, exist_ok=True)
    base_dir = pathlib.Path(a[0]).resolve().parent
    narr = cargar(NARRAR, "narrar_mod"); esc = g["escenas"]
    frases = [f for e in esc for f in e.get("narracion", [])]
    if not frases: sys.exit("El guion no tiene narración.")
    audio, tiempos = narr.sintetizar(frases, g.get("voz", "ef_dora"), float(g.get("velocidad", 1.0)), 0.45)
    import soundfile as sf; sf.write(out / "voz.wav", audio, 24000)
    # línea de tiempo: cada escena empieza poco antes de su primera frase y termina donde empieza la siguiente
    k = 0; info = []
    for e in esc:
        n = len(e.get("narracion", [])); info.append((k, k + n)); k += n
    escenas = []; fin_prev = 0.0
    for i, (e, (i0, i1)) in enumerate(zip(esc, info)):
        e = dict(e); e.pop("narracion", None)
        if i1 > i0:
            primera, ultima = tiempos[i0]["inicio"], tiempos[i1 - 1]["fin"]
            ini = 0.0 if i == 0 else max(fin_prev + .1, primera - .4)
            if i: escenas[-1]["fin"] = round(ini, 3)
            e["inicio"] = round(ini, 3); e["frases"] = [{"a": round(t["inicio"] - ini, 3), "b": round(t["fin"] - ini, 3)} for t in tiempos[i0:i1]]
            sig_ini = None; e["fin"] = round(ultima + .8, 3); fin_prev = ultima
        else:
            ini = fin_prev + (0 if i == 0 else .4); e["inicio"] = round(ini, 3); e["fin"] = round(ini + float(e.get("duracion", 3)), 3); fin_prev = e["fin"]
            if i: escenas[-1]["fin"] = round(ini, 3)
        escenas.append(e)
    escenas[-1]["fin"] = round(escenas[-1]["fin"] + (1.5 if escenas[-1].get("creditos") else .6), 3)
    cues = [{"a": round(t["inicio"] - .05, 3), "b": round(t["fin"] + .12, 3), "texto": t["texto"]} for t in tiempos]
    total = escenas[-1]["fin"]
    def datauris(x):   # las imágenes de los gráficos se incrustan para que el navegador sin pantalla las vea
        if isinstance(x, dict): return {k2: (a_datauri(base_dir / v) if k2 == "imagen" and isinstance(v, str) and not v.startswith("data:") else datauris(v)) for k2, v in x.items()}
        if isinstance(x, list): return [datauris(v) for v in x]
        return x
    proyecto = {"titulo": g.get("titulo", ""), "marca": g.get("marca", ""), "tema": g.get("tema", {}), "escenas": escenas, "cues": cues}
    json.dump(proyecto, open(out / "proyecto.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(datauris(proyecto), open(out / "_proyecto_render.json", "w", encoding="utf-8"), ensure_ascii=False)
    pal = sum(len(f.split()) for f in frases); L = [f"Guion: {len(esc)} escenas, {len(frases)} frases, {pal} palabras. Voz {g.get('voz', 'ef_dora')} (sintética): {total:.1f} s en total."]
    if solo_plan:
        print("\n".join(L)); print(f"Plan en {out}/proyecto.json (no se dibujó nada)."); return
    musica = g.get("musica") if musica_on else None
    if musica:
        comp = cargar(COMPONER, "componer_mod"); buf, nc, bpm, _ = comp.componer(total + 1, musica.get("animo", "alegre"), int(musica.get("bpm", 0)), musica.get("tono", "C"), int(musica.get("semilla", 1)))
        comp.guardar(str(out / "musica.wav"), buf); L.append(f"Música original ({musica.get('animo', 'alegre')}, {bpm} bpm) generada por código.")
    # audio final: voz + música con ducking + volumen final en dos pasadas
    ent = ["-i", str(out / "voz.wav")]; fil = "[0:a]aresample=48000,asplit=2[v1][v2];"
    if musica:
        ent += ["-i", str(out / "musica.wav")]; ml = volumen(out / "musica.wav")[0] or -20; gan = float(musica.get("volumen_lufs", -28)) - ml
        fil += f"[1:a]volume={gan:.1f}dB,aresample=48000[m];[m][v2]sidechaincompress=threshold=0.04:ratio=10:attack=15:release=500[md];[v1][md]amix=inputs=2:normalize=0:duration=first[mix]"
    else: fil += "[v1]anull[mix]"
    pre = out / "_mezcla.wav"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-nostdin", *ent, "-filter_complex", fil, "-map", "[mix]", "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(pre)], check=True)
    p1 = subprocess.run(["ffmpeg", "-v", "info", "-nostdin", "-i", str(pre), "-af", f"loudnorm=I={lufs}:TP=-1.5:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(re.search(r'\{[^{}]*"input_i"[^{}]*\}', p1, re.S).group(0))
    ln = f"loudnorm=I={lufs}:TP=-1.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true"
    final_wav = out / "audio_final.wav"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-nostdin", "-i", str(pre), "-af", ln + f",apad=whole_dur={total:.3f}", "-ar", "48000", "-c:a", "pcm_s16le", str(final_wav)], check=True); pre.unlink()   # se rellena con silencio hasta el final del video (créditos)
    li, pk = volumen(final_wav); L.append(f"Audio final: {li} LUFS, pico {pk} dBFS (objetivo {lufs} LUFS).")
    py = sys.executable
    for fmt in formatos:
        w, h = FORMATOS[fmt]; w, h = (int(w * 1.5), int(h * 1.5)) if hd else (w, h); sil = out / f"silencio_{fmt}.mp4"; fin = out / f"video_{fmt}.mp4"
        if fin.exists(): sys.exit(f"{fin} ya existe: usa otra carpeta (no se sobrescribe).")
        if reusar and sil.exists(): print(f"{fmt}: se reutiliza {sil.name}"); r = subprocess.CompletedProcess([], 0, "", "")
        else: r = subprocess.run([py, str(RENDER), str(out / "_proyecto_render.json"), "video", str(sil), "--ancho", str(w), "--alto", str(h), "--extra", str(ESCENAS_JS)], capture_output=True, text=True)
        print(r.stdout.strip()[-300:])
        if r.returncode != 0: sys.exit("Falló el dibujo:\n" + (r.stdout + r.stderr)[-1200:])
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-nostdin", "-i", str(sil), "-i", str(final_wav), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", str(fin)], check=True)
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(fin)], capture_output=True, text=True).stdout)
        subprocess.run([py, str(RENDER), str(out / "_proyecto_render.json"), "hoja", str(out / f"hoja_{fmt}.png"), "--ancho", str(w), "--alto", str(h), "--extra", str(ESCENAS_JS), "--n", "8"], capture_output=True)
        L.append(f"{fmt}: {fin.name} {w}x{h}, {d:.2f} s (esperado {total:.2f} s)" + ("" if abs(d - total) < 0.5 else "  <-- REVISAR la duración"))
    (out / "_proyecto_render.json").unlink(); (out / "informe.txt").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))
    print("Es voz sintética: declararlo al publicar. Claude no oye el audio ni ve el movimiento: mirar las hojas de cuadros y escuchar antes de publicar.")

if __name__ == "__main__":
    main()
