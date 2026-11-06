#!/usr/bin/env python3
"""Revisa un proyecto.json (escenas-web3d o animacion-2d) con las reglas de cámara, ritmo, movimiento y subtítulos
de la skill direccion-de-video. No renderiza: tarda segundos. Cada hallazgo dice qué regla, dónde y por qué.

  python3 revisar_proyecto.py PROYECTO.json            informe legible
  python3 revisar_proyecto.py PROYECTO.json --json     informe en JSON
Niveles: ERROR (arreglar antes de renderizar), AVISO (decidir), IDEA (mejora opcional). Salida 1 si hay ERROR.
Solo usa la biblioteca estándar. Los números son reglas prácticas (ver references/): puntos de partida, no leyes."""
import json, pathlib, re, sys

CPS_MAX, CPS_ERROR, LINEA_MAX, CUE_MIN = 17, 21, 42, 1.0          # subtítulos
TOMA_MIN, TOMA_MAX = 1.2, 8.0                                      # duración de una toma (s)
IDLE_MAX = 6.0                                                     # un personaje quieto sin gesto
PLANOS_APERTURA = {"general", "cuerpo", "americano"}
hallazgos = []

def h(nivel, regla, donde, texto): hallazgos.append({"nivel": nivel, "regla": regla, "donde": donde, "texto": texto})

def texto_cue(c): return " ".join(c["lines"]) if c.get("lines") else str(c.get("texto", ""))

def revisar_cues(cues):
    prev_b = None
    for i, c in enumerate(sorted(cues, key=lambda c: c["a"])):
        d = c["b"] - c["a"]; t = texto_cue(c); n = len(t.replace("\n", ""))
        lugar = f"subtítulo {i+1} ({c['a']}–{c['b']} s)"
        if d < CUE_MIN: h("AVISO", "subtitulo-corto", lugar, f"dura {d:.1f} s; menos de {CUE_MIN:.0f} s no se alcanza a leer")
        if d > 0:
            cps = n / d
            if cps > CPS_ERROR: h("ERROR", "subtitulo-rapido", lugar, f"{cps:.0f} caracteres por segundo (máximo cómodo {CPS_MAX}): no se alcanza a leer; alargar o partir")
            elif cps > CPS_MAX: h("AVISO", "subtitulo-rapido", lugar, f"{cps:.0f} caracteres por segundo (cómodo ≤ {CPS_MAX}); alargar un poco o acortar el texto")
        for l in (c.get("lines") or []):
            if len(l) > LINEA_MAX: h("AVISO", "linea-larga", lugar, f"una línea de {len(l)} caracteres (≤ {LINEA_MAX}); partirla en dos")
        if prev_b is not None and c["a"] < prev_b - 1e-6: h("AVISO", "subtitulos-encimados", lugar, "empieza antes de que termine el anterior")
        prev_b = c["b"]

def revisar_3d(p):
    dur = p.get("duracion", 0); tomas = sorted(p.get("tomas") or [], key=lambda t: t["a"])
    objetos = {o.get("id", f"o{i}"): o for i, o in enumerate(p.get("objetos") or [])}
    if tomas:
        t0 = tomas[0]
        if t0.get("plano", "medio") not in PLANOS_APERTURA and not t0.get("punto"):
            h("IDEA", "abrir-ubicando", "toma 1", f"empieza en «{t0.get('plano','medio')}»: un plano general o de cuerpo primero ubica al público (plano de establecimiento)")
        if tomas[0]["a"] > 0.01: h("AVISO", "hueco-de-camara", "toma 1", f"la primera toma empieza en {tomas[0]['a']} s: de 0 a ahí se usa la cámara libre")
        for i, t in enumerate(tomas):
            d = t["b"] - t["a"]; lugar = f"toma {i+1} ({t['a']}–{t['b']} s, {t.get('plano','medio')})"
            if d < TOMA_MIN: h("AVISO", "toma-corta", lugar, f"dura {d:.1f} s; menos de {TOMA_MIN} s no se alcanza a leer")
            if d > TOMA_MAX and not t.get("empuja") and not t.get("orbita"): h("IDEA", "toma-larga", lugar, f"dura {d:.1f} s sin movimiento de cámara; cortar a otro plano o añadir `empuja` lento")
            if i:
                a = tomas[i-1]
                if t["a"] < a["b"] - 0.01: h("AVISO", "tomas-encimadas", lugar, "empieza antes de que termine la anterior")
                elif t["a"] > a["b"] + 0.01: h("AVISO", "hueco-de-camara", lugar, f"hay un hueco de {t['a']-a['b']:.1f} s sin toma entre la anterior y esta")
                igual = a.get("plano", "medio") == t.get("plano", "medio") and (a.get("objetivo") == t.get("objetivo") and (a.get("objetivos") == t.get("objetivos"))) and not t.get("punto")
                if igual and a.get("lado", "frente") == t.get("lado", "frente"): h("AVISO", "salto-de-corte", lugar, "mismo plano, mismo personaje y mismo lado que la toma anterior: se siente un salto, no un corte; cambiar plano o lado")
                ca, cb = a.get("objetivos"), t.get("objetivos")
                if ca and cb and set(ca) == set(cb) and len(ca) == 2:
                    sa, sb = a.get("lado", "frente"), t.get("lado", "frente"); opuestos = {("der","izq"),("izq","der"),("frente","atras"),("atras","frente")}
                    if (sa, sb) in opuestos: h("AVISO", "linea-de-accion", lugar, f"la pareja pasa de «{sa}» a «{sb}»: cruzas la línea de acción y el público se desorienta; mantener el mismo lado")
        if dur > 10 and len({t.get("plano", "medio") for t in tomas}) < 3: h("IDEA", "variedad-de-planos", "tomas", "más de 10 s con menos de 3 tipos de plano; añadir un primer plano de reacción o un general")
        prom = (tomas[-1]["b"] - tomas[0]["a"]) / len(tomas)
        if len(tomas) > 1 and prom > 7: h("IDEA", "ritmo-lento", "tomas", f"promedio de {prom:.1f} s por toma: lento para video infantil; probar 3–5 s")
        if len(tomas) > 1 and prom < 1.8: h("AVISO", "ritmo-muy-rapido", "tomas", f"promedio de {prom:.1f} s por toma: muy rápido")
        for i, t in enumerate(tomas):
            for oid in ([t["objetivo"]] if t.get("objetivo") else t.get("objetivos") or []):
                if t.get("plano") in ("primer-plano", "detalle") and re.search(r"quaternius", str(objetos.get(oid, {}).get("modelo", "")), re.I):
                    h("AVISO", "cara-sin-boca", f"toma {i+1} ({t['plano']}) de «{oid}»", "los personajes de Quaternius tienen la cara negra sin boca: usar KayKit en primeros planos")
    elif p.get("camara", {}).get("mov") is None and dur > 6: h("IDEA", "sin-camara", "escena", "sin `tomas` ni movimiento de cámara en más de 6 s: probar `tomas` con 2–3 planos")
    # personajes
    for oid, o in objetos.items():
        if not o.get("modelo"): continue
        acc = o.get("acciones")
        if not acc and o.get("clip") is None and re.search(r"\.(glb|gltf|fbx)$", o["modelo"], re.I) and re.search(r"kaykit/|personajes/", o["modelo"]):
            h("AVISO", "personaje-sin-animacion", f"«{oid}»", "personaje sin `clip` ni `acciones`: se queda en pose de bind (T)")
        if acc:
            ini, fin_prev = [], 0.0   # inicio de cada acción: «a» si lo trae; si no, cuando termina la anterior (b, dura o duración de la escena)
            for j, a in enumerate(acc):
                i0 = a["a"] if "a" in a else fin_prev; ini.append(i0)
                fin_prev = a["b"] if ("ir_a" in a and "b" in a) else (i0 + a["dura"] if "dura" in a else (acc[j+1]["a"] if j+1 < len(acc) and "a" in acc[j+1] else dur))
            for j, a in enumerate(acc):
                if re.search(r"idle", str(a.get("clip", "")), re.I) and "mirar" not in a and "mirar_grados" not in a:
                    fin = ini[j+1] if j+1 < len(acc) else (ini[j] + a["dura"] if "dura" in a else dur)
                    largo = fin - ini[j]
                    if largo > IDLE_MAX: h("AVISO", "personaje-congelado", f"«{oid}» en «{a['clip']}» ({ini[j]:g}–{fin:g} s)", f"{largo:.0f} s quieto sin mirar ni gesticular (> {IDLE_MAX:.0f} s): añade `mirar`, un gesto corto o un cambio de acción")
            for j, a in enumerate(acc):
                if "ir_a" in a and "b" in a and "a" in a and a["b"] - a["a"] < 0.6: h("AVISO", "caminata-muy-corta", f"«{oid}»", "caminata de menos de 0,6 s: sin `b` el motor calcula una duración natural")
    pares = [(i, j) for i in objetos for j in objetos if i < j and objetos[i].get("acciones") and objetos[j].get("acciones")]
    for i, j in pares:
        ai, aj = objetos[i]["acciones"], objetos[j]["acciones"]
        if len(ai) > 1 and len(aj) > 1 and [x.get("clip") for x in ai] == [x.get("clip") for x in aj] and [x.get("a") for x in ai] == [x.get("a") for x in aj]:
            h("IDEA", "gemelos", f"«{i}» y «{j}»", "hacen exactamente lo mismo a la vez: se ven robóticos; desfasar `a` unas décimas o usar otro clip")
    for i, t in enumerate(p.get("titulos") or []):
        d = t["b"] - t["a"]; n = len(str(t.get("texto", "")))
        if d < 1.5 or n / max(d, 0.1) > 15: h("AVISO", "titulo-corto", f"título {i+1}", f"{d:.1f} s para {n} caracteres: darle al menos {max(1.5, n/15):.1f} s")
    if dur > 6 and not (p.get("fundido") or {}).get("salida"): h("IDEA", "cierre", "escena", "sin fundido de salida: un fundido a negro marca el final")
    revisar_cues(p.get("cues") or [])

def revisar_2d(p):
    es = p.get("escenas") or []; total = max((e["fin"] for e in es), default=0)
    for i, e in enumerate(es):
        d = e["fin"] - e["inicio"]; lugar = f"escena {i+1} ({e['inicio']}–{e['fin']} s, {e.get('tipo')})"
        if e.get("tipo") == "texto" and d < 2.0: h("AVISO", "tarjeta-corta", lugar, f"tarjeta de texto de {d:.1f} s; leer toma ≥ 2 s")
        if e.get("tipo") == "personajes" and d < 3.0: h("AVISO", "escena-corta", lugar, f"escena de personajes de {d:.1f} s; poco para que pase algo")
        for dl in e.get("dialogo") or []:
            palabras = len(str(dl.get("texto", "")).split()); dd = dl["b"] - dl["a"]
            if dd > 0 and palabras / dd > 3.2: h("AVISO", "habla-apurada", lugar, f"«{dl.get('texto','')[:30]}…»: {palabras/dd:.1f} palabras/s (cómodo ≤ 3); alargar la frase")
            if dl["b"] > d + 0.01: h("ERROR", "dialogo-fuera-de-escena", lugar, "el diálogo termina después de que acaba la escena")
        for q in e.get("personajes") or []:
            pass
    moods = [q.get("mood", "smile") for e in es for q in e.get("personajes") or []]
    if len(moods) >= 4 and len(set(moods)) == 1: h("IDEA", "un-solo-animo", "personajes", f"todos los personajes usan «{moods[0]}» en toda la historia: variar el ánimo según lo que pasa")
    if len(es) > 1 and total / len(es) > 8: h("IDEA", "ritmo-lento", "escenas", f"promedio de {total/len(es):.1f} s por escena")
    revisar_cues(p.get("cues") or [])

def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a: sys.exit(__doc__)
    p = json.loads(pathlib.Path(a[0]).read_text(encoding="utf-8"))
    (revisar_2d if "escenas" in p else revisar_3d)(p)
    orden = {"ERROR": 0, "AVISO": 1, "IDEA": 2}; hallazgos.sort(key=lambda x: orden[x["nivel"]])
    if "--json" in sys.argv: print(json.dumps(hallazgos, ensure_ascii=False, indent=1))
    else:
        for x in hallazgos: print(f"[{x['nivel']}] {x['regla']} · {x['donde']}: {x['texto']}")
        n = {k: sum(1 for x in hallazgos if x["nivel"] == k) for k in orden}
        print(f"\n{pathlib.Path(a[0]).name}: {n['ERROR']} error(es), {n['AVISO']} aviso(s), {n['IDEA']} idea(s)." + ("" if hallazgos else " Nada que reportar con estas reglas (no reemplaza mirar los cuadros)."))
    sys.exit(1 if any(x["nivel"] == "ERROR" for x in hallazgos) else 0)
main()
