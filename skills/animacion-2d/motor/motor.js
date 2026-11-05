'use strict';
/* Motor 2D en SVG: cada cuadro se dibuja con render(t) a partir de window.PROYECTO.
   PROYECTO = { ancho, alto, tema?, escenas: [{tipo, inicio, fin, ...}], cues: [{a, b, lines: [...]}], marca? }
   Mismo código para horizontal (ancho > alto) y vertical (alto > ancho). Los tipos de escena se registran con registrarEscena(). */
const P = window.PROYECTO;
const W = P.ancho || 1280, H = P.alto || 720, V = H > W;
const U = V ? W / 720 : W / 1280;                       // unidad: los tamaños se escriben para 1280x720 y se escalan
const TEMA = Object.assign({ fondoA: '#FFF3E3', fondoB: '#FFE2C6', tinta: '#243B53', acento: '#EF7B5C', acento2: '#2A9D8F', suave: '#F4B942', blanco: '#FFFFFF', gris: '#8A9BAE', caja: 'rgba(36,59,83,0.88)' }, P.tema || {});
const FONT = "Inter, 'DejaVu Sans', sans-serif";
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const seg = (t, a, b) => clamp((t - a) / (b - a));
const lerp = (a, b, k) => a + (b - a) * k;
const ease = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const easeOut = x => 1 - Math.pow(1 - x, 3);
const backOut = x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
const f = n => Math.round(n * 100) / 100;
const _cv = document.createElement('canvas').getContext('2d');
function medir(txt, size, weight) { _cv.font = `${weight} ${size}px Inter, 'DejaVu Sans', sans-serif`; return _cv.measureText(txt).width; }
function envolver(txt, size, weight, maxW) {            // parte un texto en renglones que caben en maxW
  const out = []; let cur = '';
  for (const w of String(txt).split(/\s+/)) { const t = cur ? cur + ' ' + w : w; if (cur && medir(t, size, weight) > maxW) { out.push(cur); cur = w; } else cur = t; }
  if (cur) out.push(cur); return out;
}
function T(x, y, txt, size, weight, fill, anchor, extra) {
  const t = String(txt).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  return `<text x="${f(x)}" y="${f(y)}" font-family="${FONT}" font-size="${f(size)}" font-weight="${weight}" fill="${fill}" text-anchor="${anchor || 'start'}"${extra ? ' ' + extra : ''}>${t}</text>`;
}
function parrafo(x, y, txt, size, weight, fill, maxW, anchor, lh) {   // texto con saltos de renglón; devuelve {svg, h}
  const ls = envolver(txt, size, weight, maxW), h = size * (lh || 1.25); let s = '';
  ls.forEach((l, i) => { s += T(x, y + h * i + size * .85, l, size, weight, fill, anchor); });
  return { svg: s, h: h * ls.length, lines: ls.length };
}

/* ---------- iconos simples (centrados en x,y; s = tamaño en px) ---------- */
const ICONOS = {
  check: c => `<circle r="50" fill="${c}"/><path d="M -24 2 L -8 20 L 26 -18" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" fill="none"/>`,
  cruz: c => `<circle r="50" fill="${c}"/><path d="M -20 -20 L 20 20 M 20 -20 L -20 20" stroke="#fff" stroke-width="12" stroke-linecap="round"/>`,
  flecha: c => `<path d="M -42 -10 H 14 V -34 L 46 0 L 14 34 V 10 H -42 Z" fill="${c}"/>`,
  estrella: c => `<path d="M 0 -48 L 14 -16 L 48 -14 L 22 8 L 30 42 L 0 24 L -30 42 L -22 8 L -48 -14 L -14 -16 Z" fill="${c}"/>`,
  corazon: c => `<path d="M 0 40 C -60 -2 -40 -50 0 -22 C 40 -50 60 -2 0 40 Z" fill="${c}"/>`,
  bombilla: c => `<circle cy="-10" r="30" fill="${c}"/><rect x="-14" y="18" width="28" height="12" rx="4" fill="${c}"/><rect x="-10" y="34" width="20" height="8" rx="4" fill="${c}"/>`,
  telefono: c => `<rect x="-26" y="-46" width="52" height="92" rx="10" fill="${c}"/><rect x="-20" y="-34" width="40" height="62" rx="3" fill="#fff" opacity=".9"/><circle cy="37" r="4" fill="#fff"/>`,
  nube: c => `<g fill="${c}"><circle cx="-22" cy="6" r="22"/><circle cx="6" cy="-10" r="28"/><circle cx="30" cy="8" r="20"/><rect x="-44" y="6" width="90" height="22" rx="11"/></g>`,
  engranaje: c => { let d = ''; for (let i = 0; i < 8; i++) d += `<rect x="-7" y="-50" width="14" height="22" rx="3" fill="${c}" transform="rotate(${i * 45})"/>`; return d + `<circle r="34" fill="${c}"/><circle r="14" fill="#fff"/>`; },
  candado: c => `<rect x="-30" y="-8" width="60" height="50" rx="9" fill="${c}"/><path d="M -18 -8 V -22 A 18 18 0 0 1 18 -22 V -8" stroke="${c}" stroke-width="9" fill="none"/>`,
  reloj: c => `<circle r="46" fill="none" stroke="${c}" stroke-width="10"/><path d="M 0 -26 V 0 L 20 12" stroke="${c}" stroke-width="9" stroke-linecap="round" fill="none"/>`,
  libro: c => `<path d="M -46 -30 H -4 V 34 H -46 Z M 4 -30 H 46 V 34 H 4 Z" fill="${c}"/>`,
  wifi: c => `<g fill="none" stroke="${c}" stroke-width="9" stroke-linecap="round"><path d="M -42 -10 A 60 60 0 0 1 42 -10"/><path d="M -26 8 A 36 36 0 0 1 26 8"/></g><circle cy="30" r="7" fill="${c}"/>`,
  gota: c => `<path d="M 0 -46 C 30 -6 36 10 36 22 A 36 36 0 0 1 -36 22 C -36 10 -30 -6 0 -46 Z" fill="${c}"/><path d="M -14 20 A 16 16 0 0 0 4 36" stroke="#fff" stroke-width="7" stroke-linecap="round" fill="none" opacity=".6"/>`,
  sol: c => { let d = ''; for (let i = 0; i < 10; i++) d += `<rect x="-5" y="-58" width="10" height="18" rx="5" fill="${c}" transform="rotate(${i * 36})"/>`; return d + `<circle r="30" fill="${c}"/>`; },
  arcoiris: c => ['#E4572E', '#F4A259', '#F6D55C', '#6BBF59', '#3CAEA3', '#3B6EA8', '#7A4EAB'].map((k, i) => `<path d="M ${-48 + i * 5} 30 A ${48 - i * 5} ${48 - i * 5} 0 0 1 ${48 - i * 5} 30" stroke="${k}" stroke-width="6" fill="none" stroke-linecap="round"/>`).join(''),
  casa: c => `<path d="M -46 0 L 0 -44 L 46 0 H 32 V 40 H -32 V 0 Z" fill="${c}"/><rect x="-9" y="12" width="18" height="28" fill="#fff" opacity=".9"/>`,
};
function icono(nombre, x, y, s, color, op) {
  const fn = ICONOS[nombre]; if (!fn) throw new Error('Icono desconocido: ' + nombre + ' (hay: ' + Object.keys(ICONOS).join(', ') + ')');
  return `<g transform="translate(${f(x)} ${f(y)}) scale(${f(s / 100)})" opacity="${f(op === undefined ? 1 : op)}">${fn(color || TEMA.acento)}</g>`;
}

/* ---------- personaje sencillo (busto): piel, pelo, camisa, ánimo ---------- */
function personaje(o) {
  const t = o.t || 0, ph = o.ph || 0, sc = o.s || 1, mood = o.mood || 'smile', piel = o.piel || '#E8B98F', pelo = o.pelo || '#3B2A20', camisa = o.camisa || TEMA.acento2;
  const bl = ((t + ph * 2.3) % 3.7) < 0.13, bob = Math.sin((t + ph) * 1.6) * 2 + (o.bounce || 0);
  let g = `<g transform="translate(${f(o.x)} ${f(o.y + bob * sc)}) scale(${f(sc)})" opacity="${f(o.op === undefined ? 1 : o.op)}">`;
  const estilo = o.pelo_estilo || 'corto';
  if (estilo === 'largo') g += `<path d="M -60 -70 Q -66 -142 0 -144 Q 66 -142 60 -70 Q 78 -8 68 44 Q 40 62 0 58 Q -40 62 -68 44 Q -78 -8 -60 -70 Z" fill="${pelo}"/>`;
  if (estilo === 'rizos') g += `<g fill="${pelo}"><circle cy="-122" r="62"/><circle cx="-46" cy="-98" r="34"/><circle cx="46" cy="-98" r="34"/><circle cx="-62" cy="-70" r="22"/><circle cx="62" cy="-70" r="22"/></g>`;
  g += `<rect x="-15" y="-26" width="30" height="40" rx="12" fill="${piel}" opacity=".9"/>`;
  g += `<path d="M -96 150 L -94 46 Q -92 12 -56 6 L -18 -4 Q 0 16 18 -4 L 56 6 Q 92 12 94 46 L 96 150 Z" fill="${camisa}"/>`;
  g += o.brazos || '';
  g += `<path d="M -49 -70 Q -49 -122 0 -122 Q 49 -122 49 -70 Q 49 -20 0 -8 Q -49 -20 -49 -70 Z" fill="${piel}"/>`;
  g += `<circle cx="-29" cy="-44" r="9" fill="#FF7F6B" opacity=".28"/><circle cx="29" cy="-44" r="9" fill="#FF7F6B" opacity=".28"/>`;
  if (estilo === 'corto') g += `<path d="M -52 -72 Q -54 -132 0 -132 Q 54 -132 52 -72 Q 40 -100 0 -104 Q -40 -100 -52 -72 Z" fill="${pelo}"/>`;
  if (estilo === 'largo') g += `<path d="M -51 -72 Q -54 -130 0 -130 Q 54 -130 51 -72 Q 46 -100 14 -104 Q -22 -106 -38 -84 Q -44 -76 -51 -72 Z" fill="${pelo}"/>`;
  if (estilo === 'rizos') g += `<path d="M -50 -76 Q -50 -114 0 -116 Q 50 -114 50 -76 Q 30 -98 0 -98 Q -30 -98 -50 -76 Z" fill="${pelo}"/>`;
  const ink = '#2B1B14', m = '#7A3B2E';
  if (mood === 'laugh') g += `<path d="M -28 -63 Q -18 -75 -8 -63 M 8 -63 Q 18 -75 28 -63" fill="none" stroke="${ink}" stroke-width="4" stroke-linecap="round"/>`;
  else if (bl) g += `<path d="M -26 -66 Q -18 -61 -10 -66 M 10 -66 Q 18 -61 26 -66" fill="none" stroke="${ink}" stroke-width="3.6" stroke-linecap="round"/>`;
  else if (mood === 'surprise') for (const sx of [-18, 18]) g += `<ellipse cx="${sx}" cy="-67" rx="10" ry="13" fill="#fff" stroke="#E7D6C4" stroke-width="1.6"/><circle cx="${sx}" cy="-67" r="5.6" fill="${ink}"/>`;
  else for (const sx of [-18, 18]) g += `<ellipse cx="${sx + (o.mira || 0)}" cy="-66" rx="6" ry="8.2" fill="${ink}"/><circle cx="${sx + (o.mira || 0) + 2}" cy="-69" r="2.3" fill="#fff"/>`;
  g += `<path d="${mood === 'worry' ? 'M -31 -80 Q -19 -86 -7 -93 M 7 -93 Q 19 -86 31 -80' : 'M -31 -86 Q -19 -92 -7 -87 M 7 -87 Q 19 -92 31 -86'}" fill="none" stroke="${pelo}" stroke-width="4.6" stroke-linecap="round"/>`;
  g += `<path d="M 0 -62 Q 5 -50 -1 -48" fill="none" stroke="#C48B65" stroke-width="3.2" stroke-linecap="round"/>`;
  if (mood === 'laugh') g += `<path d="M -19 -41 L 19 -41 Q 14 -18 0 -18 Q -14 -18 -19 -41 Z" fill="#8E3B35"/>`;
  else if (mood === 'calm') g += `<path d="M -12 -37 Q 0 -30 12 -37" fill="none" stroke="${m}" stroke-width="4.5" stroke-linecap="round"/>`;
  else if (mood === 'worry') g += `<path d="M -13 -29 Q 0 -40 13 -29" fill="none" stroke="${m}" stroke-width="4.5" stroke-linecap="round"/>`;
  else if (mood === 'surprise') g += `<ellipse cx="0" cy="-31" rx="7" ry="10" fill="#8E3B35"/>`;
  else g += `<path d="M -16 -39 Q 0 -24 16 -39" fill="none" stroke="${m}" stroke-width="4.5" stroke-linecap="round"/>`;
  return g + (o.frente || '') + '</g>';
}
function globo(x, y, txt, p, size, haciaX, haciaY) {     // globo de diálogo con colita hacia (haciaX, haciaY)
  if (p <= 0) return ''; const k = backOut(clamp(p)), s = (size || 30) * U, ls = envolver(txt, s, 700, 440 * U), w = Math.max(...ls.map(l => medir(l, s, 700))) + 48 * U, h = ls.length * s * 1.3 + 30 * U;
  x = clamp(x, w / 2 + 16 * U, W - w / 2 - 16 * U);   // el globo no se sale de la pantalla (vertical)
  let o = `<g transform="translate(${f(x)} ${f(y)}) scale(${f(k)})" opacity="${f(clamp(p * 2.2))}"><rect x="${f(-w / 2)}" y="${f(-h / 2)}" width="${f(w)}" height="${f(h)}" rx="${f(26 * U)}" fill="#fff" stroke="${TEMA.suave}" stroke-width="${f(4 * U)}"/>`;
  if (haciaX !== undefined) { const dx = clamp((haciaX - x) * .5, -w / 2 + 30 * U, w / 2 - 30 * U); o += `<path d="M ${f(dx - 14 * U)} ${f(h / 2 - 2)} L ${f(dx + 14 * U)} ${f(h / 2 - 2)} L ${f((haciaX - x) * .6)} ${f(h / 2 + 34 * U)} Z" fill="#fff" stroke="${TEMA.suave}" stroke-width="${f(4 * U)}" stroke-linejoin="round"/><rect x="${f(dx - 13 * U)}" y="${f(h / 2 - 6)}" width="${f(26 * U)}" height="8" fill="#fff"/>`; }
  ls.forEach((l, i) => { o += T(0, -h / 2 + 15 * U + s * 1.3 * (i + 1) - s * .3, l, s, 700, TEMA.tinta, 'middle'); });
  return o + '</g>';
}

/* ---------- escenas ---------- */
const ESCENAS = {};
function registrarEscena(nombre, fn) { ESCENAS[nombre] = fn; }
function fondoDecorado(t) {                              // manchas suaves que se mueven despacio
  let s = ''; [[.15, .2, 190], [.85, .75, 230], [.7, .12, 120]].forEach(([a, b, r], i) => { s += `<circle cx="${f(W * a + Math.sin(t * .3 + i) * 12)}" cy="${f(H * b + Math.cos(t * .25 + i) * 10)}" r="${f(r * U)}" fill="#fff" opacity=".35"/>`; });
  return s;
}
// escena "personajes": {tipo, suelo?: true, personajes: [{x, y (fracciones 0-1), s, ...personaje}], dialogo: [{quien, texto, a, b}], rotulo?}
registrarEscena('personajes', (e, tl, c) => {
  let s = fondoDecorado(c.t);
  if (e.suelo !== false) s += `<rect x="0" y="${f(H * .8)}" width="${W}" height="${f(H * .2)}" fill="${TEMA.acento2}" opacity=".18"/>`;
  const ps = e.personajes || [];
  ps.forEach((p, i) => { const ent = easeOut(seg(tl, .1 + i * .2, .7 + i * .2)); s += personaje(Object.assign({}, p, { x: p.x * W, y: p.y * H + (1 - ent) * 40 * U, s: (p.s || 1) * U * (V ? 1 : 1), t: c.t, ph: i * 1.7, op: ent })); });
  (e.objetos || []).forEach(o => { const q = easeOut(seg(tl, o.desde || 0, (o.desde || 0) + .7)); if (q > 0) s += icono(o.icono, o.x * W, o.y * H + (1 - q) * 20 * U, (o.s || 120) * U * (.6 + .4 * q), o.color || TEMA.acento, q); });   // objetos del cielo o del suelo (arcoíris, sol, gotas...)
  (e.dialogo || []).forEach(d => { const p = ps[d.quien || 0]; if (!p) return; const q = seg(tl, d.a, d.a + .4) * (1 - seg(tl, d.b - .3, d.b)); s += globo(clamp(p.x, .25, .75) * W, p.y * H - 200 * U * (p.s || 1) - 40 * U, d.texto, q, 30, p.x * W, p.y * H - 150 * U * (p.s || 1)); });
  if (e.rotulo) s += T(W / 2, H * .13, e.rotulo, 44 * U, 800, TEMA.tinta, 'middle', `opacity="${f(easeOut(seg(tl, .1, .6)))}"`);
  return s;
});
registrarEscena('texto', (e, tl, c) => {                 // tarjeta de texto grande
  let s = fondoDecorado(c.t); const k = c.primera ? 1 : easeOut(seg(tl, .05, .6)), p = parrafo(W / 2, 0, e.texto, (e.tamano || 64) * U, 800, TEMA.tinta, W * .8, 'middle', 1.2);
  s += `<g transform="translate(0 ${f(H / 2 - p.h / 2 + (1 - k) * 30)})" opacity="${f(k)}">${p.svg}</g>`;
  if (e.detalle) s += T(W / 2, H / 2 + p.h / 2 + 50 * U, e.detalle, 32 * U, 600, TEMA.gris, 'middle', `opacity="${f(c.primera ? 1 : easeOut(seg(tl, .5, 1)))}"`);
  return s;
});

/* ---------- subtítulos y marca ---------- */
function subtitulos(t) {
  const c = (P.cues || []).find(c => t >= c.a && t < c.b); if (!c) return '';
  const a = Math.min(seg(t, c.a, c.a + .15), 1 - seg(t, c.b - .15, c.b)); let size = 34 * U; const maxW = W * .88;
  const lines = c.lines || envolver(c.texto, size, 600, maxW); let wm = Math.max(...lines.map(l => medir(l, size, 600)));
  if (wm > maxW) { size = Math.floor(size * maxW / wm); wm = maxW; }
  const lh = Math.round(size * 1.35), w = wm + 56 * U, h = lines.length * lh + 22 * U, margen = V ? H * .17 : H * .045, x = W / 2 - w / 2, y = H - margen - h;
  let o = `<g opacity="${f(a)}"><rect x="${f(x)}" y="${f(y)}" width="${f(w)}" height="${f(h)}" rx="${f(18 * U)}" fill="${TEMA.caja}"/>`;
  lines.forEach((l, i) => { o += T(W / 2, y + 11 * U + lh * (i + 1) - lh * .26, l, size, 600, '#fff', 'middle'); });
  return o + '</g>';
}
function marca() {                                       // texto pequeño en una esquina (ej. el nombre del canal), opcional
  if (!P.marca) return ''; return T(W - 24 * U, 38 * U, P.marca, 22 * U, 700, TEMA.gris, 'end', 'opacity=".8"');
}

function render(t) {
  const es = P.escenas; const e = es.find(s => t >= s.inicio && t < s.fin) || es[es.length - 1]; const tl = t - e.inicio, dur = e.fin - e.inicio;
  const primera = es.indexOf(e) === 0;                   // la primera escena ya está completa en el cuadro 0 (es lo que se ve de miniatura)
  const fade = Math.min(primera ? 1 : seg(tl, 0, .35), 1 - seg(tl, dur - .35, dur));
  const fn = ESCENAS[e.tipo]; if (!fn) throw new Error('Tipo de escena desconocido: ' + e.tipo + ' (hay: ' + Object.keys(ESCENAS).join(', ') + ')');
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><defs><linearGradient id="fg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${TEMA.fondoA}"/><stop offset="1" stop-color="${TEMA.fondoB}"/></linearGradient></defs><rect width="${W}" height="${H}" fill="url(#fg)"/>` +
    `<g opacity="${f(e.sin_fundido ? 1 : fade)}">${fn(e, tl, { W, H, V, U, t, dur, TEMA, primera })}</g>${subtitulos(t)}${marca()}</svg>`;
  document.getElementById('app').innerHTML = svg;
}
window.TOTAL = Math.max(...P.escenas.map(e => e.fin)); window.CUES = P.cues || []; window.render = render; window.READY = true;
