# Índice de skills (plan: `docs/PLAN-video.md`, 2026-11-04)

★ = skill original (MIT). Los grupos se instalan con `./instalar.sh GRUPO`; en la nube solo se instala solo `plan` (las demás pesan en descargas: se instalan al pedirlas).

## Fases 4, 5 y 6: crear (hechas)
| Skill | Cuándo usarla | Origen |
|---|---|---|
| ★ **plan-de-video** | Al empezar cualquier video: ficha, camino elegido, guion medido, recursos, costo y aprobaciones. | Original |
| ★ **animacion-2d** | Cuentos y cortos 2D con personajes sencillos, en horizontal y vertical, descritos en un JSON. | Original (método del kit de cortometraje de Jeiler, motor nuevo y general) |
| ★ **video-explicativo** | Explicar o comparar con gráficos, listas, pasos y números; voz sintética, subtítulos y música; horizontal y vertical. | Original |
| ★ **voz-sintetica** | Narración en español sin internet ni costo, con el tiempo de cada frase. | Original (usa Kokoro, Apache-2.0) |
| ★ **musica-y-efectos** | Música de fondo y efectos originales hechos con código, sin derechos de terceros. | Original |
| ★ **video-3d** | Personajes 3D con cara y pelo creíbles usando modelos ya hechos (CC0) y Blender sin pantalla; primero imágenes fijas para aprobar. Explica también el camino de IA de video (sin probar). | Original (usa `bpy`, GPL-3, solo en tu computador; y personajes Kenney, CC0) |
| ★ **personajes-consistentes** | Hoja de personaje, paleta, ficha y alarma de colores para que el personaje no cambie entre escenas. | Original |
| ★ **historia-3d** | Una historia en video 3D con orden y compuertas: primero la historia y su mundo, luego los personajes a medida y aprobados, escenario con piezas 3D, tomas y revisión de que el cuento coincida con la imagen. **Probada con un cuento de 32 s.** | Original (usa Kenney y Quaternius, CC0) |
| ★ **recursos-3d** | Catálogo de recursos 3D gratis y CC0 (personajes, animaciones, muebles, naturaleza, cielos), con lo probado y lo descartado. | Original |
| ★ **escenas-web3d** | Escenas 3D ligeras en navegador (formas, **modelos GLB con animación**, imágenes, luz de estudio, cámara, curvas, fundidos, títulos y cortes con Three.js + GSAP), horizontal y vertical. **Probada con escenas de 8 s y 6 s (personajes KayKit).** | Original (usa Three.js, MIT, y GSAP, licencia gratuita; ambos solo en la caché local) |
| ★ **clips-ia** | Pedir clips de IA (Kling, Seedance, Veo) con costo y «sí» antes, prueba de 5 s y el mismo personaje. **Sin probar.** | Original |
| ★ **estudiar-video-referencia** | Sacar la receta de estilo (tiempos, ritmo, colores, sonido) de un video que te gustó, sin copiar su contenido. | Original (idea de `reelmimic`, MIT; código propio) |
| ★ **video-infantil** | Reglas extra y revisión medible (destellos, ritmo, volumen, velocidad de narración) para videos de niños; cuento de ejemplo. | Original |

| Grupo | Skills |
|---|---|
| plan | plan-de-video |
| animacion-2d | animacion-2d |
| voz | voz-sintetica |
| musica | musica-y-efectos |
| explicativo | plan-de-video, animacion-2d, voz-sintetica, musica-y-efectos, video-explicativo |
| personajes | personajes-consistentes |
| 3d | plan-de-video, personajes-consistentes, video-3d |
| infantil | plan-de-video, animacion-2d, voz-sintetica, musica-y-efectos, video-explicativo, video-infantil |
| clips-ia | plan-de-video, personajes-consistentes, clips-ia |
| recursos3d | recursos-3d |
| web3d | plan-de-video, escenas-web3d, voz-sintetica, musica-y-efectos |
| historia3d | plan-de-video, personajes-consistentes, video-3d, recursos-3d, historia-3d, voz-sintetica, musica-y-efectos |
| referencia | plan-de-video, estudiar-video-referencia |

## Pendientes
Falta lo que solo una persona puede juzgar (oír las voces y mirar el movimiento del cuento de prueba) y lo marcado como pendiente en `docs/ESTADO-historia-3d.md`. Después, probar con material real: el camino de IA de video (con el «sí» de Jeiler), un video nuevo siguiendo una receta, y que alguien escuche y mire los resultados.

Pendientes menores de la fase 4: estilos de papel o acuarela para `animacion-2d` (el kit de Jeiler los tenía como filtros) y más personajes (cuerpo entero, animales).
