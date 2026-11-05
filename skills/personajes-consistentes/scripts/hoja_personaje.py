#!/usr/bin/env python3
"""Hoja de personaje de un modelo 3D: frente, perfil, espalda y rostro en una sola imagen, más su paleta de colores.
Sirve para APROBAR al personaje antes de animarlo y como imagen de referencia (la misma en todas las escenas o clips).

Uso:  python hoja_personaje.py --personaje Model/personaje.fbx --piel Skins/piel.png --salida CARPETA [--fondo "#E8DCCB"] [--ancho 640 --alto 640]
Deja en CARPETA: hoja.png (4 vistas) | paleta.json y paleta.png (colores principales de la textura) | vista_*.png
Necesita la skill vecina video-3d y su Python con Blender (~/.cache/video-jeiler/venv-blender/bin/python). Nunca modifica el personaje."""
import argparse, json, pathlib, subprocess, sys
import numpy as np

ESC = pathlib.Path(__file__).resolve().parents[2] / "video-3d" / "scripts" / "escena_blender.py"

def paleta(png, k=6):
    """Colores principales (cuantizados) de una textura: [{hex, parte}] ordenados por presencia, sin el fondo transparente."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(png), "-vf", "scale=128:128", "-f", "rawvideo", "-pix_fmt", "rgba", "-"], capture_output=True)
    px = np.frombuffer(r.stdout, dtype=np.uint8).reshape(-1, 4); px = px[px[:, 3] > 200][:, :3]
    if len(px) == 0: return []
    q = (px // 32) * 32 + 16; vals, cnt = np.unique(q, axis=0, return_counts=True); orden = np.argsort(-cnt)[:k]
    return [{"hex": "#%02X%02X%02X" % tuple(vals[i]), "parte": round(float(cnt[i] / cnt.sum()), 3)} for i in orden]

def main():
    p = argparse.ArgumentParser(); p.add_argument("--personaje", required=True); p.add_argument("--piel"); p.add_argument("--salida", required=True)
    p.add_argument("--fondo", default="#E8DCCB"); p.add_argument("--ancho", type=int, default=640); p.add_argument("--alto", type=int, default=640)
    a = p.parse_args(); out = pathlib.Path(a.salida); out.mkdir(parents=True, exist_ok=True)
    if not ESC.exists(): sys.exit(f"Falta la skill vecina video-3d ({ESC}).")
    cmd = [sys.executable, str(ESC), "--personaje", a.personaje, "--salida", str(out), "--vistas", "cuerpo,cuerpo-perfil,cuerpo-espalda,rostro", "--ancho", str(a.ancho), "--alto", str(a.alto), "--fondo", a.fondo, "--muestras", "32"]
    if a.piel: cmd += ["--piel", a.piel]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0: sys.exit("Falló el render:\n" + (r.stdout + r.stderr)[-1500:])
    nombres = [("cuerpo", "FRENTE"), ("cuerpo-perfil", "PERFIL"), ("cuerpo-espalda", "ESPALDA"), ("rostro", "ROSTRO")]
    ent = []; fil = []
    for i, (v, et) in enumerate(nombres):
        ent += ["-i", str(out / f"vista_{v}.png")]
        fil.append(f"[{i}:v]drawtext=text='{et}':x=14:y=12:fontsize=26:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=6[v{i}]")
    fil.append("[v0][v1][v2][v3]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0[o]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ent, "-filter_complex", ";".join(fil), "-map", "[o]", "-frames:v", "1", str(out / "hoja.png")], check=True)
    pal = paleta(a.piel) if a.piel else []; json.dump(pal, open(out / "paleta.json", "w"), indent=1)
    if pal:
        ent = []; fil = []
        for i, c in enumerate(pal): ent += ["-f", "lavfi", "-i", f"color=c={c['hex'].replace('#', '0x')}:s=120x120:d=1"]; fil.append(f"[{i}:v]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", *ent, "-filter_complex", "".join(fil) + f"hstack=inputs={len(pal)}[o]", "-map", "[o]", "-frames:v", "1", str(out / "paleta.png")], check=True)
    print(f"Hoja de personaje: {out / 'hoja.png'} | paleta: {', '.join(c['hex'] for c in pal)}")
    print("Mirar la hoja a tamaño completo (ojos, boca, pelo, manos, ropa) y que Jeiler la apruebe antes de animar.")

if __name__ == "__main__":
    main()
