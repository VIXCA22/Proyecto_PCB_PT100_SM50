# Proceso de diseno y trazabilidad

Este documento resume como se llego al resultado final del proyecto, incluyendo las decisiones tecnicas guiadas por consultas y revisiones en ChatGPT ProyectoPCB.

## 1. Definicion del problema

El proyecto busca acondicionar las senales de dos sensores instalados en un motor de induccion del LabCES:

- PT100 para temperatura.
- SM-50 para torque.

La tarjeta debe entregar senales compatibles con el sistema de adquisicion, manteniendo proteccion de entradas, referencia estable, alimentacion analogica, filtrado y salida hacia B-Box.

## 2. Simulacion de los sensores

Se desarrollaron simulaciones LTspice por canal:

- `ProyectoPCB_LTspice_PT100_SM50/01_SENSOR_PT100/`
- `ProyectoPCB_LTspice_PT100_SM50/02_SENSOR_SM50/`

Las simulaciones permitieron revisar la respuesta esperada antes de pasar al PCB:

- PT100: barrido de temperatura y salida acondicionada.
- SM-50: salida contra carga/torque relativo con distintas resistencias de ganancia.

Las graficas finales se generaron desde CSV en `docs/simulacion/`.

## 3. Migracion a KiCad

El diseno se traslado a KiCad integrando:

- Esquematico principal.
- Librerias locales de simbolos.
- Footprints locales y footprints verificados contra fabricante.
- Modelos 3D para revision mecanica.
- PCB con conectores para sensores y salidas hacia B-Box.

Proyecto principal:

`PCB_PT100_SM50/PCB_PT100_SM50.kicad_pro`

## 4. Consultas y prompts que guiaron el cierre

Durante la depuracion se hicieron revisiones iterativas con prompts enfocados en:

- Corregir errores DRC sin romper el esquematico.
- Mantener las referencias visibles en Gerber y PDF de ensamble.
- Reducir o mover referencias cuando el espacio era limitado.
- Activar referencias deshabilitadas.
- Verificar footprints descargados contra BOM y datasheets.
- Dejar las borneras con modelo 3D verde manteniendo el footprint.
- Generar un ZIP Gerber valido con archivo de taladros `.drl`.
- Preparar un repositorio GitHub limpio, sin backups ni outputs pesados.

## 5. Correcciones finales aplicadas

- Reubicacion de referencias de serigrafia para eliminar advertencias DRC.
- Uso de altura minima de 0.8 mm para referencias en zonas estrechas.
- Verificacion de borneras METZ AST0250304/AST0250404.
- Confirmacion de footprints SOIC-8 para INA826AIDR y OPA2188AIDR.
- Actualizacion del footprint/modelo 3D del TVS SMF12CT1G.
- Generacion de imagenes para GitHub: KiCad esquematico, PCB 2D, PCB 3D, LTspice y graficas.
- Regeneracion del ZIP Gerber con taladros.

## 6. Resultado

El repositorio queda preparado con fuentes, documentacion, figuras y reportes finales. Los archivos de salida intermedios, backups y paquetes descargados de verificacion se excluyen por `.gitignore` o fueron eliminados cuando eran regenerables.
