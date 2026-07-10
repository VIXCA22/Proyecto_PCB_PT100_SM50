# Verificacion de ZIPs de footprints/modelos - 2026-06-25

Proyecto: PCB_PT100_SM50

## Resultado ejecutivo

Los ZIPs se extrajeron y se compararon contra el BOM de compra
`PCB_PT100_SM50/bom/99915123_DigiKey_original.csv`, el BOM de entrega
`ENTREGA_PCB_PT100_SM50_20260625/ensamble/PCB_PT100_SM50_BOM.csv` y el PCB
actual `PCB_PT100_SM50/PCB_PT100_SM50.kicad_pcb`.

Actualización: se recibió y verificó también `INA826AIDR.zip`, que sí
corresponde al BOM actual. El footprint descargado `D8.kicad_mod` es SOIC-8,
pitch 1.27 mm, y es compatible con el footprint actual de U2/U4.

Actualización final de fabricación: se reemplazaron en el PCB los footprints
críticos que dependian de ZIPs descargados: `J_PT100_1` usa
`ProyectoPCB:CONN_AST0250304_MZC`, `J_SM50` usa `ProyectoPCB:AST0250404` y
`U3` usa `ProyectoPCB_Footprints:TPS7A4901DGNT_DGN8_1P89X1P57` con el pad
térmico renombrado a `9`. Después del reemplazo, KiCad ERC/DRC quedó en 0
violaciones y 0 pads sin conectar.

Corrección posterior de `J_PT100_1`: el footprint descargado para
`CONN_AST0250304_MZC` se ajustó localmente contra el datasheet METZ
`ST025xxHDNC AST025` / `AST025xx04`. Para 3 polos, la huella queda con largo
15 mm, profundidad PCB 11 mm, pitch 5.00 mm y taladro 1.4 mm.

Corrección adicional de `J_SM50`: se completó la huella embebida y la librería
local con serigrafía y `F.CrtYd`; se eliminó `allow_missing_courtyard`. El
lado cercano a `D1` queda con courtyard ajustado para encerrar cuerpo/silk sin
solapar el TVS. También se rellenaron los planos GND. DRC final:
`drc_after_pt100_sm50_terminal_fix_20260626.rpt` con 0 violaciones, 0 pads sin
conectar y 0 problemas de paridad esquemático-PCB.

El ZIP `INA826AIDGKR.zip` queda marcado como no aplicable para esta compra:
`AIDGKR` es encapsulado DGK/VSSOP-8 de pitch 0.65 mm, mientras el PCB actual y
la compra usan `INA826AIDR`, encapsulado SOIC-8 de pitch 1.27 mm.

## ZIPs revisados

| ZIP | Veredicto | Observación |
| --- | --- | --- |
| `LibraryLoaderSetup2v50.msi.zip` | No es componente | Es instalador de Library Loader; no contiene footprint específico para el PCB. |
| `AST0250304 (1).zip` | Base para J_PT100_1, corregido localmente | Trae `CONN_AST0250304_MZC.kicad_mod`. Coincide en 3 pines y pitch 5.00 mm, pero se ajustaron profundidad y taladro contra el datasheet METZ. |
| `LIB_AST0250404.zip` | Aplicado para J_SM50 | Trae KiCad nativo `AST0250404.kicad_mod` y 3D `AST0250404.stp`. Coincide en 4 pines y pitch 5.00 mm; reemplazo aplicado en el PCB. |
| `TPS7A4901DGNT.zip` | Aplicado para U3, con ajuste | Trae `DGN8_1P89X1P57.kicad_mod` y modelo STEP. Se adaptó el pad térmico de `EPAD` a `9` para coincidir con el símbolo actual. |
| `INA826AIDGKR.zip` | No usar con el BOM actual | Es DGK/VSSOP-8. El BOM compra `INA826AIDR`, SOIC-8. |
| `INA826AIDR.zip` | Compatible con U2/U4 | Trae `D8.kicad_mod`, SOIC-8. Coincide con el MPN del BOM y con el footprint actual. |
| `OPA2188AIDR.zip` | Compatible con U5 | Trae `D8.kicad_mod`, SOIC-8. El footprint actual KiCad SOIC-8 es prácticamente equivalente. |

## Comparación de medidas principales

| Parte | Footprint actual en PCB | Footprint descargado/local comparado | Resultado |
| --- | --- | --- | --- |
| J_PT100_1 / AST0250304 | `ProyectoPCB:CONN_AST0250304_MZC` corregido | Datasheet METZ `AST025xx04`: 3 pines, pitch 5.00 mm, cuerpo PCB 15 x 11 mm, pads 2.1 mm, drill 1.4 mm | OK corregido en PCB y librería local. |
| J_SM50 / AST0250404 | `ProyectoPCB:AST0250404` aplicado | ZIP `AST0250404`, pitch 5.00 mm, pads 2.1 mm, drill 1.4 mm, modelo `AST0250404.stp` | OK aplicado en PCB y esquemático; courtyard completado sin excepción DRC. |
| U3 / TPS7A4901DGNT | `ProyectoPCB_Footprints:TPS7A4901DGNT_DGN8_1P89X1P57` aplicado | ZIP `DGN8_1P89X1P57`, pads x +/-2.0955 mm, pad térmico 1.57 x 1.89 mm | OK aplicado; pad térmico adaptado a `9`. |
| U2/U4 / INA826AIDR | SOIC-8 3.9 x 4.9 mm, pitch 1.27 mm, span x 4.95 mm, pads 1.95 x 0.60 mm | ZIP correcto `D8`, pitch 1.27 mm, span x 4.928 mm, pads 1.9812 x 0.5588 mm | Coincide. El footprint actual es compatible. |
| U2/U4 / ZIP confundido INA826AIDGKR | SOIC-8 3.9 x 4.9 mm, pitch 1.27 mm | ZIP `DGK8`, pitch 0.65 mm, VSSOP/MSOP | No coincide. No usar para el BOM actual. |
| U5 / OPA2188AIDR | SOIC-8 3.9 x 4.9 mm, pitch 1.27 mm | ZIP `D8`, pitch 1.27 mm, pad span equivalente | Compatible. El footprint actual es aceptable. |

## Recomendación antes de mandar a fabricar

1. Mantener U2/U4 como SOIC-8 para `INA826AIDR`; el ZIP correcto `INA826AIDR.zip` confirma que el footprint actual calza.
2. U3 ya quedó con footprint DGN/HVSSOP-8 PowerPAD específico y pad térmico `9`.
3. J_PT100_1 quedó corregido contra datasheet METZ; J_SM50 mantiene footprint METZ descargado.
4. Mantener U5 como SOIC-8; el ZIP de OPA confirma que el footprint actual está bien.
