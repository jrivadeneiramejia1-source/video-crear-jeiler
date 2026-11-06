# Fuentes de las skills copiadas

Cada fila dice de dónde viene una skill, qué versión se copió y con qué licencia. Sirve para saber si hay una versión nueva en el origen (se compara el commit).

| Skills | Origen | Commit copiado | Fecha | Licencia |
|---|---|---|---|---|

**Sin skills de terceros copiadas (fases 4 y 5).** Lo que usan las skills al correr (no está en el repo): `kokoro-onnx` (MIT) y los archivos del modelo Kokoro 82M de `thewh1teagle/kokoro-onnx` (Apache-2.0 el modelo), `playwright` (Apache-2.0) con Chromium, `numpy` y `soundfile`. `video-3d` usa `bpy` (Blender como módulo de Python; GPL-3, se instala en el computador de quien lo use y no se copia al repo; lo que se renderiza no queda bajo GPL) y baja personajes ya hechos de **Kenney** (kenney.nl, «Animated Characters 1 y 2» y «Blocky Characters 2.0», **CC0**, vía opengameart.org) a `~/.cache/video-jeiler/personajes/`; el instalador comprueba que su `License.txt` diga CC0 y nunca los copia al repo (el repo es público). Se probó el paquete «Animated Characters 1 (1.1)». Los personajes de Quaternius (CC0) están en Google Drive y no se pudieron bajar desde la nube; Mixamo (Adobe) pide cuenta: ninguno se usa. `escena3d.py` usa también el **Furniture Kit** y el **Nature Kit** de Kenney (CC0, vía opengameart.org), la **Universal Animation Library 1 y 2** (versión Standard) de Quaternius (CC0, vía opengameart.org: `universal_animation_librarystandard.zip` y `universal_animation_library_2standard.zip`) y cielos HDRI de **Poly Haven** (CC0, api.polyhaven.com), todo bajado a una carpeta local y nunca copiado al repo; se probaron el 2026-11-05. `escenas-web3d` baja a `~/.cache/video-jeiler/web` **Three.js 0.187.0** (MIT, `npm pack`) y **GSAP 3.15.1** (licencia gratuita «Standard no charge», https://gsap.com/standard-license; no es de código abierto, por eso nunca se copia al repo), y usa `playwright` (Apache-2.0); se probó el 2026-11-06. `estudiar-video-referencia` se inspira en la idea de `edenfunf/reelmimic` (MIT) pero su código es propio. `animacion-2d` sigue el método del kit de cortometraje de Jeiler, pero su código es nuevo.

## Revisar si hay versiones nuevas (cada mes)
```bash
python3 -I comparar-fuentes.py
```
Es de solo lectura: compara cada commit de esta tabla con el más nuevo del repo de origen y dice «igual» o «HAY CAMBIOS» (o no pudo consultar). Salida 0 = todo igual, 1 = hay cambios, 2 = no se pudo consultar alguno. Que haya cambios no obliga a actualizar: primero mirar qué cambió, volver a revisar su seguridad (`SEGURIDAD.md`) y actualizar la fila de esta tabla.
