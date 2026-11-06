---
name: escenas-web3d
description: >-
  Motor para escenas 3D de navegador (Three.js + GSAP en Chromium sin pantalla): **historias en una casa con personajes ya hechos que caminan sin patinar, se voltean, se sientan y saludan**, cuartos con ventanas y puertas, muebles listos, encuadres de cine (plano general, medio, primer plano, de dos, picado), formas 3D, modelos GLB/FBX con animación, imágenes en 3D, luces y sombras, cámara que se mueve y curvas de movimiento (rebotes, giros, entradas suaves), descritas en un JSON y renderizadas cuadro a cuadro en horizontal o vertical. Usar cuando el usuario pida "una escena 3D ligera", "figuras 3D que se muevan", "una intro o fondo 3D", "objetos girando con cámara" o cuando Blender (video-3d) sea demasiado pesado. No genera personajes a medida con cara y pelo (para eso, video-3d e historia-3d) ni dibujos 2D (animacion-2d).
---

# Escenas 3D de navegador (Three.js + GSAP)

Lo mismo que hace `animacion-2d` (Chromium sin pantalla + ffmpeg, cuadro a cuadro) pero con **3D real**: **Three.js** dibuja la escena (luces, sombras, cámara) y **GSAP** manda los tiempos y las curvas de movimiento. Sale **sin sonido**.
Idea tomada de un video de TikTok sobre 10 repos de GitHub para «estudio de motion» (Three.js, GSAP, etc.); el código es propio. Las curvas, fundidos, títulos y cortes se inspiran en cómo OpenCut (MIT) organiza su línea de tiempo; no se copió código.

## Reglas
- **Solo formas y textos inventados** en ejemplos y plantillas (el repo es público). Proyectos con datos reales viven fuera.
- Three.js (MIT) y GSAP (licencia gratuita de GSAP, no es MIT) se bajan a `~/.cache/video-jeiler/web`; **nunca se copian al repo**. Antes de usar GSAP en algo comercial o de un cliente, leer https://gsap.com/standard-license.
- Mirar imágenes sueltas (`stills`/`hoja`) **antes** de renderizar el video.
- No sobrescribe videos existentes. Claude no ve el movimiento: mide y mira cuadros; la fluidez la juzga Jeiler.
- **No dibujar de cero lo que ya existe:** personajes, muebles y edificios salen de los paquetes CC0 (`catalogo.py`); el tiempo se gasta en que el movimiento tenga sentido (caminar, girar, mirarse, encuadrar). Personajes a medida con cara y pelo: `video-3d` / `historia-3d`.
- Modelos e imágenes de terceros **no entran al repo**: viven en `~/.cache/video-jeiler/recursos3d/` o junto a tu `proyecto.json`. Solo CC0 o con permiso (ver `recursos-3d`).

## Instalar (una vez)
```bash
bash scripts/instalar_web3d.sh     # Playwright, Chromium (si no hay), Three.js (con GLTFLoader) y GSAP en la carpeta de caché
python3 scripts/descargar_paquetes.py --lista                 # personajes, casas, muebles, cocina, ciudad (todo CC0, la licencia se comprueba al bajar)
python3 scripts/descargar_paquetes.py kaykit-aventureros kaykit-muebles   # o --todo (~30 s, ~150 MB en la caché)
python3 scripts/catalogo.py cama sofá ventana                 # busca modelos en español o inglés y da la ruta para «modelo»
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
   - **Personaje con acciones** (en vez de `clip`): `"acciones": [{"a":0,"clip":"Idle"}, {"a":1,"clip":"Walking_A","ir_a":[x,z]}, {"clip":"Idle","mirar":"leo"}, {"a":12,"clip":"Spellcast_Raise","bucle":false}]`. Cada acción entra con un fundido corto desde la anterior (`mezcla`, 0,3 s). **`ir_a`** camina de verdad al punto, de frente a la marcha, y **si no pones `b` la duración sale de la velocidad natural de esa animación** (el motor la mide con los pies: no patina). Sin `a` empieza al terminar la anterior; `dura` fija cuánto dura una acción sin fin. `mirar`: id de otro personaje o `[x,z]`; `mirar_grados`. `vel`: acelera o frena la animación. Los nombres de clip pueden ir cortos (`Walk` en vez de `CharacterArmature|Walk`). `alto`: metros reales del personaje (todos quedan a escala); `frente`: giro si el modelo no mira a +Z; `piel`: color (`"#c98f63"`) para los personajes de Quaternius, que traen cara y manos casi negras.
   - **`cuarto`** (casa por dentro): `{"ancho":11,"fondo":7,"alto":3.9,"color_pared":"#f1e6d2","color_piso":"#b98b5e","pared_oculta":["frente"],"ventanas":[{"pared":"fondo","x":-2.2,"ancho":2.2,"alto":1.8,"y":1.2}],"puertas":[{"pared":"izq","x":-0.5,"ancho":1.5,"alto":2.9}]}`. Las paredes llevan el hueco exacto, marco y vidrio. Paredes: `fondo`, `frente`, `izq`, `der`; `x` se mide desde el centro de la pared mirándola desde adentro. Muebles: objetos con `modelo`. `luces.puntuales`: lámparas `[{"pos":[x,y,z],"fuerza":14}]`.
   - **`tomas`** (encuadres; cada una corta de golpe a la siguiente): `{"a":4,"b":9.6,"plano":"americano","objetivo":"ana","lado":"tres-cuartos","empuja":0.2}`. `plano`: `general`, `cuerpo`, `americano`, `medio`, `primer-plano`, `detalle`, `sobre-hombro` (con `desde` y `objetivo`). `objetivos`: dos o más (plano de dos: el primero a la izquierda). `punto: [x,z]` apunta a un lugar. `lado`: `frente`, `der`, `izq`, `atras`, `tres-cuartos`, `tres-cuartos-izq` o grados; `angulo`: `picado`, `contrapicado` o grados; `empuja`: acercamiento lento (0 a 1); `orbita`: grados; `seguir:false` fija la cámara donde estaba el personaje al empezar; `distancia`, `vis`, `y`, `fov` para ajustar. **El encuadre se adapta a la altura y al tamaño de la cabeza de cada personaje** (los de cabeza grande no salen cortados).
   - **Escala**: KayKit (personajes ≈2,4–2,7 unidades + sus muebles) y Quaternius (FBX; con `escala` por defecto 0,005 quedan en metros) son dos mundos: no mezclar personajes de uno con muebles del otro sin `alto`/`escala`. En el mundo KayKit el cuarto debe medir ≈ 11×7×3,9 y las puertas 2,9 de alto.
2. **Verificar:** `$PY scripts/render_web3d.py proyecto.json verificar` (lista clips, velocidades de caminata y avisos como «camina apurado/patinando» o «la acción empieza antes de que termine la anterior»).
3. **Mirar:** `... hoja hoja.png --n 8` o `... stills 0 2.5 5`. Abrirlas a tamaño completo: nada cortado ni tapado.
4. **Renderizar:** `... video silencio.mp4` (y `--ancho 720 --alto 1280` para vertical; en vertical el motor conserva el ancho de visión de la versión horizontal).
5. **Pegar voz y música** con `ffmpeg-skill` y **verificar** con `verificar-video`.

## Señales de alerta
- Objetos cortados por el borde: alejar la cámara (`pos`) o subir `fov`.
- Animaciones de un mismo objeto y propiedad que se pisan en el tiempo (el motor las encadena en orden de `a`).
- Prometer realismo: son formas simples o modelos de otros con sombras suaves.
- Un `clip` mal escrito: `verificar` dice el error y lista los clips válidos; el motor no adivina.
- Renderizar sin mirar antes `hoja`/`stills`.
- Caras de Quaternius en primer plano: no tienen boca ni pupilas (solo ojos blancos); usar KayKit para primeros planos con emoción y Quaternius para fondo y planos lejanos.
- Un personaje sentándose o recogiendo algo: el clip existe (`Sit_Chair_Down`, `SitDown`, `PickUp`) pero la altura de la silla y del personaje hay que ajustarla mirando un cuadro; el motor no la adivina.
- Duraciones de caminata largas con personajes KayKit (0,7 m/s): acercar los puntos de partida o usar `Running_A`.

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

### Historias en una casa (2026-11-06)
Ejemplo `ejemplo/historia-casa.json` (inventado, 17 s): cuarto de 11×7 con 2 ventanas y 1 puerta, 9 muebles KayKit, **Ana** (Mage) entra por la puerta y camina 5,7 m hasta el comedor, **Leo** (Barbarian) la saluda; 4 tomas (general del cuarto, seguimiento de Ana, plano de dos, primer plano de Leo), título, fundido y subtítulo. Renderizado a 24 fps en horizontal (408 cuadros, 2 min 46 s) y vertical (2 min 31 s), H.264 correcto, sin errores de la página.
- **Caminata medida, no a ojo:** se rastreó el hueso del pie de Ana durante 6,5 s: el pie apoyado se mueve en el mundo a **0,09 m/s, el 13 % de la velocidad del cuerpo (0,68 m/s)**; el motor midió esa velocidad natural con la misma técnica (pie apoyado que va hacia atrás a la velocidad del cuerpo; dos estimaciones distintas coinciden dentro de ±10 %). Para Quaternius «Walk» salió 1,02 m/s y para KayKit «Walking_A» 0,68 m/s a escala natural.
- **Errores reales hallados y corregidos al medir:** (1) con el tiempo detenido Three.js no reinicia el ciclo de una animación: el personaje se congelaba en la última pose tras el primer ciclo (se vio porque la altura del pie quedaba constante); ahora el ciclo se calcula aquí. (2) Los FBX de Quaternius oscurecían los colores dos veces (Blender los guarda lineales). (3) La altura de los FBX hay que medirla con el personaje ya posado. (4) Las tomas de dos personajes quedaban pegadas a uno: ahora la cámara se pone de lado respecto a la línea entre ambos. (5) El plano medio/primer plano salía demasiado cerca con cabezas grandes: ahora se mide la cabeza.
- **No se probó:** sentarse en una silla de verdad (alineación de asiento), recoger objetos (`PickUp`), varios personajes caminando cruzados, escenas de más de 20 s en un computador distinto, `sobre-hombro`, ni las caras de Quaternius en primer plano (no tienen boca). La fluidez a simple vista la juzga Jeiler: hoy se midió que el pie no patina y se vieron cuadros sueltos.
