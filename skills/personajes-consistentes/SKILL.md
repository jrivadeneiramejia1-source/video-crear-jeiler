---
name: personajes-consistentes
description: >-
  Mantiene al MISMO personaje en todas las escenas, tomas o clips: crea su hoja de personaje (frente, perfil, espalda y rostro en una imagen), saca su paleta de colores, deja una ficha con lo que no debe cambiar y compara los cuadros de distintas escenas para avisar si cambió de colores. Usar cuando el usuario diga "que el personaje se vea igual en todas las escenas", "hoja de personaje", "que no le cambie la ropa o el pelo", "personaje consistente" o antes de animar en 3D o pedir clips de IA. Los personajes son inventados; nunca de personas reales.
---

# Personajes consistentes

El error más común en videos con personajes es que cambian entre escena y escena (otra cara, otro pelo, otra ropa). Se evita con **una hoja de personaje aprobada** que se usa siempre, y con una **alarma barata** que compara colores entre escenas.

## Reglas
- **Personajes inventados.** Nada de caras o voces de personas reales ni de personajes de otras marcas.
- Los modelos 3D son de licencia libre (CC0) y viven fuera del repo; anotar su origen en la ficha y dar crédito.
- **Una persona (Jeiler) aprueba la hoja** antes de animar o pedir clips; la alarma de colores no ve la forma de la cara.
- Para clips de IA, la hoja es la imagen de referencia; no cambiarla a mitad del proyecto.
- Claude no ve el movimiento: revisa cuadros.

## Proceso
1. **Elegir el personaje:** un modelo 3D con esqueleto (ver `video-3d`) o, en 2D, los colores y rasgos de `animacion-2d` (`piel`, `pelo`, `pelo_estilo`, `camisa`).
2. **Hoja de personaje (3D):** lo mejor y lo más general es `escena3d.py historia.json carpeta --hoja` (de `video-3d`; deja `hoja_<personaje>.png` con frente, perfil, espalda y rostro de cerca, con la ropa, el pelo y los accesorios de la historia). El script `hoja_personaje.py` de abajo es el antiguo, de un solo personaje, y solo sirve con *Animated Characters 1*:
   ```bash
   $PYBL scripts/hoja_personaje.py --personaje $P/Model/characterMedium.fbx --piel $P/Skins/survivorMaleB.png --salida hoja   # solo Animated Characters 1
   ```
   Deja `hoja/hoja.png` (frente, perfil, espalda y rostro), `paleta.json` y `paleta.png`. (Necesita `video-3d` y su Python con Blender.)
3. **Ficha:** copiar `plantilla/ficha-personaje.md`, ponerle un nombre inventado, los colores de la paleta, los rasgos que **no** cambian y lo que nunca debe pasar.
4. **Aprobación de Jeiler** (hoja y una escena de prueba de 5 s).
5. **Durante la producción:** usar siempre el mismo modelo, la misma piel y la misma ficha. Con clips de IA, pasar la misma imagen de referencia y repetir sus rasgos en cada pedido.
6. **Comprobar entre escenas:** `python3 scripts/comparar_cuadros.py cuadro_referencia.png cuadro_escena2.png cuadro_escena3.png`. Compara la paleta de la zona central; avisa «posible cambio de personaje» si pasa de 0,25.
7. **Mirar los cuadros** de las escenas juntos (`look.py` de `ffmpeg-skill` o una hoja propia) y buscar cambios de forma de cara, pelo y manos.

## Distinguir a los personajes (lección de la prueba 2026-11-05)
Dos personajes con el mismo cuerpo y el mismo peinado solo cambiando la camiseta se confunden (en una prueba, un niño parecía mujer). Cada personaje principal debe diferenciarse en **al menos tres cosas**: peinado o accesorio (`coletas`, `lazo` en `escena3d.py`), color de pelo, colores de ropa y detalles (mechón, pecas, parche). Se comprueba mirando la **hoja de personajes** (`escena3d.py --hoja`) también **de espalda y de perfil**, no solo de frente. Cambiar pelo y ropa: `video-3d/scripts/personalizar_piel.py`.

## Señales de alerta
- Cambiar de modelo, de piel o de iluminación entre escenas sin avisar.
- Aprobar el personaje mirando solo el frente.
- Fiarse solo de la alarma de colores: no detecta una cara distinta con la misma ropa.

## Verificación
- [ ] La hoja de personaje fue aprobada por Jeiler.
- [ ] La ficha tiene colores, rasgos fijos y origen/licencia.
- [ ] `comparar_cuadros.py` sin avisos entre las escenas y los cuadros se miraron.
- [ ] Se dijo que la forma de la cara y del pelo la revisó una persona.

## Qué se probó (2026-11-05)
Con un personaje CC0 de Kenney: `hoja_personaje.py` produjo la hoja con las cuatro vistas (el pelo se ve completo de frente, perfil y espalda) y la paleta en unos 40 s. `comparar_cuadros.py` midió 0,09 entre instantes del mismo clip y 0,35 contra el mismo personaje con otra piel; por eso el umbral quedó en 0,25 (**pocos datos: una guía, no una prueba**). **No se probó** con personajes 2D, con clips de IA, con muchos personajes en la misma escena ni con cambios de luz grandes entre escenas (que subirían la distancia sin que cambie el personaje).
