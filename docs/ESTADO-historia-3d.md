# Estado de las historias 3D (2026-11-05)

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
python3 skills/historia-3d/scripts/crear_historia3d.py skills/video-3d/ejemplo-historia/historia.json salida --solo-plan
python3 skills/historia-3d/scripts/crear_historia3d.py skills/video-3d/ejemplo-historia/historia.json salida --ancho 854 --alto 480 --muestras 12
```
(Las variables `PYTHON_VOZ` y `PYTHON_BLENDER` dicen qué Python usar; por defecto `~/.cache/video-jeiler/venv` y `venv-blender`.)
