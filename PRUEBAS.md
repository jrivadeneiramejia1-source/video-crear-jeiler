# Qué se probó de verdad
Las pruebas de la fase 4 (2026-11-04) usaron proyectos y textos **inventados**. Cada fase agrega aquí una fila por skill con: estado, qué se probó y qué no.

| Skill | Estado | Qué se probó |
|---|---|---|
| **plan-de-video** | Probada en parte | `medir_guion.py` midió el guion del explicativo de prueba y marcó cuatro problemas en un guion malo a propósito. La plantilla se usó una vez. Falta usarla con un pedido real. |
| **animacion-2d** | Probada con un ejemplo inventado | Cuento de 20 s en horizontal y vertical sin errores; hoja de cuadros mirada; globos de diálogo corregidos en vertical. Sin probar: más de 3 personajes, escenas largas, otros computadores. |
| **voz-sintetica** | Probada | Instalador real; 115 palabras entendidas al 98,3 % por un reconocedor; tres voces de español; tiempos por frase. Sin oyentes: la naturalidad la decide Jeiler. |
| **musica-y-efectos** | Probada solo con medidas | Cuatro ánimos de 30 s (pico -6,0 dBFS; -17,7 a -20,3 LUFS) y seis efectos; espectrograma revisado. Nadie la ha escuchado. |
| **video-explicativo** | Probada con un ejemplo inventado | Video de 58,57 s en horizontal y vertical: `check.py` sin FAIL para YouTube y Shorts; subtítulos 100 % iguales a la voz re-transcrita (desfase medio 0,07 s). Seis errores de diseño y audio encontrados al mirar y corregidos. Sin probar: `--hd` completo, imágenes de marcas, `barras`, guiones largos, oyentes. |
