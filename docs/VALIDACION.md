# Validacion final del diseno

Fecha de cierre de validacion: 2026-06-26.

## Resumen

El proyecto KiCad principal fue validado despues de ajustar referencias de serigrafia, footprints criticos, modelos 3D de borneras y el paquete Gerber con taladros.

| Revision | Resultado |
| --- | --- |
| ERC KiCad | 0 errores, 0 advertencias |
| DRC KiCad | 0 violaciones |
| Pads desconectados | 0 |
| Errores de footprint | 0 |
| Paridad esquematico-PCB | 0 problemas |
| ZIP Gerber | Incluye cobre, mascara, pasta, serigrafia, contorno, `.gbrjob`, `.drl` y mapa de taladros |

## Reportes

- `docs/validacion/erc_final_20260626.rpt`
- `docs/validacion/drc_final_20260626.rpt`

## Fabricacion

El ZIP listo para subir al fabricante esta en:

`docs/fabricacion/PCB_PT100_SM50_GERBERS_CON_DRILL.zip`

Tambien se dejo una copia actualizada en:

`C:\Users\kenne\Downloads\PCB_PT100_SM50_GERBERS_CON_DRILL.zip`

## Notas de serigrafia

Se mantuvieron las referencias visibles. Las advertencias finales estaban relacionadas con texto de serigrafia sobre cobre/mascara o superposiciones entre referencias. Se corrigieron moviendo referencias y usando altura minima de 0.8 mm, que coincide con la regla configurada en KiCad para este proyecto.

## Simulaciones documentadas

Los datos finales usados para las graficas corregidas estan en `docs/simulacion/`:

- `pt100_sweep_ng_20260625.csv`
- `sm50_sweep_positive_ng_20260625.csv`
- `resumen_numerico_ng_20260625.json`

Las graficas generadas estan en `docs/figuras/` y coinciden con el resumen del PDF final de simulacion.
