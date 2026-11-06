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
