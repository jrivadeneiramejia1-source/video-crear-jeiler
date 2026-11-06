---
name: recursos-3d
description: >-
  Catálogo de dónde conseguir recursos 3D gratis y con licencia libre (personajes, animaciones, muebles, naturaleza, cielos) para los videos de este repo, con qué se pudo bajar de verdad desde la nube, la licencia de cada uno y cómo usarlos. Usar cuando haga falta un personaje, una animación, un mueble, un árbol, un cielo o un fondo que todavía no está, o cuando Jeiler pregunte "de dónde sacamos esto" o "es gratis para usar". Nada se copia al repo (es público); todo se baja a una carpeta local.
---

# Recursos 3D con licencia libre

## Reglas
- **Solo CC0** (o equivalente); se comprueba el archivo `License.txt` al bajar (los scripts lo hacen). Nada con licencia dudosa.
- **Nada se copia al repo** (es público): todo va a `~/.cache/video-jeiler/` (o `$VIDEO_JEILER_MODELOS`).
- **Sin binarios ejecutables de terceros** (regla de Jeiler): solo modelos, texturas y animaciones.
- Se da crédito aunque CC0 no lo exija: «Personajes y muebles de Kenney (kenney.nl), animaciones de Quaternius (quaternius.com), cielos de Poly Haven (polyhaven.com), CC0».

## Lo que se pudo bajar y usar (probado 2026-11-05)
| Recurso | Qué trae | Cómo | Estado |
|---|---|---|---|
| Kenney: Animated Characters 1 y 2, Blocky Characters | personajes con esqueleto; 3 animaciones (los de la serie 1 y 2) o 27 (blocky) | `scripts/descargar_personajes.sh` | Probados 1 y 2; blocky solo descargado |
| Kenney: Furniture Kit | 120 muebles y paredes (con **ventana** `wallWindow`), en OBJ | `scripts/descargar_recursos.sh` | Probado |
| Kenney: Nature Kit | 329 piezas (árboles, flores, rocas...), en OBJ | `scripts/descargar_recursos.sh` | Probado (árboles y flores en la escena) |
| KayKit: Adventurers 1.0 (Knight, Mage, Barbarian, Rogue, Rogue_Hooded) | 5 personajes low-poly en `.glb` con esqueleto, textura y **76 animaciones** cada uno (caminar, correr, saltar, atacar, celebrar...) | `escenas-web3d/scripts/descargar_personajes_kaykit.sh` (git clone; comprueba CC0) | Probado en `escenas-web3d` (Knight y Mage, 2026-11-06) |
| Quaternius: Universal Animation Library 1 y 2 (versión «Standard») | 46 + 43 animaciones: caminar, hablar, sentarse, bailar, asentir (`Yes`), correr, saltar... | `scripts/descargar_recursos.sh`; en la escena: `"anim": "ual1:Walk_Loop"` | Probadas con personajes de Kenney (copiando la dirección de los huesos) |
| Poly Haven: cielos (HDRI) | cielos reales para fondo y luz | `python3 scripts/descargar_cielo.py --listar nublado` / `ID` | Probados (nublado y parcialmente nublado) |

## Lo que se evaluó y NO se integró (por qué)
| Recurso | Licencia | Motivo |
|---|---|---|
| Quaternius: Universal Base Characters | CC0 | La página oficial solo enlaza a itch.io (error 429) y Patreon; no se pudo bajar desde la nube. Si Jeiler los baja a mano, `escena3d.py` los puede usar con otra tabla de huesos. |
| Poly Haven: modelos (521) | CC0 | Se pueden bajar por la API, pero son fotorrealistas y desentonan con el estilo de Kenney; sirven para escenas realistas. |
| MPFB2 (generador de humanos para Blender) | código GPLv3, recursos CC0 | Necesita Blender con extensión y 267 MB de recursos extra; sin probar. Candidato para humanos más realistas. |
| Rhubarb Lip Sync | MIT | Es un programa en C++: bajar el binario va contra la regla de Jeiler y compilarlo exige CMake y otras bibliotecas (sin probar); además las caras de Kenney son dibujos fijos, sin boca animable. |
| Servidores MCP de Blender | varias | Ejecutan código arbitrario dentro de Blender; el repo ya controla Blender con scripts propios y revisables. |
| Kenney.nl, Poly Pizza, itch.io | — | Bloqueados o limitados desde la nube (403/429); se usa OpenGameArt como espejo de Kenney. |

## Cómo agregar un recurso nuevo
1. Confirmar la licencia en la página oficial y en el `License.txt` del archivo.
2. Bajarlo a una carpeta nueva (no al repo) con un script que verifique la licencia.
3. Probarlo en una imagen fija (`escena3d.py --fija`) y mirarla.
4. Anotarlo en esta tabla y en `FUENTES.md` (origen, fecha, licencia) y en `PRUEBAS.md`.

## Señales de alerta
- Copiar archivos de terceros al repo.
- Usar un recurso sin haber visto una imagen suya en la escena.
- Mezclar estilos muy distintos (low-poly de Kenney con fotorrealista) sin querer.

## Verificación
- [ ] La licencia está confirmada y anotada.
- [ ] Nada de terceros entró al repo.
- [ ] El recurso se vio en una imagen fija.
- [ ] Se dio crédito en el video o la descripción.
