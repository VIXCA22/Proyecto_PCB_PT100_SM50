# Auditoria de footprints y modelos 3D

Objetivo: evitar que un modelo 3D de DigiKey/Ultra Librarian se confunda con un
footprint validado para fabricacion. Los ZIPs revisados contenian modelos STEP/STP;
la orden de compra agrego MPNs que no estaban en esos ZIPs.

## Verificado con fuente de fabricante

| Parte | Resultado |
| --- | --- |
| `INA826AIDR` | Simbolo `INA826_SOIC8` con pinout de TI. Footprint especifico `SOIC-8_3.9x4.9mm_P1.27mm_INA826AIDR` enlazado a `INA826AIDR_TI_SOIC8_D0008A.stp`. |
| `OPA2188AIDR` | Simbolo `OPA2188_SOIC8` con pinout de TI. Footprint especifico `SOIC-8_3.9x4.9mm_P1.27mm_OPA2188AIDR` enlazado a `OPA2188AIDR_TI_SOIC8_D0008A.stp`. |
| `REF3012AIDBZR` | Simbolo `REF30E_SOT23` y footprint `SOT-23-3` con modelo `REF3012AIDBZR_TI_SOT23_DBZ0003A.stp`. Pinout: 1=IN, 2=OUT, 3=GND. |
| `TPD4E1U06DBVR` | Simbolo y footprint especificos. El land pattern usa 6 pads de 1.1 mm x 0.6 mm, pitch 0.95 mm y separacion de filas 2.6 mm, segun TI DBV0006A. |
| `TPS7A4901DGNT` | Simbolo y footprint especificos. El land pattern usa pads 1.4 mm x 0.45 mm, pitch 0.65 mm, separacion de filas 4.4 mm y PowerPAD 1.57 mm x 1.89 mm, segun TI DGN0008G. |
| `C2012X7R1H105K085AC` | TDK confirma serie C2012 / EIA 0805, 2.00 mm x 1.25 mm x 0.85 mm. Se creo footprint especifico `C_0805_2012Metric_TDK_C2012X7R1H105K085AC` con su STEP local. |
| `2250066-1` | Bel/TRP confirma MagJack 10/100 tab-up. Se creo `RJ45_BelFuse_2250066-1` con 8x taladro 0.89 mm, 2x shield 1.57 mm y 2x postes NPTH 3.2 mm segun drawing C-2250066. STEP enlazado; revisar ajuste visual 3D en KiCad. |
| `1812L050/30PR` | Littelfuse 1812L050/30PR confirmado en datasheet 1812L. Se creo footprint `Fuse_1812_4532Metric_Littelfuse_1812L050-30PR`. |
| `3296W-1-102LF` | Bourns 3296W top-adjust confirmado en datasheet. Se creo `Potentiometer_Bourns_3296W_1x03_P2.54mm` con orden fisico de pads 1-3-2. |

## Consistente mecanicamente, pendiente de fuente primaria completa o STEP exacto

| Parte | Estado |
| --- | --- |
| `AST0250304` / `AST0250404` | La orden de compra indica borneras METZ de 5.00 mm. Se crearon footprints `TerminalBlock_METZ_AST0250304_1x03_P5.00mm` y `TerminalBlock_METZ_AST0250404_1x04_P5.00mm`; falta STEP/drawing local exacto. |
| `08055C104K4T2A` | El STEP se identifica como `CAP_0805_AVX`. Se creo footprint especifico `C_0805_2012Metric_AVX_08055C104K4T2A`. Pendiente confirmar land pattern oficial AVX/Kyocera si se va a liberar a fabricacion. |
| `08055C333KAT2A` | El STEP se identifica como `CAP_X7R_0805_AVX`. No es el MPN comprado para 33 nF; la compra trae `KGM21NR71H333KT`. |
| `08055C103K4T2A` | Agregado como simbolo `C_08055C103K4T2A` con footprint 0805 generico. Falta STEP exacto local. |
| `KGM21NR71H333KT` | Agregado como simbolo `C_KGM21NR71H333KT` con footprint 0805 generico. Falta STEP exacto local. |
| `GRM21BR61E106KA73K` | Agregado como simbolo `C_GRM21BR61E106KA73K` con footprint 0805 generico. Falta STEP exacto local. |
| `RT0805BRD07...` | El STEP se identifica como `RC0805N_YAG`. Se separo en footprint especifico `R_0805_2012Metric_Yageo_RT0805BRD` para no usar ese modelo en resistencias TE/CPF. |
| `CPF0805...` | Agregado como simbolo `R_CPF0805` con footprint 0805 generico. Falta STEP exacto local. |
| `SMF12CT1G` | El STEP se identifica como `SOT-363-6_2P2X1P35_ONS`. Se conserva footprint mecanico `SOT-363-6_SMF12CT1G`, pero no hay simbolo funcional porque falta confirmar pinout desde datasheet oficial. |

## Correcciones realizadas

- Corregi `2250066-1`: en la compra es Bel Fuse/TRP, no TE. El STEP local ahora se llama `2250066-1_BelFuse.stp`.
- Cree footprint y simbolo para `J_2250066_1_MAGJACK` usando el drawing oficial de Bel/TRP.
- Cambie los conectores PT100/SM50/alimentacion de 5.08 mm generico a METZ 5.00 mm cuando aplican a la compra.
- Quite el modelo 3D del footprint generico `SOIC-8_3.9x4.9mm_P1.27mm`; ahora no muestra por error un INA826 cuando el simbolo sea OPA2188, OPA188 o INA828.
- Cree footprints especificos para `INA826AIDR` y `OPA2188AIDR`, cada uno con su STEP.
- Quite el modelo 3D del footprint generico `C_0805_2012Metric`; ahora los modelos 3D de capacitor estan en footprints especificos por MPN.
- Quite el modelo 3D del footprint generico `R_0805_2012Metric`; el STEP Yageo quedo en `R_0805_2012Metric_Yageo_RT0805BRD`.
- Marque `TPS7A4901DGNT` como parte distinta del bloque LTspice `TPS7A4701_10V`. No son el mismo regulador.

## Pendientes antes de fabricar

- Abrir en KiCad el visor 3D del `RJ45_BelFuse_2250066-1` y ajustar offset/rotacion del STEP si no calza con el footprint.
- Confirmar datasheet/pinout de `SMF12CT1G` antes de conectarlo electricamente.
- Conseguir STEP exacto si quieres visual 3D para `AST0250304`, `AST0250404`, `1812L050/30PR`, `3296W-1-102LF`, `CPF0805...`, `08055C103K4T2A`, `KGM21NR71H333KT` y `GRM21BR61E106KA73K`.
- Si se cambia el regulador SM50 desde `TPS7A4701` a `TPS7A4901DGNT`, hay que actualizar tambien el esquematico electrico, no solo el footprint.

## Fuentes primarias usadas

- TI INA826: https://www.ti.com/lit/ds/symlink/ina826.pdf
- TI OPA2188: https://www.ti.com/lit/ds/symlink/opa2188.pdf
- TI REF30/REF30E: https://www.ti.com/lit/ds/symlink/ref30e.pdf
- TI TPD4E1U06: https://www.ti.com/lit/ds/symlink/tpd4e1u06.pdf
- TI TPS7A49/TPS7A4901: https://www.ti.com/lit/ds/symlink/tps7a49.pdf
- TDK C2012X7R1H105K085AC: https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C2012X7R1H105K085AC
- Bel Fuse 2250066-1: https://www.belfuse.com/products/ethernet/magjacks-icms/2250066-1
- Bel drawing C-2250066: https://www.belfuse.com/media/drawings/products/magjack%20ICMs/dr-mag-2250066.pdf
- Bel Industrial Ethernet MagJack ICMs: https://www.belfuse.com/media/datasheets/products/magjack%20ICMs/ds-mag-industrial-ethernet-magjack-icms.pdf
- Littelfuse 1812L: https://www.littelfuse.com/~/media/electronics/datasheets/resettable_ptcs/littelfuse_ptc_1812l_datasheet.pdf.pdf
- Bourns 3296: https://www.bourns.com/docs/Product-Datasheets/3296.pdf
