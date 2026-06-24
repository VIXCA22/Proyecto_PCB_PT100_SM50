# Cruce orden DigiKey 99915123 contra libreria KiCad

Fuente local: `C:\Users\kenne\Downloads\SALESORDER_EMAIL99915123.pdf`.

| Item | MPN comprado | Simbolo KiCad | Footprint | 3D local | Estado |
| --- | --- | --- | --- | --- | --- |
| INA826AIDR | INA826AIDR | `INA826_SOIC8` | `SOIC-8_3.9x4.9mm_P1.27mm_INA826AIDR` | si | Listo. |
| OPA2188AIDR | OPA2188AIDR | `OPA2188_SOIC8` | `SOIC-8_3.9x4.9mm_P1.27mm_OPA2188AIDR` | si | Listo. |
| REF3012AIDBZR | REF3012AIDBZR | `REF30E_SOT23` | `SOT-23-3` | si | Listo. |
| TPS7A4901DGNT | TPS7A4901DGNT | `TPS7A4901DGNT` | `HVSSOP-8-1EP_DGN0008G_TPS7A4901DGNT` | si | Listo; no reemplaza el bloque LTspice TPS7A4701 sin redisenar. |
| TPD4E1U06DBVR | TPD4E1U06DBVR | `TPD4E1U06DBVR` | `SOT-23-6_DBV0006A_TPD4E1U06DBVR` | si | Listo. |
| SMF12CT1G | SMF12CT1G | pendiente | `SOT-363-6_SMF12CT1G` | si | Footprint mecanico listo; falta pinout funcional. |
| PTC 1812 | 1812L050/30PR | `F_1812L050_30PR` | `Fuse_1812_4532Metric_Littelfuse_1812L050-30PR` | no | Listo mecanicamente. |
| Yageo 2.49k | RT0805BRD072K49L | `R_RT0805BRD` | `R_0805_2012Metric_Yageo_RT0805BRD` | si | Listo. |
| Yageo 1k | RT0805BRD071KL | `R_RT0805BRD` | `R_0805_2012Metric_Yageo_RT0805BRD` | si | Listo. |
| Yageo 49.9R | RT0805BRD0749R9L | `R_RT0805BRD` | `R_0805_2012Metric_Yageo_RT0805BRD` | si | Listo. |
| Yageo 200R | RT0805BRD07200RL | `R_RT0805BRD` | `R_0805_2012Metric_Yageo_RT0805BRD` | si | Listo. |
| Yageo 10k | RT0805BRD0710KL | `R_RT0805BRD` | `R_0805_2012Metric_Yageo_RT0805BRD` | si | Listo. |
| Yageo 73.2k | RT0805BRD0773K2L | `R_RT0805BRD` | `R_0805_2012Metric_Yageo_RT0805BRD` | si | Listo. |
| AVX 100nF | 08055C104K4T2A | `C_08055C104K4T2A` | `C_0805_2012Metric_AVX_08055C104K4T2A` | si | Listo con STEP del ZIP. |
| AVX 10nF | 08055C103K4T2A | `C_08055C103K4T2A` | `C_0805_2012Metric` | no | Footprint 0805 listo; falta STEP exacto. |
| AVX 33nF | KGM21NR71H333KT | `C_KGM21NR71H333KT` | `C_0805_2012Metric` | no | Footprint 0805 listo; no confundir con ZIP 08055C333KAT2A. |
| TDK 1uF | C2012X7R1H105K085AC | `C_C2012X7R1H105K085AC` | `C_0805_2012Metric_TDK_C2012X7R1H105K085AC` | si | Listo. |
| Murata 10uF | GRM21BR61E106KA73K | `C_GRM21BR61E106KA73K` | `C_0805_2012Metric` | no | Footprint 0805 listo; falta STEP exacto. |
| METZ 4 pos | AST0250404 | `SM50_4WIRE_CONN` | `TerminalBlock_METZ_AST0250404_1x04_P5.00mm` | no | Listo mecanicamente, paso 5.00 mm. |
| METZ 3 pos | AST0250304 | `PT100_3WIRE_CONN` / `PWR_BIPOLAR_3PIN` | `TerminalBlock_METZ_AST0250304_1x03_P5.00mm` | no | Listo mecanicamente, paso 5.00 mm; revisar cantidad comprada contra cantidad real de conectores. |
| Bourns trimmer | 3296W-1-102LF | `RV_3296W_1_102LF` | `Potentiometer_Bourns_3296W_1x03_P2.54mm` | no | Listo; footprint usa orden fisico de pads 1-3-2. |
| TE 160R | CPF0805B160RE1 | `R_CPF0805` | `R_0805_2012Metric` | no | Footprint 0805 listo. |
| TE 180R | CPF0805B180RE1 | `R_CPF0805` | `R_0805_2012Metric` | no | Footprint 0805 listo. |
| TE 200R | CPF0805B200RE1 | `R_CPF0805` | `R_0805_2012Metric` | no | Footprint 0805 listo. |
| Bel MagJack | 2250066-1 | `J_2250066_1_MAGJACK` | `RJ45_BelFuse_2250066-1` | si | Footprint desde drawing Bel; revisar calce 3D visual. |

## Observaciones importantes

- La orden compra `KGM21NR71H333KT` para 33 nF. El ZIP anterior `08055C333KAT2A` no corresponde exactamente a ese MPN.
- La orden compra borneras METZ `AST0250304` y `AST0250404` de 5.00 mm, no 5.08 mm.
- El conector `2250066-1` es Bel Fuse/TRP en la orden, no TE.
- El modelo 3D Yageo ya no esta en el resistor 0805 generico; quedo en el footprint especifico Yageo.
