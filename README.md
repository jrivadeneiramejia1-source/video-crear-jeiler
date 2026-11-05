# video-crear-jeiler

Skills para **crear videos desde cero**, de todo tipo: explicativos, animaciones 2D, 3D, videos infantiles y clips con IA.
Es la pareja de `video-editar-jeiler` (cortar, limpiar el audio, subtitular, comprimir y publicar) y hermano de `agent-skills-jeiler`, `app-skills-jeiler` y `apk-skills-jeiler`.

Cada carpeta de `skills/` es una skill: un archivo `SKILL.md` con instrucciones para que Claude sepa cuándo y cómo usarla.

## Estado: fases 4, 5 y 6 hechas (crear)
Hay 12 skills: `plan-de-video`, `animacion-2d`, `video-explicativo`, `voz-sintetica`, `musica-y-efectos`, `video-3d`, `personajes-consistentes`, `video-infantil`, `clips-ia` (**sin probar**), `estudiar-video-referencia`, `historia-3d` (piezas probadas; **video completo en pausa**) y `recursos-3d`. El orden y los grupos están en `INDICE-DE-SKILLS.md`. Lo probado y lo no probado: `PRUEBAS.md`.

**¿Quieres pedir un video?** Lee `COMO-PEDIR-UN-VIDEO.md` (qué decirme y en qué orden trabajo).

## Cómo usarlas (cuando haya skills)
Una skill solo funciona si está en la carpeta de skills de Claude (`~/.claude/skills/`). El instalador copia por grupos:

```bash
./instalar.sh --lista        # ver los grupos
./instalar.sh explicativo    # plan, animación 2D, voz, música y explicativos
./instalar.sh 3d             # personajes 3D (Blender) con personajes consistentes
./instalar.sh infantil       # explicativo + reglas y revisión para videos de niños
./instalar.sh referencia     # sacar la receta de estilo de un video que te gustó
./instalar.sh historia3d     # historias en 3D: personajes, escenario, tomas y recursos
```
**En sesiones en la nube** se instalan solos los grupos de `grupos-activos.txt`, con un hook de inicio en `.claude/`; solo funciona si este repo está cargado como repo de la sesión. El instalador no pisa una skill que ya exista con el mismo nombre y que no haya instalado él. Mejor pocos grupos a la vez: cada skill agrega su descripción al contexto y eso gasta tokens.

## Reglas
- Repo **público**: nunca datos de personas (ver `SEGURIDAD.md` y `CLAUDE.md`).
- Nada gasta créditos (Higgsfield, Canva, ElevenLabs) sin permiso y estimación del costo.
- Licencia MIT para lo original (`LICENSE`); lo de terceros, con su licencia en `third-party/` y su origen en `FUENTES.md`.
- Qué está probado de verdad y qué no: `PRUEBAS.md`.
