# Tarjeta de acondicionamiento de senales para sensores PT100 y SM-50

Repositorio de diseno electronico para una tarjeta PCB de acondicionamiento de senales orientada a la adquisicion de temperatura y torque en un motor de induccion. El proyecto integra simulaciones en LTspice, diseno esquematico y PCB en KiCad, librerias locales, modelos 3D, BOM y documentacion tecnica.

## Objetivo del proyecto

Disenar e implementar una tarjeta de circuito impreso que acondicione las senales provenientes de sensores PT100 y SM-50, de forma que puedan ser adquiridas de manera confiable por el sistema de medicion.

## Alcance tecnico

1. Comprender y aplicar fundamentos de diseno PCB usando KiCad.
2. Verificar mediante simulacion y pruebas el comportamiento de los sensores de temperatura y torque.
3. Integrar en una PCB las etapas de proteccion, referencia, excitacion, amplificacion y salida analogica.
4. Mantener un repositorio Git con archivos de diseno, documentacion tecnica e historial de desarrollo.

## Estructura del repositorio

| Ruta | Contenido |
| --- | --- |
| `PCB_PT100_SM50/` | Proyecto KiCad principal: esquematico, PCB, librerias, modelos 3D, BOM y reportes. |
| `ProyectoPCB_LTspice_PT100_SM50/` | Simulaciones LTspice de PT100, SM-50 y sistema combinado. |
| `PCB_PT100_SM50/docs/` | Imagenes y documentacion visual del esquematico. |
| `PCB_PT100_SM50/outputs/` | Reportes generados para validacion del diseno. |
| `zz_archivo_depuro_20260624/` | Archivo local de respaldos, temporales y salidas regenerables. Ignorado por Git. |

## Estado de validacion

- KiCad ERC: `0 violations`.
- Reporte final: `PCB_PT100_SM50/outputs/erc_after_cleanup.rpt`.
- Proyecto KiCad: `PCB_PT100_SM50/PCB_PT100_SM50.kicad_pro`.
- Esquematico principal: `PCB_PT100_SM50/PCB_PT100_SM50.kicad_sch`.
- PCB principal: `PCB_PT100_SM50/PCB_PT100_SM50.kicad_pcb`.

Nota: los warnings originales de ERC eran administrativos de libreria (`lib_symbol_mismatch` y una libreria faltante para `ProyectoPCB`). Se registro la libreria faltante y se dejo `lib_symbol_mismatch` en `ignore`, porque el esquematico usa simbolos locales ajustados manualmente sin errores electricos asociados.

## Como revisar el diseno

1. Abrir `PCB_PT100_SM50/PCB_PT100_SM50.kicad_pro` con KiCad 9.
2. Ejecutar `Inspect -> Electrical Rules Checker` para confirmar el ERC.
3. Revisar el PCB desde `PCB_PT100_SM50.kicad_pcb` y las librerias locales en `symbols/`, `footprints/` y `3d/`.
4. Abrir las simulaciones LTspice desde:
   - `ProyectoPCB_LTspice_PT100_SM50/01_SENSOR_PT100/`
   - `ProyectoPCB_LTspice_PT100_SM50/02_SENSOR_SM50/`
   - `ProyectoPCB_LTspice_PT100_SM50/03_SISTEMA_COMPLETO_3PT100_1SM50/`

## Componentes y bloques principales

| Bloque | Funcion |
| --- | --- |
| Proteccion de entrada | TVS/ESD y PPTC para proteger lineas de sensores. |
| Referencia y regulacion | Referencia de precision y reguladores para polarizacion analogica. |
| Acondicionamiento PT100 | Amplificacion y filtrado para sensor de temperatura. |
| Acondicionamiento SM-50 | Excitacion y amplificacion para sensor de torque. |
| Interfaz B-Box | Conectores y salidas analogicas hacia el sistema de adquisicion. |

## Limpieza del repositorio

Los respaldos historicos, caches de KiCad, archivos `.raw/.log/.db` de LTspice y temporales de importacion se movieron a `zz_archivo_depuro_20260624/`. Esa carpeta se mantiene localmente como respaldo recuperable, pero queda fuera del repositorio por `.gitignore`.

## Herramientas

- KiCad 9.0
- LTspice
- Git / GitHub
