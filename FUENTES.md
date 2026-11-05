# Fuentes de las skills copiadas

Cada fila dice de dónde viene una skill, qué versión se copió y con qué licencia. Sirve para saber si hay una versión nueva en el origen (se compara el commit).

| Skills | Origen | Commit copiado | Fecha | Licencia |
|---|---|---|---|---|

**Sin skills de terceros copiadas (fases 4 y 5).** Lo que usan las skills al correr (no está en el repo): `kokoro-onnx` (MIT) y los archivos del modelo Kokoro 82M de `thewh1teagle/kokoro-onnx` (Apache-2.0 el modelo), `playwright` (Apache-2.0) con Chromium, `numpy` y `soundfile`. `video-3d` usa `bpy` (Blender como módulo de Python; GPL-3, se instala en el computador de quien lo use y no se copia al repo; lo que se renderiza no queda bajo GPL) y baja personajes ya hechos de **Kenney** (kenney.nl, «Animated Characters 1 y 2» y «Blocky Characters 2.0», **CC0**, vía opengameart.org) a `~/.cache/video-jeiler/personajes/`; el instalador comprueba que su `License.txt` diga CC0 y nunca los copia al repo (el repo es público). Se probó el paquete «Animated Characters 1 (1.1)». Los personajes de Quaternius (CC0) están en Google Drive y no se pudieron bajar desde la nube; Mixamo (Adobe) pide cuenta: ninguno se usa. `estudiar-video-referencia` se inspira en la idea de `edenfunf/reelmimic` (MIT) pero su código es propio. `animacion-2d` sigue el método del kit de cortometraje de Jeiler, pero su código es nuevo.

## Revisar si hay versiones nuevas (cada mes)
```bash
python3 -I comparar-fuentes.py
```
Es de solo lectura: compara cada commit de esta tabla con el más nuevo del repo de origen y dice «igual» o «HAY CAMBIOS» (o no pudo consultar). Salida 0 = todo igual, 1 = hay cambios, 2 = no se pudo consultar alguno. Que haya cambios no obliga a actualizar: primero mirar qué cambió, volver a revisar su seguridad (`SEGURIDAD.md`) y actualizar la fila de esta tabla.
