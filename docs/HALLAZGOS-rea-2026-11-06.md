# Hallazgos de la investigación con REA — crear (2026-11-06)

**Resultado corto:** REA no hizo falta. Para cada vacío ya existía una herramienta libre, así que se probó esa y REA queda de reserva. Todo se probó en la nube de Claude, con audio inventado; nada se instaló en computadores de Jeiler.

| # | Vacío | Herramienta | Licencia | Resultado |
| --- | --- | --- | --- | --- |
| 1 | Boca que habla (2D) | `lip-sync-engine@1.0.3` (Rhubarb compilado a WebAssembly, 9 formas de boca) | MIT | **FUNCIONA, pero en español sale floja** |
| 2 | Estilos 2D más marcados | `p5.brush@3.0.0` (acuarela, rayado, lápiz) | MIT | **FUNCIONA**: acuarela y rayado, mismo resultado en 2 corridas |
| 3 | Textos animados y transiciones | Ya existe en `animacion-2d` | propia | Cubierto; no hace falta herramienta nueva |
| 4 | Animaciones Lottie | Archivos de LottieFiles | Lottie Simple License | Licencia clara; **sin probar** un archivo real |

## 1. Boca que habla
- Instalado con `npm install --ignore-scripts`; corre en un Chromium sin pantalla (su código pide navegador; no se probó en Node). Por defecto baja sus archivos de `unpkg.com`; se le pasaron rutas locales para no depender de internet. Los modelos pesan unos 38 MB.
- Mismo audio dos veces = mismas formas de boca (probado).
- **Problema:** usa reconocimiento de voz en inglés y no tiene opción de idioma. En español marca las palabras como «desconocidas» y adivina cómo suenan con reglas del inglés. Con una frase de 2,9 s en cada idioma, la boca siguió la voz con correlación 0,17 en español (0,00 sin darle el texto) contra 0,51 en inglés. Es **una sola muestra por idioma**, con voz sintética: indica la tendencia, no es una medida firme.
- Sin probar: verla en movimiento sobre un personaje; voces humanas; la alternativa `wawa-lipsync` (MIT, tiempo real con Web Audio; su página no dice si sirve sin conexión ni si es independiente del idioma).
- Idea para decidir con Jeiler: una boca que siga solo el **volumen** de la voz (abre más cuando suena más fuerte) no depende del idioma. No está escrita ni probada.

## 2. Estilos 2D
- `p5.brush` en versión independiente (sin p5.js) necesita WebGL2: funcionó en Chromium sin pantalla con el renderizador por software. Una escena de prueba (papel, sol en acuarela, colina, rayado) tardó unos 5 s con todo y arranque del navegador.
- Mismo número de semilla = imagen idéntica byte a byte en dos navegadores nuevos.
- Se ve claramente más a acuarela que los filtros SVG actuales. El trazo de lápiz casi no se ve en la prueba.
- Sin probar: animación cuadro a cuadro (tiempo por cuadro, si el trazo «tiembla» entre cuadros); estilo recorte de papel (no se encontró librería libre para ese).
- El origen de coordenadas está en el centro del lienzo, no en una esquina.

## 3. Textos animados y transiciones
Ya cubierto en este repo por `animacion-2d` (transiciones, tarjetas de texto, subtítulos). Descartado `ffmpeg-concat` (transiciones OpenGL): su repositorio está archivado desde julio de 2026.

## 4. Lottie
LottieFiles dice que sus animaciones gratis se pueden usar en proyectos comerciales, sin obligación de dar crédito, modificar y redistribuir bajo la misma licencia; no se pueden juntar para armar un servicio competidor. Esa regla es de la página general: **cada archivo se revisa por separado antes de usarlo**.

## Fuentes (páginas abiertas el 2026-11-06)
- [lip-sync-engine, README](https://cdn.jsdelivr.net/npm/lip-sync-engine@1.0.3/README.md)
- [wawa-lipsync en GitHub](https://github.com/wass08/wawa-lipsync)
- [p5.brush en GitHub](https://github.com/acamposuribe/p5.brush)
- [Licencia de animaciones de LottieFiles](https://help.lottiefiles.com/animation-licensing-basics-)
- [mifi/ffmpeg-concat](https://github.com/mifi/ffmpeg-concat)
