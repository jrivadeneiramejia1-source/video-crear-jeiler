---
name: estudiar-video-referencia
description: >-
  Estudia un video que a Jeiler le gustó (por ejemplo uno de TikTok) para sacar su «receta» de estilo y hacer otro propio parecido: formato, tramos con tiempos, ritmo, paleta de colores, volumen y tempo de la música, y qué copiar y qué NO. Mide con un script y mira una hoja de cuadros. Copia el ESTILO, nunca el contenido (texto, música, marcas de agua, nombres de usuario, código o dibujos de otra persona). Usar cuando el usuario diga "quiero un video como este", "hazme uno parecido a este de TikTok", "analiza este video", "repite el estilo de este" o mande un video ajeno de referencia.
---

# Estudiar un video de referencia

Sirve para entender **por qué funciona** un video ajeno (cómo está armado, cuánto dura cada parte, qué colores y qué ritmo tiene) y construir **otro distinto** con la misma idea de estilo. No sirve para copiarlo, recortarlo ni republicarlo.

## Reglas
- **Estilo sí, contenido no.** No se copia el texto, la letra, la música, la animación idéntica, el código, los dibujos, las marcas de agua ni el nombre de usuario. Un video «igual pero con otro nombre» no es un estilo: es una copia.
- **Jeiler entrega el archivo.** No se baja de plataformas por nuestra cuenta (bajar con herramientas puede ir contra sus términos).
- **El material ajeno no sale de aquí:** no va al repo (es público; `.gitignore` bloquea `referencias/` y `receta_*/`), no se sube a servicios externos (IA de video, ElevenLabs, etc.) y no se usa como material del video nuevo.
- Se trabaja en una **carpeta nueva**; el archivo recibido no se ejecuta ni se modifica.
- Archivos de comunidades indígenas o de personas reales: no son «referencias»; no se tocan (ver `CLAUDE.md`).
- Claude no oye ni ve el movimiento: mira cuadros y mide; lo que suena y cómo se mueve lo juzga Jeiler.

## Proceso
1. **Copiar el video** a una carpeta de trabajo nueva (por ejemplo `referencias/`, que no se sube).
2. **Medir:** `python3 scripts/receta.py referencias/video.mp4 --salida receta_video` (4 s para un video de 40 s). Deja `receta.md`, `receta.json` y `hoja.png`.
3. **Mirar `hoja.png`** (un cuadro cada 2,5 s) y escribir los tramos reales con sus tiempos: qué aparece, qué se mueve, qué texto aparece (se describe con otras palabras; **no se copia**). Los tramos del script son candidatos: **comprobarlos contra los cuadros**.
4. **Quitar lo que no es del autor:** los últimos segundos con la pantalla final de la plataforma, la marca de agua que se mueve y el nombre de usuario. No cuentan como estilo.
5. **Sonido:** mirar el volumen (si el pico llega a 0 dBFS está saturado: no imitarlo) y el tempo. Si el reconocedor de voz (`subtitulos/transcribir.py`) devuelve frases sin sentido, casi seguro es una canción con letra: **no se copia la letra ni la música**.
6. **Escribir la receta** con `plantilla/receta-estilo.md`: formato, estructura por tiempos, paleta (códigos de color), tipo de letra (descrito), ritmo, sonido, y dos listas: «se copia» y «no se copia».
7. **Proponer el video nuevo:** idea y texto propios (o de Jeiler) usando la receta; elegir el camino con `plan-de-video` y las skills de crear (`animacion-2d`, `video-explicativo`, `musica-y-efectos`, `video-3d`). **Jeiler aprueba la receta y el plan antes de producir.**

## Señales de alerta
- Copiar el poema, la letra, el código o el nombre de la persona.
- Usar la grabación ajena como parte del video nuevo.
- Fiarse de los tramos del script sin mirar los cuadros.
- Imitar el volumen saturado.

## Verificación
- [ ] El archivo recibido no entró al repo ni a servicios externos.
- [ ] La receta separa «se copia» de «no se copia»; no contiene texto, letra ni nombres ajenos.
- [ ] Los tramos se comprobaron contra la hoja de cuadros.
- [ ] Marca de agua y pantalla final fueron excluidas del análisis.
- [ ] Jeiler aprobó la receta antes de producir.

## Qué se probó (2026-11-05)
`receta.py` se probó con **un video inventado de 9 s con tres colores y un tempo conocido (120)**: midió 117 pulsos por minuto (2,5 % de error), halló los dos cortes (3 s y 6 s) y los tres tramos de color. También se probó con dos videos de otros creadores (no están en este repo y no se usan como ejemplo): los tramos coincidieron con lo que se ve en las hojas de cuadros, pero **no separó los pasos dentro de un tramo largo**; eso lo vio Claude en la hoja. Los umbrales están sin calibrar (con 0,20 los destellos de una animación cuentan como cambios bruscos). **No se probó:** hacer un video nuevo siguiendo una receta; videos horizontales ni de más de 5 minutos; detectar texto en pantalla (no hay lector de texto instalado: lo lee Claude en la hoja); distinguir voz de música de forma automática.
