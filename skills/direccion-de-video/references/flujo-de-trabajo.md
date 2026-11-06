# Flujo de trabajo: más rápido y mejor

## Idea central
Trabajar **de lo barato a lo caro** y de **lo general a lo particular**. El cine y la animación llaman a esto preproducción (guion, storyboard, planificación de lugares y recursos) antes de producir; Wikipedia, «Pre-production»: la preproducción termina cuando termina la planificación y empieza el contenido. Aquí se aplica con los límites de una sola persona y una sola máquina.

## Costos medidos en este repositorio (nube, 2026-11-06)
| Acción | Tiempo | Cuándo |
|---|---|---|
| `verificar` (escenas-web3d) | 3–8 s | siempre, tras cada cambio |
| `stills` de 1 a 6 momentos | 5–20 s | para mirar actitud, encuadre, cortes |
| `hoja` de 8 cuadros | 10–25 s | para ver el ritmo de toda la escena |
| Video de 17 s a 24 fps | 2 min 31 s a 2 min 46 s por formato | una sola vez, al final |
| Video de 6 s a 30 fps con 2 personajes | 40–59 s | pruebas de movimiento aisladas |
Regla: **ningún render completo antes de que `hoja` y `revisar_proyecto.py` estén limpios.**

## Cada paso: qué entrega y quién lo aprueba
| Paso | Entrega | Aprueba |
|---|---|---|
| Premisa | una frase + público + duración | Jeiler |
| Guion medido | texto con segundos por frase | Jeiler |
| Voz | audio y tiempo de cada frase | Jeiler (escucha) |
| Storyboard/animatic | hoja de cuadros sobre la voz | Jeiler (mira) |
| Bloqueo | proyecto con acciones y tomas simples | `revisar_proyecto.py` + hoja |
| Movimiento | cuadros de inicio, mitad y final de cada acción | medición + Jeiler |
| Pulido | curvas, fundidos, títulos, parpadeo, boca | Jeiler |
| Sonido | mezcla y música | medición (LUFS) + Jeiler |
| Entrega | video final verificado | `verificar-video` + Jeiler |

## Cómo no perder tiempo
- **Reutilizar:** personajes y muebles de `catalogo.py`; escenas completas copiadas de `ejemplo/`.
- **Un cambio por vez** y mirar; si algo se rompe, se sabe cuál fue.
- **Medir antes de creer:** la caminata se mide con los pies (el motor lo hace); las alturas con una vara de referencia; los tiempos con el reloj del render.
- **Dos formatos:** mirar `stills` en horizontal y vertical desde el bloqueo, no al final.
- **Registrar lo aprendido** en `LECCIONES.md` apenas ocurre.

## Qué decide Jeiler y qué no
Jeiler aprueba la historia, la voz y lo que se publica. La técnica (planos, curvas, tiempos) se decide con estas reglas y se explica en pocas frases.
