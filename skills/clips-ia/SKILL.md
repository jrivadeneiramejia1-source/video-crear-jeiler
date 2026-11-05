---
name: clips-ia
description: >-
  Guía para pedir clips de video generados con IA (Kling, Seedance, Veo u otros, por Higgsfield o Canva) a partir de una imagen aprobada, sin gastar créditos por sorpresa: estima el costo primero, pide el «sí» de Jeiler, prueba con un clip corto de unos 5 s, mantiene al mismo personaje con la misma imagen de referencia y marca el video como hecho con IA. Usar cuando el usuario diga "un clip con IA", "que se vea realista", "genera un video con Higgsfield", "con Kling" o "con Veo", o cuando lo que se quiere no se pueda dibujar ni modelar en 3D. SIN PROBAR: ninguna generación se pudo hacer todavía.
---

# Clips con IA

Un clip de IA se pide con texto y una imagen, y la herramienta lo genera. Se ve más «de película» que el 2D o el 3D de este repo, pero **cuesta créditos, el resultado varía entre intentos y los personajes cambian de cara o de ropa entre clips**. Por eso es el último camino, no el primero.

## Estado (2026-11-05): sin probar
- **Canva:** al intentar generar video respondió que no está disponible con el plan actual (pide un plan de pago). No se gastó nada.
- **Higgsfield:** en las sesiones hechas hasta hoy solo aparecieron herramientas de publicar juegos, no las de **generar**. Para activarlas, Jeiler abre claude.ai/customize/connectors, entra al conector de Higgsfield y permite sus herramientas.
- **Nada de lo de abajo se ha ejecutado.** Los precios y los límites gratis cambian y **no se pudieron verificar en las páginas oficiales**: se piden siempre a la herramienta antes de generar.

## Reglas
- **Créditos solo con el «sí» de Jeiler** en ese mismo mensaje y **con el número** (cuánto cuesta el clip) a la vista. Un «sigue con la fase 6» no autoriza gastar. Si se puede, se fija un tope (`max_credits`) igual a la cotización o menor.
- **Primero la prueba más barata:** un clip de unos 5 s y la menor calidad que sirva. Solo si sale bien se pide más.
- **Nada de personas reales:** no se suben fotos, caras ni voces de personas reales (ni de niños) y no se imitan. Los archivos de comunidades indígenas no se suben a ningún servicio. Lo que se sube a un servicio externo puede guardarse allí.
- **Personajes inventados** y siempre con **la misma imagen de referencia** aprobada (ver `personajes-consistentes`).
- **Declarar que es IA:** en los créditos y en la descripción («clip generado con IA»). Las reglas de YouTube y TikTok sobre contenido hecho con IA **hay que verificarlas en sus páginas oficiales antes de publicar**.
- Nada se publica solo.
- Claude no ve el movimiento: mira cuadros del clip y mide; Jeiler decide si se ve bien.

## Antes de gastar: ¿hace falta IA?
| Si lo que quieres es... | Mejor camino (gratis) |
|---|---|
| personajes y escenas sencillas, cuentos, explicaciones | `animacion-2d` o `video-explicativo` |
| personajes 3D que se mueven, la misma cara siempre | `video-3d` (Blender, camino B) |
| naturaleza, multitudes, cámara «de cine», cosas que no se dibujan | **clips de IA** (esta skill) |

## Proceso
1. **Imagen aprobada:** hoja de personaje o imagen fija que Jeiler vio y aceptó. Sin imagen aprobada, no se genera.
2. **Prompt** en una sola acción por clip, con: sujeto (de la ficha), acción, cámara (plano, movimiento), luz, estilo, duración y **lo que no debe pasar** (texto en pantalla, manos extra, cambios de ropa). Ejemplo: «La niña de la ficha camina hacia la cámara bajo la lluvia suave; plano medio, cámara fija; luz de tarde; estilo ilustración suave; 5 s; sin texto ni logos.»
3. **Cotizar:** pedir a la herramienta el precio del clip (sin generar). Decirle a Jeiler: herramienta, modelo, duración, calidad, **créditos** y cuántos le quedan. **Esperar su «sí».**
4. **Generar la prueba** de ~5 s y esperar con la herramienta de estado (no repetir el pedido mientras corre: duplicaría el gasto).
5. **Revisar:** extraer cuadros del inicio, medio y final (`ffmpeg-skill/scripts/look.py`) y buscar caras deformadas, manos de más, texto ilegible, cambios de ropa; comparar el personaje con la imagen de referencia (`personajes-consistentes/scripts/comparar_cuadros.py`).
6. **Decidir con Jeiler:** si sirve, se piden los demás clips con la misma imagen y el mismo estilo de prompt; si no, se ajusta el prompt o se vuelve a `video-3d` o 2D. **Cada reintento es otra cotización.**
7. **Montar** con `video-editar-jeiler` (cortar, voz, música, subtítulos) y revisar con `verificar-video`.

## Señales de alerta
- Generar «para ver cómo sale» sin cotizar ni preguntar.
- Pedir muchos clips largos de una vez.
- Cambiar la imagen de referencia o el estilo del prompt entre clips y esperar el mismo personaje.
- Subir material de personas reales, de niños o de comunidades indígenas.
- Publicar sin declarar que es IA.

## Verificación
- [ ] Jeiler dijo «sí» a un costo concreto antes de cada generación.
- [ ] Se empezó con un clip de ~5 s.
- [ ] El personaje coincide con la imagen aprobada en los cuadros revisados.
- [ ] El video final dice que usa IA y las reglas de la plataforma se verificaron.
- [ ] Se dijo qué no se pudo comprobar (movimiento, oído).

## Qué se probó (2026-11-05)
**Nada se generó.** Solo se verificó que Canva rechaza generar video con el plan actual y que las herramientas de generar de Higgsfield no estaban disponibles en la sesión. El proceso de arriba sigue las reglas de Jeiler (créditos solo con su «sí» y una estimación) y con lo que el conector de Higgsfield indica para algunas de sus herramientas (ver el precio antes, fijar un tope `max_credits`, esperar con `jobs_wait`); para generar video no se pudo comprobar. **Está sin ejecutar de punta a punta.** Falta: activar las herramientas de generar, que Jeiler diga «sí» a un costo concreto, probar un clip de 5 s y revisar si el personaje se mantiene.
