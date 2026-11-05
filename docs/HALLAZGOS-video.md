# Hallazgos para video (búsqueda con Sonnet, 2026-11-04)
Material para que Opus haga el plan. No se instaló ni se subió nada.

## 0. Qué tan confiable es esto
- **Verificado por mí:** licencias, fechas y estrellas de los repos (API de GitHub); el contenido de tus skills; el estado de tus conectores.
- **NO verificado:** precios y cupos gratis (solo blogs y resúmenes de búsqueda; no pude abrir páginas oficiales) y la calidad real de cada herramienta (no instalé ni corrí nada).
- Las estrellas de GitHub no garantizan calidad ni seguridad. La lista «awesome» que usé la hace un sitio comercial que además califica la seguridad de los repos: no me fío de esa nota.

## 1. Lo que ya tienes (y lo que falta)
| Qué | Estado | Nota |
|---|---|---|
| `cortometrajes-educativos` (tu skill) | Funciona, 4 videos hechos | Dibuja 2D con código (SVG + Playwright + ffmpeg), voz real de la persona limpiada con sherpa-onnx, subtítulos alineados y verificación con medidas. Es lo más difícil y ya está resuelto. |
| `buscar-herramientas-video` (tu skill) | Funciona | Sin 3D (lo rechazaste). Menú de estilos A–E. Manim y DeepFilterNet fallaron en la nube. |
| `youtube-agent-skill` (tu fork, MIT) | **Sin instalar** | 11 skills: guion con ganchos, título y miniatura, retención, Shorts desde un video largo, SEO, capítulos. Cubre publicar, que hoy no tienes. |
| Plugin `animation-studio` (en tu directorio) | Sin instalar | Cortos dibujados a mano en código, música sintetizada, 1080p y vertical 9:16. Es casi tu estilo. |
| Plugins `Video Cleanup`, `AudioPod` | Sin instalar / pide cuenta | Limpieza de audio y video (ffmpeg), transcribir, separar voces. Tu cadena local ya hace parte de esto gratis. |
| Conectores | Canva ✔ conectado · Higgsfield ✔ conectado (gasta créditos) · ElevenLabs y Riverside a medio conectar | Higgsfield solo con tu permiso expreso (tu regla). |

**Huecos que tú no mencionaste:** música y efectos de sonido; voz sintética para cuando la persona no pueda grabar; formato vertical (TikTok/Shorts) además del horizontal; miniaturas y títulos; publicación; subtítulos en otros idiomas; clips de IA (más realistas); fotos o video de archivo libres; repetir el estilo de un video que te gusta (tu video de flores).

## 2. Mapa por etapas y candidatos
Costo: **G** gratis, **C** créditos/pago, **GPU** necesita tarjeta gráfica (tu sesión en la nube no tiene; tú no tienes computador propio).

| Etapa | Candidatos (licencia) | Mi lectura |
|---|---|---|
| Guion | `jtydhr88/screenwriting-skills` (MIT, 2k★); tu propia sección «Escribir el guion» | Lo tuyo ya es específico y bueno. Esta es opcional, para narrativa. |
| Dibujo 2D en código | Tu motor; `buildwithhanif/claude-animation-skill` (MIT), `kelano86/what-if-animation` (MIT, corre con modelo gratis), `JohnHeibel/ClaudeAnimationBase` (p5.js), `animation-studio` | Ideas para estilos nuevos sin salir de tu método. Todas G. |
| Marco de video en código | **Remotion** (React; licencia propia: gratis para individuos y organizaciones de hasta 3 personas), **HyperFrames** de HeyGen (Apache-2.0, 79k★, tardó 23,5 min en una prueba de 15 s), Motion Canvas (MIT) | Remotion sirve; la licencia pide pago si la usas dentro de una empresa de más de 3 personas. Tu motor actual ya cumple; esto es para ampliar. |
| Clips de IA | Kling (créditos diarios, clips de ~5 s), Runway (125 créditos una sola vez), Luma (~30 al mes), Pika, Dreamina, Veo 3.1 en la app de Gemini (cupo diario) | **C.** Los cupos gratis cambian y los blogs se contradicen. Veo por API **no** tiene nivel gratis. Sirve para «lo que no se puede dibujar», no para lo central. |
| Modelos abiertos de video | Wan 2.2/2.5, LTX-2 (Apache-2.0), HunyuanVideo 1.5 | **GPU:** de unos 8 GB (Wan 1.3B) a 54 GB (Wan 14B completo). Colab/Kaggle gratis darían ~15–30 h por semana, sin garantía. No encaja con tu situación hoy. |
| Voz sintética | Kokoro (Apache-2.0, español, sin clonar), Piper (MIT, sin conexión), Chatterbox (MIT, clona voz), CosyVoice2 (Apache-2.0); en Cloudflare Workers AI: Deepgram Aura-2 en español y MeloTTS | G (Cloudflare: 10.000 Neurons al día gratis). **Clonar la voz de alguien exige su permiso escrito.** XTTS y F5-TTS parecen de uso no comercial (de memoria; verificar). |
| Reconocer voz y subtítulos | Lo que ya usas (Parakeet, sherpa-onnx); Whisper (Workers AI: large-v3-turbo) | Ya resuelto. |
| Música y sonido | Pixabay y Pexels (licencia libre, piden clave gratis), Freesound, Archive.org, NASA; MusicGen/ACE-Step (necesitan GPU) | Pixabay no deja revender el archivo suelto; Pexels tampoco. Revisar cada licencia. |
| Montaje y retoques | `kajisho5/ffmpeg-skill` (MIT, 4,5k★, 42 herramientas de ffmpeg y servidor MCP), Video Cleanup | Útil para recortar, unir, convertir a vertical, quemar subtítulos. |
| Repetir el estilo de un video | `edenfunf/reelmimic` (MIT; usa yt-dlp; Node 22.18+ y Python 3.10+) | Es justo tu video de flores: copia el **estilo**, no el contenido. Hay que mirarlo antes. |
| Publicar y crecer | `youtube-agent-skill` (tu fork); Riverside (conector) | Tú subes; ninguna debe publicar sola. |
| Renderizar sin computador | Tu sesión en la nube (ya lo haces) y GitHub Actions: gratis en repos públicos con servidores estándar (privados gastan tu cupo de US$12) | Sirve para videos largos o pruebas repetidas. |

## 3. Qué NO conviene (y por qué)
- **OpenMontage entero** (`calesthio`, 76k★): licencia **AGPL-3.0** (te obliga a abrir el código si lo ofreces como servicio), 164 MB, 700+ skills, 82 archivos que lanzan programas, y casi todo lo bueno pide APIs de pago. Sirve para **copiar ideas** (etapas con aprobación del usuario), no para instalar.
- **Instalar las 419 skills de la lista:** un test de ese mismo sitio dio que Claude Code **sin ninguna skill** hizo un video que pasó los 4 controles en 4,4 min. Las skills aportan estilo, flujo o material, no magia. Mejor reforzar tu kit con 3 a 5 piezas.
- **AI Video Enhancer Studio:** solo Windows y tarjeta NVIDIA.
- **3D:** lo rechazaste.
- **Modelos abiertos de video:** sin GPU no hay forma razonable hoy.

## 4. Riesgos y reglas
- **Etiquetas de IA:** según resúmenes de prensa, YouTube desde mayo de 2026 marca solo los videos con IA fotorrealista que no se declaren; lo animado o irreal va en la descripción; guion y subtítulos con IA no se declaran. TikTok exige etiquetar IA realista. **Verificar en las páginas oficiales.** Tus créditos ya dicen «hecha con apoyo de IA»: buen hábito.
- **Personas reales:** voz o cara de alguien, solo con su permiso; los cortos son para conocidos de la universidad.
- **Archivos de comunidades indígenas:** irreemplazables; no se modifican ni se suben a servicios externos (ElevenLabs, AudioPod, clips de IA).
- **Wayuunaiki:** hay un modelo pequeño de reconocimiento (Whisper-small, ~1,7 h de audio de la Biblia) y traducción en investigación; **no encontré voz sintética**. No prometer nada.
- **Copiar videos ajenos:** solo el estilo; descargar con yt-dlp puede ir contra los términos de la plataforma.
- **Seguridad de skills de terceros:** leer sus scripts; instalar con `--ignore-scripts`; nada de binarios descargados (tu regla).

## 5. Decisiones que el plan necesita de ti
1. ¿Seguimos con el **2D dibujado en código** (tu estilo) o también quieres probar **clips de IA** (más realistas, pero con créditos)?
2. **Presupuesto:** ¿solo gratis, o hasta cuánto al mes?
3. **Voz:** ¿siempre la grabada por la persona, o también voz sintética cuando no pueda grabar (con su permiso)?
4. **Idiomas:** ¿solo español? (la pregunta de wayuunaiki sigue sin respuesta).
5. **Dónde se publica:** YouTube, TikTok, WhatsApp… ¿y también vertical?
6. **Tu video de flores de TikTok:** ¿lo incluimos en el plan como primer caso de «repetir el estilo»?
7. **Dónde viven las skills:** ¿un cuarto repo `video-skills-jeiler` (como los otros tres)?

## 6. Qué se le pide a Opus
Un plan por fases, igual que el de los otros repos: qué agregar, qué escribir original, qué descartar, orden y tamaño, cómo probar cada skill en una tarea real, y qué verificar al final. Con criterio propio: que corrija o amplíe este mapa si ve huecos.
