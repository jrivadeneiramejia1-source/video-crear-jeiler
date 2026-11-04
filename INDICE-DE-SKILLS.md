# Índice de skills (plan: `docs/PLAN-video.md`, 2026-11-04)

★ = skill original (MIT). Los grupos se instalan con `./instalar.sh GRUPO`; en la nube solo se instala solo `plan` (las demás pesan en descargas: se instalan al pedirlas).

## Fase 4: crear, lo básico (hecha)
| Skill | Cuándo usarla | Origen |
|---|---|---|
| ★ **plan-de-video** | Al empezar cualquier video: ficha, camino elegido, guion medido, recursos, costo y aprobaciones. | Original |
| ★ **animacion-2d** | Cuentos y cortos 2D con personajes sencillos, en horizontal y vertical, descritos en un JSON. | Original (método del kit de cortometraje de Jeiler, motor nuevo y general) |
| ★ **video-explicativo** | Explicar o comparar con gráficos, listas, pasos y números; voz sintética, subtítulos y música; horizontal y vertical. | Original |
| ★ **voz-sintetica** | Narración en español sin internet ni costo, con el tiempo de cada frase. | Original (usa Kokoro, Apache-2.0) |
| ★ **musica-y-efectos** | Música de fondo y efectos originales hechos con código, sin derechos de terceros. | Original |

| Grupo | Skills |
|---|---|
| plan | plan-de-video |
| animacion-2d | animacion-2d |
| voz | voz-sintetica |
| musica | musica-y-efectos |
| explicativo | plan-de-video, animacion-2d, voz-sintetica, musica-y-efectos, video-explicativo |

## Pendientes (fases siguientes)
| Grupo | Skills | Fase | Estado |
|---|---|---|---|
| personajes | ★ personajes-consistentes, skills oficiales de FLUX (MIT) | 5 | pendiente |
| 3d | ★ video-3d (dos caminos: IA de video y Blender) | 5 | pendiente |
| infantil | ★ video-infantil | 5 | pendiente |
| clips-ia | ★ clips-ia | 6 | pendiente |
| referencia | ★ estudiar-video-referencia | 6 | pendiente |

Pendientes menores de la fase 4: estilos de papel o acuarela para `animacion-2d` (el kit de Jeiler los tenía como filtros) y más personajes (cuerpo entero, animales).
