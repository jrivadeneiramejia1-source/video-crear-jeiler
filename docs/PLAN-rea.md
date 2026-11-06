# Plan: investigar con REA (ingeniería inversa) herramientas para crear video

Hecho el 2026-11-06. Plan completo y vivo en el documento de Claude; esta es la copia para el repo.
Decisiones de Jeiler: investigar los **cinco vacíos** en el orden de la tabla; apps (APK/Electron) **solo con su permiso por cada app**; este plan también va en los repos (rama + PR, nunca `main` directo).

## Objetivo
Usar REA solo donde haga falta: descubrir **cómo** otras páginas públicas logran un efecto de video que este repo no tiene, y con esa «receta» buscar una herramienta **libre** que haga lo mismo. REA no entrega herramientas, entrega la receta. Primero se busca si la herramienta libre ya existe; REA entra solo si no aparece nada.

## Qué es REA y qué parte sirve
REA (`morluto/rea`, paquete npm `rea-agents`, licencia MIT) es un servidor MCP que mira por dentro páginas web y apps. Para video sirve sobre todo el módulo de **páginas web** (se conecta a un Chrome por CDP y lista scripts, recursos y red). Secundarios: JavaScript/Electron y WASM. Solo con permiso: APK de Android. No se usan: binarios nativos, Frida, firmware, EVM.

**Probado (fase 0, 2026-11-06):** `rea-agents@6.8.0` se instala en la nube con `--ignore-scripts` y se conecta a un Chromium sin pantalla; lista los scripts de una página con su tamaño y huella. **No** dice por sí solo «esta página usa la librería X»: eso se saca leyendo el código capturado (`--include-script-sources`). Sin probar: páginas públicas reales y el módulo de apps.

## Vacíos de este repo (crear)
| # | Vacío | Por qué falta | Qué mirar con REA | Estado |
| --- | --- | --- | --- | --- |
| 1 | Boca que se mueve con la voz (lip sync) en 2D | Rhubarb se descartó (programa compilado) | Páginas públicas de avatares que hablan en el navegador: qué librería JS o WASM usan | Confirmado |
| 2 | Estilos 2D más marcados (recorte, acuarela, cuaderno) | Los filtros actuales son suaves | Demos web con esos estilos: qué efectos o shaders usan | Confirmado |
| 3 | Textos animados y transiciones tipo editor web | Solo está en el plan, sin skill | Editores de video en línea: qué librería animan | Por confirmar |
| 4 | Animaciones Lottie descargadas | Falta probar y revisar la licencia de cada archivo | Sitios de animaciones gratis: formato y licencia real | Por confirmar |

## Reglas
**Legales.** Se mira para aprender la técnica, nunca para copiar. No se copia código, arte, plantillas, fuentes, música ni efectos de pago. No se saltan pagos, cuentas, marcas de agua ni protecciones. Antes de cada objetivo se leen sus términos de uso; si prohíben la ingeniería inversa, solo se observa lo público o se descarta. Lo que se integre sigue `SEGURIDAD.md` y `third-party/LEEME.md` (MIT, Apache-2.0, BSD, CC0, Unlicense se copian con su licencia; GPL/AGPL solo ideas; sin licencia solo enlace).

**Seguridad.** REA solo de la fuente oficial. Todo se instala en la nube de Claude, nunca en los computadores de Jeiler, en carpeta nueva, con `--ignore-scripts` y sin ejecutar programas bajados. Si el sistema bloquea algo, no se rodea: se para y se explica. No se analizan videos reales ni archivos de comunidades. Nada se publica sin el «sí» de Jeiler.

## Método por vacío (7 pasos)
1. Pregunta en una línea.
2. Buscar primero lo libre (GitHub, npm, pip): licencia libre, mantenido, sin cuenta ni clave, sin GPU, funciona sin pantalla. Si aparece, saltar al paso 6.
3. Elegir 2 o 3 objetivos públicos y leer sus términos.
4. REA en modo observación: librerías cargadas, archivos WASM, formatos, licencias publicadas.
5. Convertir la receta en candidatos libres.
6. Prueba mínima: el mismo segundo dos veces da el mismo cuadro, 3 imágenes a tamaño completo, segundos por cuadro, textos nítidos.
7. Anotar en `docs/HALLAZGOS-rea-FECHA.md` (FUNCIONA / NO, versión, licencia) y mostrar una hoja de muestras para que Jeiler elija.

## Fases
| Fase | Qué se hace | Entrega | Estado |
| --- | --- | --- | --- |
| 0 | Preparar REA en la nube | REA funciona sí/no | Hecha |
| 1 | Confirmar los vacíos 3 y 4 y buscar primero lo libre | Lista final de vacíos | Pendiente |
| 2 | Páginas web con REA, vacíos 1 a 4 en orden | HALLAZGOS-rea y hoja de muestras | Pendiente |
| 3 | Apps (APK/Electron), solo con permiso por cada app | Candidatos extra | Opcional |
| 4 | Integrar lo que Jeiler elija (rama + PR, licencia en `third-party/`) | PR por repo | Pendiente |

## Fuera de alcance
Binarios nativos, servicios de pago para imitarlos, Higgsfield (gasta créditos) y 3D, salvo que Jeiler lo pida.
