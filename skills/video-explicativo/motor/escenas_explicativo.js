'use strict';
/* Tipos de escena para videos explicativos. Se cargan con render.py --extra escenas_explicativo.js (después del motor de animacion-2d).
   e.frases = [{a, b}] (tiempos de cada frase de la narración, relativos al inicio de la escena); los elementos aparecen cuando se dice su frase:
   los n elementos de una escena se asignan a las ÚLTIMAS n frases (si hay menos frases que elementos, se reparten parejo). */
function revela(e, i, n, dur) {
  const fr = e.frases || [];
  if (fr.length >= n) return fr[fr.length - n + i].a;
  return .5 + i * Math.max(.6, (dur - 1.2) / Math.max(n, 1));
}
function tarjeta(x, y, w, h, fill, stroke, op) { return `<rect x="${f(x)}" y="${f(y)}" width="${f(w)}" height="${f(h)}" rx="${f(28 * U)}" fill="${fill}" stroke="${stroke || 'none'}" stroke-width="${f(4 * U)}" opacity="${f(op === undefined ? 1 : op)}"/>`; }
function imagenSvg(src, x, y, s, op) { return `<image href="${src}" x="${f(x - s / 2)}" y="${f(y - s / 2)}" width="${f(s)}" height="${f(s)}" preserveAspectRatio="xMidYMid meet" opacity="${f(op === undefined ? 1 : op)}"/>`; }
function marcaVisual(m, x, y, s, color, op) {   // m: nombre de ícono, o {imagen: data-uri}
  if (!m) return ''; if (typeof m === 'object' && m.imagen) return imagenSvg(m.imagen, x, y, s, op); return icono(m, x, y, s, color, op);
}
function tituloEscena(e, tl, y) { return e.titulo ? T(W / 2, y, e.titulo, 46 * U, 800, TEMA.tinta, 'middle', `opacity="${f(easeOut(seg(tl, .05, .5)))}"`) : ''; }

registrarEscena('titulo', (e, tl, c) => {
  let s = fondoDecorado(c.t); const k = c.primera ? 1 : easeOut(seg(tl, .05, .7)), p = parrafo(W / 2, 0, e.texto, (V ? 66 : 70) * U, 800, TEMA.tinta, W * .84, 'middle', 1.15);
  const gy = H / 2 - p.h / 2 - (e.icono || e.imagen ? 70 * U : 0);
  if (e.icono || e.imagen) s += marcaVisual(e.imagen ? { imagen: e.imagen } : e.icono, W / 2, gy - 80 * U + (1 - k) * 20, 140 * U, TEMA.acento, k);
  s += `<g transform="translate(0 ${f(gy + (1 - k) * 30)})" opacity="${f(k)}">${p.svg}</g>`;
  if (e.detalle) s += T(W / 2, gy + p.h + 56 * U, e.detalle, 34 * U, 600, TEMA.gris, 'middle', `opacity="${f(c.primera ? 1 : easeOut(seg(tl, .6, 1.2)))}"`);
  return s;
});

registrarEscena('lista', (e, tl, c) => {
  let s = fondoDecorado(c.t) + tituloEscena(e, tl, H * .16); const items = e.items, n = items.length, size = (V ? 42 : 40) * U, maxW = W * (V ? .70 : .64), x0 = W * (V ? .08 : .14), gap = 22 * U;
  const L = items.map(it => envolver(it, size, 700, maxW)), hs = L.map(l => Math.max(88 * U, l.length * size * 1.25 + 36 * U)), total = hs.reduce((p, q) => p + q, 0) + gap * (n - 1);
  const top = H * (e.titulo ? .22 : .1), area = H * (V ? .56 : .66); let y = top + Math.max(0, (area - total) / 2);   // las tarjetas se apilan según su altura real (no se pisan)
  items.forEach((it, i) => {
    const t0 = revela(e, i, n, c.dur), q = easeOut(seg(tl, t0, t0 + .5)), h = hs[i];
    if (q > 0) {
      s += `<g transform="translate(${f((1 - q) * -60 * U)} 0)" opacity="${f(q)}">${tarjeta(x0 - 24 * U, y, W - 2 * x0 + 48 * U, h, '#fff', TEMA.suave)}${icono('check', x0 + 30 * U, y + h / 2, 56 * U, TEMA.acento2)}`;
      L[i].forEach((l, j) => { s += T(x0 + 80 * U, y + h / 2 + size * .34 + (j - (L[i].length - 1) / 2) * size * 1.25, l, size, 700, TEMA.tinta); }); s += '</g>';
    }
    y += h + gap;
  });
  return s;
});

registrarEscena('comparar', (e, tl, c) => {
  let s = fondoDecorado(c.t) + tituloEscena(e, tl, H * .12); const lados = [e.izquierda, e.derecha], cols = [TEMA.acento, TEMA.acento2], cw = V ? W * .86 : W * .42;
  let size = (V ? 30 : 31) * U; const alto = k => { const hs = lados.map(L => 86 * U + 24 * U + L.puntos.reduce((p, pt) => p + envolver(pt, k, 600, cw - 120 * U).length * k * 1.2 + 18 * U, 0) + 16 * U); return Math.max(...hs); };
  let ch = alto(size); const tope = V ? H * .30 : H * .62; if (ch > tope) { size *= tope / ch * .95; ch = alto(size); }
  const y0 = V ? H * .17 : H * .5 - ch / 2 + H * .03, pos = V ? [[W * .07, y0], [W * .07, y0 + ch + 28 * U]] : [[W * .06, y0], [W * .52, y0]];
  lados.forEach((L, i) => {
    const t0 = revela(e, i, 2, c.dur), q = easeOut(seg(tl, t0, t0 + .6)); if (q <= 0) return; const [x, y] = pos[i];
    s += `<g transform="translate(${f((1 - q) * (V ? 0 : (i ? 60 : -60)) * U)} ${f((1 - q) * (V ? 40 : 0) * U)})" opacity="${f(q)}">${tarjeta(x, y, cw, ch, '#fff', cols[i])}`;
    s += `<rect x="${f(x)}" y="${f(y)}" width="${f(cw)}" height="${f(86 * U)}" rx="${f(28 * U)}" fill="${cols[i]}"/><rect x="${f(x)}" y="${f(y + 50 * U)}" width="${f(cw)}" height="${f(36 * U)}" fill="${cols[i]}"/>`;
    s += marcaVisual(L.imagen ? { imagen: L.imagen } : L.icono, x + 52 * U, y + 43 * U, 54 * U, '#fff');
    s += T(x + (L.icono || L.imagen ? 96 * U : cw / 2), y + 56 * U, L.titulo, 36 * U, 800, '#fff', L.icono || L.imagen ? 'start' : 'middle');
    let yy = y + 86 * U + 24 * U;
    L.puntos.forEach((pt, j) => {
      const ls = envolver(pt, size, 600, cw - 120 * U), h = ls.length * size * 1.2 + 18 * U, pq = easeOut(seg(tl, t0 + .35 + j * .55, t0 + .8 + j * .55));
      if (pq > 0) { s += `<g opacity="${f(pq)}">${icono(L.malo ? 'cruz' : 'check', x + 40 * U, yy + size * .55, 34 * U, cols[i])}`; ls.forEach((l, k) => { s += T(x + 72 * U, yy + size * .85 + k * size * 1.2, l, size, 600, TEMA.tinta); }); s += '</g>'; }
      yy += h;
    });
    s += '</g>';
  });
  if (!V) s += `<g opacity="${f(easeOut(seg(tl, .8, 1.3)))}">${icono('flecha', W / 2, H * .5, 70 * U, TEMA.suave)}</g>`;
  return s;
});

registrarEscena('numero', (e, tl, c) => {
  let s = fondoDecorado(c.t); const q = easeOut(seg(tl, .1, Math.min(1.6, c.dur * .5))), val = Math.round((e.valor || 0) * q), k = backOut(seg(tl, .05, .6));
  const txt = (e.prefijo || '') + val + (e.sufijo || '');
  if (e.icono) s += marcaVisual(e.icono, W / 2, H * .24, 110 * U, TEMA.acento2, k);
  s += `<g transform="translate(${W / 2} ${f(H * .5)}) scale(${f(Math.max(.01, k))})">${T(0, 0, txt, (V ? 220 : 240) * U, 800, TEMA.acento, 'middle')}</g>`;
  const p = parrafo(W / 2, H * .6, e.texto || '', 46 * U, 700, TEMA.tinta, W * .8, 'middle'); s += `<g opacity="${f(easeOut(seg(tl, .7, 1.2)))}">${p.svg}</g>`;
  return s;
});

registrarEscena('pasos', (e, tl, c) => {
  let s = fondoDecorado(c.t) + tituloEscena(e, tl, H * .13); const ps = e.pasos, n = ps.length, size = (V ? 40 : 34) * U;
  if (V) {
    const y0 = H * .22, step = Math.min(210 * U, (H * .6) / n);
    s += `<rect x="${f(W * .16 - 4 * U)}" y="${f(y0)}" width="${f(8 * U)}" height="${f(step * (n - 1))}" fill="${TEMA.suave}" opacity=".6"/>`;
    ps.forEach((p, i) => { const q = easeOut(seg(tl, revela(e, i, n, c.dur), revela(e, i, n, c.dur) + .5)); if (q <= 0) return; const y = y0 + i * step;
      s += `<g opacity="${f(q)}" transform="translate(${f((1 - q) * 40 * U)} 0)"><circle cx="${f(W * .16)}" cy="${f(y)}" r="${f(40 * U)}" fill="${TEMA.acento}"/>${T(W * .16, y + 16 * U, i + 1, 46 * U, 800, '#fff', 'middle')}${parrafo(W * .16 + 70 * U, y - size * .75, p, size, 700, TEMA.tinta, W * .62, 'start').svg}</g>`; });
  } else {
    const y = H * .42, x0 = W * .17, dx = (W - 2 * x0) / Math.max(n - 1, 1), mw = Math.min(dx * .92, 330 * U);   // márgenes para que el texto del primero y del último quepan
    s += `<rect x="${f(x0)}" y="${f(y - 4 * U)}" width="${f(W - 2 * x0)}" height="${f(8 * U)}" fill="${TEMA.suave}" opacity=".6"/>`;
    ps.forEach((p, i) => { const q = easeOut(seg(tl, revela(e, i, n, c.dur), revela(e, i, n, c.dur) + .5)); if (q <= 0) return; const x = n === 1 ? W / 2 : x0 + i * dx;
      s += `<g opacity="${f(q)}" transform="translate(0 ${f((1 - q) * 30 * U)})"><circle cx="${f(x)}" cy="${f(y)}" r="${f(46 * U)}" fill="${TEMA.acento}"/>${T(x, y + 18 * U, i + 1, 52 * U, 800, '#fff', 'middle')}${parrafo(x, y + 80 * U, p, size, 700, TEMA.tinta, mw, 'middle').svg}</g>`; });
  }
  return s;
});

registrarEscena('barras', (e, tl, c) => {   // barras animadas: datos = [{nombre, valor}]; los valores los pone quien escribe el guion y debe poder citar su fuente
  let s = fondoDecorado(c.t) + tituloEscena(e, tl, H * .13); const ds = e.datos, mx = Math.max(...ds.map(d => d.valor)), n = ds.length;
  const x0 = W * (V ? .1 : .14), x1 = W * (V ? .9 : .86), y0 = H * .24, hh = H * (V ? .52 : .56), bh = Math.min(70 * U, hh / n * .6);
  ds.forEach((d, i) => { const q = easeOut(seg(tl, revela(e, i, n, c.dur), revela(e, i, n, c.dur) + .9)), y = y0 + (hh / n) * i + (hh / n - bh) / 2, w = (x1 - x0 - 190 * U) * (d.valor / mx) * q;
    s += `<g opacity="${f(clamp(q * 3))}">${T(x0, y - 10 * U, d.nombre, 30 * U, 700, TEMA.tinta)}<rect x="${f(x0)}" y="${f(y)}" width="${f(Math.max(w, 1))}" height="${f(bh)}" rx="${f(14 * U)}" fill="${i % 2 ? TEMA.acento2 : TEMA.acento}"/>${T(x0 + w + 14 * U, y + bh / 2 + 11 * U, Math.round(d.valor * q) + (e.unidad || ''), 34 * U, 800, TEMA.tinta)}</g>`; });
  if (e.fuente) s += T(W / 2, H * .88 - (V ? H * .17 : 0) * 0, 'Fuente: ' + e.fuente, 24 * U, 600, TEMA.gris, 'middle');
  return s;
});

registrarEscena('cierre', (e, tl, c) => {
  let s = fondoDecorado(c.t); const k = easeOut(seg(tl, .05, .7)), p = parrafo(W / 2, 0, e.texto, (V ? 58 : 62) * U, 800, TEMA.tinta, W * .84, 'middle', 1.15);
  const gy = H * .38 - p.h / 2; if (e.icono) s += marcaVisual(e.icono, W / 2, gy - 70 * U, 110 * U, TEMA.acento, k);
  s += `<g transform="translate(0 ${f(gy + (1 - k) * 30)})" opacity="${f(k)}">${p.svg}</g>`;
  (e.creditos || []).forEach((l, i) => { s += T(W / 2, H * .62 + i * 40 * U, l, 26 * U, 600, TEMA.gris, 'middle', `opacity="${f(easeOut(seg(tl, 1 + i * .3, 1.6 + i * .3)))}"`); });
  return s;
});
