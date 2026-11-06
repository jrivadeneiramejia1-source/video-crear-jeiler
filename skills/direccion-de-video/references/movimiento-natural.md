# Movimiento natural de personajes

**[F]** = fuente abierta citada en `fuentes.md`; **[P]** = regla práctica (punto de partida).

## Caminar
- Un ciclo de caminata se arma con cuatro poses clave: **contacto, abajo, paso (passing) y arriba**; además de las piernas se mueven brazos, cadera, tronco y cabeza juntos **[F: Wikipedia, «Walk cycle»]**.
- En una marcha madura, cada pierna pasa alrededor de **60 % del ciclo apoyada y 40 % en el aire** **[F: Wikipedia, «Gait (human)»]**. Por eso un pie apoyado no debe moverse respecto al suelo.
- Los brazos van **contrarios a las piernas** (pierna derecha adelante, brazo izquierdo adelante) **[P]**; al ir más rápido el balanceo cambia **[F: «Gait (human)» menciona que cambia con la velocidad]**.
- **En el motor (`escenas-web3d`):**
  - `ir_a` calcula el tiempo del ciclo por los **metros recorridos / metros por segundo naturales** de esa animación (medidos con los huesos de los pies): sin patinar ni al arrancar ni al frenar.
  - Arranca con aceleración (`arranque`, 0,45 s) y frena (`frenado`, 0,55 s); `0` los desactiva. Medido: 0 → 0,68 m/s en 0,45 s; pie apoyado a 5–14 % de la velocidad del cuerpo.
  - Sin `b`, la duración sale de la velocidad natural. Con `b`, avisa si los pasos quedan muy apurados o lentos (< 0,6 o > 1,6 veces lo natural).
  - Personajes KayKit caminan natural a ≈ 0,5–0,7 m/s (pasos cortos de muñeco): para ir más rápido, `Running_A` o acercar los puntos; Quaternius «Walk» ≈ 1,0 m/s.

## Giros y miradas
- Girar toma ≈ **0,3–0,4 s** (`giro` = 0,35 s con curva suave) **[P]**. Un giro instantáneo se ve como teletransporte.
- **Los ojos adelantan a la cabeza y la cabeza al cuerpo** **[P]**: si el personaje cambia de dirección, primero mira. Con modelos de cara fija: dar la mirada un instante antes con `mirar` en una acción corta de `Idle`.
- `mirar` hacia el interlocutor al empezar a hablar y al reaccionar: sostiene la **coincidencia de miradas [F]**.

## Inicio y final de una acción (anticipación y asentado)
- Antes de una acción grande, un pequeño movimiento en sentido contrario: **10–20 % del tiempo de la acción** **[F: guía MIT de movimiento, «motion-design-skill»]**; al terminar, un **asentado de 20–30 %** del tiempo y un respiro de 100–200 ms antes de lo siguiente.
- Los clips (`SitDown`, `PickUp`, `Cheer`) ya traen anticipación y asentado: no encimarles otra acción antes de que terminen (`revisar_proyecto.py` y `verificar` avisan; sin `a` empieza al terminar la anterior).
- **Seguimiento y acción superpuesta:** las partes que cuelgan (pelo, capa, bufanda, brazo suelto) se atrasan **50–150 ms** respecto a la parte que las lleva **[F: guía MIT, escala de interfaz; en personajes equivale a 1–4 cuadros]**.

## Curvas y tiempos
- Entrar = **ease-out** (llega suave); salir = **ease-in**; entre dos puntos = **ease-in-out**; **lineal solo para rotación continua o velocidad de crucero** **[F: guía MIT]**. Una salida dura **65–75 %** de lo que dura la entrada **[F]**.
- Peso = tiempo: lo pesado se mueve lento; lo ligero, rápido; tristeza ≥ 600 ms, alegría 200–400 ms, urgencia 100–200 ms **[F: guía MIT, valores de interfaz]**.
- Rebote (`pop`, `[.175,.885,.32,1.275]`): pasarse **10–30 %** del destino para sensación juguetona; 0 % para seriedad **[F]**.
- Un solo foco a la vez: con 3+ elementos animados, que no más de un tercio se mueva al mismo tiempo **[F: guía MIT, «regla de 1/3»]**.

## Cuerpo en reposo
- **Nada congelado [P]:** un personaje quieto debe tener al menos respiración o cambio de peso. `Idle` ya lo trae; si un `Idle` dura más de ~6 s sin `mirar` ni otro gesto, `revisar_proyecto.py` avisa.
- **Evitar el gemelo [P]:** dos personajes que hacen lo mismo a la vez se ven robóticos; desfasar `a` unas décimas (0,1–0,3 s) y usar clips distintos (`Walking_A` y `Walking_B`).
- **Manos [P]:** las manos acompañan lo que se dice; un gesto antes de la palabra clave. Con clips de oficio (`Interact`, `Use_Item`, `Spellcast_Raise`) en vez de dibujar a mano.
- **Proporciones:** personajes de cabeza grande (KayKit, Quaternius) caminan con pasos cortos; el encuadre y la velocidad se adaptan (ya lo hace el motor).

## Síntomas y remedio
| Se ve así | Causa probable | Remedio |
|---|---|---|
| Patina | cadencia no ligada al avance | `ir_a` sin `b`; no cambiar `vel` sin mirar |
| Camina en cámara rápida | `b` muy corto para esa animación | dar más tiempo o usar `Running` |
| Se detiene de golpe | `frenado` en 0 o acción que corta | dejar `frenado` ≥ 0,4 |
| Salta de pose | acciones superpuestas o `mezcla` muy corta | `mezcla` 0,3 s; sin `a` para encadenar |
| Se congela tras un ciclo | (corregido) ciclo de animación | actualizar el motor |
| Mira a otro lado | `frente` mal puesto | probar `"frente": 3.1416` |
| Entra por la pared | punto `ir_a` mal puesto | ver `hoja` desde arriba (`angulo: 80`) |
