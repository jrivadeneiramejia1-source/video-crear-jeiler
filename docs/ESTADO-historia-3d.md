# Estado de las historias 3D (2026-11-05)

## Versión 2 de «Lila y el arcoíris» (corrige lo que Jeiler vio en la versión 1)
- **Pies:** en la v1 la revisión daba por bueno cualquier pie a menos de 1 % del borde y solo miraba el primer cuadro de cada tramo. Ahora `escena3d.py` mide inicio, mitad y final de CADA tramo y exige pies ≥ 16 % sobre el borde de abajo y cabeza con 4 % de aire (con la regla nueva, la v1 daba 11 avisos, con pies hasta en −5 %). Se subieron/alejaron cámaras (tomas 1, 3, 4, 5, 7, 8): pies más bajos medidos 21 %. Se miraron a tamaño completo inicio, mitad y final de las 8 tomas del video final con la banda de subtítulos marcada (`marcar_banda.py`): pies siempre sobre la banda y subtítulos de una sola línea sin tapar caras.
- **Alegría:** toma 7 sin `saltar`: gesto `alegria` (brazos arriba que se agitan) + `balanceo`, pies en el suelo.
- **Voces:** `--guion` (GUION.md para grabar), `--voces-propias` (una por frase o por personaje; limpieza con `audio-limpio`; la duración real manda; solo en carpetas fuera del repo) y Piper opcional (`instalar_piper.sh`). 6 muestras de una misma frase enviadas a Jeiler para elegir.
- Dibujo: 389 cuadros en 75 min (11,6 s por cuadro). `check.py` YouTube: 18 comprobaciones, 0 fallas (avisos: 854x480 y sin pista de subtítulos suave). −14,8 LUFS, pico −1,0 dBTP.
- **Sin probar / pendiente:** nadie ha oído las voces (incluidas las 6 muestras) ni visto el movimiento; las voces del video v2 siguen siendo las de Kokoro de la v1 (no se cambiaron sin que Jeiler elija); `--voces-propias` se probó solo con voces sintéticas inventadas hechas pasar por grabaciones (una por frase en wav y mp3, una por personaje con alineación 93 % y 86 % de palabras), nunca con voces humanas reales; Cloudflare Workers AI no se probó (pide cuenta y clave de Jeiler); `balanceo` casi no se nota en cuadros fijos. Falla vista: el saludo de Lila en la toma 8 levanta el brazo a la altura del hombro (no por encima de la cabeza) y en la toma 8 la ventana queda cortada sin arcoíris al bajar la cámara.

## Hecho y probado: «Lila y el arcoíris» (video de prueba de 32,4 s)
- Se hizo de punta a punta con `skills/historia-3d/scripts/crear_historia3d.py`: voces sintéticas (narrador, Lila y Tito), 30 tramos de toma, **389 cuadros dibujados en 81 minutos** (12,5 s por cuadro a 854x480, 12 muestras, 12 cuadros de dibujo por segundo duplicados a 24), música calmada original, subtítulos y revisión.
- Mediciones del video final: 18 comprobaciones de `check.py` sin fallas (avisos: 854x480 y subtítulos quemados, sin pista suave); -14,7 LUFS integrados, pico -1,0 dBTP; sin destellos; lectura 135 palabras por minuto y 13,9 letras por segundo (guía infantil: 140 y 15, sin calibrar).
- Cuadros mirados por Claude: título, cuarto con ventana 3D y lluvia, hoja de personajes (Lila con coletas y lazos rosados, Tito con pelo corto), la toma desde la ventana con el arcoíris completo, el salto (ambos despegan) y el saludo de Lila.
- **Errores encontrados al revisar el video y corregidos:** el salto no despegaba del suelo (la animación de Kenney no mueve el cuerpo hacia arriba: se agregó un arco en el aire), Lila nunca saludaba (los ejes del brazo derecho están espejados: la mano iba hacia atrás), quien habla perdía su animación de salto, personajes con los pies fuera del cuadro en tres tomas, franja de cielo sobre la pared (faltaba techo), color mal etiquetado en el MP4, subtítulos con nombres que subían la velocidad de lectura.

## Sin probar o sin resolver
- **Nadie ha oído las voces ni la música, ni visto el movimiento** (solo se miraron cuadros y se midió). Falta el juicio de Jeiler.
- Resolución 854x480 (un cuento de 32 s a 1280x720 tardaría cerca de 2 horas y media).
- Las caras de Kenney son dibujos fijos: no mueven la boca ni cambian de expresión (Tito tiene una boca «o» siempre).
- Un solo cuarto; faltan sillas y sofás donde sentarse (las animaciones de sentarse existen, sin probar en una toma).
- Personajes de otros paquetes (KayKit, Universal Base Characters) y humanos más realistas (MPFB2): sin probar.
- Gestos `senala`, `asiente`, `niega` y `preocupado`: vistos en imágenes fijas, no en movimiento.

## Cómo repetirlo
```bash
bash skills/video-3d/scripts/instalar_blender.sh                       # bpy (Blender sin pantalla)
bash skills/video-3d/scripts/descargar_personajes.sh animated-characters-2
bash skills/video-3d/scripts/descargar_recursos.sh                     # muebles, naturaleza, animaciones
python3 skills/video-3d/scripts/descargar_cielo.py overcast_soil_puresky kloofendal_48d_partly_cloudy_puresky
bash skills/video-3d/ejemplo-historia/crear_pieles.sh                  # pieles de Lila y Tito
bash skills/voz-sintetica/scripts/instalar_voz.sh                      # voces
pip: en ese mismo venv hace falta playwright y pillow para crear_pieles.sh (~/.cache/video-jeiler/venv/bin/pip install playwright pillow)
python3 skills/historia-3d/scripts/crear_historia3d.py skills/video-3d/ejemplo-historia/historia.json salida --solo-plan
python3 skills/historia-3d/scripts/crear_historia3d.py skills/video-3d/ejemplo-historia/historia.json salida --ancho 854 --alto 480 --muestras 12
```
(Las variables `PYTHON_VOZ` y `PYTHON_BLENDER` dicen qué Python usar; por defecto `~/.cache/video-jeiler/venv` y `venv-blender`.)
