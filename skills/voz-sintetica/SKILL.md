---
name: voz-sintetica
description: Convierte un texto en voz en español, sin internet y gratis (modelo Kokoro), y guarda el tiempo exacto de cada frase para sincronizar subtítulos y escenas sin reconocer la voz. Sirve para narrar explicativos, borradores y muestras cuando la persona aún no puede grabar. Usar cuando el usuario diga "ponle una voz", "narración automática", "voz de computadora", "hazme el audio del guion" o "una muestra con voz". No clona voces de personas ni imita a nadie.
---

# Voz sintética

Voz de narración en español con Kokoro (82 millones de parámetros, corre en CPU). Cada frase sale con su inicio y su fin, así que el video se arma sobre tiempos exactos.

## Reglas
- **Es una voz sintética: declararlo** al publicar (créditos y descripción) y, si la plataforma lo pide, en su etiqueta de contenido sintético.
- **No clonar voces.** Esta skill no copia la voz de nadie. Si algún día se quiere la voz de una persona, solo con su permiso escrito y con una herramienta aparte.
- Para videos que van con la voz real de alguien (como los cortos de la universidad), esta voz sirve solo de **guía o muestra**: la narración final la graba la persona.
- Los textos de personas reales (nombres) se escriben como los confirmó Jeiler.
- Claude no oye: la calidad de la voz (acento, entonación) la juzga el oído de Jeiler.

## Instalar (una vez)
```bash
bash scripts/instalar_voz.sh     # ~355 MB desde github.com y pypi.org; crea ~/.cache/video-jeiler con su propio Python
PY=~/.cache/video-jeiler/venv/bin/python
```

## Proceso
1. Escribir el texto **una frase por línea** (frases de 6 a 14 palabras suenan mejor; ver `plan-de-video/scripts/medir_guion.py`).
2. `$PY scripts/narrar.py texto.txt voz.wav --voz ef_dora --tiempos tiempos.json` (`--velocidad 0.9` para más lento, `--pausa 0.6` para pausas más largas).
3. Voces de español: `ef_dora` (mujer), `em_alex` y `em_santa` (hombres) (`$PY scripts/narrar.py --voces` lista todas; las de otros idiomas no son para español).
4. Revisar `tiempos.json` y la duración; si se pasa, recortar el texto, no acelerar la voz.
5. El volumen final se deja con `ffmpeg-skill` (`audio.py`, `check.py`) o con `crear_explicativo.py` de `video-explicativo`.
6. Pedir a Jeiler que **escuche una muestra** antes de producir todo.

## Señales de alerta
- Palabras raras (siglas, nombres de marcas, números largos): escribirlas como se dicen («H-T-T-P-S», «dos mil veintiséis») o cambiar la frase.
- Voz sintética presentada como si fuera una persona.
- Usar esta voz en lugar de la de una persona que ya iba a grabar sin avisarle.

## Verificación
- [ ] `tiempos.json` coincide con la duración del audio.
- [ ] Jeiler escuchó una muestra y la aprobó.
- [ ] Los créditos dicen que la voz es sintética.

## Qué se probó (2026-11-04)
El instalador real bajó los modelos (325 MB y 28 MB) y el Python propio sin errores. Una narración de prueba de 115 palabras salió a unos 0,40 s por palabra con pausas, y un reconocedor automático entendió el 98,3 % de sus palabras (una medida de claridad, no de naturalidad). Se probaron las tres voces de español listadas, la velocidad y los tiempos por frase. **No se probó** con textos muy largos, con números ni siglas, ni con oyentes: cómo suena lo decide Jeiler. Licencias: Kokoro (Apache-2.0) y `kokoro-onnx` (MIT), según sus repositorios.
