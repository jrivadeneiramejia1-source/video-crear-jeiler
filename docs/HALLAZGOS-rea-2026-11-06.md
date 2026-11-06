# Qué mostró REA (2026-11-06) y qué se hizo con eso

REA (`morluto/rea`, MIT) es una herramienta para mirar programas y páginas por dentro. Aquí se usó **solo de forma pasiva** (mirar, sin cambiar nada) sobre sitios públicos de **código abierto**: `rea list-browser-targets`, `inspect-web-page` y `analyze-web-bundle` contra un Chromium propio. No se analizó ningún editor ni sitio de IA cerrado: copiar su funcionamiento interno puede violar sus términos de uso y derechos de autor.

| Objetivo | Licencia | Lo que REA mostró | Qué se aprovechó |
|---|---|---|---|
| opencut.app (editor de video web) | MIT | Solo `Next.js` y `React` con confianza alta; el motor de video no se ve desde fuera (la página carga 12–22 scripts de la interfaz). | Poco. Se leyó su código abierto (`OpenCut-classic`): curvas con nombre (incluida «pop»), fundido, texto animado y cortes. Sin copiar código. |
| threejs.org/editor (editor de escenas de Three.js) | MIT | 127 scripts analizados, 0 fallas, mapa de módulos completo: `GLTFLoader`, `SkeletonUtils`, `BufferGeometryUtils`, `RoomEnvironment`, `TextGeometry` + `FontLoader`, `TGALoader`, `AnimationPathHelper`, un reproductor (`Player.js`) y un trazador de rayos. | **Modelos GLB con animación**, **luz de estudio** (`RoomEnvironment`) e **imágenes en 3D** en `escenas-web3d`. |

## Lo que se descartó (y por qué)
- **Texto 3D** (`TextGeometry`): necesita archivos de tipografía en formato propio que el paquete de Three.js no trae; los títulos animados en 2D ya cubren el caso.
- **Transcripción dentro del navegador** (OpenCut usa `@huggingface/transformers`): `video-editar-jeiler/subtitulos` ya transcribe con Parakeet.
- **Cambio de velocidad con tono intacto** (OpenCut usa `soundtouchjs`): `ffmpeg-skill` ya lo hace con `atempo`.
- **Editor web de Motion Canvas** (`editor.motioncanvas.io`): no se pudo abrir desde la nube (sin respuesta); su sitio de documentación sí abre, pero no aporta al motor.
- **Remotion**: licencia con límites; no se copia nada.
- **`video-editar-jeiler`**: ya trae karaoke ASS, fondo desenfocado, rampas de velocidad y forma de onda; no se cambió.

## Límites de REA en este uso
Su análisis es estático: dice qué módulos y librerías carga una página, no cómo funciona su motor por dentro; en sitios con la interfaz separada del motor (OpenCut) aporta poco y conviene leer el código abierto. En un sitio sin empaquetar (el editor de Three.js) el mapa de módulos sí fue muy útil.

## Segunda ronda: personajes, casas y encuadres ya hechos (2026-11-06)
Objetivo: no dibujar todo desde cero; reutilizar personajes, casas, ventanas y movimientos hechos, para gastar el esfuerzo en que el cuerpo y los brazos se muevan con sentido.

**Dónde se buscó:** la API de búsqueda de GitHub (organización `KayKit-Game-Assets`), las páginas de Quaternius en OpenGameArt (licencia leída en cada página), el índice de `devanshutak25/3d-resources` y listas de «awesome». Poly Pizza y kenney.nl responden 403 desde la nube; itch.io sigue bloqueado.

**REA en esta ronda:** `inspect-web-page --include-script-sources` sobre el ejemplo oficial `webgl_animation_skinning_blending` de Three.js (MIT). Devolvió el código fuente del ejemplo y confirmó la técnica: mezclar animaciones con pesos (`crossFadeTo` con «warping» para sincronizar ciclos de caminar y correr) y esperar a que termine el ciclo antes de mezclar. REA no puede decir cómo se verá; por eso la mezcla se calculó por tiempo y se midió con huesos (ver `escenas-web3d`).

| Paquete | Licencia | Resultado |
|---|---|---|
| KayKit Adventurers | CC0 | Elenco principal: cara con rasgos, 76 animaciones (caminar, sentarse, saludar, recoger, lanzar...). Estilo muñeco (cabeza grande). |
| KayKit Furniture / Restaurant / Prototype / City | CC0 | Muebles, cocina, paredes con ventana y puerta, ciudad; mismo estilo y escala que los personajes. Muebles probados. |
| Quaternius Animated Character Pack | CC0 | 52 personas de oficios cotidianos, solo 11 animaciones, **cara negra sin boca**. Útil para fondo; `piel` pinta la cara pero no agrega rasgos. |
| Quaternius House Interior / Buildings / Street / Farm | CC0 | Muebles y edificios a escala real (con 0,005). Casa medida; el resto solo descargado. |
| Quaternius Animated Human | CC0 | Descartado: maniquí blanco sin cara. |

**Qué se añadió a `escenas-web3d`:** acciones de personaje con caminata calculada sobre los pies (sin patinar), giros, mirar a otro personaje, mezcla entre animaciones; `cuarto` con paredes, ventanas y puertas; `tomas` con planos de cine que se adaptan al tamaño de cada personaje; carga de FBX; `descargar_paquetes.py` y `catalogo.py` (búsqueda en español).

**Lo que sigue pendiente (se dice sin adornos):** caras con emoción y boca animada (los modelos traen caras fijas; un camino a evaluar es VRM con expresiones, sin probar), sentarse/recoger con alineación exacta, y que una persona mire el movimiento: aquí solo se midió y se vieron cuadros.
