# Footprints KiCad para PT100 y SM50

Esta carpeta contiene una libreria local de KiCad para que los footprints no dependan
de rutas absolutas ni de librerias globales de otra instalacion.

## Archivos principales

- `ProyectoPCB.kicad_sym`: simbolos KiCad con pinout fisico o asignacion mecanica.
- `ProyectoPCB.pretty/`: footprints locales.
- `3dmodels/`: modelos STEP/STP copiados desde ZIPs o fuente de fabricante.
- `CRUCE_ORDEN_COMPRA_DK99915123.md`: cruce entre la orden DigiKey y la libreria local.

## Regla importante

No asignes solo un SOIC-8 generico a cualquier INA. El INA826 y el INA828 pueden usar
encapsulados SOIC-8, pero no son pin-compatibles. Usa el simbolo correcto:

- INA826: `ProyectoPCB:INA826_SOIC8`
- INA828: `ProyectoPCB:INA828_SOIC8`

En `01_SENSOR_PT100/Sensor_PT100.asc`, U1 usa `INA826`, aunque el texto del bloque
menciona INA828. Para PCB, decide cual integrado vas a montar y usa su simbolo KiCad
correspondiente.

## Asignaciones recomendadas

| Circuito | Referencias | Simbolo KiCad | Footprint |
| --- | --- | --- | --- |
| PT100 | Resistencias Yageo RT0805 de la compra | `ProyectoPCB:R_RT0805BRD` | `ProyectoPCB:R_0805_2012Metric_Yageo_RT0805BRD` |
| PT100 | Resistencias TE CPF0805 de la compra | `ProyectoPCB:R_CPF0805` | `ProyectoPCB:R_0805_2012Metric` |
| PT100 | Otras resistencias 0805 | `ProyectoPCB:R_0805` | `ProyectoPCB:R_0805_2012Metric` |
| PT100 | C1, C3, C4 si son 100nF AVX | `ProyectoPCB:C_08055C104K4T2A` | `ProyectoPCB:C_0805_2012Metric_AVX_08055C104K4T2A` |
| PT100 | C2 si usas el TDK 1uF | `ProyectoPCB:C_C2012X7R1H105K085AC` | `ProyectoPCB:C_0805_2012Metric_TDK_C2012X7R1H105K085AC` |
| PT100 | U1 actual del `.asc` | `ProyectoPCB:INA826_SOIC8` | `ProyectoPCB:SOIC-8_3.9x4.9mm_P1.27mm_INA826AIDR` |
| PT100 | U2 si montas OPA2188AIDR | `ProyectoPCB:OPA2188_SOIC8` | `ProyectoPCB:SOIC-8_3.9x4.9mm_P1.27mm_OPA2188AIDR` |
| PT100 | U4 / REF30E1_IDEAL | `ProyectoPCB:REF30E_SOT23` | `ProyectoPCB:SOT-23-3` |
| PT100 | Sensor RTD 3 hilos | `ProyectoPCB:PT100_3WIRE_CONN` | `ProyectoPCB:TerminalBlock_METZ_AST0250304_1x03_P5.00mm` |
| PT100 | Alimentacion +15/GND/-15 | `ProyectoPCB:PWR_BIPOLAR_3PIN` | `ProyectoPCB:TerminalBlock_METZ_AST0250304_1x03_P5.00mm` |
| PT100 | Salida a BBOX | `ProyectoPCB:BBOX_OUT_2PIN` | `ProyectoPCB:TerminalBlock_1x02_P5.08mm` |
| SM50 | Resistencias Yageo RT0805 de la compra | `ProyectoPCB:R_RT0805BRD` | `ProyectoPCB:R_0805_2012Metric_Yageo_RT0805BRD` |
| SM50 | Resistencias TE CPF0805 de la compra | `ProyectoPCB:R_CPF0805` | `ProyectoPCB:R_0805_2012Metric` |
| SM50 | C5 si compras KGM21 33nF | `ProyectoPCB:C_KGM21NR71H333KT` | `ProyectoPCB:C_0805_2012Metric` |
| SM50 | C5 si usas el ZIP 08055C333KAT2A | `ProyectoPCB:C_08055C333KAT2A` | `ProyectoPCB:C_0805_2012Metric_AVX_08055C333KAT2A` |
| SM50 | C3, C4 de 10nF AVX | `ProyectoPCB:C_08055C103K4T2A` | `ProyectoPCB:C_0805_2012Metric` |
| SM50 | C1, C2 de 10uF Murata | `ProyectoPCB:C_GRM21BR61E106KA73K` | `ProyectoPCB:C_0805_2012Metric` |
| SM50 | U2 | `ProyectoPCB:INA826_SOIC8` | `ProyectoPCB:SOIC-8_3.9x4.9mm_P1.27mm_INA826AIDR` |
| SM50 | U1 simplificado | `ProyectoPCB:TPS7A4701_10V_MODULE` | `ProyectoPCB:TPS7A4701_10V_Module_5Pin_P2.54mm` |
| SM50 | Regulador TPS7A4901 fisico, si redisenas esa etapa | `ProyectoPCB:TPS7A4901DGNT` | `ProyectoPCB:HVSSOP-8-1EP_DGN0008G_TPS7A4901DGNT` |
| SM50 | Celda SM50 / puente | `ProyectoPCB:SM50_4WIRE_CONN` | `ProyectoPCB:TerminalBlock_METZ_AST0250404_1x04_P5.00mm` |
| SM50 | Alimentacion +15/GND/-15 | `ProyectoPCB:PWR_BIPOLAR_3PIN` | `ProyectoPCB:TerminalBlock_METZ_AST0250304_1x03_P5.00mm` |
| SM50 | Salida a BBOX | `ProyectoPCB:BBOX_OUT_2PIN` | `ProyectoPCB:TerminalBlock_1x02_P5.08mm` |

## Componentes de la orden y ZIPs

| Componente | Simbolo KiCad | Footprint | Estado |
| --- | --- | --- | --- |
| INA826AIDR | `ProyectoPCB:INA826_SOIC8` | `ProyectoPCB:SOIC-8_3.9x4.9mm_P1.27mm_INA826AIDR` | Pinout y 3D enlazados. |
| OPA2188AIDR | `ProyectoPCB:OPA2188_SOIC8` | `ProyectoPCB:SOIC-8_3.9x4.9mm_P1.27mm_OPA2188AIDR` | Pinout y 3D enlazados. |
| REF3012AIDBZR | `ProyectoPCB:REF30E_SOT23` | `ProyectoPCB:SOT-23-3` | Pinout y 3D enlazados. |
| TPD4E1U06DBVR | `ProyectoPCB:TPD4E1U06DBVR` | `ProyectoPCB:SOT-23-6_DBV0006A_TPD4E1U06DBVR` | Pinout, footprint y 3D enlazados. |
| TPS7A4901DGNT | `ProyectoPCB:TPS7A4901DGNT` | `ProyectoPCB:HVSSOP-8-1EP_DGN0008G_TPS7A4901DGNT` | Pinout, PowerPAD y 3D enlazados. |
| SMF12CT1G | pendiente | `ProyectoPCB:SOT-363-6_SMF12CT1G` | Footprint mecanico y 3D listos; falta confirmar pinout. |
| 2250066-1 | `ProyectoPCB:J_2250066_1_MAGJACK` | `ProyectoPCB:RJ45_BelFuse_2250066-1` | Footprint desde drawing Bel C-2250066 y STEP enlazado; revisar ajuste 3D visual. |
| 1812L050/30PR | `ProyectoPCB:F_1812L050_30PR` | `ProyectoPCB:Fuse_1812_4532Metric_Littelfuse_1812L050-30PR` | Footprint listo; sin 3D local. |
| 3296W-1-102LF | `ProyectoPCB:RV_3296W_1_102LF` | `ProyectoPCB:Potentiometer_Bourns_3296W_1x03_P2.54mm` | Footprint listo; sin 3D local. |
| AST0250304 | `ProyectoPCB:PT100_3WIRE_CONN` o `ProyectoPCB:PWR_BIPOLAR_3PIN` | `ProyectoPCB:TerminalBlock_METZ_AST0250304_1x03_P5.00mm` | Paso 5.00 mm, sin 3D local. |
| AST0250404 | `ProyectoPCB:SM50_4WIRE_CONN` | `ProyectoPCB:TerminalBlock_METZ_AST0250404_1x04_P5.00mm` | Paso 5.00 mm, sin 3D local. |
| RT0805BRD07... | `ProyectoPCB:R_RT0805BRD` | `ProyectoPCB:R_0805_2012Metric_Yageo_RT0805BRD` | 3D Yageo enlazado solo a este footprint especifico. |
| CPF0805... | `ProyectoPCB:R_CPF0805` | `ProyectoPCB:R_0805_2012Metric` | 0805 mecanico; sin STEP exacto local. |
| 08055C104K4T2A | `ProyectoPCB:C_08055C104K4T2A` | `ProyectoPCB:C_0805_2012Metric_AVX_08055C104K4T2A` | STEP de DigiKey enlazado; land pattern oficial AVX pendiente. |
| 08055C103K4T2A | `ProyectoPCB:C_08055C103K4T2A` | `ProyectoPCB:C_0805_2012Metric` | 0805 mecanico; sin STEP exacto local. |
| KGM21NR71H333KT | `ProyectoPCB:C_KGM21NR71H333KT` | `ProyectoPCB:C_0805_2012Metric` | 0805 mecanico; sin STEP exacto local. |
| 08055C333KAT2A | `ProyectoPCB:C_08055C333KAT2A` | `ProyectoPCB:C_0805_2012Metric_AVX_08055C333KAT2A` | Este venia en ZIP, pero no es el MPN 33nF comprado. |
| C2012X7R1H105K085AC | `ProyectoPCB:C_C2012X7R1H105K085AC` | `ProyectoPCB:C_0805_2012Metric_TDK_C2012X7R1H105K085AC` | TDK confirma C2012/EIA 0805; STEP enlazado. |
| GRM21BR61E106KA73K | `ProyectoPCB:C_GRM21BR61E106KA73K` | `ProyectoPCB:C_0805_2012Metric` | 0805 mecanico; sin STEP exacto local. |

## Nota sobre TPS7A4701

El simbolo LTspice actual `TPS7A4701_10V` tiene solo 5 pines: `IN`, `EN`, `GND`,
`NR`, `OUT`. Por eso la libreria incluye un footprint de modulo/header de 5 pines.
Ese footprint no representa el integrado TPS7A4701 fisico completo. Si vas a montar
el IC real, hay que crear el simbolo completo del TPS7A4701 y asignar su encapsulado
real antes de fabricar.

Nota adicional: `TPS7A4901DGNT` no es `TPS7A4701`. El footprint/simbolo de
`TPS7A4901DGNT` esta disponible, pero no debe reemplazar automaticamente el bloque
LTspice `TPS7A4701_10V`.

## Fuentes de pinout y land pattern consultadas

- INA826: https://www.ti.com/lit/ds/symlink/ina826.pdf
- INA828: https://www.ti.com/lit/ds/symlink/ina828.pdf
- OPA188: https://www.ti.com/lit/ds/symlink/opa188.pdf
- OPA2188: https://www.ti.com/lit/ds/symlink/opa2188.pdf
- REF30E: https://www.ti.com/lit/ds/symlink/ref30e.pdf
- TPD4E1U06: https://www.ti.com/lit/ds/symlink/tpd4e1u06.pdf
- TPS7A49/TPS7A4901: https://www.ti.com/lit/ds/symlink/tps7a49.pdf
- TDK C2012X7R1H105K085AC: https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=C2012X7R1H105K085AC
- Bel 2250066-1: https://www.belfuse.com/products/ethernet/magjacks-icms/2250066-1
- Bel drawing C-2250066: https://www.belfuse.com/media/drawings/products/magjack%20ICMs/dr-mag-2250066.pdf
- Littelfuse 1812L: https://www.littelfuse.com/~/media/electronics/datasheets/resettable_ptcs/littelfuse_ptc_1812l_datasheet.pdf.pdf
- Bourns 3296: https://www.bourns.com/docs/Product-Datasheets/3296.pdf
