---
name: video-explicativo
description: >-
  Crea un video explicativo completo y gratis a partir de un guion: voz sintética en español, escenas animadas (título, listas, comparaciones, pasos, números, barras y cierre), subtítulos y música original, en horizontal y en vertical desde el mismo guion. Usar cuando el usuario diga "un video que explique...", "compara A con B en un video", "un video de pasos o de consejos", "un explicativo corto" o "hazme un Short que explique". No hace cuentos con personajes (usar animacion-2d), 3D ni videos con una persona real (usar video-editar-jeiler).
---

# Video explicativo

Un solo comando convierte `guion.json` en el video terminado: la voz sintética marca el tiempo de cada frase, cada escena aparece cuando se dice lo que muestra, los subtítulos salen de la misma narración y la música baja sola cuando se habla. Todo corre en la nube y sin costo.

## Reglas
- **Es voz sintética y música generada: declararlo** en los créditos y al publicar (el ejemplo ya trae las líneas de créditos).
- **Datos y cifras:** solo los que Jeiler pueda respaldar; la escena `barras` pide `fuente`. No inventar estadísticas ni comparar marcas con afirmaciones que no se hayan verificado el mismo día.
- **Logos:** solo para nombrar o comparar, nunca para aparentar apoyo de la marca; de Simple Icons (CC0) o un archivo que dé Jeiler; no redibujar logos (ver `graficos-por-palabra` en `video-editar-jeiler`). Una imagen de marca se pasa en `imagen` (ruta de un PNG).
- Antes de dibujar, **revisar el plan** (`--solo-plan`) y **mirar la hoja de cuadros**: dibujar cuesta unos 2 a 3 minutos por formato.
- Nada se publica solo; no se sobrescribe un video existente.
- Claude no oye el audio ni ve el movimiento: Jeiler escucha y mira antes de publicar.

## Instalar (una vez)
Instalar el grupo `explicativo` y preparar voz y dibujo:
```bash
bash ../voz-sintetica/scripts/instalar_voz.sh
bash ../animacion-2d/scripts/instalar_render.sh
PY=~/.cache/video-jeiler/venv/bin/python
```

## Proceso
1. **Planear** con `plan-de-video`: guion de 6 a 14 palabras por frase, medido (`medir_guion.py --voz sintetica --duracion 60`).
2. **Escribir `guion.json`** (ver `ejemplo/guion.json`). Cada escena lleva `tipo`, sus textos y `narracion` (lista de frases). Tipos:
   - `titulo` (`texto`, `detalle`, `icono`) · `lista` (`titulo`, `items`) · `comparar` (`izquierda` y `derecha` con `titulo`, `puntos`, `icono` o `imagen`, `malo`: true para ✗) · `pasos` (`titulo`, `pasos`) · `numero` (`valor`, `prefijo`, `sufijo`, `texto`) · `barras` (`datos`: nombre y valor, `unidad`, `fuente`) · `cierre` (`texto`, `creditos`).
   - Los elementos de una escena aparecen cuando se dicen: se asignan a las **últimas n frases** de su narración (en `pasos` conviene una frase de introducción y luego una por paso).
   - Íconos: check, cruz, flecha, estrella, corazon, bombilla, telefono, nube, engranaje, candado, reloj, libro, wifi, casa.
   - Opcionales: `musica` (`animo`: alegre, calmo, misterio, epico; `tono`; `volumen_lufs`), `voz` (ef_dora, em_alex, em_santa), `velocidad`, `marca`, `tema` (colores).
3. **Plan:** `$PY scripts/crear_explicativo.py guion.json salida --solo-plan` (escenas, frases y duración con la voz; no dibuja).
4. **Crear:** `$PY scripts/crear_explicativo.py guion.json salida` (horizontal 1280x720 y vertical 720x1280; `--formatos vertical` para uno solo; `--lufs -16` para otro volumen; `--sin-musica`). Deja `video_horizontal.mp4`, `video_vertical.mp4`, `hoja_*.png`, `proyecto.json`, `audio_final.wav` e `informe.txt`. Si solo cambia el audio, `--reusar` evita dibujar otra vez.
5. **Mirar** las hojas de cuadros (horizontal y vertical) y buscar textos cortados, tarjetas encimadas o subtítulos tapados.
6. **Verificar** con `verificar-video` de `video-editar-jeiler` (o `ffmpeg-skill/check.py --platform youtube|shorts --content`) y pasar los subtítulos por `subtitulos/verificar_subtitulos.py` si se quiere doble comprobación.
7. Pedir a Jeiler que **escuche y mire** una muestra; ajustar el guion (no la velocidad) y repetir.

## Señales de alerta
- Frases de más de 16 palabras: se subtitulan y se dicen mal.
- Escenas con demasiados elementos (más de 4 por escena): partirla.
- Cifras sin fuente o comparaciones de marcas sin verificar.
- Texto que se corta en vertical: revisar siempre las dos hojas.
- Música que tapa la voz (bajar `volumen_lufs`).

## Verificación
- [ ] `--solo-plan` revisado y duración dentro de la meta.
- [ ] Hojas de cuadros mirada en horizontal y vertical.
- [ ] `check.py` o `verificar-video` sin FAIL.
- [ ] Créditos con voz sintética, música generada y fuentes de cada dato.
- [ ] Jeiler escuchó una muestra.

## Qué se probó (2026-11-04)
Un video de ejemplo **inventado** («¿Qué es una PWA?», 6 escenas, 16 frases, 144 palabras) se creó de punta a punta en horizontal y vertical (4 min 16 s en total; 1757 cuadros por formato). Resultado: duración 58,57 s en los dos (la esperada), volumen -14,2 LUFS con pico -1,5 dBFS; `check.py` sin FAIL (18 comprobaciones) para YouTube y para Shorts. Una transcripción automática independiente del **video final con voz y música mezcladas** coincidió 100 % con los subtítulos, con un desfase de 0,07 s en promedio (máximo 0,16 s). Las hojas de cuadros, mirando horizontal y vertical, quedaron limpias.

**Fallos reales que aparecieron al mirar y se corrigieron:** tarjetas de lista encimadas con textos largos, texto encimado en la comparación, tarjetas que invadían los subtítulos en vertical, primer paso cortado en el borde izquierdo, audio más corto que la imagen (se perdían los créditos) y un primer cuadro casi en blanco (la miniatura de un feed). Los últimos arreglos (primer cuadro y opción `--hd`) se comprobaron con cuadros sueltos, **sin volver a dibujar el video completo**.

**Avisos que quedan:** el vertical sale a 720x1280 y Shorts pide 1080x1920 (usar `--hd`, probado solo con un cuadro); no lleva pista de subtítulos aparte (usar el `.srt` de `subtitulos`).

**No se probó** con imágenes de marcas, con las escenas `barras` y `numero` en un video completo, con guiones de más de 3 minutos, con otras voces, con el modo `--hd` completo ni con oyentes: Jeiler no ha escuchado la voz ni la música.
