# Referencias técnicas y componentes

Este documento resume las fuentes técnicas conservadas en el proyecto y las verificaciones principales de componentes.

## Fuentes del proyecto

| Ruta | Uso |
| --- | --- |
| `PCB_PT100_SM50/PCB_PT100_SM50.kicad_sch` | Esquemático KiCad principal. |
| `PCB_PT100_SM50/PCB_PT100_SM50.kicad_pcb` | PCB final. |
| `PCB_PT100_SM50/symbols/` | Símbolos locales usados por el esquemático. |
| `PCB_PT100_SM50/footprints/` | Footprints locales y ajustados. |
| `PCB_PT100_SM50/3d/` | Modelos 3D usados en KiCad. |
| `ProyectoPCB_LTspice_PT100_SM50/` | Simulaciones LTspice. |
| `PCB_PT100_SM50/ltspice_models/` | Modelos SPICE copiados al proyecto KiCad. |
| `docs/simulacion/calculos_PT100_SM50_VALORES_ACTUALES_v2.csv` | Cálculos finales de PT100, SM-50 e interfaz B-Box. |
| `docs/referencias/referencias_completas_proyecto_PCB.txt` | Referencias finales, teóricas, de PCB y de trazabilidad usadas en la memoria vigente. |
| `docs/bitacora/bitacora_PCB_actualizada_27_06_2026.pdf` | Bitácora cronológica del proyecto desde el 11/03/2026 hasta el 27/06/2026. |
| `docs/figuras/diagrama_bloques_valores_actuales.png` | Diagrama de bloques con valores actuales de ambos canales. |

## Componentes revisados

| Bloque | Componentes / modelos | Resultado |
| --- | --- | --- |
| Entrada PT100 | Bornera METZ AST0250304, TVS/ESD, resistencias de excitación | Footprint ajustado contra datasheet y validado por DRC. |
| Entrada SM-50 | Bornera METZ AST0250404, protección y excitación | Footprint aplicado con modelo 3D verde y DRC limpio. |
| Amplificación | INA826AIDR, OPA2188AIDR | Footprints SOIC-8 compatibles con BOM. |
| Regulación/referencia | TPS7A4901DGNT, REF3012, reguladores auxiliares | Footprint PowerPAD ajustado con pad térmico correcto. |
| Protección | SMF12CT1G, PPTC 1812 | Footprints y serigrafía revisados. |
| Interfaz | RJ45 / B-Box | Modelo 3D y conectividad revisados. |

## Verificación de footprints descargados

El resumen completo está en:

`docs/referencias/RESUMEN_VERIFICACION_FOOTPRINTS_DESCARGADOS_20260625.md`

Los paquetes crudos descargados de proveedores no se versionan porque ocupan espacio y contienen formatos que no se usan directamente en KiCad. En el repositorio se conservan las librerías finales necesarias para abrir y fabricar el proyecto.

## Norma práctica usada para referencias

Para serigrafía se mantuvo la regla del proyecto KiCad:

- Altura mínima de texto: 0.8 mm.
- Espesor mínimo usado en referencias pequeñas: 0.1 mm.
- Las referencias se movieron fuera de pads, máscara y contornos de componentes.

Esto evita advertencias DRC y mantiene legibilidad razonable en fabricación.
