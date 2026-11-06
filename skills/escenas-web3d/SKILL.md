---
name: escenas-web3d
description: >-
  Motor para escenas 3D sencillas de navegador (Three.js + GSAP en Chromium sin pantalla): formas 3D, **personajes y modelos GLB con animación**, imágenes en 3D, luces y sombras, cámara que se mueve y curvas de movimiento (rebotes, giros, entradas suaves), descritas en un JSON y renderizadas cuadro a cuadro en horizontal o vertical. Usar cuando el usuario pida "una escena 3D ligera", "figuras 3D que se muevan", "una intro o fondo 3D", "objetos girando con cámara" o cuando Blender (video-3d) sea demasiado pesado. No genera personajes a medida con cara y pelo (para eso, video-3d e historia-3d) ni dibujos 2D (animacion-2d).
---

# Escenas 3D de navegador (Three.js + GSAP)

Lo mismo que hace `animacion-2d` (Chromium sin pantalla + ffmpeg, cuadro a cuadro) pero con **3D real**: **Three.js** dibuja la escena (luces, sombras, cámara) y **GSAP** manda los tiempos y las curvas de movimiento. Sale **sin sonido**.
Idea tomada de un video de TikTok sobre 10 repos de GitHub para «estudio de motion» (Three.js, GSAP, etc.); el código es propio. Las curvas, fundidos, títulos y cortes se inspiran en cómo OpenCut (MIT) organiza su línea de tiempo; no se copió código.

## Reglas
- **Solo formas y textos inventados** en ejemplos y plantillas (el repo es público). Proyectos con datos reales viven fuera.
- Three.js (MIT) y GSAP (licencia gratuita de GSAP, no es MIT) se bajan a `~/.cache/video-jeiler/web`; **nunca se copian al repo**. Antes de usar GSAP en algo comercial o de un cliente, leer https://gsap.com/standard-license.
- Mirar imágenes sueltas (`stills`/`hoja`) **antes** de renderizar el video.
- No sobrescribe videos existentes. Claude no ve el movimiento: mide y mira cuadros; la fluidez la juzga Jeiler.
- Formas básicas (caja, esfera, cilindro, cono, toro, plano) y modelos `.glb` que ya traigan su textura y animaciones. Personajes a medida con cara y pelo: `video-3d` / `historia-3d`.
- Modelos e imágenes de terceros **no entran al repo**: viven en `~/.cache/video-jeiler/recursos3d/` o junto a tu `proyecto.json`. Solo CC0 o con permiso (ver `recursos-3d`).

## Instalar (una vez)
```bash
bash scripts/instalar_web3d.sh     # Playwright, Chromium (si no hay), Three.js (con GLTFLoader) y GSAP en la carpeta de caché
bash scripts/descargar_personajes_kaykit.sh   # (opcional) 5 personajes CC0 con esqueleto y 76 animaciones, comprueba la licencia
PY=~/.cache/video-jeiler/venv/bin/python
```

## Proceso
1. **Escribir `proyecto.json`** (ver `ejemplo/proyecto.json`): `duracion`, `fondo`, `suelo`, `niebla`, `camara` (`pos`, `mira`, `fov`, `mov` con tramos `a`–`b` en segundos), `luces`, `objetos` (`forma`, `color`, `pos`, `tam`, `rot` en radianes, `metal`, `rugoso`, `anim` con `prop`: `pos`|`rot`|`esc`, `hasta`, `a`, `b`, `ease`: `suave`, `frena`, `arranca`, `arranca-frena`, `pop` (se pasa y vuelve), `lineal`, una curva propia `[x1,y1,x2,y2]` (cubic-bezier como en CSS) o cualquier nombre de GSAP como `bounce.out`), `cues` (subtítulos: `a`, `b`, `texto`) y, opcionales:
   - `fundido`: `{"entrada": 0.5, "salida": 0.7, "color": "#000000"}` (aparece y se apaga desde/hacia ese color).
   - `titulos`: `a`, `b`, `texto`, `lugar` (`arriba`|`centro`|`abajo`), `entrada` (`sube`|`fundido`|`pop`), `color`, `tam` (px). Distintos de los subtítulos: son grandes y animados.
   - `luces.entorno`: `"estudio"` añade luz de estudio (reflejos y brillo realistas en materiales y modelos); `entorno_fuerza` (0 a 1).
   - Modelos: objeto con `"modelo": "kaykit/Knight.glb"` (se busca junto al proyecto y en `recursos3d/`), `clip`: nombre o número de la animación (`bucle`: false para una sola vez; `vel`: velocidad; `clip_a`: segundo en que empieza), `pos`/`rot`/`tam` (número o `[x,y,z]`) y las mismas `anim` de movimiento. `verificar` **lista los clips** de cada modelo.
   - Imágenes: objeto con `"imagen": "fotos/logo.png"` y `"tam": [ancho, alto, 1]` (plano con la imagen, con transparencia).
   - Corte de cámara: en `camara.mov`, un tramo `{"corte": 4, "pos": [...], "mira": [...]}` salta de golpe a esa vista en el segundo 4.
2. **Verificar:** `$PY scripts/render_web3d.py proyecto.json verificar`.
3. **Mirar:** `... hoja hoja.png --n 8` o `... stills 0 2.5 5`. Abrirlas a tamaño completo: nada cortado ni tapado.
4. **Renderizar:** `... video silencio.mp4` (y `--ancho 720 --alto 1280` para vertical; en vertical el motor conserva el ancho de visión de la versión horizontal).
5. **Pegar voz y música** con `ffmpeg-skill` y **verificar** con `verificar-video`.

## Señales de alerta
- Objetos cortados por el borde: alejar la cámara (`pos`) o subir `fov`.
- Animaciones de un mismo objeto y propiedad que se pisan en el tiempo (el motor las encadena en orden de `a`).
- Prometer realismo: son formas simples o modelos de otros con sombras suaves.
- Un `clip` mal escrito: `verificar` dice el error y lista los clips válidos; el motor no adivina.
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

### Modelos, imágenes y luz de estudio (2026-11-06)
Idea sacada de mirar con REA el editor de Three.js (threejs.org/editor, MIT): usa `GLTFLoader`, `SkeletonUtils`, `RoomEnvironment` y un cargador de texturas. Probado con **Knight y Mage de KayKit Adventurers 1.0 (CC0)**: 76 clips cada uno, 6 s a 30 fps en horizontal (59 s) y vertical (40 s), H.264 correcto; las poses cambian entre cuadros (PSNR 20,7 dB entre 2,0 y 2,3 s); un plano con imagen rota en 3D; los errores (clip mal escrito, modelo o imagen que no existe) salen con mensaje claro y código de salida 1; `/m/` no sirve archivos fuera de las carpetas permitidas (`..`, `%2e%2e` y rutas absolutas dan 404). **No se probó** con modelos con compresión Draco/KTX2, con varias animaciones mezcladas a la vez, con modelos de más de 20 MB, ni con tarjeta gráfica real; la cara de los modelos no se anima (son dibujos fijos).
