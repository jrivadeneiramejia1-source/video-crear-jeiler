---
name: video-infantil
description: >-
  Crea y revisa videos para niños pequeños (cuentos, canciones, lecciones cortas) con reglas extra de seguridad, ritmo y accesibilidad: personajes inventados y amables, voz sintética tranquila, nada de sustos ni destellos, texto grande y poco, y una revisión medible (destellos, cortes por minuto, golpes de volumen, velocidad de narración) más una revisión de una persona adulta. Usar cuando el usuario diga "un video para niños", "un cuento infantil", "para niños de preescolar", "una canción para niños", "contenido para menores" o publique en un canal infantil. Se apoya en video-explicativo (motor 2D, voz y música).
---

# Video infantil

Un video para niños se hace con más cuidado que uno para adultos: lo que ven no se puede «deshacer» y no pueden juzgar por sí mismos qué es seguro. Esta skill **añade reglas y una revisión** encima del flujo de `video-explicativo`; no es otro motor.

## Reglas
- **Todo inventado.** Personajes, nombres, voces y cuentos son inventados. Nada de niños reales (ni sus nombres, voces, caras o dibujos), ni personajes o canciones de otras marcas.
- **Voz sintética tranquila.** Se declara en la descripción y en los créditos («voz sintética»). Nada de clonar voces; menos aún de niños o de personas conocidas sin permiso escrito.
- **Nada de sustos:** sin gritos, sin golpes de volumen, sin destellos, sin personajes feos, sucios, armados o con sangre (ojo con los paquetes 3D: muchos son soldados o zombis; ver `video-3d`).
- **Un solo mensaje por video**, pocas palabras, una frase por idea, 5 a 8 palabras por frase. Los más pequeños casi no leen: **la voz cuenta y el subtítulo acompaña**.
- **Ritmo calmado:** menos de 12 cortes de escena por minuto, escenas de 6 s o más, música baja (≈ -27 LUFS debajo de la voz), sin anuncios ni «compra» ni enlaces a otros sitios.
- **Datos:** el video no pide nombre, edad, foto ni ubicación a nadie, ni sugiere buscar cosas fuera.
- **Una persona adulta revisa antes de publicar** (Jeiler o quien él indique): la máquina no sabe si algo asusta, si es violento o si enseña algo bueno.
- **Publicar:** nada se publica solo. YouTube pide declarar si el video es «para niños» (cambia comentarios, anuncios y funciones) y que se declare el contenido realista hecho con IA; **esas reglas cambian y no se pudieron leer en las páginas oficiales desde esta sesión: verificarlas antes de subir.**
- Claude no oye el audio ni ve el movimiento: mira cuadros y mide.

## Proceso
1. **Idea y mensaje único** en una frase («Esperar trae cosas bonitas»). Edad objetivo (3–5, 6–8) y duración corta (≤ 60 s para empezar).
2. **Guion corto** con el formato de `video-explicativo/ejemplo` (ver `ejemplo/guion.json` de esta skill: cuento con dos personajes, objetos, diálogos atados a frases de la narración y cierre con créditos). Medir ritmo con `plan-de-video` (`medir_guion.py`).
3. **Plan sin dibujar** (revisar antes de gastar tiempo): `python3 video-explicativo/scripts/crear_explicativo.py ejemplo/guion.json carpeta --solo-plan`
4. **Construir:** `python3 video-explicativo/scripts/crear_explicativo.py ejemplo/guion.json carpeta` (horizontal 1280x720 y vertical 720x1280; `--hd` para 1080p). Voz `ef_dora` a velocidad 0,9 y música «calmo» funcionaron bien para esto.
5. **Mirar** `hoja_horizontal.png` y `hoja_vertical.png` (cuadros): globos de diálogo sin tapar nada, textos completos, personajes con la cara visible, subtítulos legibles.
6. **Revisión medible:**
   ```bash
   python3 scripts/revisar_infantil.py carpeta/video_horizontal.mp4 [--srt subtitulos.srt]
   ```
   Mide destellos (límite 3 por segundo, guía WCAG 2.3.1; aquí es una **estimación**), cortes por minuto, golpes de volumen y velocidad de narración. Sale con código 1 si algo avisa; corregir y repetir.
7. **Revisión técnica** general con `verificar-video` (`check.py --content`): volumen, formato, audio presente.
8. **Una persona adulta lo ve y lo escucha completo** y firma el «sí». Recién entonces se piensa en publicar (con `publicar-video` de `video-editar-jeiler`, que no publica solo).

## Coherencia entre el cuento y lo que se ve
Si la narración dice «por la ventana», tiene que haber una ventana en el cuadro; si dice «arcoíris», se ve el arcoíris. En el cuento de ejemplo en 2D se mencionaba una ventana que no estaba dibujada y se corrigió el texto. Para historias con escenarios y objetos, usar `historia-3d` (revisa lo que el cuento dice que se ve) en vez del motor 2D.

## Señales de alerta
- Aprobar un video porque `revisar_infantil.py` dijo OK: solo mide cuatro cosas.
- Voz sintética sin declarar; música con derechos de otros.
- Muchos textos en pantalla: el niño no los lee y el adulto los lee tarde.
- Personajes tomados de paquetes 3D de «sobrevivientes» o zombis.
- Prometer que es «apto para niños» o que cumple una ley (COPPA, etc.): eso no lo decide una skill ni Claude.

## Verificación
- [ ] Todo inventado; sin datos de personas ni de niños reales.
- [ ] Voz sintética declarada en créditos y descripción.
- [ ] `revisar_infantil.py` sin avisos (o avisos explicados), hojas de cuadros miradas en horizontal y vertical.
- [ ] Una persona adulta lo vio y escuchó entero y dio el «sí».
- [ ] Reglas de la plataforma («para niños», etiqueta de IA) verificadas antes de subir.

## Qué se probó (2026-11-05)
Con el cuento inventado de `ejemplo/guion.json` («Lila y el arcoíris», 4 escenas, 53 palabras, voz sintética `ef_dora`, música calmada): se construyó en horizontal y vertical sin errores de la página. **La primera versión (voz a 0,9) fue de 25,8 s y el revisor avisó «narración a 150 palabras por minuto»; se bajó la voz a 0,8** y la versión final (29,9 s, 898 cuadros) dio: destellos 0, volumen -14,2 LUFS con diferencia máxima de 4,4 LU, pico -1,3 dBFS, 10,7 letras por segundo y 126 palabras por minuto, todo OK; `check.py` para YouTube: 18 comprobaciones, 0 fallas y 1 aviso (el MP4 no lleva pista de subtítulos; el `.srt` se hizo aparte con `subtitulos/a_srt.py`). **Errores de diseño encontrados al mirar las hojas de cuadros y corregidos:** el arcoíris tapaba los globos de diálogo (ahora los globos se dibujan encima de los objetos), el título chocaba con la nube y las gotas caían sobre un globo (se movieron en el ejemplo), y en vertical los créditos de cierre se cortaban por los lados (ahora se parten en renglones). Todavía en vertical el subtítulo grande tapa los hombros de los personajes (no la cara). La revisión medible también se probó con videos de prueba hechos con ffmpeg: un parpadeo de 6 Hz avisó, un golpe de volumen avisó y un explicativo calmado quedó OK. **El contador de «cortes» solo cuenta cortes secos y marcó 0 aquí porque las escenas cambian con fundido**: no mide el ritmo de un video con fundidos. **No se probó:** que alguien oyera la voz ni la música (se midió, no se escuchó); el movimiento; niños reales ni opinión de educadores; las reglas oficiales de YouTube o TikTok; los umbrales (12 cortes por minuto, 8 LU, 15 letras por segundo, 140 palabras por minuto) son guías **sin calibrar**.
