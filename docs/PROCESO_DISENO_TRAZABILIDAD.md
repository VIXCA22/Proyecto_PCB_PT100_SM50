# Proceso de diseño y trazabilidad

Este documento resume cómo se llegó al resultado final del proyecto y registra las decisiones técnicas tomadas durante la revisión del diseño.

## 1. Definición del problema

El proyecto busca acondicionar las señales de dos sensores instalados en un motor de inducción del LabCES:

- PT100 para temperatura.
- SM-50 para torque.

La tarjeta debe entregar señales compatibles con el sistema de adquisición, manteniendo protección de entradas, referencia estable, alimentación analógica, filtrado y salida hacia B-Box.

## 2. Simulación de los sensores

Se desarrollaron simulaciones LTspice por canal:

- `ProyectoPCB_LTspice_PT100_SM50/01_SENSOR_PT100/`
- `ProyectoPCB_LTspice_PT100_SM50/02_SENSOR_SM50/`

Las simulaciones permitieron revisar la respuesta esperada antes de pasar al PCB:

- PT100: barrido de temperatura y salida acondicionada.
- SM-50: salida contra carga/torque relativo con distintas resistencias de ganancia.

Las gráficas finales se generaron desde CSV en `docs/simulacion/`.

## 3. Migración a KiCad

El diseño se trasladó a KiCad integrando:

- Esquemático principal.
- Librerías locales de símbolos.
- Footprints locales y footprints verificados contra fabricante.
- Modelos 3D para revisión mecánica.
- PCB con conectores para sensores y salidas hacia B-Box.

Proyecto principal:

`PCB_PT100_SM50/PCB_PT100_SM50.kicad_pro`

## 4. Revisiones que guiaron el cierre

Durante la depuración se hicieron revisiones iterativas enfocadas en:

- Corregir errores DRC sin romper el esquemático.
- Mantener las referencias visibles en Gerber y PDF de ensamble.
- Reducir o mover referencias cuando el espacio era limitado.
- Activar referencias deshabilitadas.
- Verificar footprints descargados contra BOM y datasheets.
- Dejar las borneras con modelo 3D verde manteniendo el footprint.
- Generar un ZIP Gerber válido con archivo de taladros `.drl`.
- Preparar un repositorio GitHub limpio, sin respaldos ni salidas pesadas.

## 5. Correcciones finales aplicadas

- Reubicación de referencias de serigrafía para eliminar advertencias DRC.
- Uso de altura mínima de 0.8 mm para referencias en zonas estrechas.
- Verificación de borneras METZ AST0250304/AST0250404.
- Confirmación de footprints SOIC-8 para INA826AIDR y OPA2188AIDR.
- Actualización del footprint/modelo 3D del TVS SMF12CT1G.
- Generación de imágenes para GitHub: KiCad esquemático, PCB 2D, PCB 3D, LTspice y gráficas.
- Regeneración del ZIP Gerber con taladros.

## 6. Bitácora del proceso

La bitácora actualizada se conserva en:

- `docs/bitacora/bitacora_PCB_actualizada_27_06_2026.pdf`
- `docs/bitacora/bitacora_PCB_actualizada_27_06_2026.tex`

Este documento registra el avance desde el 11/03/2026 hasta el 27/06/2026. La secuencia de trabajo se puede resumir así:

| Periodo | Actividad principal | Resultado para el proyecto |
| --- | --- | --- |
| 11/03/2026-18/03/2026 | Inicio, aprendizaje de KiCad, práctica de PCB y revisión de reglas básicas de diseño. | Se definió el alcance inicial y se estableció el flujo de esquemático, footprint y PCB. |
| 25/03/2026-30/03/2026 | Estudio de ruido, sensores y revisión técnica. | Se identificó la necesidad de filtrado, blindaje, cableado adecuado y acondicionamiento diferencial. |
| 08/04/2026-24/04/2026 | Arquitectura del sistema, validación previa de sensores y ajuste de adquisición. | Se separaron los bloques de temperatura, torque, adquisición e interfaz. |
| 29/04/2026-15/05/2026 | Revisión de hojas de datos, puente Wheatstone, rango dinámico, offset y resolución. | Se consolidaron las fórmulas base para PT100, SM-50 y salida hacia la interfaz de adquisición. |
| 19/05/2026-28/05/2026 | Validación de datos reales del SM-50, memoria de cálculo y revisión de interfaz BoomBox/B-Box. | Se fijaron criterios de excitación, ganancia, resolución y conexión física. |
| 31/05/2026-07/06/2026 | Alimentación, conectores, RJ45, organización funcional y PT100 de tres hilos. | Se definieron conectores de sensor, salidas 8P8C, bloques de PCB y criterios de referencia. |
| 08/06/2026-21/06/2026 | Depuración del PT100, referencias técnicas, LTspice, selección de amplificadores, EMI e integración KiCad. | Se cerró la arquitectura eléctrica y se pasó a implementación formal del esquemático. |
| 22/06/2026-27/06/2026 | Protecciones, footprints, ruteo, valores finales, memoria, referencias y fabricación. | Se obtuvo una PCB con ERC/DRC limpios, figuras finales, cálculos actualizados y paquete Gerber. |

La bitácora se usa como evidencia de proceso. Los cálculos finales vigentes son los conservados en `docs/simulacion/calculos_PT100_SM50_VALORES_ACTUALES_v2.csv` y en la memoria final citada en `docs/referencias/referencias_completas_proyecto_PCB.txt`.

## 7. Resultado

El repositorio queda preparado con fuentes, documentación, figuras y reportes finales. Los archivos de salida intermedios, respaldos y paquetes descargados de verificación se excluyen por `.gitignore` o fueron eliminados cuando eran regenerables.
