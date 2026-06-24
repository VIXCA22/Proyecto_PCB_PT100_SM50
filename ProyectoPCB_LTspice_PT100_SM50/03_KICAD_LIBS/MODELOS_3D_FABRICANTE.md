# Modelos 3D de fabricante

Los ZIPs indicados contienen modelos STEP/STP, no siempre footprints KiCad
completos. Copie los modelos dentro del proyecto para no depender de rutas en
`Downloads`.

Carpeta local:

```text
03_KICAD_LIBS/3dmodels/
```

## Modelos copiados

| Componente | Archivo local | Uso actual |
| --- | --- | --- |
| 2250066-1 | `2250066-1_BelFuse.stp` | Enlazado al footprint `RJ45_BelFuse_2250066-1`. El patron de taladros se tomo del drawing Bel/TRP C-2250066; revisar ajuste visual del STEP en KiCad antes de fabricar. |
| C2012X7R1H105K085AC | `C2012X7R1H105K085AC_TDK_0805_1uF.step` | Enlazado al footprint especifico `C_0805_2012Metric_TDK_C2012X7R1H105K085AC`. |
| 08055C333KAT2A | `08055C333KAT2A_AVX_0805_33nF.step` | Enlazado al footprint especifico `C_0805_2012Metric_AVX_08055C333KAT2A`. Ojo: la orden compra `KGM21NR71H333KT`, no este MPN. |
| 08055C104K4T2A | `08055C104K4T2A_AVX_0805_100nF.step` | Enlazado al footprint especifico `C_0805_2012Metric_AVX_08055C104K4T2A`. |
| RT0805BRD0710KL / 1KL / 200RL / 49R9L / 73K2L / 2K49L | `RT0805BRD_Yageo_0805.step` | Enlazado al footprint especifico `R_0805_2012Metric_Yageo_RT0805BRD`. |
| SMF12CT1G | `SMF12CT1G_ONS_SOT363-6.step` | Enlazado al footprint `SOT-363-6_SMF12CT1G`; falta confirmar simbolo/pinout antes de usarlo electricamente. |
| TPD4E1U06DBVR | `TPD4E1U06DBVR_TI_SOT23-6_DBV0006A.stp` | Enlazado al footprint y simbolo `TPD4E1U06DBVR`. |
| TPS7A4901DGNT | `TPS7A4901DGNT_TI_HVSSOP8_DGN0008G.stp` | Enlazado al footprint y simbolo `TPS7A4901DGNT`. |
| REF3012AIDBZR | `REF3012AIDBZR_TI_SOT23_DBZ0003A.stp` | Enlazado al footprint `SOT-23-3` y simbolo `REF30E_SOT23`. |
| OPA2188AIDR | `OPA2188AIDR_TI_SOIC8_D0008A.stp` | Enlazado al footprint especifico `SOIC-8_3.9x4.9mm_P1.27mm_OPA2188AIDR`. |
| INA826AIDR | `INA826AIDR_TI_SOIC8_D0008A.stp` | Enlazado al footprint especifico `SOIC-8_3.9x4.9mm_P1.27mm_INA826AIDR`. |

## Piezas de la orden sin STEP local exacto

| Componente | Estado |
| --- | --- |
| 08055C103K4T2A | Simbolo `C_08055C103K4T2A`, footprint generico `C_0805_2012Metric`, sin 3D exacto local. |
| KGM21NR71H333KT | Simbolo `C_KGM21NR71H333KT`, footprint generico `C_0805_2012Metric`, sin 3D exacto local. |
| GRM21BR61E106KA73K | Simbolo `C_GRM21BR61E106KA73K`, footprint generico `C_0805_2012Metric`, sin 3D exacto local. |
| CPF0805B160RE1 / 180RE1 / 200RE1 | Simbolo `R_CPF0805`, footprint generico `R_0805_2012Metric`, sin 3D exacto local. |
| 1812L050/30PR | Simbolo y footprint `Fuse_1812_4532Metric_Littelfuse_1812L050-30PR`, sin 3D local. |
| AST0250304 / AST0250404 | Footprints METZ a paso 5.00 mm, sin 3D local. |
| 3296W-1-102LF | Simbolo y footprint `Potentiometer_Bourns_3296W_1x03_P2.54mm`, sin 3D local. |

## Notas de uso

- Los modelos 3D estan enlazados con rutas relativas usando `${KIPRJMOD}/../03_KICAD_LIBS/3dmodels/...`.
- Si se abre `01_SENSOR_PT100/Sensor_PT100.kicad_pro` o un proyecto dentro de `02_SENSOR_SM50`, esas rutas siguen apuntando al mismo lugar.
- El footprint generico `R_0805_2012Metric` ya no tiene modelo 3D Yageo; el modelo Yageo quedo solo en `R_0805_2012Metric_Yageo_RT0805BRD`.
- Los footprints genericos `C_0805_2012Metric` y `SOIC-8_3.9x4.9mm_P1.27mm` no tienen modelo 3D especifico para evitar mostrar una pieza equivocada.
