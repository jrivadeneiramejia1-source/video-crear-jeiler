# Plan: repos de skills para hacer y editar videos de todo tipo

Hecho con Opus el 2026-11-04, a partir de la búsqueda con Sonnet (`HALLAZGOS-video.md`) y de una segunda búsqueda sobre 3D, edición, voz y contenido infantil.
Lo ejecuta una sesión de **Sonnet**, por fases, con el «sí» de Jeiler en cada decisión marcada con ❓.

**Idea central:** no se trata solo de cortos 2D. Hay que poder **crear** cualquier video (explicativo, infantil, 3D, tutorial, promo, corto animado) y **editar** cualquier video (cortar, limpiar el audio, unir voces, subtitular, poner logos cuando se nombran, comprimir, verificar y preparar para publicar). Por eso propongo **dos repos**: uno para crear y otro para editar.

---

## 0. Por qué el 3D salió mal (y cómo evitarlo)
Lo más probable es que ese video se armara **con figuras hechas desde cero en código** (esferas, cilindros). Así se pueden hacer objetos, pero no caras ni pelo creíbles: eso le cuesta semanas a un artista profesional. No es un fallo de herramienta, es de método.

Hay dos caminos que sí funcionan:
| Camino | Cómo | Ventaja | Costo |
|---|---|---|---|
| **A. IA de video** | Un modelo como Kling, Seedance o Veo (los tienes por Higgsfield) anima un personaje 3D a partir de una imagen aprobada. | Caras, pelo y luz de calidad «de estudio». | Créditos. Clips cortos (5 a 10 s). Menos control fino. |
| **B. Blender con personajes ya hechos** | Personajes 3D profesionales gratis (licencia CC0, como Quaternius o Kenney, o Mixamo de Adobe), animados y renderizados con Blender sin pantalla en la nube. | Gratis, el mismo personaje en todas las escenas, control total. | Lento sin tarjeta gráfica. Se ve más «de videojuego» que «de película». |

**Regla nueva para todo 3D o IA:** primero imágenes fijas grandes de la cara, las manos y el pelo; Jeiler las aprueba; recién ahí se anima. Así no se gastan créditos ni horas en algo que se ve raro.

---

## 1. Reglas para quien ejecute este plan
1. **Una fase por vez.** Al terminar: informe corto y esperar el «sí» de Jeiler.
2. **Nunca a `main` directo.** Rama de trabajo y PR; unir solo si Jeiler lo pide.
3. **Licencias:** MIT, Apache-2.0, BSD, CC0 o Unlicense se pueden copiar (guardando la licencia en `third-party/`). GPL o AGPL: solo ideas. Sin licencia: solo enlazar.
4. **Revisar antes de agregar:** leer el `SKILL.md` completo y sus scripts, pasar `gitleaks`, buscar comandos de riesgo, instalar con `--ignore-scripts` y sin binarios descargados.
5. **Sin nombres repetidos** entre los cinco repos ni con las skills de claude.ai (`cortometrajes-educativos`, `buscar-herramientas-video`).
6. **Nunca pedir ni guardar claves.** Lo que necesite clave queda documentado; la pone Jeiler.
7. **Créditos y pagos:** nada que gaste créditos (Higgsfield, Canva, ElevenLabs) sin el «sí» de Jeiler **y** una estimación previa del costo.
8. **Personas reales:** voz, cara o nombre de alguien solo con su permiso. Nunca clonar una voz sin permiso escrito.
9. **Archivos de comunidades indígenas:** nunca se modifican, nunca se suben a servicios externos.
10. **Nada se publica solo.** Las skills preparan; Jeiler sube.
11. **Datos que cambian** (precios, cupos gratis, reglas de las plataformas): verificar en la página oficial el día de la ejecución, con fecha.
12. **Honestidad:** cada informe dice qué quedó sin probar, y que Claude no puede oír el audio ni ver el video en movimiento (solo mide y mira cuadros).

---

## 2. Decisiones de Jeiler ❓
| # | Pregunta | Recomendación |
|---|---|---|
| D1 | ¿Dos repos nuevos, uno para **crear** y otro para **editar**? | Sí: `video-crear-jeiler` y `video-editar-jeiler` (los nombres los eliges tú). El de editar sirve también para videos que grabes con el teléfono. |
| D2 | ¿Públicos o privados? | **Públicos y sin datos personales:** las pruebas en GitHub Actions son gratis en repos públicos. Los nombres de las estudiantes y sus audios nunca entran. |
| D3 | ¿Cuánto se puede gastar en créditos al mes? | Empezar en **0** y aprobar una sola prueba pequeña (unos US$5 o menos) para comparar el 3D por IA con el de Blender. |
| D4 | 3D: ¿qué camino probar? | **Los dos**, con la misma escena de 5 s; eliges viendo el resultado. |
| D5 | ¿Voz sintética permitida? | Sí, para borradores y narraciones con voces genéricas. Clonar una voz, solo con permiso escrito de esa persona. |
| D6 | ¿Habrá videos para niños que se publiquen? | Tratarlos con reglas extra (sección 4, `video-infantil`) y marcarlos «para niños» en YouTube si van dirigidos a ellos. |
| D7 | Idiomas | Español. Para wayuunaiki no hay voz sintética: solo subtítulos revisados por un hablante nativo. |
| D8 | ¿Instalación automática por grupos (hook de inicio), como en los otros repos? | Sí. |
| D9 | ¿Actualizo tus skills de claude.ai para quitar «nada de 3D»? | Sí. Yo te dejo el texto nuevo y tú lo subes (no las puedo editar desde aquí). |
| D10 | ¿Me pasas el `kit-cortometraje.zip` para meter tu motor 2D (sin los ejemplos con datos reales) en el repo de crear? | Sí, si lo tienes. |

---

## 3. Qué va en cada repo
★ = skill original (nueva, licencia MIT). Las demás son de terceros y se revisan antes (regla 3 y 4).

### Repo A: `video-crear-jeiler` (crear desde cero)
| Grupo | Skills | Para qué |
|---|---|---|
| `plan` | ★**plan-de-video** | Del pedido al guion técnico para **cualquier tipo** de video: escenas, tomas, duración, voz, música, recursos, formato (horizontal, vertical o ambos) y costo estimado. Pregunta el tipo de video y elige el camino. |
| `animacion-2d` | ★**animacion-2d** (tu motor, versión general sin datos personales); `hyperframes` de HeyGen (Apache-2.0); skills oficiales de GSAP (verificar licencia) | Cortos, explicativos y gráficos animados dibujados en código. Gratis y en la nube. |
| `explicativo` | ★**video-explicativo** | Comparaciones y explicaciones con gráficos, logos, texto animado y datos (ej.: «Gemini contra ChatGPT»). Usa `animacion-2d` o `hyperframes`. |
| `personajes` | ★**personajes-consistentes**; skills oficiales de FLUX (`black-forest-labs/skills`, MIT) | Hoja de personaje (rasgos, ropa, colores, vistas) para que sea el mismo en todas las escenas; revisión de caras, manos y pelo. |
| `3d` | ★**video-3d** | Los dos caminos de la sección 0 con plantillas de cámara y luz, lista de personajes CC0 y la revisión «primero fijas». Blender con `bpy` (Python) y Cycles en CPU. |
| `clips-ia` | ★**clips-ia** | Imagen aprobada → clip de video con Kling, Seedance o Veo vía Higgsfield o Canva. Estima el costo, pide el «sí», prueba 5 s primero y marca el video como hecho con IA. |
| `voz` | ★**voz-sintetica** | Voz de narración en español con Kokoro o Piper **por sherpa-onnx** (la librería que tu kit ya usa, sin nada nuevo). Incluye «voz guía» para las muestras de 30 s y revisión de la licencia de cada voz. |
| `musica` | ★**musica-y-efectos** | Música compuesta en código (sin problemas de licencia) o de bibliotecas con licencia clara (Pixabay, Freesound CC0, Kevin MacLeod CC-BY), efectos de sonido y mezcla bajo la voz. |
| `infantil` | ★**video-infantil** | Ritmo, colores, repetición, canciones, nada que asuste, valor educativo real (no «relleno de IA»), personajes consistentes y reglas de YouTube para niños. |
| `referencia` | ★**estudiar-video-referencia** | Toma un video que Jeiler entrega (ej.: el de flores de TikTok) y saca su «receta»: tomas, tiempos, colores, ritmo, música y texto. Copia el estilo, nunca el contenido. Idea de `reelmimic` (MIT). |

Plugins del directorio para probar (no van en el repo): `animation-studio` (cortos dibujados en código con música sintetizada) y `video-shotcraft` (videos de producto con Remotion).

### Repo B: `video-editar-jeiler` (editar y terminar)
| Grupo | Skills | Para qué |
|---|---|---|
| `cortar` | `ffmpeg-skill` (`kajisho5`, MIT, 42 herramientas; revisar su servidor MCP antes); `auto-editor` (Unlicense, quita silencios) | Cortar, unir, acelerar, reencuadrar, quitar silencios. |
| `editar-por-texto` | ★**editar-por-texto** | Editar diciendo qué cambiar: «quita la parte donde digo X», «deja solo hasta aquí». Transcribe con tiempos por palabra y arma la lista de cortes. |
| `graficos-por-palabra` | ★**graficos-por-palabra** | Cuando la voz dice una palabra clave, aparece en ese momento un logo, una imagen o un texto («Gemini» → logo de Gemini). Logos de Simple Icons (CC0), solo para nombrar o comparar, nunca para aparentar apoyo de la marca. |
| `audio` | ★**audio-limpio** (de tu kit: DPDFNet, recorte de saturación, volumen); RNNoise dentro de ffmpeg; Demucs (MIT) para separar voz y música | Quitar ruido, **unir varias voces** al mismo volumen, bajar la música cuando alguien habla y dejar el volumen final para cada plataforma. |
| `subtitulos` | ★**subtitulos** (de tu kit: alineación por palabra) | Subtítulos clásicos o animados palabra por palabra (estilo TikTok), archivos `.srt` y `.vtt`, zonas seguras en vertical y traducción con revisión humana. |
| `exportar` | ★**exportar-para** | Versión para YouTube, Shorts, TikTok, Reels (9:16), WhatsApp (tamaño máximo) o Drive. Comprime sin que se note y lo comprueba con una medida de calidad (VMAF). |
| `mejorar-imagen` | dentro de `exportar-para` y `ffmpeg-skill` | Estabilizar, color, nitidez. Aumentar resolución o fluidez con IA solo con créditos (Higgsfield) o con tarjeta gráfica. |
| `verificar` | ★**verificar-video** | Puerta de calidad antes de entregar: duración, resolución, volumen, picos, cuadros negros o congelados, silencios, subtítulos desfasados, textos fuera de zona segura, tamaño, caras, manos y pelo en 3D o IA, derechos de música, imágenes y logos, y etiqueta de IA. |
| `publicar` | Tu fork `youtube-agent-skill` (MIT, 11 skills: guion con gancho, título y miniatura, Shorts, SEO, capítulos, retención); ★**publicar-video** | Preparar título, descripción con créditos, miniatura, capítulos, etiqueta de IA y marca «para niños». Jeiler sube. |
| `analizar` | plugin `watch-video` (directorio) o fotogramas con ffmpeg y transcripción | Entender un video ajeno o revisar el propio. Lo usa `estudiar-video-referencia`. |

---

## 4. Contenido de las skills originales (mínimo de cada una)
Formato de los otros repos: cuándo usar, reglas, proceso, señales de alerta, verificación y «qué se probó».
- **plan-de-video:** preguntar tipo, público, duración, formatos, voz (real o sintética), presupuesto. Elegir camino (2D, explicativo, 3D Blender, 3D IA, edición de material grabado). Guion técnico por escenas con tiempos. Costo estimado y qué queda sin probar.
- **video-3d:** camino A y B; checklist de fijas (rasgos simétricos, ojos y dientes bien, pelo completo, manos con 5 dedos, sin piezas flotando). Nunca crear caras desde figuras básicas.
- **clips-ia:** prompt con cámara, luz, acción y estilo; primero la imagen; clip de prueba de 5 s; el mismo personaje en todos los clips (misma imagen de referencia); costo por clip antes de pedirlo.
- **voz-sintetica:** español con acento neutro o latino si existe; ritmo de unos 0,52 s por palabra (medido en tu kit); avisar siempre que es voz sintética.
- **musica-y-efectos:** la música nunca tapa la voz; volumen final −16 LUFS (−14 para algunas plataformas, verificar); guardar la licencia de cada pista en los créditos.
- **video-infantil:** sin sustos ni violencia, frases cortas, repetición, colores claros, nada de IA fotorrealista de niños reales, contenido revisado por un adulto, reglas de YouTube para niños.
- **editar-por-texto y graficos-por-palabra:** trabajar siempre en una copia del video; mostrar la lista de cortes o de gráficos antes de renderizar; Jeiler aprueba.
- **verificar-video:** usar `ffprobe`, `ebur128`, `blackdetect`, `freezedetect` y `silencedetect` de ffmpeg, más cuadros a tamaño completo. Informe: probado y bien, falló, no se pudo probar.

---

## 5. Fases (orden y tamaño)
| Fase | Qué | Tamaño | Cómo se prueba |
|---|---|---|---|
| 0 | Decisiones, crear los dos repos vacíos, kit | Pequeño | — |
| 1 | Base de los dos repos: instalador por grupos, hook, licencias, `FUENTES.md`, `SEGURIDAD.md`, `PRUEBAS.md`, `comparar-fuentes.py` (copiados de los otros repos) | Pequeño | Instalar dos veces; gitleaks |
| 2 | **Editar, lo básico:** `audio-limpio`, `subtitulos`, `exportar-para`, `verificar-video`, `ffmpeg-skill`, `auto-editor` | Mediano | Un video de 1 min que grabes tú con el teléfono (tu voz, tu permiso) |
| 3 | **Editar, avanzado:** `editar-por-texto`, `graficos-por-palabra`, `publicar` | Mediano | El ejemplo «Gemini contra ChatGPT» sobre tu grabación |
| 4 | **Crear, lo básico:** `plan-de-video`, `animacion-2d`, `video-explicativo`, `voz-sintetica`, `musica-y-efectos` | Mediano | Un explicativo de 60 s en horizontal y vertical, gratis |
| 5 | **Crear, 3D y personajes:** `personajes-consistentes`, `video-3d` (los dos caminos), `video-infantil` | Grande | La misma escena de 5 s por los dos caminos; un clip infantil de 30 s |
| 6 | **IA y referencia:** `clips-ia`, `estudiar-video-referencia` | Mediano | Tu video de flores (cuando lo mandes); 1 clip de IA con tu «sí» |
| 7 | Pruebas reales y de activación sola; `PRUEBAS.md` | Mediano | Un video completo de cada tipo |
| 8 | Mantener: `comparar-fuentes.py` cada mes; precios, cupos y reglas cada 3 meses | Pequeño | — |

---

## 6. Dónde corre cada cosa
| Dónde | Qué | Costo |
|---|---|---|
| Sesión en la nube (CPU) | ffmpeg, tu motor 2D, HyperFrames o Remotion, Blender en CPU, voz con sherpa-onnx, limpieza de audio, subtítulos, auto-editor | Gratis (tus límites de uso de Claude) |
| GitHub Actions (repo público) | Renders largos o repetidos | Gratis en repos públicos |
| Higgsfield, Canva, ElevenLabs | Clips de IA, imágenes, voces premium, aumentar resolución | Créditos |
| Cloudflare Workers AI (opcional) | Imágenes FLUX, voz, transcripción | 10.000 Neurons al día gratis; necesita tu cuenta y tu token como secreto |
| Tarjeta gráfica (Colab, Kaggle o un PC con NVIDIA) | Modelos abiertos de video, Demucs rápido, aumentar resolución | Gratis con límites inestables; no se usa por ahora |

---

## 7. Qué NO se hará (y por qué)
- **Caras o pelo hechos desde figuras básicas en código:** por eso salió mal el 3D.
- **OpenMontage entero:** licencia AGPL, enorme y casi todo pide APIs de pago. Solo ideas.
- **Modelos abiertos de video (Wan, LTX-2, Hunyuan):** necesitan tarjeta gráfica de 8 a 54 GB.
- **Copiar las skills de Remotion o de Higgsfield de terceros:** no declaran licencia; solo enlazar.
- **Blender MCP** (`mcp-for-blender`, MIT): necesita Blender abierto en un computador; queda anotado para cuando tengas uno.
- **Instalar las 419 skills de la lista:** un test de terceros mostró que Claude sin skills ya hace un video aceptable. Se agregan solo las que aportan algo medible.
- **Publicar automáticamente** en YouTube o TikTok.

---

## 8. Verificar al final (con fecha)
- Licencias: Rhubarb Lip Sync (GitHub no la reconoce), skills oficiales de GSAP, cada voz de Piper y Kokoro, packs de Quaternius y Kenney, términos actuales de Mixamo.
- Que `bpy` (Blender como módulo de Python) se instale en la nube y renderice en CPU (la versión de Python importa).
- Precios y cupos de Higgsfield, Kling, Veo, Canva y ElevenLabs (los blogs se contradicen).
- Reglas de YouTube y TikTok sobre IA y contenido infantil, en sus páginas oficiales.
- Límites de tamaño de WhatsApp y specs de cada plataforma.

## Lo verificado y lo que no
- **Verificado** (API de GitHub, 2026-11-04): licencias de HyperFrames (Apache-2.0), ffmpeg-skill (MIT), auto-editor (Unlicense), Demucs (MIT), Simple Icons (CC0), kokoro-onnx (MIT), Chatterbox (MIT), Piper (MIT), LTX-2 (Apache-2.0), reelmimic (MIT), mcp-for-blender (MIT), youtube-agent-skill (MIT, tu fork); y que OpenMontage es AGPL-3.0 y remotion-dev/skills no declara licencia.
- **Según la documentación de Remotion (por búsqueda):** gratis para personas y organizaciones de hasta 3 personas. **Según el anuncio de Webflow:** GSAP es gratis también para uso comercial.
- **No verificado:** precios, cupos gratis, calidad real de cada herramienta, y si cada cosa corre en la nube. Eso se prueba en las fases 2 a 7.
