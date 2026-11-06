---
name: direccion-de-video
description: >-
  Guía del oficio para hacer mejores videos animados y más rápido: el orden de trabajo paso a paso (premisa, guion medido, voz primero, storyboard y animatic, bloqueo, pulido, sonido, revisión), reglas de cámara y montaje (planos, cortes, línea de acción), movimiento natural de personajes (caminar, brazos, giros, anticipación) y caras (parpadeo, boca, cejas), con una revisión automática de proyectos que aplica esas reglas. Usar al empezar cualquier video con personajes, antes de renderizar, o cuando Jeiler diga «se ve duro», «no se ve natural», «el personaje patina», «cómo lo hago mejor/más rápido». Para armar la escena en sí: escenas-web3d o animacion-2d.
---

# Dirección de video: el oficio, en orden

Las herramientas ya existen (`escenas-web3d`, `animacion-2d`, `voz-sintetica`, `recursos-3d`). Lo que cambia la calidad es **el orden en que se trabaja y las reglas de cine y animación** que se aplican. Esta skill junta ese conocimiento (fuentes en `references/fuentes.md`) y lo vuelve revisable con un script.

## Cuándo usarla
- Al empezar un video con personajes (plan antes de tocar nada).
- Antes de un render largo: `revisar_proyecto.py` cuesta segundos y evita rehacer minutos.
- Cuando algo «se ve raro»: ir a la tabla de síntomas de `references/movimiento-natural.md`.

## Proceso (cada paso termina en una compuerta: sin ella no se pasa al siguiente)
1. **Premisa de una frase** (quién, qué quiere, qué lo impide, cómo termina), público y duración. *Compuerta: Jeiler la aprueba.*
2. **Guion con tiempo medido** (`plan-de-video`): palabras por segundo reales, no a ojo. Recortar antes de dibujar: un segundo sobrante cuesta lo mismo que uno bueno.
3. **Voz primero** (`voz-sintetica`): el audio manda; la animación se ajusta a él, no al revés. *Compuerta: duración total y tiempo de cada frase.*
4. **Storyboard y animatic**: una imagen por toma (`stills`/`hoja`) puesta sobre la voz. Es la prueba más barata del ritmo. *Compuerta: Jeiler mira la hoja.*
5. **Recursos** (`catalogo.py`, `recursos-3d`): personajes, cuarto y muebles ya hechos; no dibujar de cero lo que existe. Misma familia de estilo y escala (KayKit con KayKit).
6. **Bloqueo** (poses y lugares, sin pulir): `acciones`, `tomas` y `cuarto` con valores simples. Revisar con `verificar` y `revisar_proyecto.py`.
7. **Movimiento**: caminata, giros, miradas, gestos; ajustar con las reglas de `movimiento-natural.md`. Mirar `stills` en los momentos clave (inicio, mitad, final de cada acción).
8. **Pulido**: curvas, fundidos, títulos, parpadeo y boca. Solo después de aprobar el bloqueo.
9. **Sonido y música** (`musica-y-efectos`, `ffmpeg-skill`): volumen y silencios; pasos y golpes sincronizados con los cortes.
10. **Revisión final** (`verificar-video`) y **render completo una sola vez**.

**Por qué este orden (y cómo ir más rápido):** en la nube un video de 17 s a 24 fps tardó ≈ 2 min 46 s por formato (≈10 veces la duración), mientras que un cuadro suelto tarda un par de segundos. Se itera con cuadros sueltos y hojas; el video completo se renderiza al final, una vez. Cambiar el guion después de animar es lo más caro; cambiar una curva es lo más barato.

## Reglas que más pesan (detalle y fuentes en `references/`)
- **Cámara:** empezar con un plano que ubique (general), entrar a medio y primer plano; no repetir el mismo plano dos veces seguidas; cortar cuando empieza o termina una acción; no cruzar la línea de acción en una conversación. (`camara-y-montaje.md`)
- **Caminar:** los pies no deslizan (el paso se calcula por metros recorridos), se arranca y se frena con aceleración, los brazos van contrarios a las piernas, se gira mirando primero. (`movimiento-natural.md`)
- **Nada congelado:** un personaje quieto más de ~6 s sin respirar, mirar o gesticular se siente muerto.
- **Caras:** parpadeo cada 3–6 s, cejas para la emoción, boca por sílabas, ojos antes que la cabeza. (`caras-y-expresion.md`)
- **Subtítulos:** ≤ 17 caracteres por segundo y ≤ 42 por línea; cada uno visible ≥ 1 s.

## Revisar un proyecto (segundos, sin renderizar)
```bash
python3 scripts/revisar_proyecto.py ../escenas-web3d/ejemplo/historia-casa.json
python3 scripts/revisar_proyecto.py ../animacion-2d/ejemplo/proyecto.json --json
```
Funciona con proyectos de `escenas-web3d` y de `animacion-2d`. Cada hallazgo trae nivel (ERROR / AVISO / IDEA), la regla, el lugar y el porqué. Salida 1 si hay ERROR. No reemplaza mirar los cuadros: avisa de lo medible.

## Señales de alerta
- Animar antes de tener la voz y el storyboard aprobados.
- Pulir (curvas, brillos) un bloqueo que Jeiler no vio.
- Renderizar el video completo para «ver cómo queda» (usar `stills`).
- Dibujar a mano un personaje, un mueble o una caminata que ya existe en los paquetes.
- Confiar en un número de esta guía marcado «regla práctica»: son puntos de partida, se ajustan mirando.

## Verificación
- [ ] La premisa, el guion y la voz tienen compuerta aprobada.
- [ ] `revisar_proyecto.py` sin ERROR y con los AVISO entendidos (corregidos o decididos).
- [ ] Se miraron cuadros del inicio, mitad y final de cada acción y de cada toma, en horizontal y vertical.
- [ ] Se dijo qué no se pudo ver (el movimiento a simple vista lo juzga Jeiler).
