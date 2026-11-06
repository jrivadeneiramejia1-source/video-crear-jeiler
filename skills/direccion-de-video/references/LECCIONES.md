# Lecciones aprendidas (se añaden aquí; cada una con cómo se descubrió y cómo se evita)

| Fecha | Lección | Cómo se descubrió | Cómo se evita |
|---|---|---|---|
| 2026-11-06 | Con el tiempo detenido (`setEffectiveTimeScale(0)`), Three.js **no reinicia el ciclo** de una animación: el personaje se congelaba en la última pose después del primer ciclo | Se rastreó el hueso del pie y su altura salía constante | Calcular el ciclo (`tiempo % duración`) en el motor; medir pies, no creer a ojo |
| 2026-11-06 | Los FBX de Blender traen colores lineales y Three.js los oscurecía dos veces (pieles negras) | Colores crudos del FBX leídos con un script; la vista previa oficial también mostraba caras negras: era diseño | `convertLinearToSRGB`; comparar con la vista previa del autor antes de «arreglar» |
| 2026-11-06 | La altura de un FBX se debe medir con el personaje **ya posado** y con el esqueleto aplicado | Una vara de 1,7 m puesta al lado mostró la escala real | Vara de referencia en una escena de prueba |
| 2026-11-06 | Cabeza grande = encuadre «medio» y «primer plano» demasiado cerrados | Cuadros del plano medio mostraban solo cabeza y hombros | Medir la cabeza (`cabeza[id]`) y ajustar la distancia |
| 2026-11-06 | Una toma de dos personajes se coloca de lado respecto a la línea que los une, no según uno de ellos | La cámara quedó pegada a un personaje | Ya resuelto en el motor; mantener `lado` constante en la pareja |
| 2026-11-06 | La velocidad de una caminata se mide con el pie apoyado; el **paso se debe ligar a los metros recorridos**, no al reloj | Medición de patinaje: 13 % con reloj; ciclo por distancia lo mantiene en 5–14 % incluso al arrancar y frenar | `ir_a` sin `b`; el motor mide y avisa |
| 2026-11-06 | Los paquetes con licencia «CC0» deben verificarse en la **página** o en `LICENSE.txt` en el momento de bajar | Un paquete sin archivo de licencia dentro del zip | `descargar_paquetes.py` falla si no dice CC0 |
| 2026-11-06 | Un paquete puede ser CC0 y aun así no servir (Animated Human: maniquí sin cara; Quaternius: cara sin boca) | Se renderizó antes de adoptarlo | Mirar un cuadro antes de añadir cualquier recurso al catálogo |
