---
name: musica-y-efectos
description: Crea música de fondo original y efectos de sonido con código (sin muestras ni melodías de nadie, así que sin problemas de derechos), y enseña a ponerlos debajo de una voz con bajada automática del volumen. Elige ánimo (alegre, calmo, misterio, épico), tono y duración. También guía para usar música de bibliotecas con licencia clara. Usar cuando el usuario diga "ponle música", "música de fondo", "efectos de sonido", "un sonido cuando aparezca el logo" o "música sin derechos de autor". No compone canciones con letra ni imita artistas.
---

# Música y efectos

La música sale de **acordes, un arpegio, un bajo y percusión suave** generados con código: no usa muestras ni melodías de terceros, así que no hay derechos de otros que cuidar. Es música de fondo sencilla, pensada para ir **debajo de una voz**.

## Reglas
- Claude **no puede oír**: mide volumen y pico y mira un espectrograma, pero si la música «suena bien» lo decide Jeiler con una muestra de 30 s.
- Nada de imitar canciones, artistas o jingles conocidos.
- Si se usa música de una biblioteca (Pixabay, Freesound, Archive.org...), **anotar la licencia y la fuente** en los créditos; revisar las condiciones del día, porque cambian. Pixabay y Pexels no permiten revender el archivo suelto.
- La música nunca tapa la voz: más baja que la voz y con bajada automática (ducking).

## Proceso
1. **Ánimo y duración:** alegre (112 bpm, con percusión), calmo (76 bpm), misterio (88 bpm, tono menor) o épico (100 bpm, menor y con bajo fuerte).
2. **Componer:** `python3 scripts/componer.py musica.wav --duracion 60 --animo calmo --tono C --semilla 1` (misma semilla, misma música; otra semilla, otra variación). Sale estéreo de 48 kHz con el pico en -6 dBFS.
3. **Muestra:** que Jeiler oiga 30 s antes de usarla en todo el video; ajustar `--animo`, `--tono` o `--bpm`.
4. **Efectos:** `python3 scripts/efectos.py carpeta_efectos` crea `pop`, `ding`, `clic`, `whoosh`, `exito` y `error` (mono, 48 kHz, pico -3 dBFS).
5. **Mezclar bajo la voz:** con `video-explicativo` ya va incluido (música a -28 LUFS con bajada automática). A mano, con `ffmpeg-skill`: `python3 ../ffmpeg-skill/scripts/audio.py VIDEO --music musica.wav --duck --music-volume -18`.
6. **Comprobar:** `ffmpeg-skill/scripts/check.py VIDEO --platform youtube --content` (volumen, pico, cortes de audio).

## Señales de alerta
- Música que compite con la voz (se entienden menos las palabras).
- Un final cortado de golpe: usar duraciones de compases enteros (el script ya agrega un cierre suave).
- Efectos en cada gesto: cansa; pocos y con sentido.

## Verificación
- [ ] Jeiler oyó la música (o se dijo que no se pudo comprobar).
- [ ] El pico y el volumen final están dentro de lo pedido para la plataforma.
- [ ] Los créditos dicen «música original generada por código» o la licencia de la pista usada.

## Qué se probó (2026-11-04)
Se compusieron los cuatro ánimos (30 s cada uno): pico exacto de -6,0 dBFS y volumen entre -17,7 y -20,3 LUFS; el espectrograma muestra el ritmo y los cambios de acorde esperados. Se generaron los seis efectos. Se usó la música «calmo» en un video explicativo de prueba (ver `video-explicativo`). **No se probó con oyentes**: la calidad musical no está verificada. Es música sencilla de fondo; no reemplaza a un compositor para algo que deba destacar.
