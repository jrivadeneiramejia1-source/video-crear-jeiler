---
name: animacion-2d
description: Motor para dibujar animaciones 2D sencillas con código (sin programas de dibujo ni internet): personajes de busto con ánimos, globos de diálogo, tarjetas de texto, subtítulos y transiciones, en horizontal o vertical desde el mismo proyecto. Se describe el video en un archivo JSON y se renderiza cuadro a cuadro. Usar cuando el usuario diga "una animación de...", "un cuento animado", "dibujitos sencillos", "un corto 2D" o "personajes que hablen". Para explicar o comparar con gráficos usar video-explicativo. No hace 3D ni realismo.
---

# Animación 2D con código

Un **motor** que dibuja cada cuadro como un SVG en un navegador sin pantalla (Chromium) y los une con ffmpeg. Los dibujos son sencillos a propósito: personajes de busto, fondos suaves, texto claro. Lo describe un `proyecto.json`; el mismo proyecto sale **horizontal (1280x720) y vertical (720x1280)**.

## Reglas
- **Solo personajes y textos inventados** en los ejemplos y plantillas de este repo (es público). Nunca poner nombres, historias o voces de personas reales en el repo; los proyectos con datos reales viven fuera de él.
- Mirar imágenes sueltas (`stills`/`hoja`) **antes** de renderizar el video completo: renderizar cuesta unos 2 minutos por minuto de video y por formato.
- No sobrescribe videos existentes. El video sale **sin sonido**: la voz y la música se pegan después (`video-explicativo`, `voz-sintetica`, `musica-y-efectos` o `ffmpeg-skill`).
- Claude no ve el movimiento: mide y mira cuadros; la fluidez la juzga Jeiler.
- Sin 3D ni caras realistas: para eso, las skills de 3D de este repo (cuando existan).

## Instalar (una vez)
```bash
bash scripts/instalar_render.sh    # Playwright (Python) y un Chromium; en las sesiones en la nube ya hay uno
PY=~/.cache/video-jeiler/venv/bin/python
```

## Proceso
1. **Escribir `proyecto.json`** (ver `ejemplo/proyecto.json`): `escenas` con `tipo`, `inicio` y `fin` en segundos (contiguas, sin huecos) y `cues` (subtítulos: `a`, `b` y `lines` o `texto`). Tipos incluidos: `personajes` (hasta 2 o 3 personas con `mood`: smile, laugh, calm, worry, surprise; `pelo_estilo`: corto, largo, rizos; colores; `dialogo` con globos) y `texto` (tarjeta de texto grande). `video-explicativo` agrega `titulo`, `lista`, `comparar`, `numero`, `pasos`, `barras` y `cierre` (se cargan con `--extra`).
2. **Verificar:** `$PY scripts/render.py proyecto.json verificar` (errores de la página, escenas seguidas, subtítulos dentro del video).
3. **Mirar:** `$PY scripts/render.py proyecto.json hoja hoja.png --n 8` (8 cuadros repartidos) o `stills 5 12.5 30` (momentos exactos). Abrir las imágenes a tamaño completo: textos que caben, nada tapado.
4. **Renderizar:** `$PY scripts/render.py proyecto.json video silencio.mp4` (y `--ancho 720 --alto 1280` para vertical; `--fps 24` para ir más rápido).
5. **Pegar la voz** y la música con `ffmpeg-skill` y **verificar** con `verificar-video` (de `video-editar-jeiler`) o `check.py`.

## Ampliar el motor
Nuevos tipos de escena: un archivo `.js` con `registrarEscena('nombre', (e, tl, c) => svg)` (ver `motor/motor.js`: funciones `T`, `parrafo`, `icono`, `personaje`, `globo`; `c.W`, `c.H`, `c.V`, `c.U` para adaptarse a horizontal y vertical) y cargarlo con `--extra`. Íconos incluidos: check, cruz, flecha, estrella, corazon, bombilla, telefono, nube, engranaje, candado, reloj, libro, wifi, casa.

## Señales de alerta
- Texto que se sale del cuadro en vertical (revisar siempre las dos formas).
- Escenas con huecos o choques de tiempo (`verificar` lo dice).
- Prometer personajes detallados o movimientos complejos: el motor hace dibujos sencillos.
- Nombres o historias reales dentro del repo.

## Verificación
- [ ] `verificar` sin errores.
- [ ] Se miró la hoja de cuadros en horizontal y en vertical.
- [ ] El video final se comprobó con `check.py` o `verificar-video`.
- [ ] Se dijo que no se pudo ver el movimiento.

## Qué se probó (2026-11-04)
Un cuento de ejemplo **inventado** de 20 s (4 escenas, 2 personajes, 3 globos y subtítulos) se renderizó en horizontal y en vertical sin errores (600 cuadros en unos 38 s cada uno, a 30 fps); el vertical pasó la verificación de Shorts sin fallos graves. Se miró una hoja de 8 cuadros y un cuadro vertical a tamaño completo. Error real encontrado y corregido: los globos de diálogo se salían de la pantalla en vertical. El motor se basa en el método del kit de cortometrajes de Jeiler (SVG por cuadro, Chromium y ffmpeg), pero es **nuevo y general**: no incluye sus personajes, historias ni nombres. **No se probó** con más de 3 personajes, con escenas largas (más de 3 minutos), con otras tipografías ni en otros computadores (necesita Chromium y las fuentes Inter o DejaVu).
