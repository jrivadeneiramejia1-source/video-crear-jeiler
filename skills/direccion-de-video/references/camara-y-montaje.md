# Cámara y montaje

Leyenda: **[F]** lo dice una fuente abierta citada en `fuentes.md`; **[P]** regla práctica de oficio (punto de partida, se ajusta mirando).

## Planos y qué cuentan (nombres de `escenas-web3d`)
| `plano` | Muestra | Úsalo para |
|---|---|---|
| `general` | el lugar entero y quién está | ubicar al público al inicio de una escena **[F: plano de establecimiento]** |
| `cuerpo` / `americano` | de pies o rodillas a cabeza | acción, caminar, entrar y salir |
| `medio` | cintura a cabeza | conversación, gestos con las manos |
| `primer-plano` | cabeza | emoción, reacción |
| `detalle` | un objeto o parte de la cara | una pista, un objeto clave |
| `sobre-hombro` | un personaje de espaldas y el otro de frente | diálogo cara a cara |

## Secuencia de una escena **[P]**
General (ubica) → medio/cuerpo (acción) → primer plano (emoción) → volver a abrir al terminar. **No repetir el mismo plano del mismo personaje dos veces seguidas**: se siente salto, no corte. Un establecimiento puede omitirse si el lugar ya es conocido y se quiere ir rápido **[F: hoy se usa menos que antes]**.

## Duración de cada toma **[P]**
| Tipo | Rango | Nota |
|---|---|---|
| general que ubica | 2–5 s | más corta si el público ya conoce el lugar |
| acción (caminar, entrar) | lo que dure la acción | cortar cuando empieza o termina el gesto |
| medio con diálogo | 3–6 s | cambiar al terminar la frase |
| primer plano de reacción | 1,5–3 s | más largo solo si hay emoción que leer |
Menos de ~1,2 s no se alcanza a leer; más de ~8 s sin movimiento aburre. Promedio de una historia infantil: 3–5 s.

## Cortes
- **Cortar en la acción [F]:** cortar cuando alguien empieza un movimiento y continuarlo en la toma siguiente; el movimiento «esconde» el corte y da sensación de tiempo continuo.
- **Coincidencia de miradas [F]:** si un personaje mira fuera de cuadro, la toma siguiente muestra lo que mira; el público asume que es lo que ve. En el motor: `mirar` hacia el otro personaje y la toma siguiente sobre ese personaje.
- **Plano y contraplano:** dos personajes que hablan se muestran alternando, siempre con el primero a un lado y el segundo al otro.
- **Línea de acción (regla de los 180°) [P, bien establecida]:** imaginar la línea que une a los dos personajes y dejar la cámara siempre de un mismo lado; si se cruza, el personaje de la izquierda salta a la derecha y el público se desorienta. En el motor: el plano de dos pone la cámara de lado respecto a esa línea; mantener `lado` del mismo signo (`der` con `der`) en las tomas sobre la misma pareja.
- **Efecto Kuleshov [F]:** el público lee una emoción en un rostro neutro según la imagen que viene después. Con caras fijas (KayKit, Quaternius), la emoción la dan **la toma siguiente y la postura del cuerpo**, no la cara.
- **Transiciones:** corte por defecto; fundido a negro para pasar el tiempo o terminar; nada de efectos de adorno.

## Composición
- **Aire hacia donde se mira o camina [P]:** dejar más espacio delante que detrás del personaje (`punto` a un lado del personaje, o `altura_mira`).
- **Cabeza con aire [P]:** sin cortar la cabeza por arriba; un poco de aire por encima.
- **Tercios [P]:** el rostro o el punto de interés en una línea de tercios, no en el centro, salvo para solemnidad.
- **Cámara a la altura de los ojos** como base; `picado` (desde arriba) hace pequeño al personaje; `contrapicado` (desde abajo) lo hace grande **[P]**.
- **Movimiento de cámara con motivo:** `empuja` lento hacia un personaje cuando algo importa; `orbita` solo para revelar.

## Video vertical (Shorts/Reels) **[P]**
- Planos más cerrados (se ve en pantalla pequeña) y un solo foco por toma.
- Subtítulos arriba de la zona del dedo (margen inferior ≈ 17 %, ya aplicado en `animacion-2d`).
- Cortes algo más seguidos; el primer segundo ya tiene que mostrar algo (miniatura).
- Probar siempre el mismo proyecto en 720×1280: el motor conserva el ancho de visión, pero cambia la altura que cabe.

## Lo que mide `revisar_proyecto.py`
Primer plano distinto de general/cuerpo al empezar, planos repetidos seguidos, tomas de menos de 1,2 s o más de 8 s, variedad de planos, línea de acción en parejas, subtítulos largos o rápidos.
