# Revisión de seguridad

Base creada el 2026-11-04. Todavía no hay skills de terceros en este repo.

## Cómo se revisa cada cosa antes de agregarla
1. **Licencia** primero (ver `third-party/LEEME.md`): MIT, Apache-2.0, BSD, CC0 o Unlicense se pueden copiar; GPL o AGPL, solo ideas; sin licencia, solo enlazar.
2. **Leer el `SKILL.md` completo y sus scripts.** Buscar comandos de riesgo: descargar y ejecutar a la vez (`curl ... | sh`), `eval`, `rm -rf /`, `base64 -d`, `nc -e`, `sudo`.
3. **gitleaks** (busca claves y tokens escritos en archivos) sobre los archivos y el historial.
4. Instalar dependencias con `--ignore-scripts` y sin ejecutar binarios descargados.
5. **No se usa `snyk/agent-scan`:** pide cuenta y token de Snyk y sube el contenido de las skills a su servicio. Queda a decisión de Jeiler.

## Privacidad (el repo es público)
- No se suben nombres de estudiantes, voces, caras, audios ni capturas de videos reales. Los ejemplos usan personajes y textos inventados.
- `.gitignore` bloquea audios, videos y las carpetas `entregas/` y `privado/` como red de seguridad, pero no reemplaza la revisión a mano antes de cada commit.
- Archivos de comunidades indígenas: no se modifican ni se suben a servicios externos.

## Resultado (fase 4)
- **Sin código de terceros copiado.** Los scripts propios solo llaman a ffmpeg, a Chromium sin pantalla y a modelos locales.
- **Internet:** solo `instalar_voz.sh` (github.com: modelos de Kokoro; pypi.org: paquetes) e `instalar_render.sh` (pypi.org; y el sitio de Playwright si no hay ningún Chromium). El resto corre sin conexión. Los instaladores usan un Python propio (`~/.cache/video-jeiler/venv`) y no tocan el del sistema. No verifican una huella de los modelos descargados: pendiente.
- **Privacidad:** el motor y los ejemplos usan personajes y textos inventados; el kit original de Jeiler (con nombres e historias reales) se quedó fuera del repo. `crear_explicativo.py` incrusta imágenes del guion dentro de un archivo temporal para dibujarlas; no sube nada.
- **Búsqueda de patrones de riesgo** (`curl | sh`, `eval`, `exec`, `os.system`, `shell=True`, `sudo`): ninguno. **gitleaks:** 0 hallazgos.

## Resultado (fase 5: 3D, personajes consistentes, infantil)
- **Sin código de terceros copiado.** `escena_blender.py` y `hoja_personaje.py` solo corren dentro de `bpy` en el computador local; `comparar_cuadros.py` y `revisar_infantil.py` solo llaman a ffmpeg y numpy.
- **Internet:** `instalar_blender.sh` (pypi.org, ~400 MB: el paquete `bpy`) y `descargar_personajes.sh` (opengameart.org: zips de Kenney; **verifica que `License.txt` diga CC0** y, si no, no instala). No verifican una huella de los archivos descargados: pendiente. Los instaladores usan un Python propio (`~/.cache/video-jeiler/venv-blender`) y no tocan el del sistema.
- **Privacidad:** los personajes 3D son modelos públicos de licencia libre y viven fuera del repo; los ejemplos infantiles son inventados (nada de niños, nombres ni voces reales). `.gitignore` bloquea además `__pycache__`.
- **Videos para niños:** la skill dice que una persona adulta debe verlos y escucharlos completos; nada se publica solo, y la skill no declara que un video «cumpla» una ley (COPPA u otra).
- **Camino de IA de video (sin probar):** cualquier clip con IA gasta créditos y sube imágenes de referencia a un servicio externo: solo con el «sí» de Jeiler y una estimación del costo, y nunca con archivos de comunidades indígenas ni con personas reales.
- **Búsqueda de patrones de riesgo** (`curl | sh`, `eval`, `os.system`, `shell=True`, `sudo`) y **gitleaks**: ver el commit de esta fase.

## Resultado (fase 6: IA de video y videos de referencia)
- **Sin código de terceros copiado.** `receta.py` solo llama a ffmpeg y usa numpy; no sube nada a internet. La idea viene de `reelmimic` (MIT) pero no se copió su código.
- **Material ajeno:** los videos de referencia son de otros creadores. No entran al repo (`.gitignore` bloquea `referencias/` y `receta_*/`, que incluyen cuadros de esos videos) ni se suben a servicios externos, y no se usan como material del video nuevo. La skill separa «se copia» (estilo) de «no se copia» (texto, letra, música, código, marcas de agua, nombres de usuario).
- **Clips de IA:** gastan créditos y suben imágenes a un servicio externo. La skill exige el «sí» de Jeiler con un costo concreto antes de cada generación, y prohíbe subir personas reales, niños o archivos de comunidades indígenas. No se generó nada.
- **Búsqueda de patrones de riesgo** y **gitleaks**: ver el commit de esta fase.

## Resultado (herramientas de historias 3D, 2026-11-05)
- **Sin código de terceros copiado.** `escena3d.py`, `personalizar_piel.py`, `descargar_recursos.sh` y `descargar_cielo.py` son propios.
- **Internet:** `descargar_recursos.sh` (opengameart.org: zips de Kenney y Quaternius; comprueba que su licencia diga CC0) y `descargar_cielo.py` (api.polyhaven.com y dl.polyhaven.org, solo librería estándar de Python). `escena3d.py` y `personalizar_piel.py` no usan internet. No se verifica una huella de lo descargado: pendiente.
- **Solo modelos, texturas y animaciones** (sin binarios ejecutables de terceros). Las pieles se redibujan desde SVG con Chromium sin pantalla.
- **Archivos descargados:** se tratan como datos; Blender importa FBX, OBJ y glTF (formatos que pueden traer mallas muy pesadas: se probó con paquetes de Kenney y Quaternius, de tamaño normal).
- **Se instalaron bibliotecas del sistema** (Mesa/EGL) en la nube solo para probar EEVEE; se descartó y no hacen falta.

