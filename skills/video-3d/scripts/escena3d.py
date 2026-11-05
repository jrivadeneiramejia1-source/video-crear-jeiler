#!/usr/bin/env python3
"""Escena 3D completa de una HISTORIA: cuarto armado con muebles de Kenney (con ventana real en 3D), exterior con pasto, lluvia y arcoíris,
personajes YA HECHOS con gestos, y cámaras por toma. Blender sin pantalla, Cycles en CPU. Todo sale de un archivo JSON.

Uso:  python escena3d.py HISTORIA.json CARPETA [--tomas 1,3] [--fija ID:SEGUNDO ...] [--ancho 960 --alto 540 --muestras 16 --fps-render 12] [--solo-revisar]
  --fija 2:1.5     solo una imagen fija de la toma 2 en el segundo 1,5 (para aprobar personajes y escenario ANTES de renderizar el video)
  --tomas 1,3      renderiza solo esas tomas (se puede continuar: los cuadros que ya existen no se repiten)
  --hoja           HOJA DE PERSONAJES: cada personaje del reparto de frente, de perfil, de espalda y su rostro (de frente y de perfil), en una imagen por personaje (hoja_ID.png)
  --solo-revisar   solo revisa que lo que dice el cuento (campo "muestra") esté de verdad dentro del cuadro y que los personajes no se tapen
Deja en CARPETA: fijas/*.png | tomas/toma_N/cuadros/*.png | tomas/toma_N.mp4 (mudo) | escena_muda.mp4 | informe.txt
Formato del JSON: ver ../ejemplo-historia/historia.json y SKILL.md (historia-3d). Medidas en METROS; el cuarto: x a lo ancho, y hacia el fondo (la pared con ventana), z hacia arriba.
Usar el Python de la instalación (~/.cache/video-jeiler/venv-blender/bin/python, ver instalar_blender.sh)."""
import argparse, json, math, os, pathlib, random, re, subprocess, sys, time
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Euler, Matrix, Quaternion, Vector

BASE = pathlib.Path(os.environ.get("VIDEO_JEILER_MODELOS", pathlib.Path.home() / ".cache" / "video-jeiler"))
MUEBLES = BASE / "recursos" / "muebles" / "Models"; NATURA = BASE / "recursos" / "naturaleza" / "Models" / "OBJ format"; PERS = BASE / "personajes"
COLOR_PARED = None; MAT_PARED = None; HIST_DIR = pathlib.Path(".")
ESC = 0.2   # el kit de muebles mide 10 unidades por pared: con 0,2 cada pared mide 2 m y la puerta 2 m

def rgb(h):
    h = h.lstrip("#"); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [(x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4) for x in c] + [1]
def lerp(a, b, t): return a + (b - a) * t
def suave(t): t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)
def vec(v, z=0.0): return Vector((v[0], v[1], v[2] if len(v) > 2 else z))

def material(nombre, color, rugosidad=.8, emision=None, fuerza=1.0):
    m = bpy.data.materials.new(nombre); m.use_nodes = True; b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = rgb(color); b.inputs["Roughness"].default_value = rugosidad
    if emision:
        b.inputs["Emission Color"].default_value = rgb(emision); b.inputs["Emission Strength"].default_value = fuerza
    return m

def vidrio(m):
    nt = m.node_tree; nt.nodes.clear(); o = nt.nodes.new("ShaderNodeOutputMaterial"); t = nt.nodes.new("ShaderNodeBsdfTransparent"); g = nt.nodes.new("ShaderNodeBsdfGlossy"); g.inputs["Roughness"].default_value = .05
    x = nt.nodes.new("ShaderNodeMixShader"); x.inputs[0].default_value = .07; nt.links.new(t.outputs[0], x.inputs[1]); nt.links.new(g.outputs[0], x.inputs[2]); nt.links.new(x.outputs[0], o.inputs[0])

def importar_obj(ruta, pos=(0, 0, 0), giro=0, esc=1.0, centrar=True, nombre=None):
    antes = set(bpy.data.objects.keys()); bpy.ops.wm.obj_import(filepath=str(ruta)); nuevos = [o for o in bpy.data.objects if o.name not in antes and o.type == 'MESH']
    if not nuevos: sys.exit(f"{ruta} no trajo ninguna malla.")
    if centrar:
        xs = [c[0] for o in nuevos for c in o.bound_box]; ys = [c[1] for o in nuevos for c in o.bound_box]; cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        for o in nuevos: o.location.x -= cx; o.location.y -= cy
    ancla = bpy.data.objects.new(nombre or ("p_" + ruta.stem), None); bpy.context.scene.collection.objects.link(ancla)
    for o in nuevos:
        o.parent = ancla
        for m in o.data.materials:
            if m and "glass" in m.name.lower(): vidrio(m)
            elif m and m.use_nodes and "Principled BSDF" in m.node_tree.nodes:
                p = m.node_tree.nodes["Principled BSDF"]; p.inputs["Roughness"].default_value = .75; p.inputs["Metallic"].default_value = 0 if "metal" not in m.name.lower() else .4
    if COLOR_PARED and ruta.stem.startswith("wall"):    # la cara grande de la pared del kit viene gris oscura («metalDark»): se pinta del color del cuarto
        for o in nuevos:
            for i, m in enumerate(o.data.materials):
                if m and m.name.startswith("metalDark"): o.data.materials[i] = MAT_PARED
    ancla.scale = (ESC * esc,) * 3; ancla.location = vec(pos); ancla.rotation_euler = (0, 0, math.radians(giro)); return ancla

def apuntar(obj, direccion):    # la luz o la cámara miran en esa dirección
    obj.rotation_euler = Vector(direccion).to_track_quat('-Z', 'Y').to_euler()

# ---------- escenario ----------
def construir_escenario(E, ids):
    global COLOR_PARED, MAT_PARED
    sc = bpy.context.scene; c = E["cuarto"]; W, L = c.get("ancho", 6), c.get("largo", 4); nx, ny = int(W // 2), int(L // 2)
    COLOR_PARED = c.get("pared"); MAT_PARED = material("pared", COLOR_PARED, .9) if COLOR_PARED else None
    for i in range(nx):
        for j in range(ny): importar_obj(MUEBLES / "floorFull.obj", (-W / 2 + (i + 1) * 2, -L / 2 + (j + 1) * 2, 0), 0, 1, False, f"piso_{i}_{j}")
    vx = c.get("ventana_x", 0); seg_ven = int((vx + W / 2) // 2)
    for i in range(nx):    # pared del fondo (con la ventana en el tramo que toca)
        pieza = "wallWindow" if i == seg_ven else "wall"; a = importar_obj(MUEBLES / f"{pieza}.obj", (-W / 2 + (i + 1) * 2, L / 2, 0), 0, 1, False, "ventana" if pieza == "wallWindow" else f"pared_fondo_{i}")
        if pieza == "wallWindow": ids["ventana"] = a
    for j in range(ny):    # paredes laterales
        importar_obj(MUEBLES / "wall.obj", (-W / 2, -L / 2 + (j + 1) * 2, 0), 90, 1, False, f"pared_izq_{j}")
        importar_obj(MUEBLES / "wall.obj", (W / 2, -L / 2 + j * 2, 0), -90, 1, False, f"pared_der_{j}")
    if c.get("techo", True):    # techo: sin él, las tomas de abajo hacia arriba muestran el cielo sobre la pared
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 12.9 * ESC)); t = bpy.context.object; t.scale = (W + .4, L + .4, 1); t.name = "techo"; t.data.materials.append(material("techo", c.get("techo_color", "#F3E7D3"), .95))
    for k, p in enumerate(E.get("piezas", [])):
        a = importar_obj(MUEBLES / f"{p['pieza']}.obj", (p["x"], p["y"], p.get("z", 0)), p.get("giro", 0), p.get("esc", 1.0), True, p.get("id", f"{p['pieza']}_{k}")); ids[a.name] = a
    ex = E.get("exterior", {}); y0 = L / 2 + 0.2
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, y0 + 40, -0.02)); suelo = bpy.context.object; suelo.scale = (120, 80, 1); suelo.name = "pasto"; suelo.data.materials.append(material("pasto", ex.get("pasto", "#7FB069"), .95))
    for k, a in enumerate(ex.get("arboles", [])): importar_obj(NATURA / f"{a.get('tipo', 'tree_default')}.obj", (a["x"], a["y"], 0), a.get("giro", 0), a.get("esc", 4.0) / ESC * ESC * 1.0, False, f"arbol_{k}")
    for k, a in enumerate(ex.get("flores", [])): importar_obj(NATURA / f"{a.get('tipo', 'flower_yellowA')}.obj", (a["x"], a["y"], 0), a.get("giro", 0), a.get("esc", 3.0), False, f"flor_{k}")
    rng = random.Random(3); lluvia = []    # gotas largas y finas que caen delante de la ventana
    mg = material("gota", "#CFE3F2", .2, "#CFE3F2", 1.5); xs = (vx - 1.4, vx + 1.4)
    for k in range(int(ex.get("gotas", 140))):
        bpy.ops.mesh.primitive_cube_add(size=1); g = bpy.context.object; g.scale = (.006, .006, .22); g.data.materials.append(mg); g.name = f"gota_{k}"
        lluvia.append((g, rng.uniform(*xs), rng.uniform(L / 2 + .15, L / 2 + 3.5), rng.uniform(0, 3), rng.uniform(3.2, 4.8)))
    ids["lluvia"] = lluvia
    arco = []; cols = ["#E4572E", "#F4A259", "#F6D55C", "#6BBF59", "#3CAEA3", "#3B6EA8", "#7A4EAB"]
    ax, ay = ex.get("arcoiris_x", vx + 1.2), ex.get("arcoiris_y", L / 2 + 14)
    for k, col in enumerate(cols):
        bpy.ops.mesh.primitive_torus_add(major_radius=5.6 - k * .22, minor_radius=.11, major_segments=96, minor_segments=8, location=(ax, ay, 0), rotation=(math.radians(90), 0, 0)); t = bpy.context.object
        t.scale = (1, 1, .25); t.name = f"arco_{k}"; t.data.materials.append(material(f"arco{k}", col, .5, col, 0)); arco.append(t); t.hide_render = True
    ids["arcoiris"] = arco

CIELOS = {"lluvia": ("#A9B7C2", "#7F8E9B", 1.1, 1.0), "despejado": ("#CFE8F7", "#6FB6E8", 3.2, 1.0), "arcoiris": ("#DDEEF7", "#7CC0EC", 3.6, 1.0)}
def mundo(E):
    sc = bpy.context.scene; w = bpy.data.worlds.new("cielo"); sc.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    o = nt.nodes.new("ShaderNodeOutputWorld"); b = nt.nodes.new("ShaderNodeBackground"); nt.links.new(b.outputs[0], o.inputs[0]); cielos = E.get("exterior", {}).get("cielos")
    if cielos:    # cielos reales (HDRI de Poly Haven, CC0): uno por tipo de cielo; se mezclan al pasar de uno a otro
        ea = nt.nodes.new("ShaderNodeTexEnvironment"); eb = nt.nodes.new("ShaderNodeTexEnvironment"); mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = 'RGBA'
        nt.links.new(ea.outputs["Color"], mx.inputs[6]); nt.links.new(eb.outputs["Color"], mx.inputs[7]); nt.links.new(mx.outputs[2], b.inputs["Color"]); imgs = {}
        for tipo, nombre in cielos.items():
            ruta = BASE / "recursos" / "cielos" / f"{nombre}_1k.hdr"
            if not ruta.exists(): sys.exit(f"Falta el cielo {ruta}: python3 scripts/descargar_cielo.py {nombre}")
            imgs[tipo] = bpy.data.images.load(str(ruta))
        return {"rampa": None, "fondo": b, "hdri": {"a": ea, "b": eb, "mix": mx, "img": imgs}}
    r = nt.nodes.new("ShaderNodeValToRGB"); mr = nt.nodes.new("ShaderNodeMapRange"); sp = nt.nodes.new("ShaderNodeSeparateXYZ"); tc = nt.nodes.new("ShaderNodeTexCoord")
    mr.inputs["From Min"].default_value = -.05; mr.inputs["From Max"].default_value = .7
    nt.links.new(tc.outputs["Generated"], sp.inputs[0]); nt.links.new(sp.outputs["Z"], mr.inputs["Value"]); nt.links.new(mr.outputs["Result"], r.inputs["Fac"]); nt.links.new(r.outputs["Color"], b.inputs["Color"])
    return {"rampa": r, "fondo": b, "hdri": None}
def poner_cielo(W, sol, a, b, m):
    ca, cb = CIELOS[a], CIELOS[b]
    if W["hdri"]:
        h = W["hdri"]; h["a"].image = h["img"].get(a) or next(iter(h["img"].values())); h["b"].image = h["img"].get(b) or next(iter(h["img"].values())); h["mix"].inputs[0].default_value = m
        W["fondo"].inputs["Strength"].default_value = lerp(.9 if a == "lluvia" else 1.0, .9 if b == "lluvia" else 1.0, m)
    else:
        mix = lambda p, q: [lerp(x, y, m) for x, y in zip(rgb(p)[:3], rgb(q)[:3])]; e = W["rampa"].color_ramp; e.elements[0].color = mix(ca[0], cb[0]) + [1]; e.elements[1].color = mix(ca[1], cb[1]) + [1]
        W["fondo"].inputs["Strength"].default_value = lerp(.85 if a == "lluvia" else 1.0, .85 if b == "lluvia" else 1.0, m)
    sol.data.energy = lerp(ca[2], cb[2], m)

# ---------- personajes ----------
def accion_de(ruta, patron):
    """Importa un archivo de animación y deja su esqueleto oculto (con su acción puesta) para usarlo como guía de movimiento."""
    antes = set(bpy.data.objects.keys()); acs_antes = set(bpy.data.actions.keys()); bpy.ops.import_scene.fbx(filepath=str(ruta))
    nuevos = [o for o in bpy.data.objects if o.name not in antes]; arm = next((o for o in nuevos if o.type == 'ARMATURE'), None)
    for o in nuevos:
        if o.type == 'MESH': bpy.data.objects.remove(o, do_unlink=True)
    cand = [bpy.data.actions[n] for n in bpy.data.actions.keys() if n not in acs_antes and re.search(patron, n, re.I) and "target" not in n.lower()]
    if arm is None or not cand: sys.exit(f"{ruta}: no hay animación que coincida con «{patron}».")
    act = cand[0]; act.use_fake_user = True; arm.animation_data_create(); arm.animation_data.action = act
    if hasattr(arm.animation_data, "action_slot") and arm.animation_data.action_slot is None and len(act.slots): arm.animation_data.action_slot = act.slots[0]
    arm.hide_render = True; arm.hide_viewport = True; return {"arm": arm, "act": act}

def poner_accesorio(arm, acc):
    """Piezas sencillas pegadas a la cabeza (coletas, lazo) para que se note quién es quién; el pelo y la cara del personaje siguen siendo los de Kenney."""
    hb = arm.data.bones["Head"]; Mb = hb.matrix_local; centro = Mb.translation + (Mb.to_3x3() @ Vector((0, 1, 0))) * hb.length * .5; cz = centro.z; piezas = []
    def esfera(nombre, pos, esc, color, giro=(0, 0, 0)):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=18, ring_count=10, radius=1, location=(0, 0, 0)); o = bpy.context.object; o.name = nombre; o.scale = esc; o.rotation_euler = giro
        bpy.ops.object.shade_smooth(); o.data.materials.append(material(nombre, color, .6)); piezas.append((o, pos))
    k = acc.get("tipo")
    if k == "coletas":
        for lado in (-1, 1):
            esfera(f"coleta_{lado}", (lado * .6, .12, cz - .12), (.17, .17, .42), acc.get("color", "#2A1515"), (0, math.radians(lado * 12), 0))
            esfera(f"atado_{lado}", (lado * .56, .06, cz + .2), (.11, .11, .09), acc.get("atado", "#F26B8A"))
    elif k == "lazo":
        for lado in (-1, 1): esfera(f"lazo_{lado}", (-.28 + lado * .17, -.18, cz + .5), (.2, .08, .13), acc.get("color", "#F26B8A"), (0, math.radians(lado * 28), 0))
        esfera("lazo_nudo", (-.28, -.18, cz + .5), (.07, .07, .07), acc.get("color", "#F26B8A"))
    for o, pos in piezas:
        M = Matrix.Translation(Vector(pos)) @ Euler(o.rotation_euler).to_matrix().to_4x4() @ Matrix.Diagonal(Vector((*o.scale, 1)))
        o.parent = arm; o.parent_type = 'BONE'; o.parent_bone = "Head"; o.matrix_parent_inverse = (Mb @ Matrix.Translation((0, hb.length, 0))).inverted() @ M
        o.location = (0, 0, 0); o.rotation_euler = (0, 0, 0); o.scale = (1, 1, 1)

def crear_personaje(pid, cfg):
    paquete = PERS / cfg.get("paquete", "animated-characters-2"); antes = set(bpy.data.objects.keys()); bpy.ops.import_scene.fbx(filepath=str(paquete / "Model" / cfg.get("modelo", "characterMedium.fbx")))
    nuevos = [o for o in bpy.data.objects if o.name not in antes]; arm = next(o for o in nuevos if o.type == 'ARMATURE'); mallas = [o for o in nuevos if o.type == 'MESH']
    if cfg.get("piel"):
        cfg["piel"] = str(pathlib.Path(cfg["piel"]) if os.path.isabs(cfg["piel"]) else HIST_DIR / cfg["piel"])   # ruta relativa al archivo de la historia
        if not os.path.exists(cfg["piel"]): sys.exit(f"Falta la piel de «{pid}»: {cfg['piel']}. En el ejemplo se crea con ejemplo-historia/crear_pieles.sh (ver personalizar_piel.py).")
        m = bpy.data.materials.new(f"piel_{pid}"); m.use_nodes = True; nt = m.node_tree; t = nt.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(str(pathlib.Path(cfg["piel"]).resolve())); t.interpolation = 'Closest'
        nt.links.new(t.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"]); nt.links.new(t.outputs["Alpha"], nt.nodes["Principled BSDF"].inputs["Alpha"]); nt.nodes["Principled BSDF"].inputs["Roughness"].default_value = .85
        for me in mallas: me.data.materials.clear(); me.data.materials.append(m)
    ancla = bpy.data.objects.new(f"actor_{pid}", None); bpy.context.scene.collection.objects.link(ancla); arm.parent = ancla; bpy.context.view_layer.update()
    zs = [(me.matrix_world @ Vector(c)).z for me in mallas for c in me.bound_box]; alto_modelo = max(zs) - min(zs); k = cfg.get("altura", 1.3) / alto_modelo; ancla.scale = (k, k, k)
    acs = {}
    for nombre, (archivo, patron) in {"idle": ("idle.fbx", "idle"), "correr": ("run.fbx", "run"), "saltar": ("jump.fbx", "jump")}.items():
        if (paquete / "Animations" / archivo).exists(): acs[nombre] = accion_de(paquete / "Animations" / archivo, patron)
    for acc in cfg.get("accesorios", []): poner_accesorio(arm, acc)
    arm.animation_data_clear(); P = {"ancla": ancla, "arm": arm, "acs": acs, "cfg": cfg, "mallas": mallas, "factor": 1.0}; P["orden"] = huesos_ordenados(arm); return P

def _mapa(cuerpo, brazo, antebrazo, mano, muslo, pierna, pie, punta, dedos):
    m = {"Hips": cuerpo[0], "Spine": cuerpo[1], "Chest": cuerpo[2], "UpperChest": cuerpo[3], "Neck": cuerpo[4], "Head": cuerpo[5]}
    for lado, sufijo in (("Left", "L"), ("Right", "R")):
        s = lambda t: t.replace("#", sufijo).replace("@", sufijo.lower())    # «#» = L o R en mayúscula, «@» = l o r en minúscula
        m.update({f"{lado}Shoulder": s(cuerpo[6]), f"{lado}Arm": s(brazo), f"{lado}ForeArm": s(antebrazo), f"{lado}Hand": s(mano), f"{lado}UpLeg": s(muslo), f"{lado}Leg": s(pierna), f"{lado}Foot": s(pie), f"{lado}Toes": s(punta)})
        for i in (1, 2, 3): m[f"{lado}HandIndex{i}"] = s(dedos[0].format(i)); 
        for i in (1, 2): m[f"{lado}HandThumb{i}"] = s(dedos[1].format(i))
    return m
# Nombres de los huesos de las bibliotecas de animación de Quaternius (CC0) -> nombres del esqueleto de los personajes de Kenney
MAPA_UAL1 = _mapa(("DEF-hips", "DEF-spine.001", "DEF-spine.002", "DEF-spine.003", "DEF-neck", "DEF-head", "DEF-shoulder.#"), "DEF-upper_arm.#", "DEF-forearm.#", "DEF-hand.#", "DEF-thigh.#", "DEF-shin.#", "DEF-foot.#", "DEF-toe.#", ("DEF-f_index.0{}.#", "DEF-thumb.0{}.#"))
MAPA_UAL2 = _mapa(("pelvis", "spine_01", "spine_02", "spine_03", "neck_01", "Head", "clavicle_@"), "upperarm_@", "lowerarm_@", "hand_@", "thigh_@", "calf_@", "foot_@", "ball_@", ("index_0{}_@", "thumb_0{}_@"))
BIBLIOTECAS = {"ual1": ("AnimationLibrary_Godot_Standard.glb", MAPA_UAL1), "ual2": ("UAL2_Standard.glb", MAPA_UAL2)}
_GUIAS = {}
def cargar_guia(spec):
    """«ual1:Walk_Loop» -> guía de movimiento de la biblioteca de animaciones (se importa una vez por biblioteca)."""
    lib, _, nombre = spec.partition(":"); archivo, mapa = BIBLIOTECAS[lib]
    if lib not in _GUIAS:
        ruta = next(iter((BASE / "recursos" / lib).rglob(archivo)), None)
        if ruta is None: sys.exit(f"Falta la biblioteca {lib}: ejecuta scripts/descargar_recursos.sh")
        antes = set(bpy.data.objects.keys()); bpy.ops.import_scene.gltf(filepath=str(ruta)); nuevos = [o for o in bpy.data.objects if o.name not in antes]
        arm = next(o for o in nuevos if o.type == 'ARMATURE')
        for o in nuevos:
            if o.type != 'ARMATURE': bpy.data.objects.remove(o, do_unlink=True)
        arm.hide_render = True; arm.hide_viewport = True; _GUIAS[lib] = arm
    act = bpy.data.actions.get(nombre)
    if act is None: sys.exit(f"{lib}: no hay animación «{nombre}». Opciones: {', '.join(sorted(a.name for a in bpy.data.actions))}")
    return {"arm": _GUIAS[lib], "act": act, "mapa": mapa}

def curvas(act):    # Blender 5 guarda las curvas de una acción en capas/tiras/canales; las versiones anteriores, en act.fcurves
    if hasattr(act, "fcurves") and act.fcurves is not None: return list(act.fcurves)
    return [fc for ly in act.layers for st in ly.strips for cb in getattr(st, "channelbags", []) for fc in cb.fcurves]

def pose_guia(guia, frame):
    """Matrices de pose (en el espacio del esqueleto) del esqueleto de la animación en un cuadro, calculadas a mano desde sus curvas y su pose de reposo
    (no se lee la pose evaluada de Blender porque en modo sin pantalla puede venir desactualizada)."""
    if "curvas" not in guia:
        guia["curvas"] = [(m.group(1), m.group(2), fc.array_index, fc) for fc in curvas(guia["act"]) for m in [re.match(r'pose\.bones\["(.+?)"\]\.(location|rotation_quaternion|scale)$', fc.data_path)] if m]
    base = {}
    for nombre, prop, i, fc in guia["curvas"]:
        d = base.setdefault(nombre, {"location": [0, 0, 0], "rotation_quaternion": [1, 0, 0, 0], "scale": [1, 1, 1]}); d[prop][i] = fc.evaluate(frame)
    ga = guia["arm"]; M = {}
    def pm(b):
        if b.name in M: return M[b.name]
        d = base.get(b.name); B = Matrix.LocRotScale(Vector(d["location"]), Quaternion(d["rotation_quaternion"]).normalized(), Vector(d["scale"])) if d else Matrix.Identity(4)
        M[b.name] = (b.matrix_local @ B) if b.parent is None else (pm(b.parent) @ (b.parent.matrix_local.inverted() @ b.matrix_local) @ B); return M[b.name]
    for b in ga.data.bones: pm(b)
    return M

def reorientar(P, guia, frame):
    """Hace que cada hueso del modelo apunte igual que el mismo hueso del esqueleto de la animación. Los dos esqueletos no descansan en la misma pose
    (el modelo está en «T» y la animación parte con los brazos abajo), así que se copia la DIRECCIÓN de cada hueso, no los números de la animación."""
    Mg = pose_guia(guia, frame); arm = P["arm"]; Mm = {}; mapa = guia.get("mapa") or {}
    reposo_g = {b.name: b.matrix_local.translation.copy() for b in guia["arm"].data.bones}
    hg = mapa.get("Hips", "Hips"); factor = (arm.data.bones["Hips"].matrix_local.translation.z / reposo_g[hg].z) if guia.get("mapa") and hg in reposo_g and abs(reposo_g[hg].z) > 1e-6 else 1.0
    for b in P["orden"]:
        pb = arm.pose.bones[b.name]; pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = (1, 0, 0, 0); pb.location = (0, 0, 0); pb.scale = (1, 1, 1)
        A = b.matrix_local.copy() if b.parent is None else Mm[b.parent.name] @ (b.parent.matrix_local.inverted() @ b.matrix_local)
        nombre_g = mapa.get(b.name, b.name) if mapa else b.name; g = Mg.get(nombre_g)
        if g is None or b.length < 1e-6: Mm[b.name] = A; continue
        d_t = (g.to_3x3() @ Vector((0, 1, 0))).normalized(); cur = (A.to_3x3() @ Vector((0, 1, 0))).normalized(); q = cur.rotation_difference(d_t).to_matrix()
        rot = A.to_3x3(); Mp = (q @ rot).to_4x4(); Mp.translation = A.translation
        pb.rotation_quaternion = (rot.inverted() @ q @ rot).to_quaternion()
        if b.name == "Hips" and nombre_g in reposo_g:    # el movimiento del cuerpo (agacharse, sentarse, saltar) se copia en proporción a la altura
            delta = (g.translation - reposo_g[nombre_g]) * factor; pb.location = rot.inverted() @ delta; Mp.translation = A.translation + delta
        Mm[b.name] = Mp

def huesos_ordenados(arm):
    prof = lambda b: 0 if b.parent is None else 1 + prof(b.parent)
    return sorted(arm.data.bones, key=prof)

def giro_hueso(arm, hueso, eje, grados):    # gira un hueso sobre su eje local por encima de lo que ya hace la animación
    pb = arm.pose.bones.get(hueso)
    if pb is None or abs(grados) < 1e-3: return
    e = [0, 0, 0]; e[eje] = 1; pb.rotation_mode = 'QUATERNION'; pb.rotation_quaternion = pb.rotation_quaternion @ Quaternion(e, math.radians(grados))

def env(t, a, b, rampa=.25):   # entra y sale suave
    return suave((t - a) / rampa) * (1 - suave((t - (b - rampa)) / rampa)) if b > a else 0

def gesto(arm, nombre, t, a, b):
    k = env(t, a, b); tt = t - a
    if k <= 0: return
    if nombre == "asiente": giro_hueso(arm, "Head", 0, k * 11 * math.sin(2 * math.pi * 1.8 * tt))
    elif nombre == "niega": giro_hueso(arm, "Head", 1, k * 26 * math.sin(2 * math.pi * 1.7 * tt))
    elif nombre == "habla": giro_hueso(arm, "Head", 0, k * 4 * math.sin(2 * math.pi * 1.6 * tt)); giro_hueso(arm, "Head", 1, k * 5 * math.sin(2 * math.pi * .8 * tt))
    elif nombre == "preocupado": giro_hueso(arm, "Head", 0, k * 14); giro_hueso(arm, "Head", 2, k * 6 * math.sin(2 * math.pi * .6 * tt))
    # Los brazos derecho e izquierdo tienen los ejes espejados (medido): el izquierdo sube hacia afuera con Z, el derecho con X
    elif nombre == "saluda": giro_hueso(arm, "RightArm", 0, k * 100); giro_hueso(arm, "RightForeArm", 0, k * 32 * math.sin(2 * math.pi * 2.0 * tt))
    elif nombre == "alegria": giro_hueso(arm, "LeftArm", 2, k * 95); giro_hueso(arm, "RightArm", 0, k * 100)
    elif nombre == "senala": giro_hueso(arm, "RightArm", 2, k * 80)

def posar(P, s, t, cfg_t):
    """Deja al personaje en la pose del instante t (segundos) de la toma, según lo que diga la toma."""
    an = P["ancla"]; arm = P["arm"]; p0 = vec(cfg_t["pos"]); p1 = vec(cfg_t.get("hasta", cfg_t["pos"])); dur = s.get("dur_total", s["dur"]); u = suave(t / dur) if "hasta" in cfg_t else 0
    p = p0.lerp(p1, u); an.location = p
    if "mira_a" in cfg_t:
        d = vec(cfg_t["mira_a"]) - p; rz = math.atan2(d.x, -d.y)
    elif "hasta" in cfg_t:
        d = p1 - p0; rz = math.atan2(d.x, -d.y)
    else: rz = math.radians(cfg_t.get("giro", 0))
    an.rotation_euler = (0, 0, rz)
    nombre = cfg_t.get("anim", "idle"); guia = cargar_guia(nombre) if ":" in nombre else (P["acs"].get(nombre) or P["acs"]["idle"]); f0, f1 = guia["act"].frame_range; largo = max(f1 - f0, 1)
    vel = cfg_t.get("vel", 1.0); frame = f0 + ((t * P["cfg"].get("fps_anim", 30) * vel) % largo)
    reorientar(P, guia, frame)
    salto = cfg_t.get("salto_m", 0.25 if nombre == "saltar" else 0.0)    # la animación de salto de Kenney agacha y estira pero no despega: se agrega el arco en el aire (sin(pi*fase))
    if salto: fase = ((t * P["cfg"].get("fps_anim", 30) * vel) % largo) / largo; an.location = (p.x, p.y, p.z + salto * abs(math.sin(math.pi * fase)))
    if "cabeza_a" in cfg_t:     # la cabeza mira un punto (en metros), repartido entre cuello y cabeza
        mt = arm.matrix_world.to_translation(); d = vec(cfg_t["cabeza_a"]) - (mt + Vector((0, 0, P["cfg"].get("altura", 1.3) * .85)))
        yaw = math.degrees(math.atan2(d.x, -d.y)) - math.degrees(rz); yaw = (yaw + 180) % 360 - 180; yaw = max(-75, min(75, yaw))
        pit = math.degrees(math.atan2(-d.z, math.hypot(d.x, d.y))); pit = max(-25, min(25, pit)); r = suave(t / .5)
        giro_hueso(arm, "Neck", 1, r * yaw * .4); giro_hueso(arm, "Head", 1, r * yaw * .6); giro_hueso(arm, "Head", 0, r * pit)
    for g in cfg_t.get("gestos", []): gesto(arm, g["g"], t, g["t"], g["t"] + g.get("dur", 1.0))
    bpy.context.view_layer.update()

# ---------- cámara y render ----------
def poner_camara(cam, cfg, t, dur):
    u = suave(t / dur) if "hasta" in cfg else 0; h = cfg.get("hasta", cfg)
    pos = vec(cfg["pos"]).lerp(vec(h["pos"]), u); mira = vec(cfg["mira"]).lerp(vec(h["mira"]), u); lente = lerp(cfg.get("lente", 35), h.get("lente", cfg.get("lente", 35)), u)
    cam.location = pos; cam.rotation_euler = (mira - pos).to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = lente; cam.data.sensor_width = 36; cam.data.sensor_fit = 'HORIZONTAL'

def cielo_en(toma, t):
    c = toma.get("cielo", "lluvia")
    if isinstance(c, str): return c, c, 0.0
    return c["de"], c["a"], suave((t - c["en"]) / c.get("dura", 1.5))

def actualizar_exterior(ids, a, b, m, t, sol_energia=None):
    llu = ids["lluvia"]; n = len(llu); v = (1 - m) if a == "lluvia" and b != "lluvia" else (m if b == "lluvia" and a != "lluvia" else (1.0 if a == "lluvia" else 0.0))
    for k, (g, x, y, z0, vel) in enumerate(llu):
        g.hide_render = not (k < n * v); g.location = (x, y, (z0 - vel * t) % 3.6)
    ar = (m if (b == "arcoiris" and a != "arcoiris") else (1.0 if a == "arcoiris" else 0.0))
    for q in ids["arcoiris"]:
        q.hide_render = ar <= 0.01; q.active_material.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 1.6 * ar

def revisar_cuadro(H, ids, cam, E, personajes, avisos):
    sc = bpy.context.scene
    for s in H["tomas"]:
        t0 = s.get("t_ini", 0.0); poner_camara(cam, s["camara"], t0, s.get("dur_total", s["dur"])); bpy.context.view_layer.update(); a, b, m = cielo_en(s, t0)
        for pid, P in personajes.items():
            if pid in s.get("personajes", {}): posar(P, s, t0, s["personajes"][pid])
        for nombre in s.get("muestra", []):
            objetivo = None
            if nombre in personajes and nombre in s.get("personajes", {}): objetivo = personajes[nombre]["ancla"].location + Vector((0, 0, personajes[nombre]["cfg"].get("altura", 1.3) * (0.88 if str(s["id"]).endswith("rostro") or str(s["id"]).endswith("rostro_perfil") else 0.5)))
            elif nombre == "ventana" and "ventana" in ids: objetivo = ids["ventana"].location + Vector((-1.0, -0.0, 1.3))
            elif nombre in ("lluvia", "arcoiris"):
                ok = (nombre == "lluvia" and "lluvia" in (a, b)) or (nombre == "arcoiris" and "arcoiris" in (a, b))
                if not ok: avisos.append(f"toma {s['id']}: dice mostrar «{nombre}» pero el cielo de esa toma no lo tiene ({a}->{b})."); continue
                objetivo = Vector((E["exterior"].get("arcoiris_x", 0) if nombre == "arcoiris" else E["cuarto"].get("ventana_x", 0), E["cuarto"].get("largo", 4) / 2 + (E["exterior"].get("arcoiris_y", 14) if nombre == "arcoiris" else 2), 4.5 if nombre == "arcoiris" else 2.2))
            elif nombre in ids and hasattr(ids[nombre], "location"): objetivo = ids[nombre].location + Vector((0, 0, .5))
            if objetivo is None: avisos.append(f"toma {s['id']}: «{nombre}» no existe en la escena."); continue
            c = world_to_camera_view(sc, cam, objetivo)
            if not (0.02 < c.x < 0.98 and 0.02 < c.y < 0.98 and c.z > 0): avisos.append(f"toma {s['id']}: «{nombre}» NO se ve dentro del cuadro (posición en pantalla {c.x:.2f},{c.y:.2f}).")
            elif nombre in personajes and nombre in s.get("personajes", {}) and s.get("plano") not in ("medio", "cerca") and not str(s["id"]).endswith("rostro") and not str(s["id"]).endswith("rostro_perfil"):
                an = personajes[nombre]["ancla"].location; al = personajes[nombre]["cfg"].get("altura", 1.3)    # cuerpo completo: pies y cabeza dentro del cuadro (si no, poner "plano": "medio")
                for parte, z in (("los pies", 0.0), ("la cabeza", al * 0.97)):
                    q = world_to_camera_view(sc, cam, Vector((an.x, an.y, z)))
                    if not (0.01 < q.y < 0.99): avisos.append(f"toma {s['id']}: «{nombre}» sale cortado: {parte} quedan fuera del cuadro (si es un plano medio a propósito, poner \"plano\": \"medio\" en la toma).")

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter); p.add_argument("historia"); p.add_argument("salida")
    p.add_argument("--tomas", default=""); p.add_argument("--fija", action="append", default=[]); p.add_argument("--ancho", type=int, default=960); p.add_argument("--alto", type=int, default=540)
    p.add_argument("--muestras", type=int, default=16); p.add_argument("--fps-render", type=int, default=12); p.add_argument("--solo-revisar", action="store_true"); p.add_argument("--hoja", action="store_true"); a = p.parse_args()
    global HIST_DIR; HIST_DIR = pathlib.Path(a.historia).resolve().parent; H = json.load(open(a.historia, encoding="utf-8")); out = pathlib.Path(a.salida); out.mkdir(parents=True, exist_ok=True); E = H["escenario"]
    for f in (MUEBLES / "wall.obj", NATURA / "tree_default.obj"):
        if not f.exists(): sys.exit(f"Falta {f}. Ejecuta scripts/descargar_recursos.sh (muebles y naturaleza de Kenney, CC0).")
    if a.hoja:    # tomas automáticas de la hoja de personajes (cada vista es una «toma» de 1 s)
        H["tomas"] = []; vistas = [("frente", [0, -3], (0, -1.0, .72), 50, (0, 0.9, .62)), ("perfil", [3, 0.9], (0, -1.0, .72), 50, (0, 0.9, .62)), ("espalda", [0, 3], (0, -1.0, .72), 50, (0, 0.9, .62)),
                                   ("rostro", [0, -3], (0, .35, 1.0), 50, (0, 0.9, 1.0)), ("rostro_perfil", [3, 0.9], (0, .35, 1.0), 50, (0, 0.9, 1.0))]
        for pid, cfg in H["reparto"].items():
            al = cfg.get("altura", 1.3)
            for k, (nom, mira, cp, lente, cm) in enumerate(vistas):
                z = cp[2] * al / 1.3 if nom.startswith("rostro") else cp[2] * al / 1.3 + .1
                H["tomas"].append({"id": f"{pid}_{nom}", "dur": 1.0, "cielo": "despejado", "muestra": [pid], "camara": {"pos": [cp[0], cp[1], z], "mira": [cm[0], cm[1], (cm[2] * al / 1.3) + (0 if nom.startswith("rostro") else .1)], "lente": lente},
                                      "personajes": {q: ({"pos": [0, 0.9], "mira_a": mira} if q == pid else {"pos": [30, 30], "mira_a": [0, 0]}) for q in H["reparto"]}})
        a.fija = [f"{t['id']}:0.3" for t in H["tomas"]]; H["escenario"]["piezas"] = []; H["exposicion"] = -1.0; H["escenario"]["cuarto"]["luz_interior"] = 60
    bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; ids = {}
    W = mundo(E); construir_escenario(E, ids)
    personajes = {pid: crear_personaje(pid, cfg) for pid, cfg in H["reparto"].items()}
    sol = bpy.data.objects.new("sol", bpy.data.lights.new("sol", 'SUN')); sc.collection.objects.link(sol); sol.data.angle = math.radians(6); apuntar(sol, (0, -.75, -.55))
    cuarto = E["cuarto"]; luz = bpy.data.objects.new("relleno", bpy.data.lights.new("relleno", 'AREA')); sc.collection.objects.link(luz); luz.location = (0, 0, 2.5); luz.data.size = 3.5; luz.data.energy = cuarto.get("luz_interior", 260)
    cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam")); sc.collection.objects.link(cam); sc.camera = cam
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = a.muestras; sc.cycles.use_denoising = True; sc.cycles.use_adaptive_sampling = True; sc.cycles.max_bounces = 4; sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = a.ancho, a.alto, 100; sc.view_settings.view_transform = 'Standard'; sc.view_settings.exposure = H.get("exposicion", -0.2); sc.render.image_settings.file_format = 'PNG'
    avisos = []; revisar_cuadro(H, ids, cam, E, personajes, avisos); L = [f"{len(H['tomas'])} tomas | {a.ancho}x{a.alto}, {a.muestras} muestras, {a.fps_render} cuadros por segundo de dibujo (Cycles, CPU)"] + ["AVISO " + x for x in avisos]
    if avisos: print("\n".join("AVISO " + x for x in avisos), flush=True)
    else: print("Revisión de «muestra»: todo lo que dice el cuento se ve en el cuadro.", flush=True)
    if a.solo_revisar: (out / "informe.txt").write_text("\n".join(L) + "\n", encoding="utf-8"); return
    def dibujar(s, t, ruta):
        t = t + s.get("t_ini", 0.0)    # una toma partida en tramos (cuando cambia quien habla) sigue su recorrido de cámara y de personajes
        ca, cb, m = cielo_en(s, t); poner_cielo(W, sol, ca, cb, m); actualizar_exterior(ids, ca, cb, m, t); poner_camara(cam, s["camara"], t, s.get("dur_total", s["dur"]))
        for pid, P in personajes.items():
            if pid in s.get("personajes", {}): posar(P, s, t, s["personajes"][pid]); [setattr(o, "hide_render", False) for o in [P["ancla"]] + P["mallas"]]
            else: [setattr(o, "hide_render", True) for o in [P["ancla"]] + P["mallas"]]
        sc.render.filepath = str(ruta); bpy.ops.render.render(write_still=True)
    tomas = {str(s["id"]): s for s in H["tomas"]}
    if a.fija:
        (out / "fijas").mkdir(exist_ok=True)
        for f in a.fija:
            i, _, t = f.partition(":"); s = tomas[i]; t0 = time.time(); dibujar(s, float(t or 0), out / "fijas" / f"toma_{i}_t{float(t or 0):g}.png"); print(f"fija {f}: {time.time() - t0:.1f} s", flush=True)
        if a.hoja:
            for pid in H["reparto"]:
                ent = [str(out / "fijas" / f"toma_{pid}_{n}_t0.3.png") for n in ("frente", "perfil", "espalda", "rostro", "rostro_perfil")]
                subprocess.run(["ffmpeg", "-v", "error", "-y"] + sum([["-i", e] for e in ent], []) + ["-filter_complex", f"hstack=inputs={len(ent)}", str(out / f"hoja_{pid}.png")], check=True); print(f"hoja_{pid}.png", flush=True)
        return
    sel = [x for x in a.tomas.split(",") if x] or list(tomas); t_ini = time.time(); n_total = 0
    for i in sel:
        s = tomas[i]; d = out / "tomas" / f"toma_{i}" / "cuadros"; d.mkdir(parents=True, exist_ok=True); n = max(1, int(round(s["dur"] * a.fps_render)))
        for k in range(n):
            ruta = d / f"{k + 1:04d}.png"
            if ruta.exists(): continue
            dibujar(s, k / a.fps_render, ruta); n_total += 1
            if k in (0, 4) or (k + 1) % 20 == 0: print(f"toma {i}: cuadro {k + 1}/{n} ({(time.time() - t_ini) / max(n_total, 1):.1f} s por cuadro)", flush=True)
        mp4 = out / "tomas" / f"toma_{i}.mp4"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(a.fps_render), "-i", str(d / "%04d.png"), "-vf", f"fps=24,scale={a.ancho}:{a.alto}:out_color_matrix=bt709:out_range=tv", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", str(mp4)], check=True)
    L.append(f"dibujados {n_total} cuadros en {time.time() - t_ini:.0f} s ({(time.time() - t_ini) / max(n_total, 1):.1f} s por cuadro)")
    if len(sel) == len(tomas):
        lista = out / "tomas" / "lista.txt"; lista.write_text("".join(f"file 'toma_{i}.mp4'\n" for i in tomas), encoding="utf-8")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lista), "-c", "copy", str(out / "escena_muda.mp4")], check=True); L.append("video mudo: escena_muda.mp4")
    (out / "informe.txt").write_text("\n".join(L) + "\n", encoding="utf-8"); print("\n".join(L))

if __name__ == "__main__":
    main()
