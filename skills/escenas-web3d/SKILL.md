---
name: escenas-web3d
description: >-
  Motor para escenas 3D sencillas de navegador (Three.js + GSAP en Chromium sin pantalla): formas 3D con luces y sombras, cámara que se mueve y objetos con curvas de movimiento (rebotes, giros, entradas suaves), descritas en un JSON y renderizadas cuadro a cuadro en horizontal o vertical. Usar cuando el usuario pida "una escena 3D ligera", "figuras 3D que se muevan", "una intro o fondo 3D", "objetos girando con cámara" o cuando Blender (video-3d) sea demasiado pesado. No hace personajes con cara (para eso, video-3d e historia-3d) ni dibujos 2D (animacion-2d).
---

# Escenas 3D de navegador (Three.js + GSAP)

Lo mismo que hace `animacion-2d` (Chromium sin pantalla + ffmpeg, cuadro a cuadro) pero con **3D real**: **Three.js** dibuja la escena (luces, sombras, cámara) y **GSAP** manda los tiempos y las curvas de movimiento. Sale **sin sonido**.
Idea tomada de un video de TikTok sobre 10 repos de GitHub para «estudio de motion» (Three.js, GSAP, etc.); el código es propio. Las curvas, fundidos, títulos y cortes se inspiran en cómo OpenCut (MIT) organiza su línea de tiempo; no se copió código.

## Reglas
- **Solo formas y textos inventados** en ejemplos y plantillas (el repo es público). Proyectos con datos reales viven fuera.
- Three.js (MIT) y GSAP (licencia gratuita de GSAP, no es MIT) se bajan a `~/.cache/video-jeiler/web`; **nunca se copian al repo**. Antes de usar GSAP en algo comercial o de un cliente, leer https://gsap.com/standard-license.
- Mirar imágenes sueltas (`stills`/`hoja`) **antes** de renderizar el video.
- No sobrescribe videos existentes. Claude no ve el movimiento: mide y mira cuadros; la fluidez la juzga Jeiler.
- Solo formas básicas (caja, esfera, cilindro, cono, toro, plano). Personajes con cara y pelo: `video-3d` / `historia-3d`.

## Instalar (una vez)
```bash
bash scripts/instalar_web3d.sh     # Playwright, Chromium (si no hay), Three.js y GSAP en la carpeta de caché
PY=~/.cache/video-jeiler/venv/bin/python
```

## Proceso
1. **Escribir `proyecto.json`** (ver `ejemplo/proyecto.json`): `duracion`, `fondo`, `suelo`, `niebla`, `camara` (`pos`, `mira`, `fov`, `mov` con tramos `a`–`b` en segundos), `luces`, `objetos` (`forma`, `color`, `pos`, `tam`, `rot` en radianes, `metal`, `rugoso`, `anim` con `prop`: `pos`|`rot`|`esc`, `hasta`, `a`, `b`, `ease`: `suave`, `frena`, `arranca`, `arranca-frena`, `pop` (se pasa y vuelve), `lineal`, una curva propia `[x1,y1,x2,y2]` (cubic-bezier como en CSS) o cualquier nombre de GSAP como `bounce.out`), `cues` (subtítulos: `a`, `b`, `texto`) y, opcionales:
   - `fundido`: `{"entrada": 0.5, "salida": 0.7, "color": "#000000"}` (aparece y se apaga desde/hacia ese color).
   - `titulos`: `a`, `b`, `texto`, `lugar` (`arriba`|`centro`|`abajo`), `entrada` (`sube`|`fundido`|`pop`), `color`, `tam` (px). Distintos de los subtítulos: son grandes y animados.
   - Corte de cámara: en `camara.mov`, un tramo `{"corte": 4, "pos": [...], "mira": [...]}` salta de golpe a esa vista en el segundo 4.
2. **Verificar:** `$PY scripts/render_web3d.py proyecto.json verificar`.
3. **Mirar:** `... hoja hoja.png --n 8` o `... stills 0 2.5 5`. Abrirlas a tamaño completo: nada cortado ni tapado.
4. **Renderizar:** `... video silencio.mp4` (y `--ancho 720 --alto 1280` para vertical; en vertical el motor conserva el ancho de visión de la versión horizontal).
5. **Pegar voz y música** con `ffmpeg-skill` y **verificar** con `verificar-video`.

## Señales de alerta
- Objetos cortados por el borde: alejar la cámara (`pos`) o subir `fov`.
- Animaciones de un mismo objeto y propiedad que se pisan en el tiempo (el motor las encadena en orden de `a`).
- Prometer realismo: son formas simples con sombras suaves.
- Renderizar sin mirar antes `hoja`/`stills`.

## Verificación
- [ ] `verificar` sin errores.
- [ ] Se miró la hoja en horizontal y en vertical.
- [ ] El video final se comprobó con `check.py` o `verificar-video`.
- [ ] Se dijo que no se pudo ver el movimiento.

## Qué se probó (2026-11-06)
Una escena de ejemplo **inventada** de 8 s (caja, esfera y cono; giro, subida, rebote, cámara orbitando con un corte a los 4 s, curvas `pop`/`suave`/bezier, fundido, 2 títulos y 2 subtítulos) se renderizó en horizontal (1280x720) y vertical (720x1280), 240 cuadros a 30 fps en unos 25-29 s cada una, con H.264 correcto según `ffprobe`; se miró la hoja de 8 cuadros y un cuadro vertical. Error real corregido: en vertical se cortaban objetos (ahora se conserva el ancho de visión). Probado con Three.js 0.187.0, GSAP 3.15.1 y el Chromium de la nube (dibuja con SwiftShader, sin tarjeta gráfica). **No se probó** con modelos GLB/personajes, texturas, escenas largas (más de 1 minuto), otros computadores ni con tarjeta gráfica real.

### Ampliación (2026-11-06)
Se midió con cuadros sueltos: el fundido empieza y termina casi negro (brillo 16 de 255 en el cuadro 0), el corte de los 4 s cambia la imagen de golpe (PSNR 19 dB entre 3,99 s y 4,01 s), el título «pop» entra y el vertical conserva títulos y subtítulos dentro del cuadro. **No se probó** el título `fundido`/`abajo`, curvas bezier propias con valores extremos ni un corte con varias cámaras seguidas.
