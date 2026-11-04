# video-crear-jeiler

Skills para **crear videos desde cero**, de todo tipo: explicativos, animaciones 2D, 3D, videos infantiles y clips con IA.
Es la pareja de `video-editar-jeiler` (cortar, limpiar el audio, subtitular, comprimir y publicar) y hermano de `agent-skills-jeiler`, `app-skills-jeiler` y `apk-skills-jeiler`.

Cada carpeta de `skills/` es una skill: un archivo `SKILL.md` con instrucciones para que Claude sepa cuándo y cómo usarla.

## Estado: base lista, skills en camino
Por ahora el repo tiene solo la base (instalador, hook de inicio, licencia, reglas de privacidad). Las skills llegan por fases; el orden está en `INDICE-DE-SKILLS.md`.

## Cómo usarlas (cuando haya skills)
Una skill solo funciona si está en la carpeta de skills de Claude (`~/.claude/skills/`). El instalador copia por grupos:

```bash
./instalar.sh --lista        # ver los grupos
./instalar.sh plan voz       # instalar esos grupos
```
**En sesiones en la nube** se instalan solos los grupos de `grupos-activos.txt`, con un hook de inicio en `.claude/`; solo funciona si este repo está cargado como repo de la sesión. El instalador no pisa una skill que ya exista con el mismo nombre y que no haya instalado él. Mejor pocos grupos a la vez: cada skill agrega su descripción al contexto y eso gasta tokens.

## Reglas
- Repo **público**: nunca datos de personas (ver `SEGURIDAD.md` y `CLAUDE.md`).
- Nada gasta créditos (Higgsfield, Canva, ElevenLabs) sin permiso y estimación del costo.
- Licencia MIT para lo original (`LICENSE`); lo de terceros, con su licencia en `third-party/` y su origen en `FUENTES.md`.
- Qué está probado de verdad y qué no: `PRUEBAS.md`.
