# En pausa: video de prueba «Lila y el arcoíris» en 3D (2026-11-05)

**Decisión de Jeiler:** primero se buscan todas las skills y herramientas necesarias y se completa este repo; **después** se retoma el video de prueba. No hay ninguna tarea programada.

## Lo que ya funciona (probado con imágenes fijas de 640x360, unos 5 s cada una)
- `skills/video-3d/scripts/escena3d.py`: arma desde un JSON un cuarto con muebles de Kenney (cama, mesa, lámpara, planta, **ventana 3D con marco**), exterior con pasto, árboles, **lluvia** y **arcoíris**, personajes de Kenney con gestos y cámaras por toma. Revisa solo que lo que dice el cuento (`muestra`) esté dentro del cuadro: ya detectó dos tomas mal encuadradas.
- `personalizar_piel.py`: cambia colores de pelo y ropa o quita dibujos desde el SVG de origen de la piel (fiel al original: diferencia media 0,25 de 255).
- `descargar_recursos.sh`: muebles y naturaleza de Kenney (CC0). `ejemplo-historia/`: historia de 7 tomas y `crear_pieles.sh` (Lila con coletas y lazos, Tito sin calavera).
- Hallazgo clave: las animaciones de Kenney se hicieron con los brazos abajo y el modelo está en «T»; **se copia la dirección de cada hueso** (`reorientar`) en vez de los números de la animación.
- EEVEE no sirve aquí (con OpenGL por software sale roto o negro): se usa Cycles en CPU, unos 5 s por imagen a 640x360 con 12 muestras.

## Pendiente antes de renderizar el video
1. Pared sobreexpuesta (bajar `luz_interior` o la exposición) y suelo muy claro.
2. El arcoíris no aparece en la toma 5 tras corregir su forma: acomodar posición y tamaño.
3. Comprobar los gestos (saludar, señalar, alegría) en imágenes fijas; la toma 6 usa la animación de salto.
4. Hoja de personajes grande (frente, perfil, espalda, rostro) de Lila y Tito para aprobarla con Jeiler **antes** de animar.
5. Voces (narrador, Lila, Tito), música, subtítulos y el orquestador `crear_historia3d.py` (aún no existe).
6. Estimación: unos 8 s por cuadro a 960x540 con 16 muestras y 12 cuadros por segundo de dibujo; una historia de 35 s ≈ 420 cuadros ≈ 1 hora de CPU.
7. Cuento y dibujo deben coincidir: el cuento antiguo en 2D (`video-infantil/ejemplo`) decía «por la ventana» y no tenía ventana; Tito parecía una mujer.

## Cómo retomar
```bash
bash skills/video-3d/scripts/instalar_blender.sh && bash skills/video-3d/scripts/descargar_personajes.sh animated-characters-2 && bash skills/video-3d/scripts/descargar_recursos.sh
bash skills/video-3d/ejemplo-historia/crear_pieles.sh
~/.cache/video-jeiler/venv-blender/bin/python skills/video-3d/scripts/escena3d.py skills/video-3d/ejemplo-historia/historia.json salida --fija 3:1 --ancho 640 --alto 360 --muestras 12
```
