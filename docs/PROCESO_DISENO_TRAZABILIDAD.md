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

## 6. Resultado

El repositorio queda preparado con fuentes, documentación, figuras y reportes finales. Los archivos de salida intermedios, respaldos y paquetes descargados de verificación se excluyen por `.gitignore` o fueron eliminados cuando eran regenerables.
