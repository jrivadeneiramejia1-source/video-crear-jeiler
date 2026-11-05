# Búsqueda de herramientas para crear videos desde cero (2026-11-05)

Pedido de Jeiler: buscar con empeño todas las skills y herramientas necesarias y completar este repo antes del video de prueba. Se buscó con la búsqueda web (resúmenes, sin leer las páginas oficiales completas: **los datos de licencia vienen de resúmenes y de los archivos `License.txt` bajados**) y se probó lo que se pudo bajar desde la nube.

## Integrado y probado
- **Quaternius Universal Animation Library 1 y 2 (CC0, versión «Standard»):** 46 y 43 animaciones con dos esqueletos distintos; se aplican a los personajes de Kenney copiando la dirección de cada hueso. Probadas: hablar, caminar, bailar, sentarse, asentir, brazos cruzados.
- **Kenney Furniture Kit y Nature Kit (CC0):** cuarto con ventana 3D, muebles, árboles, flores.
- **Poly Haven (CC0):** API pública sin clave; se bajan cielos (HDRI) y se usan de fondo y de luz.
- **Personalizar pieles** desde los SVG de origen de Kenney (fiel al original: diferencia media 0,25 de 255).
- **Hoja de personajes** automática y revisión de «lo que dice el cuento se ve».

## Evaluado y no integrado
Ver la tabla de `skills/recursos-3d/SKILL.md`: Universal Base Characters (no se pudo bajar), modelos de Poly Haven (estilo distinto), MPFB2 (pesado, sin probar), Rhubarb (binario/compilación), KayKit (sin probar), servidores MCP de Blender (código arbitrario).

## Skills de terceros vistas (no copiadas)
- `aicontentskills/ai-video-storyboard-skill` (MIT): plan de tomas para video con IA (6–18 tomas, composición, cámara, luz). Se tomó la idea de «lista de tomas con cámara y luz»; el flujo propio ya la cubre en `historia-3d`.
- `soasme/Violyra`, `Miftahul-Islam-Efaz/Motion-graphics-skill`, `agentara/skills`, `inferen-sh/skills (storyboard-creation)`: no se leyeron sus archivos; sin evaluar.
- Servidores MCP de Blender (`sandraschi/blender-mcp`, `blender-mcp-rs`, `blender-mcp-server` en PyPI): sirven para controlar Blender desde Claude Desktop o Cursor; descartados por la ejecución de código arbitrario y porque `bpy` por scripts ya cubre lo necesario.
- `agmmnn/polydown` (MIT): descargador de Poly Haven; se escribió uno propio y pequeño (`descargar_cielo.py`, solo librería estándar).

## Lo que sigue faltando (para el video de prueba)
1. `crear_historia3d.py`: orquestador (voces por personaje, música, subtítulos, mezcla y revisión).
2. Arcoíris y pared/luz afinados (ver `docs/PAUSA-historia-3d.md`).
3. Más personajes (KayKit, Universal Base Characters bajados a mano por Jeiler) y sillas/sillones donde sentarse.
4. Boca: las caras de Kenney son dibujos fijos; para labios habría que usar personajes con boca animable (Universal Base Characters, MPFB2).
