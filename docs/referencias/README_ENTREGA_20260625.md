# Entrega PCB PT100 + SM50

Fecha de preparación: 2026-06-25

## Estado general

- Proyecto KiCad corregido y validado.
- ERC final: 0 errores, 0 warnings.
- DRC final: 0 violaciones.
- Pads sin conectar: 0.
- Paridad esquemático-PCB: 0 issues.
- Conectores RJ45 BBOX corregidos: pines 3, 5 y 6 en GND para PT100 y SM50.
- Footprints críticos actualizados contra los ZIPs/modelos revisados: `J_PT100_1` = AST0250304, `J_SM50` = AST0250404, `U3` = TPS7A4901DGNT DGN/HVSSOP-8 PowerPAD.
- La alimentación -15 V queda usada como alimentación negativa/protegida de opamps/INA y BBOX, no como salida de sensor.

## Para fabricar PCB

Archivo recomendado para subir directo al fabricante:

`fabricacion/PCB_PT100_SM50_GERBERS_CON_DRILL.zip`

Ese ZIP incluye las capas Gerber y el archivo de taladros Excellon `PCB_PT100_SM50.drl` en la raíz del ZIP, para evitar el error "There is no drill layer in the file".

También se puede enviar al fabricante el contenido de:

`fabricacion/`

Incluye:

- `gerbers/`: capas Gerber exportadas desde KiCad.
- `drill/`: archivo Excellon de taladros y mapa PDF.
- `ensamble_visual/`: Gerber/PDF/SVG de referencia visual con `F.Fab`, `F.SilkS` y borde de placa para ver mejor las etiquetas de componentes. Usar como apoyo de revisión/ensamble, no como reemplazo de los Gerbers de fabricación.

## Para ensamble

Usar:

- `ensamble/PCB_PT100_SM50_BOM.csv`
- `ensamble/PCB_PT100_SM50_BOM_unitaria.csv`
- `ensamble/PCB_PT100_SM50_pos.csv`
- `ensamble/99915123_DigiKey_original.csv`
- `ensamble/REVISION_BOM_FOOTPRINTS_20260625.csv`

Nota: H1-H4 y el logo estan marcados como `board_only` y excluidos de BOM/POS.

Referencias cortas: se normalizaron las referencias largas de resistencias/capacitores/trimmers a designadores compactos tipo letra + número. Cambios principales: `R_LIM_PT100` -> `R9`, `R_LIM_SM50` -> `R11`, `R_ISO_PT100` -> `R12`, `R_ISO_SM50` -> `R13`, `RSET_PT100` -> `R14`, `C_OUT_SM50` -> `C27`, `C_OUT_PT100` -> `C28`, `TRIM_SM50` -> `RV1`, `TRIM_PT100` -> `RV2`. En zonas densas el texto de referencia en PCB se dejó en 0.8 mm, respetando el mínimo DRC del proyecto.

Referencias activas: se dejaron visibles las referencias reales del PCB en `F.SilkS`/`F.Fab` y se reubicaron las que tocaban cobre o serigrafía. Solo permanecen ocultos los placeholders de gráficos/logos (`REF**`, `G***`) y las referencias de potencia en el esquemático (`#PWR`, `#FLG`), por convención de KiCad.

## Validación

Archivos principales:

- `validacion/erc_final_conjunto_20260625.rpt`
- `validacion/drc_final_conjunto_20260625.rpt`
- `validacion/netlist_final_conjunto_20260625.xml`
- `validacion/PCB_PT100_SM50_esquematico_20260625.pdf`
- `validacion/pcb_layers_pdf_export/PCB_PT100_SM50.pdf`
- `validacion/PCB_PT100_SM50_3D_20260625.step`
- `validacion/RESUMEN_VERIFICACION_FOOTPRINTS_DESCARGADOS_20260625.md`

## Simulación

Las corridas se hicieron con el motor `ngspice.dll` incluido en KiCad 9.0, no con LTspice.

Resultados principales:

- PT100, 130 C: `VOUT_PT100_BBOX = 4.369544 V`.
- SM50, escala completa bipolar, RG=340 ohm: `VOUT_SM50_BBOX = +/-4.39 V`.
- Simulación conjunta idealizada: el SM-50 se documenta con salida bipolar nominal dentro del rango +/-5 V.

Archivos:

- `simulacion/sim_kicad_ngspice_pt100_sweep_ng_20260625.csv`
- `docs/simulacion/sm50_sweep_bipolar_ng_20260629.csv`
- `simulacion/sim_kicad_ngspice_numeric_summary_ng_20260625.json`
- `simulacion/sim_kicad_ngspice_conjunto_ideal_pos_ng_20260625.log`

Nota: el netlist SPICE exportado directamente desde el esquemático KiCad aún contiene placeholders de símbolos sin modelo SPICE asignado. Por eso las simulaciones numéricas finales usan bancos idealizados compatibles con ngspice de KiCad.

## Fuentes KiCad

`fuentes_kicad/` contiene el proyecto KiCad corregido y las librerías locales necesarias para reabrirlo:

- `.kicad_pro`
- `.kicad_sch`
- `.kicad_pcb`
- tablas de librerías
- footprints, símbolos y modelos 3D locales

## GitHub

Al momento de preparar esta entrega, el repositorio local no tiene remoto configurado (`git remote -v` no muestra `origin`). Por eso no se pudo confirmar ni hacer push a GitHub desde esta copia.
