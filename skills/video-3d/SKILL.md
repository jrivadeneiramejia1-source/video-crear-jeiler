---
name: video-3d
description: Hace videos con personajes 3D que se ven bien (cara, pelo y manos completos) usando personajes profesionales ya hechos, con esqueleto y animaciones, de licencia libre, y Blender sin pantalla ni tarjeta gráfica (Cycles en CPU). Primero produce imágenes fijas de frente, medio cuerpo y rostro para aprobarlas y solo después anima. También explica el otro camino (clips con IA de video, con créditos). Usar cuando el usuario diga "un video en 3D", "un personaje 3D que se mueva", "animación 3D", "que no se vea raro como la vez pasada" o "personajes tipo videojuego". Nunca arma caras ni pelo desde figuras básicas en código.
---

# Video 3D

**Por qué falló el 3D anterior:** se armaron cabezas y pelo desde cero con figuras básicas en código. Eso no da caras creíbles, ni con esta ni con ninguna herramienta. Aquí se hace al revés: **personajes ya hechos por artistas** (con esqueleto y animaciones, licencia CC0) y la skill solo los pone en escena, los ilumina y los renderiza.

## Los dos caminos
| | A. Clips con IA de video | B. Blender con personajes ya hechos (esta skill) |
|---|---|---|
| Cómo se ve | Más realista o «de película»; caras y pelo variables entre tomas | Estilizado, «de videojuego»; el mismo personaje exacto en todas las escenas |
| Costo | **Créditos** (un clip de 5 s) | Gratis; tiempo de CPU (~6 s por cuadro a 960x540) |
| Control | Poco (se pide con texto) | Total (cámara, luz, animación) |
| Estado en este repo | **Sin probar** (ver abajo) | **Probado** |

**Camino A, hoy:** la generación con IA no se pudo probar. El conector de Canva dijo que generar video «no está disponible con tu plan actual» (pide un plan de pago) y en esta sesión no aparecieron las herramientas de **generar** de Higgsfield (solo las de publicar juegos): para usarlas hay que abrir claude.ai/customize/connectors, entrar al conector y poner esas herramientas como permitidas. **No se gastó ningún crédito.** La skill `clips-ia` (fase siguiente) lo desarrolla.

## Reglas
- **Primero imágenes fijas, después animación.** Frente, medio cuerpo y rostro (y perfil y espalda con `personajes-consistentes`) se enseñan a Jeiler; solo con su «sí» se anima.
- **Personajes de licencia libre y con crédito:** Kenney (CC0) viene por `scripts/descargar_personajes.sh`. Mixamo (Adobe) pide cuenta; los de Quaternius (CC0) están en Google Drive y no se pudieron bajar desde esta sesión. Nunca copiar un personaje al repo (es público): viven en `~/.cache/video-jeiler/personajes/`.
- **No para niños sin revisar:** muchos personajes de estos paquetes son soldados o zombis con ropa sucia; escoger skins amables (ver `video-infantil`).
- Nada de caras de personas reales ni imitar a alguien; los personajes son inventados.
- Nada que gaste créditos sin el «sí» de Jeiler y una estimación del costo.
- Claude no ve el movimiento: mira cuadros y mide; la fluidez la juzga Jeiler.

## Instalar (una vez)
```bash
bash scripts/instalar_blender.sh          # Blender como módulo de Python (bpy), ~400 MB desde pypi.org
bash scripts/descargar_personajes.sh      # personajes CC0 de Kenney (OpenGameArt) a ~/.cache/video-jeiler/personajes
PYBL=~/.cache/video-jeiler/venv-blender/bin/python
P=~/.cache/video-jeiler/personajes/animated-characters-1
```
(`bpy` 5.x tiene versiones para Python 3.11 y 3.13. EEVEE necesita tarjeta gráfica y aquí se cae: se usa Cycles en CPU.)

## Proceso
1. **Elegir el personaje y su piel** y escribir su ficha (`personajes-consistentes`).
2. **Fijas para aprobar:**
   ```bash
   $PYBL scripts/escena_blender.py --personaje $P/Model/characterMedium.fbx --piel $P/Skins/survivorMaleB.png \
       --animacion $P/Animations/idle.fbx --vistas cuerpo,medio,rostro --salida fijas --ancho 960 --alto 540
   ```
   Abrir `fijas/vista_*.png` a tamaño completo y revisar con la lista de abajo. Si el personaje mira hacia otro lado, `--giro 180`.
3. **Esperar el «sí»** de Jeiler con las fijas.
4. **Animar:** `... --animacion idle.fbx --animacion jump.fbx --animar --encuadre medio --segundos 5 --salida clip` (las animaciones se encadenan y se repiten hasta llenar los segundos). Calidad: `--muestras 24` (borrador) a `64`; `--ancho 1280 --alto 720` tarda más. **Estimación:** unos 6 s por cuadro a 960x540 y 24 muestras con 4 núcleos (5 s a 24 fps ≈ 11 minutos). Para ahorrar tiempo, renderizar a 12 fps y duplicar los cuadros.
5. **Voz y música:** pegarlas con `ffmpeg-skill` (de `video-editar-jeiler`) o `video-explicativo`/`voz-sintetica`/`musica-y-efectos`.
6. **Verificar:** `ffmpeg-skill/scripts/check.py clip/escena.mp4 --platform youtube --content`, mirar una hoja de cuadros y repetir la comparación de colores (`comparar_cuadros.py`).

## Lista de revisión de las fijas (a ojo)
- Ojos, boca y cejas simétricos y en su lugar; sin dientes ni lengua raros.
- **Pelo completo** desde todos los ángulos (frente, perfil, espalda): sin huecos ni piezas sueltas.
- Manos con cinco dedos o forma de manopla limpia; nada atravesando el cuerpo.
- Ropa y colores iguales en todas las vistas; sin texturas estiradas.
- Se entiende de qué tamaño es el personaje respecto del suelo y del fondo.

## Señales de alerta
- Animar sin haber aprobado las fijas.
- Pelo o cara hechos «a mano» en código.
- Prometer realismo con un personaje de bajo polígono (es un estilo, no una versión barata de lo realista).
- Renderizar a tamaño completo sin haber medido el tiempo de un cuadro.

## Verificación
- [ ] Las fijas (frente, medio, rostro) fueron aprobadas por Jeiler.
- [ ] El personaje tiene licencia CC0 anotada y créditos en el video.
- [ ] `check.py` sin FAIL; hoja de cuadros mirada.
- [ ] Se dijo qué no se pudo comprobar (movimiento, oído, camino A).

## Qué se probó (2026-11-05)
**Camino B, de punta a punta con un personaje de Kenney (Animated Characters 1, CC0):** instalación real de `bpy` 5.2.3 (Python 3.13); tres fijas (cuerpo, medio, rostro) en 5,6 a 7,1 s cada una; clip de 5 s con animaciones encadenadas (120 cuadros a 960x540 y 24 muestras, 684 s en total, 5,7 s por cuadro); `check.py` dio 14 comprobaciones sin FAIL (avisos: 960x540, sin audio y etiqueta de color). En la hoja de cuadros la cara, el pelo y las manos se mantienen iguales en todos los instantes (no hay deformaciones), y la comparación de colores entre instantes dio 0,09 (mismo personaje) contra 0,35 con otra piel. **Errores reales encontrados y corregidos:** el encuadre salió tan cerca que solo se veían las piernas (ahora se calcula con la altura real del personaje), el suelo salía quemado de luz y EEVEE se cae sin tarjeta gráfica (se usa Cycles). **No se probó:** el camino A (ver arriba), 1280x720 ni 1080p, personajes con expresiones o labios sincronizados, varios personajes o accesorios, cámara en movimiento, los personajes de Quaternius ni Mixamo, ni otro computador.
