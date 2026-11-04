# Revisión de seguridad

Base creada el 2026-11-04. Todavía no hay skills de terceros en este repo.

## Cómo se revisa cada cosa antes de agregarla
1. **Licencia** primero (ver `third-party/LEEME.md`): MIT, Apache-2.0, BSD, CC0 o Unlicense se pueden copiar; GPL o AGPL, solo ideas; sin licencia, solo enlazar.
2. **Leer el `SKILL.md` completo y sus scripts.** Buscar comandos de riesgo: descargar y ejecutar a la vez (`curl ... | sh`), `eval`, `rm -rf /`, `base64 -d`, `nc -e`, `sudo`.
3. **gitleaks** (busca claves y tokens escritos en archivos) sobre los archivos y el historial.
4. Instalar dependencias con `--ignore-scripts` y sin ejecutar binarios descargados.
5. **No se usa `snyk/agent-scan`:** pide cuenta y token de Snyk y sube el contenido de las skills a su servicio. Queda a decisión de Jeiler.

## Privacidad (el repo es público)
- No se suben nombres de estudiantes, voces, caras, audios ni capturas de videos reales. Los ejemplos usan personajes y textos inventados.
- `.gitignore` bloquea audios, videos y las carpetas `entregas/` y `privado/` como red de seguridad, pero no reemplaza la revisión a mano antes de cada commit.
- Archivos de comunidades indígenas: no se modifican ni se suben a servicios externos.

## Resultado
- Sin skills todavía: nada que revisar. Cada fase anota aquí qué se revisó y qué se encontró.
