# Validación final del diseño

Fecha de cierre de validación: 2026-06-26.

## Resumen

El proyecto KiCad principal fue validado después de actualizar el esquemático, el PCB, las vistas documentales y el paquete Gerber con taladros.

| Revisión | Resultado |
| --- | --- |
| ERC KiCad | 0 errores, 0 advertencias |
| DRC KiCad | 0 violaciones |
| Pads desconectados | 0 |
| Errores de footprint | 0 |
| Paridad esquemático-PCB | 0 problemas |
| ZIP Gerber | Incluye cobre, máscara, pasta, serigrafía, contorno, `.gbrjob`, `.drl` y mapa de taladros |

## Reportes

- `docs/validacion/erc_final_20260626.rpt`
- `docs/validacion/drc_final_20260626.rpt`

## Fabricación

El ZIP listo para subir al fabricante está en:

`docs/fabricacion/PCB_PT100_SM50_GERBERS_CON_DRILL.zip`

También se dejó una copia actualizada en:

`C:\Users\kenne\Downloads\PCB_PT100_SM50_GERBERS_CON_DRILL.zip`

## Notas de serigrafía

Se mantuvieron las referencias visibles. Las advertencias finales estaban relacionadas con texto de serigrafía sobre cobre/máscara o superposiciones entre referencias. Se corrigieron moviendo referencias y usando altura mínima de 0.8 mm, que coincide con la regla configurada en KiCad para este proyecto.

## Simulaciones documentadas

Los datos finales usados para las gráficas corregidas están en `docs/simulacion/`:

- `pt100_sweep_ng_20260625.csv`
- `sm50_sweep_positive_ng_20260625.csv`
- `resumen_numerico_ng_20260625.json`

Las gráficas generadas están en `docs/figuras/` y coinciden con los logs nuevos de LTspice y los PDF exportados `escPT100.pdf` / `escSM50.pdf`.
