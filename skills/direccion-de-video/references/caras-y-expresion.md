# Caras y expresión

**[F]** fuente abierta citada; **[P]** regla práctica; **[E]** hecho en este repositorio y medido.

## Qué cuenta una cara
- **Los ojos y las cejas llevan la emoción**; la boca la acompaña **[P]**. Cejas hacia arriba y adentro = preocupación; hacia arriba y afuera = sorpresa; juntas y bajas = enojo. En `animacion-2d` el parámetro `mood` ya combina ojos, cejas y boca (`smile`, `laugh`, `calm`, `worry`, `surprise`).
- **Parpadeo [P]:** cada 3–6 s, dura 0,1–0,15 s; que no parpadeen a la vez todos los personajes. **[E]** `animacion-2d` parpadea cada 3,7 s durante 0,13 s con desfase por personaje.
- **Mirada:** mirar a quien habla; mirar a un objeto un instante antes de tocarlo; apartar la mirada al dudar **[P]**. En 2D, `mira` desplaza las pupilas.
- **Asimetría [P]:** una ceja un poco más alta o una comisura más arriba evita la cara de muñeco rígido.

## Dibujar una cara de personaje sencillo **[P]**
1. Cabeza como óvalo; los **ojos a la mitad de la altura** de la cabeza (no arriba) y separados cerca de **un ojo de ancho**.
2. Nariz mínima (una curva), **boca a un tercio entre la nariz y el mentón**, mejillas con color suave.
3. Cejas con la misma curva que el pelo del flequillo para que el rostro se vea de una sola familia.
4. Pocas formas, gruesas y limpias: se leen mejor en pantallas pequeñas.
5. Mantener la **misma cara en todas las escenas**: `personajes-consistentes` (hoja, paleta y comparación de colores).

## Boca y habla
- La boca no abre en cada letra sino en cada **sílaba**: unas 3–7 por segundo en español hablado, con abertura distinta en cada una **[P]**. Entre frases queda **cerrada**.
- **[E] Implementado en `animacion-2d`:** cuando un personaje tiene un `dialogo` activo, la boca se abre y cierra por sílabas (cuenta de grupos de vocales del texto, 3–7,5 por segundo, abertura variable y asentimiento leve de cabeza); cerrada antes de empezar (0,12 s) y al terminar (0,2 s). Probado con ocho cuadros del ejemplo: abierta en cuatro, cerrada en cuatro (incluidos los dos posteriores a la frase, que la muestran cerrada).
- **Mejor, sin probar:** formas de boca (visemas) tomadas del audio real. Candidatos abiertos, todos MIT y **sin probar aquí**: `met4citizen/HeadTTS` (Kokoro en navegador con marcas de tiempo y visemas), `OpenFaceFX/OpenFaceFX` (audio + texto → curvas de visemas), `Amoner/lipsync-engine` (sincronía de labios para animación 2D en navegador).

## Caras en modelos 3D hechos
- **KayKit:** cara fija con rasgos (ojos, cejas, nariz), sin animación facial. La emoción la dan postura, clip (`Cheer`, `Hit_A`, `Interact`) y el corte siguiente (**efecto Kuleshov [F]**).
- **Quaternius:** cara negra con ojos blancos (diseño del autor); usar en planos medios y lejanos, nunca en primer plano.
- **Pendiente:** expresiones y boca animada en 3D (VRM con expresiones, o cabezas separadas). Sin probar.

## Cuándo usar 2D y cuándo 3D para una escena de conversación
| Necesito | Mejor |
|---|---|
| Que se vea la boca hablar y las cejas | `animacion-2d` (boca por sílabas + `mood`) |
| Que camine, entre a un cuarto, se siente | `escenas-web3d` |
| Las dos cosas en un video | escenas 3D para movimiento y lugares; cortes a 2D en primeros planos de diálogo |
