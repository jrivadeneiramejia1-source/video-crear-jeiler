---
name: historia-3d
description: >-
  Convierte una historia en un video 3D en el orden correcto y con compuertas: primero la historia y su mundo (lugar, época, clima, tono y nivel de formalidad), después los personajes hechos a medida de esa historia (modelo, pelo, ropa y accesorios que encajan con el mundo del cuento, hoja de personaje aprobada de frente, perfil, espalda y rostro), después el escenario con piezas 3D reales (ventana, cama, lluvia, arcoíris, cielos), después las tomas con animaciones y cámaras, y al final voz, música y subtítulos. Revisa que todo lo que dice el cuento esté dentro del cuadro y que los personajes se distingan. Usar cuando Jeiler diga "creemos un video sobre tal historia", "un cuento en 3D", "un video con personajes 3D" o "hazme el video de esta historia con avatares". ESTADO: probada de punta a punta con un cuento de ejemplo de 32 s (dibujo con Blender, voces sintéticas, música y subtítulos); nadie ha oído ni visto el video en movimiento todavía.
---

# Historia en 3D

Un video con historia falla casi siempre por lo mismo: los personajes se ven raros o se parecen entre sí, y el dibujo no muestra lo que dice el cuento (en una prueba, el cuento hablaba de una ventana que no existía y un niño parecía mujer). Esta skill **fija el orden**: nada pasa a la siguiente etapa sin aprobar la anterior. **La historia manda:** los personajes se crean a partir de ella, no al revés (una historia elegante no lleva personajes con ropa deportiva; una historia de granja no lleva trajes).

## Reglas
- **Orden obligatorio:** historia y su mundo → personajes hechos a medida de la historia → hoja de personajes aprobada → escenario → tomas de prueba (imágenes fijas) → video → voz, música y subtítulos.
- **Primero la historia, después los personajes** (los personajes son lo más difícil, por eso se hacen con la historia ya clara). Cada personaje justifica su ropa, peinado y accesorios con la historia (lugar, época, clima, ocasión, oficio, tono). Se ven de frente, de perfil, de espalda y de cerca (pelo, cara, manos, proporciones) y los **mira Claude** con ojos críticos y los **aprueba Jeiler** antes de seguir.
- **Se tienen que distinguir** a simple vista, también de espalda: pelo/peinado/accesorio distinto, colores de ropa distintos. Si dos personajes se parecen, no se sigue.
- **El cuento y la imagen coinciden.** Todo lo que el cuento nombra y se puede ver (ventana, lluvia, arcoíris, cama, oso de peluche...) existe como pieza 3D y aparece en el cuadro de esa toma. Se declara en `"muestra"` y `escena3d.py` avisa si algo no se ve.
- **3D de verdad:** ventana, muebles, árboles y cielo son piezas 3D (Kenney, Quaternius, Poly Haven; todo CC0). Nunca caras ni pelo armados con figuras básicas; los accesorios (coletas, lazo) sí, y se dicen.
- **Apropiado para quien lo vea:** no usar skins de zombis, soldados o con calaveras en cuentos infantiles (se pueden quitar con `personalizar_piel.py`). Para niños, además `video-infantil`.
- Personajes **inventados**; nada de personas reales ni de niños reales. Nada que gaste créditos sin el «sí» de Jeiler.
- Claude no oye ni ve el movimiento: mira cuadros y mide.

## Proceso (con compuertas)
1. **Historia y mundo** (`plan-de-video`): idea en una frase; **ficha del mundo**: lugar, época, clima, momento del día, tono (alegre, elegante, de misterio...), nivel de formalidad y paleta de colores; **lista de lo que debe verse** (lugares y objetos que nombra el cuento); tomas con narración y diálogo. Solo después se piensa en quién la cuenta. → *Jeiler aprueba la historia.*
2. **Personajes a partir de la historia:** para cada uno, quién es en el cuento (edad, oficio, carácter) y **qué ropa, peinado y accesorios le corresponden en ese mundo** (ej.: un baile elegante pide trajes y vestidos; un día de lluvia en casa, ropa cómoda). Elegir modelo y paquete (`video-3d`), personalizar la piel (`personalizar_piel.py`: pelo, ropa, quitar dibujos) y accesorios (`accesorios` en el JSON: `coletas`, `lazo`). Si ningún modelo da el vestuario que la historia pide, se dice y se buscan otros (`recursos-3d`) antes de forzar uno que no encaja. Escribir la ficha (`personajes-consistentes`).
3. **Hoja de personajes:** `escena3d.py historia.json carpeta --hoja` deja `hoja_<personaje>.png` (frente, perfil, espalda, rostro y rostro de perfil). Revisar: pelo completo por todos lados, cara limpia, manos, proporciones, que se distingan entre sí. → *Jeiler aprueba.*
4. **Escenario:** armar el cuarto (`cuarto`, `piezas`, `exterior`: pasto, árboles, flores, lluvia, arcoíris, `cielos` reales con `descargar_cielo.py`). Imágenes fijas de cada lugar.
5. **Plan y tomas de prueba:** `python3 scripts/crear_historia3d.py historia.json carpeta --solo-voces` (hace las voces y dice cuánto dura cada frase y cada toma), luego `--solo-plan` (revisa encuadres y que todo lo que dice el cuento se vea, **sin dibujar**) y `--solo-fijas` (una imagen por toma). Revisar encuadre (personajes de cuerpo completo salvo `"plano": "medio"`, ventana visible), luz y que no haya avisos. Animaciones: las de Kenney (`idle`, `correr`, `saltar`) y las de Quaternius con la forma `ual1:Walk_Loop` / `ual2:Yes` (caminar, hablar, sentarse, bailar, asentir...). Quien habla usa `ual1:Idle_Talking_Loop` solo (se desactiva con `"anim_habla": false`, por ejemplo en un salto de alegría).
6. **Video:** `python3 scripts/crear_historia3d.py historia.json carpeta` (voz por personaje, dibujo, música, subtítulos y revisión; si se corta, se vuelve a correr y **no repite los cuadros ya dibujados**). Tiempo medido: **12,5 s por cuadro a 854x480 con 12 muestras y 12 cuadros de dibujo por segundo** (después se duplican a 24); un cuento de 32 s tardó **81 minutos**. Avisar a Jeiler antes de empezar. Para cambiar solo una toma, borrar su carpeta en `render/tomas/` y volver a correr.
7. **Voz, música y subtítulos:** los hace `crear_historia3d.py` (voces `em_santa` narrador, `ef_dora` y `em_alex` para personajes; música calmada original; subtítulos con los diálogos entre comillas). Revisión con `video-editar-jeiler` (`check.py`); si es infantil, `video-infantil` (`revisar_infantil.py`).
8. **Revisión final:** `check.py`, hoja de cuadros, coherencia cuento-imagen, y Jeiler lo ve y lo escucha.

## Formato del JSON (resumen; ejemplo completo en `video-3d/ejemplo-historia/historia.json`)
- `mundo` (lugar, clima, tono, formalidad, por qué esa ropa: es la ficha de la historia; no la usa el programa, la lee la persona).
- `voces` {narrador, y un nombre por personaje: `voz`, `velocidad`} · `musica` {animo, tono, lufs}.
- `reparto` (por personaje: `paquete`, `piel`, `altura`, `accesorios`) · `escenario`: `cuarto` {ancho, largo, `pared`, `ventana_x`, `luz_interior`, `techo`}, `piezas` [{pieza, x, y, giro, esc}], `exterior` {`arboles`, `flores`, `cielos`, `arcoiris_x`, `arcoiris_y`}.
- `tomas`: `id`, `cielo` (o `{de, a, en, dura}` para pasar de lluvia a arcoíris), `muestra` (lo que el cuento dice que se ve), `lineas` [{quien, texto}], `pausa_inicio`, `cola`, `plano` ("medio" si se corta a propósito), `anim_habla`, `camara` {pos, mira, lente, hasta}, `personajes` {pos, hasta, mira_a, cabeza_a, anim, vel, salto_m, gestos}.
- Gestos: `asiente`, `niega`, `habla`, `preocupado`, `saluda`, `alegria`, `senala`. Medidas en metros; el cuarto: x a lo ancho, y hacia la pared del fondo (con la ventana), z hacia arriba.

## Señales de alerta
- Elegir o crear personajes antes de tener la historia y su mundo.
- Personajes con ropa que no encaja con el cuento (por ejemplo, ropa deportiva en una historia elegante).
- Empezar a animar sin hoja de personajes aprobada.
- Dos personajes que solo cambian de color de camiseta.
- Un cuento que nombra algo que no hay en la escena.
- Prometer el video antes de medir cuánto tarda el dibujo.

## Verificación
- [ ] La historia y su mundo (ficha) estaban aprobados antes de crear los personajes.
- [ ] El vestuario de cada personaje encaja con el lugar, la época, el clima y el tono de la historia.
- [ ] Hoja de personajes aprobada por Jeiler (frente, perfil, espalda, rostro).
- [ ] `escena3d.py` sin avisos de «no se ve dentro del cuadro».
- [ ] Imagen fija de cada toma revisada.
- [ ] El texto del cuento coincide con lo que se ve.
- [ ] Se dijo qué no se pudo comprobar (movimiento, oído).

## Qué se probó (2026-11-05)
Con la historia de ejemplo «Lila y el arcoíris» (siete tomas, **sin renderizar el video**): `escena3d.py` armó un cuarto con ventana 3D, mesa, lámpara, planta, exterior con árboles, lluvia y cielo real; la hoja de personajes salió automática (Lila con coletas y lazos rosados, Tito con pelo corto, pelo completo de frente, perfil y espalda); el revisor de `muestra` encontró dos tomas mal encuadradas; las animaciones de Kenney y de las dos bibliotecas de Quaternius (hablar, caminar, bailar, sentarse, asentir, brazos cruzados) se vieron bien en imágenes fijas. **Errores encontrados y corregidos:** los brazos salían abiertos (las animaciones parten de otra pose: ahora se copia la dirección de cada hueso), accesorios gigantes por un error de escala, pared gris, arcoíris aplastado. **No se probó:** el video completo, el movimiento, voces y música, subtítulos, gestos de saludar y señalar en movimiento, tomas con sillas donde sentarse, labios sincronizados (las caras de Kenney son dibujos fijos), otros personajes. **Pendiente:** el orquestador `crear_historia3d.py`, el arcoíris en la toma 5 y afinar la luz (ver `docs/PAUSA-historia-3d.md`).
