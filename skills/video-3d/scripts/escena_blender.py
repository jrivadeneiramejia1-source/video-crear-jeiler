#!/usr/bin/env python3
"""Escena 3D con un personaje YA HECHO (rigged y animado) en Blender sin pantalla, con Cycles en CPU (sin tarjeta gráfica).
Nunca arma caras ni pelo con figuras básicas: se usan personajes profesionales de licencia libre (ver SKILL.md).

Uso:  python escena_blender.py --personaje Model/personaje.fbx --salida CARPETA [opciones]
  --piel imagen.png        textura (skin) del personaje
  --animacion a.fbx [...]  archivos con la animación (se pueden pasar varios: se encadenan; si son más cortos que --segundos, se repiten)
  --vistas cuerpo,medio,rostro   SOLO imágenes fijas para que Jeiler las apruebe ANTES de animar; no anima. Encuadres: cuerpo, medio, rostro;
                           con sufijo -perfil o -espalda para verlos de lado o por detrás (ej.: cuerpo-perfil,rostro-perfil,cuerpo-espalda)
  --animar                 renderiza la animación: cuadros PNG y un video mudo escena.mp4
  --segundos 5 --fps 24 --ancho 1280 --alto 720 --muestras 24   calidad (más muestras = menos ruido y más tiempo)
  --giro 0                 grados para girar al personaje si mira hacia otro lado    --fondo "#E8DCCB"  color del fondo y del suelo
  --encuadre cuerpo|medio|rostro   cámara para --animar (por defecto medio)
Deja en CARPETA: vista_*.png | cuadros/0001.png ... | escena.mp4 | informe.txt. Nunca modifica los archivos del personaje.
Usar el Python de la instalación (~/.cache/video-jeiler/venv-blender/bin/python, ver instalar_blender.sh)."""
import argparse, math, pathlib, subprocess, sys, time
import bpy
from mathutils import Vector

def args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--personaje", required=True); p.add_argument("--salida", required=True); p.add_argument("--piel"); p.add_argument("--animacion", action="append", default=[])
    p.add_argument("--vistas", default=""); p.add_argument("--animar", action="store_true"); p.add_argument("--segundos", type=float, default=5); p.add_argument("--fps", type=int, default=24)
    p.add_argument("--ancho", type=int, default=1280); p.add_argument("--alto", type=int, default=720); p.add_argument("--muestras", type=int, default=24)
    p.add_argument("--giro", type=float, default=0); p.add_argument("--fondo", default="#E8DCCB"); p.add_argument("--encuadre", default="medio", choices=["cuerpo", "medio", "rostro"])
    return p.parse_args()

def hex_a_rgb(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c]   # sRGB -> lineal

def importar(ruta):
    ruta = pathlib.Path(ruta); antes = {o.name for o in bpy.data.objects}
    if ruta.suffix.lower() == ".fbx": bpy.ops.import_scene.fbx(filepath=str(ruta))
    elif ruta.suffix.lower() in (".glb", ".gltf"): bpy.ops.import_scene.gltf(filepath=str(ruta))
    else: sys.exit(f"Formato no soportado: {ruta.suffix} (usar .fbx, .glb o .gltf)")
    return [o for o in bpy.data.objects if o.name not in antes]

def caja(mallas, frames):
    """Caja que contiene al personaje en varios cuadros de la animación (x0, x1, y0, y1, zmin, zmax)."""
    sc = bpy.context.scene; pts = []
    for f in frames:
        sc.frame_set(f); dg = bpy.context.evaluated_depsgraph_get()
        for m in mallas:
            ev = m.evaluated_get(dg); me = ev.to_mesh()
            pts += [ev.matrix_world @ v.co for v in me.vertices]; ev.to_mesh_clear()
    xs, ys, zs = [p.x for p in pts], [p.y for p in pts], [p.z for p in pts]
    return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)

def poner_camara(cam, caja_, encuadre, ancho, alto, azimut=0):
    x0, x1, y0, y1, z0, z1 = caja_; h = z1 - z0; cx = (x0 + x1) / 2; cy = (y0 + y1) / 2
    zi, zs = {"cuerpo": (0.0, 1.0), "medio": (0.42, 1.0), "rostro": (0.70, 1.0)}[encuadre]
    alto_vista = (zs - zi) * h * 1.18; zc = z0 + (zi + zs) / 2 * h
    cam.data.lens = 50; cam.data.sensor_width = 36; cam.data.sensor_fit = 'HORIZONTAL'
    vfov = 2 * math.atan((36 * alto / ancho) / 2 / 50); dist = (alto_vista / 2) / math.tan(vfov / 2)
    az = math.radians(azimut); cam.location = (cx + dist * math.sin(az), cy - dist * math.cos(az), zc); cam.rotation_euler = (math.radians(90), 0, az)

def main():
    a = args(); out = pathlib.Path(a.salida); out.mkdir(parents=True, exist_ok=True); sc = None
    if not (a.vistas or a.animar): sys.exit("Falta --vistas (imágenes fijas para aprobar) o --animar.")
    bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene
    nuevos = importar(a.personaje); mallas = [o for o in nuevos if o.type == 'MESH']; arm = next((o for o in nuevos if o.type == 'ARMATURE'), None)
    if not mallas: sys.exit("El archivo del personaje no trae ninguna malla.")
    if a.giro and arm: arm.rotation_euler[2] += math.radians(a.giro)
    elif a.giro: [setattr(m, "rotation_euler", (m.rotation_euler[0], m.rotation_euler[1], m.rotation_euler[2] + math.radians(a.giro))) for m in mallas]
    if a.piel:   # textura sin suavizar (estilo de bajo polígono)
        mat = bpy.data.materials.new("piel"); mat.use_nodes = True; nt = mat.node_tree; tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(str(pathlib.Path(a.piel).resolve())); tex.interpolation = 'Closest'; nt.links.new(tex.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
        nt.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.85
        for m in mallas: m.data.materials.clear(); m.data.materials.append(mat)
    sc.render.fps = a.fps; total_cuadros = max(1, int(round(a.segundos * a.fps)))
    if a.animacion and arm:   # animaciones de otros archivos -> acciones del mismo esqueleto, encadenadas en la pista NLA y repetidas hasta llenar los segundos
        arm.animation_data_create(); pista = arm.animation_data.nla_tracks.new(); inicio = 1; acciones = []
        for ruta in a.animacion:
            extra = importar(ruta); ar = next((o for o in extra if o.type == 'ARMATURE'), None)
            acc = ar.animation_data.action if ar and ar.animation_data else None
            if acc is None: sys.exit(f"{ruta} no trae una animación.")
            acciones.append(acc)
            for o in extra: bpy.data.objects.remove(o, do_unlink=True)
        k = 0
        while inicio < total_cuadros + 1:
            acc = acciones[k % len(acciones)]; largo = max(1, int(acc.frame_range[1] - acc.frame_range[0]))
            tira = pista.strips.new(acc.name + f"_{k}", inicio, acc); inicio = int(tira.frame_end) + 1; k += 1
            if k > 400: break
        arm.animation_data.action = None
    sc.frame_start, sc.frame_end = 1, total_cuadros
    muestreo = list(range(1, total_cuadros + 1, max(1, total_cuadros // 12))); cj = caja(mallas, muestreo); x0, x1, y0, y1, z0, z1 = cj
    h = z1 - z0
    # suelo, fondo, luces, cámara
    bpy.ops.mesh.primitive_plane_add(size=40, location=((x0 + x1) / 2, (y0 + y1) / 2, z0)); suelo = bpy.context.object
    ms = bpy.data.materials.new("suelo"); ms.use_nodes = True; ms.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = hex_a_rgb(a.fondo) + [1]; ms.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 1
    suelo.data.materials.append(ms)
    sc.world = bpy.data.worlds.new("mundo"); sc.world.use_nodes = True; fondo = sc.world.node_tree.nodes["Background"]; fondo.inputs[0].default_value = hex_a_rgb(a.fondo) + [1]; fondo.inputs[1].default_value = 0.55
    bpy.ops.object.light_add(type='SUN', location=(h * 1.5, -h * 2, h * 3)); sol = bpy.context.object; sol.rotation_euler = (math.radians(50), 0, math.radians(35)); sol.data.energy = 2.2; sol.data.angle = math.radians(6)
    bpy.ops.object.light_add(type='AREA', location=(-h * 1.5, -h * 1.5, h * 1.2)); rel = bpy.context.object; rel.data.energy = 200 * h * h; rel.data.size = h; rel.rotation_euler = (math.radians(75), 0, math.radians(-35))
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = a.muestras; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = a.ancho, a.alto, 100
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.exposure = -0.4; sc.render.image_settings.file_format = 'PNG'
    L = [f"Personaje: {pathlib.Path(a.personaje).name} | altura {h:.2f} (unidades de Blender) | cuadros {total_cuadros} a {a.fps} fps | {a.ancho}x{a.alto}, {a.muestras} muestras (Cycles, CPU)"]
    if a.vistas:
        for v in [x.strip() for x in a.vistas.split(",") if x.strip()]:
            base, _, lado = v.partition("-"); az = {"": 0, "perfil": 90, "espalda": 180}.get(lado)
            if base not in ("cuerpo", "medio", "rostro") or az is None: sys.exit(f"Vista desconocida: {v}")
            poner_camara(cam, cj, base, a.ancho, a.alto, az); sc.frame_set(1); sc.render.filepath = str(out / f"vista_{v}.png"); t = time.time(); bpy.ops.render.render(write_still=True); L.append(f"vista {v}: {time.time() - t:.1f} s -> vista_{v}.png")
    if a.animar:
        poner_camara(cam, cj, a.encuadre, a.ancho, a.alto); (out / "cuadros").mkdir(exist_ok=True); t = time.time()
        for f in range(1, total_cuadros + 1):
            sc.frame_set(f); sc.render.filepath = str(out / "cuadros" / f"{f:04d}.png"); bpy.ops.render.render(write_still=True)
            if f in (1, 5) or f % 20 == 0: print(f"cuadro {f}/{total_cuadros} ({(time.time() - t) / f:.1f} s por cuadro)", flush=True)
        L.append(f"animación: {total_cuadros} cuadros en {time.time() - t:.0f} s ({(time.time() - t) / total_cuadros:.1f} s por cuadro)")
        mp4 = out / "escena.mp4"
        if mp4.exists(): sys.exit(f"{mp4} ya existe: usa otra carpeta (no se sobrescribe).")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(a.fps), "-i", str(out / "cuadros" / "%04d.png"), "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(mp4)], check=True)
        L.append(f"video mudo: {mp4}")
    (out / "informe.txt").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))

if __name__ == "__main__":
    main()
