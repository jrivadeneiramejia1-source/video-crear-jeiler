---
name: plan-de-video
description: Convierte una idea de video en un plan de producción: pregunta lo que falta (público, tipo, duración, formatos, voz, música, plataforma, presupuesto), elige el camino más adecuado entre explicativo, cuento animado 2D, video con una persona real, 3D o clips de IA, mide el guion y deja una ficha con escenas, recursos, licencias, costo y aprobaciones. Usar al empezar CUALQUIER video, cuando el usuario diga "quiero hacer un video de...", "ayúdame con el guion de un video", "qué necesito para hacer este video" o antes de gastar créditos. Propone alternativas que el usuario quizá no conoce.
---

# Plan de video

Antes de dibujar, grabar o gastar créditos: una ficha corta, el camino elegido y el guion medido. Evita rehacer un video entero porque faltaba una pregunta.

## Reglas
- **Hacer las preguntas que faltan en un solo mensaje, con opciones con letras**, y proponer una respuesta recomendada para cada una (Jeiler no tiene por qué saber todas las opciones). Lo que no se responda, se asume con el valor recomendado y se dice.
- Nada que gaste créditos (Higgsfield, Canva, ElevenLabs) sin el «sí» de Jeiler **y** una estimación del costo en el plan.
- Personas reales (voz, cara, nombre): solo con su permiso; nombres escritos como los confirmó Jeiler.
- Archivos de comunidades indígenas: nunca se modifican ni se suben a servicios externos.
- Decir siempre qué no se podrá comprobar (oído humano, teléfono real, reglas de la plataforma).

## Proceso
1. **Entender la idea** en dos líneas y llenar `plantilla/plan.md` (sección 1) con las respuestas; completar lo que falte con lo recomendado.
2. **Elegir el camino** (tabla de abajo) y nombrar al menos **una alternativa** que se descartó y por qué.
3. **Escribir el guion** frase por frase (una idea por frase, 6 a 14 palabras) y medirlo:
   `python3 scripts/medir_guion.py guion.txt --voz sintetica --duracion 60` (o `--voz persona`). Corregir hasta que no haya avisos y la duración esté dentro del 15 %.
4. **Armar la tabla de escenas** (sección 3): qué dice, qué se ve y cuántos segundos.
5. **Listar recursos y licencias** (sección 4) y el **costo** (sección 5). Si usa créditos: precio por clip, cuántos clips y total, con la fecha de verificación del precio.
6. **Producir una muestra corta** (15 a 30 s) y pedir la aprobación antes de la versión completa.
7. Enseñar el plan a Jeiler y esperar el «sí»; guardar `plan.md` junto al proyecto.

## Caminos (qué skill usar)
| Quiere... | Camino | Costo | Estado |
|---|---|---|---|
| Explicar o comparar algo con gráficos, pasos y números (60 s) | `video-explicativo` | Gratis, en la nube | Probado |
| Un cuento corto con personajes sencillos | `animacion-2d` (+ `voz-sintetica` o voz de una persona) | Gratis | Probado |
| Un video grabado con teléfono o cámara (con una persona real) | `video-editar-jeiler`: `audio-limpio`, `subtitulos`, `editar-por-texto`, `graficos-por-palabra` | Gratis | Probado con videos inventados |
| Música o efectos | `musica-y-efectos` | Gratis | Probado (medidas; sin oyentes) |
| 3D con caras y pelo creíbles, o clips realistas | `video-3d`, `clips-ia` (fases siguientes) | Créditos (IA) o horas de CPU (Blender) | **Aún no existen** |
| Video para niños | `video-infantil` (fase siguiente) | Gratis | **Aún no existe** |
| Repetir el estilo de un video que le gusta | `estudiar-video-referencia` (fase siguiente) | Gratis | **Aún no existe** |

Mientras una skill «aún no exista», decirlo y proponer lo más cercano que sí funciona (por ejemplo, un explicativo 2D en lugar de 3D).

## Ideas que Jeiler quizá no conoce (proponerlas cuando encajen)
- Un **explicativo con voz sintética** como primera versión y reemplazar la voz cuando haya una persona.
- **Versión vertical y horizontal** del mismo video desde el mismo guion (cuesta unos 2 minutos de dibujo por formato).
- **Subtítulos siempre**: muchas personas ven sin sonido; además ayudan a la accesibilidad.
- **Etiqueta de IA y «para niños»** decididas desde el plan, no al subir.
- Publicar primero un **Short de 20 a 30 s** como prueba de interés.

## Señales de alerta
- Empezar a producir sin guion medido ni muestra aprobada.
- Prometer un acabado que el camino elegido no da (por ejemplo, realismo con dibujos sencillos).
- Un guion que solo suena bien «en la cabeza» (leerlo en voz alta o medirlo).
- Créditos sin presupuesto ni aprobación.

## Verificación
- [ ] La ficha está completa y Jeiler la aprobó.
- [ ] `medir_guion.py` sin avisos y duración dentro del 15 % de la meta.
- [ ] Hay al menos una alternativa descartada con su motivo.
- [ ] Costo y licencias escritos; ningún gasto sin «sí».
- [ ] El plan dice qué no se podrá comprobar.

## Qué se probó (2026-11-04)
`medir_guion.py` midió el guion del video explicativo de prueba (144 palabras, estimación de 58 s con voz sintética; falta comparar con la duración real del video) y marcó cuatro problemas de estilo en un guion malo a propósito (frase larga, punto y coma, promedio alto y duración fuera de meta). La plantilla de plan se usó para el explicativo de prueba. **Falta** usarla con un pedido real de Jeiler y calibrar los ritmos con más voces (los 0,40 y 0,52 s por palabra salen de pruebas anteriores).
