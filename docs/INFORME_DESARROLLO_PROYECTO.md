# Informe de desarrollo del proyecto

Fecha de redaccion: 2026-06-27.

## Proyecto

Este proyecto consistio en disenar y documentar una tarjeta de circuito impreso para el acondicionamiento de las senales de un sensor de temperatura PT100 y un sensor de carga/torque SM-50, pensada para integrarse al sistema de medicion de un motor trifasico de induccion del LabCES. La tarjeta se planteo como una etapa intermedia entre los sensores instalados en el banco y la interfaz de adquisicion, por lo que el diseno se enfoco en entregar senales de voltaje limpias, protegidas y dentro de rangos utiles para la B-Box o el sistema de adquisicion disponible.

El punto de partida fue una investigacion previa de LabCES orientada al calculo de eficiencia de motores mediante el estandar IEEE 112, metodo C. En ese trabajo se identifico la necesidad de medir temperatura, velocidad, potencia y carga para estimar la eficiencia del motor bajo distintos puntos de operacion. Tambien se documento que la temperatura se midio con sensores RTD instalados en los bobinados del estator y que la senal de carga requeria una revision cuidadosa, ya que durante pruebas previas el comportamiento del sensor no fue suficientemente confiable. Por esa razon, esta PCB se trabajo como una mejora de acondicionamiento y documentacion, no como una prueba experimental final del banco.

## Fuentes usadas

| Fuente | Uso en el proyecto |
| --- | --- |
| `Proyecto_eficiencia_LabCES-20260627T040051Z-3-001.zip/Reporte_final_P.pdf` | Contexto del banco de LabCES, estandar IEEE 112, metodo C, sensores usados y problemas encontrados en pruebas previas. |
| `Proyecto_eficiencia_LabCES-20260627T040051Z-3-001.zip/Caracterizacion_de_todo_los_sensores_y_lista_de_materiales.pdf` | Datos experimentales previos de PT100, salida de instrumentacion y prueba de carga. |
| `Proyecto_eficiencia_LabCES-20260627T040051Z-3-001.zip/Interface-Book-2022-Edition.pdf` | Fundamento general de celdas de carga, galgas extensiometricas, excitacion, sensibilidad y errores de montaje. |
| `C:/Users/kenne/Downloads/SM-S-Type.pdf` | Datos del sensor SM S-Type: salida nominal 3.0 mV/V, puente de 350 ohm y excitacion maxima de 15 VDC. |
| `docs/simulacion/pt100_sweep_ng_20260625.csv` | Valores usados para las graficas del canal PT100. |
| `docs/simulacion/sm50_sweep_positive_ng_20260625.csv` | Valores usados para las graficas del canal SM-50. |
| `PCB_PT100_SM50/COMPONENTES_A_USAR_KICAD.csv` | Lista base de componentes, bloques funcionales y MPN seleccionados. |
| `ProyectoPCB_LTspice_PT100_SM50/03_KICAD_LIBS/AUDITORIA_FOOTPRINTS.md` | Trazabilidad de simbolos, footprints, modelos 3D y fuentes primarias revisadas. |
| `docs/VALIDACION.md` | Resultado final de ERC, DRC y paquete de fabricacion. |

## Desarrollo por objetivos especificos

### 1. Comprension del problema y fundamentos del acondicionamiento

Primero se delimito el problema de medicion. El banco del LabCES requiere variables electricas y mecanicas para evaluar el desempeno de un motor trifasico de induccion. Dentro de esas variables, la temperatura y la carga/torque requieren acondicionamiento porque no entregan directamente una senal de voltaje amplia y facil de adquirir.

Para el PT100 se partio del comportamiento resistivo de un RTD. La resistencia aumenta con la temperatura, pero para convertir esa variacion en voltaje hace falta excitar el sensor con una corriente estable. En el diseno final se uso una referencia de 1.25 V y una resistencia de ajuste de 2.49 kohm, lo que produce una corriente cercana a 0.5 mA. Esta corriente genera una caida de tension sobre el PT100 que luego se amplifica y filtra.

Para el SM-50 se tomo como base el comportamiento de una celda de carga tipo puente de galgas extensiometricas. La hoja del sensor SM S-Type indica una salida nominal de 3.0 mV/V, resistencia de puente de 350 ohm y excitacion maxima de 15 VDC. Con una excitacion de 10 V, la senal diferencial esperada a escala completa queda alrededor de 30 mV. Por eso fue necesario usar un amplificador de instrumentacion con ganancia ajustada, de forma que la salida llegue a un rango cercano a 0-10 V sin saturar.

### 2. Verificacion mediante simulacion

La verificacion inicial se realizo en LTspice. Se separaron los canales para evitar que la depuracion de un sensor afectara al otro:

| Canal | Archivo principal | Proposito |
| --- | --- | --- |
| PT100 | `ProyectoPCB_LTspice_PT100_SM50/01_SENSOR_PT100/Sensor_PT100.asc` | Simular la resistencia del RTD, la corriente de excitacion, la amplificacion y la salida hacia B-Box. |
| SM-50 | `ProyectoPCB_LTspice_PT100_SM50/02_SENSOR_SM50/sensor_SM50.asc` | Simular el puente de galgas, la excitacion de 10 V, la ganancia del INA826 y la salida acondicionada. |

En el canal PT100 se uso el modelo cuadratico de resistencia para temperaturas positivas:

`R(T) = 100 * (1 + 3.9083e-3*T - 5.775e-7*T^2)`

La simulacion barre temperaturas representativas y calcula tanto la resistencia nominal como las condiciones baja y alta usadas para visualizar variacion. En el canal SM-50 se barrio la carga desde 0 lb hasta 50 lb y se comparo la salida real hacia B-Box contra una salida ideal y contra el limite de 10 V.

Las graficas del repositorio se generaron desde los CSV en `docs/simulacion/`, no desde valores escritos a mano. Esto permite que las figuras sean repetibles.

### 3. Diseno del esquematico en KiCad

Despues de validar rangos en LTspice, el circuito se traslado a KiCad. El esquematico final se organizo por bloques funcionales: alimentacion, proteccion, canal PT100, canal SM-50, filtrado y salida hacia la B-Box.

En el bloque de alimentacion se considero la disponibilidad de rieles desde la B-Box y la necesidad de una excitacion regulada para el SM-50. El regulador TPS7A4901 se selecciono para generar la referencia de excitacion positiva de 10 V del puente, manteniendo un margen adecuado frente al maximo permitido por el sensor. En el bloque PT100 se incorporo una referencia REF3012 de 1.25 V para establecer la corriente de excitacion. El uso de OPA2188 se justifico por su baja deriva, mientras que el INA826 se uso como amplificador de instrumentacion para senales diferenciales pequenas.

| Bloque | Decision tomada | Justificacion |
| --- | --- | --- |
| PT100 | Excitacion de aproximadamente 0.5 mA | Reduce autocalentamiento y genera una caida medible sobre el RTD. |
| PT100 | REF3012 como referencia de 1.25 V | Permite definir la corriente con una resistencia precisa. |
| PT100 | OPA2188 como operacional de precision | Baja deriva, adecuado para senales lentas de temperatura. |
| PT100/SM-50 | INA826 como amplificador diferencial | Su ganancia se define con una sola resistencia: `G = 1 + 49.4 kohm/RG`. |
| SM-50 | Excitacion de 10 V | Compatible con la hoja del SM S-Type y produce cerca de 30 mV a escala completa. |
| SM-50 | Rango de salida cercano a 0-10 V | Facilita la lectura por la B-Box sin exceder el limite esperado. |
| Entradas/salidas | Filtros RC y proteccion | Reducen ruido y protegen ante transitorios o manipulacion del banco. |

### 4. Migracion a PCB, footprints y fabricacion

La migracion a PCB se realizo en el proyecto `PCB_PT100_SM50/PCB_PT100_SM50.kicad_pro`. Se usaron librerias locales para no depender de rutas externas de KiCad y se auditaron los footprints contra componentes reales de la lista de compra. Esto fue importante porque varios archivos descargados de proveedores incluian modelos 3D, pero no siempre un footprint mecanico listo para fabricar.

Las borneras de sensores se cambiaron a METZ de paso 5.00 mm, correspondientes a AST0250304 para PT100 y AST0250404 para SM-50. Los integrados INA826AIDR y OPA2188AIDR quedaron con footprints SOIC-8 especificos y modelos 3D separados para evitar que un modelo equivocado se heredara desde un footprint generico. El RJ45 de interfaz B-Box se trabajo con el modelo Bel Fuse 2250066-1 y se reviso el ajuste mecanico dentro de KiCad.

Durante el cierre se corrigieron advertencias de serigrafia, referencias superpuestas y reglas de texto. La validacion final quedo con:

| Revision | Resultado |
| --- | --- |
| ERC KiCad | 0 errores, 0 advertencias |
| DRC KiCad | 0 violaciones |
| Pads desconectados | 0 |
| Errores de footprint | 0 |
| Paquete Gerber | Incluye cobre, mascara, pasta, serigrafia, contorno, `.gbrjob`, `.drl` y mapa de taladros |

El ZIP listo para fabricacion quedo en `docs/fabricacion/PCB_PT100_SM50_GERBERS_CON_DRILL.zip`.

### 5. Documentacion y repositorio

El repositorio se dejo organizado para que el proyecto pueda abrirse, revisarse y fabricarse sin depender de archivos temporales. Las simulaciones LTspice se conservaron en `ProyectoPCB_LTspice_PT100_SM50/`, el proyecto KiCad principal en `PCB_PT100_SM50/`, las figuras en `docs/figuras/`, los CSV de resultados en `docs/simulacion/` y la salida de fabricacion en `docs/fabricacion/`.

Tambien se generaron imagenes del esquematico, PCB 2D, PCB 3D, esquematicos LTspice y graficas. Esto permite que el README explique visualmente el estado del proyecto sin obligar a abrir KiCad o LTspice.

## Datos usados en las graficas

### Grafica: resistencia del PT100

Fuente: `docs/simulacion/pt100_sweep_ng_20260625.csv`.

| Temperatura (degC) | R PT100 nominal (ohm) | R baja (ohm) | R alta (ohm) |
| ---: | ---: | ---: | ---: |
| 0 | 100.000000 | 100.000000 | 101.952706 |
| 20 | 107.793500 | 105.849456 | 109.734656 |
| 50 | 119.397125 | 117.470406 | 121.320956 |
| 100 | 138.505500 | 136.607656 | 138.505500 |

La resistencia nominal simulada coincide con el comportamiento esperado de un PT100: alrededor de 100 ohm a 0 degC y 138.5 ohm a 100 degC. Esta tabla tambien sirve para comparar la simulacion con la caracterizacion previa, donde se reportaron promedios cercanos de 100 ohm, 107.793 ohm, 119.395 ohm y 138.5 ohm para 0, 20, 50 y 100 degC.

### Grafica: respuesta electrica del PT100

Fuente: `docs/simulacion/pt100_sweep_ng_20260625.csv`.

| Temperatura (degC) | Salida hacia B-Box (V) | Salida filtrada (V) |
| ---: | ---: | ---: |
| 0 | 2.328272 | 2.367077 |
| 20 | 2.509540 | 2.551366 |
| 50 | 2.779427 | 2.825751 |
| 100 | 3.223866 | 3.277597 |

La salida aumenta con la temperatura y queda dentro de un rango de adquisicion practico. El objetivo no fue medir directamente la resistencia con un multimetro, sino convertir la variacion del PT100 en un voltaje estable y filtrado.

### Grafica: tension diferencial del puente SM-50

Fuente: `docs/simulacion/sm50_sweep_positive_ng_20260625.csv`.

| Carga (lb) | Tension diferencial del puente (mV) |
| ---: | ---: |
| 0 | 0.000000 |
| 10 | 6.005764 |
| 20 | 12.026310 |
| 30 | 18.061161 |
| 40 | 24.110794 |
| 50 | 30.174255 |

La simulacion reproduce el orden de magnitud esperado por la hoja del SM S-Type: una celda de 3.0 mV/V excitada con 10 V entrega cerca de 30 mV a escala completa. El resultado a 50 lb es 30.174255 mV, por lo que el modelo usado para el puente es coherente con la especificacion.

### Grafica: salida acondicionada del SM-50

Fuente: `docs/simulacion/sm50_sweep_positive_ng_20260625.csv`.

| Carga (lb) | Salida real hacia B-Box (V) | Salida ideal (V) | Limite (V) |
| ---: | ---: | ---: | ---: |
| 0 | 0.016155 | -0.000028 | 10.000000 |
| 10 | 1.815897 | 1.837410 | 10.000000 |
| 20 | 3.619975 | 3.679269 | 10.000000 |
| 30 | 5.428405 | 5.525563 | 10.000000 |
| 40 | 7.241199 | 7.376311 | 10.000000 |
| 50 | 9.058375 | 9.231526 | 10.000000 |

La salida acondicionada crece casi linealmente y permanece por debajo del limite de 10 V. Esto permite usar el rango dinamico disponible sin saturar la etapa de adquisicion.

## Antecedente experimental usado como referencia

En esta etapa no se realizo una prueba experimental propia de la PCB final, porque el prototipo aun no se habia fabricado ni probado en el banco. Para no presentar una validacion inexistente, la parte experimental se redacta como antecedente documentado a partir de la investigacion previa entregada en el ZIP.

El reporte previo describe que se instalaron sensores RTD en los bobinados del estator del motor de induccion. Despues de la instalacion se verifico la resistencia de los sensores y se concluyo que los valores eran congruentes con la temperatura ambiente. Luego se construyo un circuito de instrumentacion en protoboard para convertir la variacion del RTD en una senal de voltaje y se realizo un barrido de temperatura.

### Datos previos de PT100

Fuente: `Caracterizacion_de_todo_los_sensores_y_lista_de_materiales.pdf`.

| Temperatura (degC) | Resistencia promedio reportada (ohm) |
| ---: | ---: |
| 0 | 100.000 |
| 20 | 107.793 |
| 50 | 119.395 |
| 100 | 138.500 |

Estos valores fueron utiles como referencia porque coinciden con el comportamiento esperado del modelo PT100 usado en la simulacion. Por lo tanto, aunque no reemplazan una calibracion de la PCB final, si justifican que el rango de resistencia elegido para la simulacion es razonable.

### Datos previos de salida de instrumentacion

Fuente: `Caracterizacion_de_todo_los_sensores_y_lista_de_materiales.pdf`.

| Temperatura medida (degC) | Salida de instrumentacion previa (V) |
| ---: | ---: |
| 40 | 2.00 |
| 50 | 2.03 |
| 60 | 2.36 |
| 70 | 2.73 |
| 80 | 3.03 |
| 90 | 3.30 |
| 100 | 3.50 |
| 110 | 3.80 |
| 120 | 4.20 |
| 130 | 4.38 |

La tendencia del antecedente fue creciente y aproximadamente lineal, lo cual respalda la idea de convertir la variacion resistiva del PT100 en una senal analogica. La PCB actual no copia exactamente ese circuito, ya que reemplaza la etapa de protoboard por una solucion con referencia estable, amplificadores de precision, filtros y proteccion.

### Datos previos de carga

Fuente: `Caracterizacion_de_todo_los_sensores_y_lista_de_materiales.pdf`.

| Porcentaje | Carga nominal (lb) | Carga nominal (kg) | Carga real aplicada (lb) | Carga real aplicada (kg) | Voltaje medido (mV) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.00000 | 0.00000 | 0.000 | 0.0 |
| 20 | 10 | 4.53592 | 2.77341 | 1.258 | -83.6 |
| 40 | 20 | 9.07184 | 11.09585 | 5.033 | -77.1 |
| 60 | 30 | 13.60776 | 19.27499 | 8.743 | -70.6 |
| 80 | 40 | 18.14368 | 30.40832 | 13.793 | -61.8 |
| 100 | 50 | 22.67960 | 38.60290 | 17.510 | -55.7 |

El reporte previo indica que la medicion de carga presento comportamiento oscilante y no completamente confiable. Por eso estos datos se usaron solo como referencia historica del banco, no como calibracion del canal SM-50 de la PCB. La decision tecnica fue simular el SM-50 desde su sensibilidad nominal de mV/V y dejar la calibracion experimental como una tarea posterior a la fabricacion.

## Alcance experimental y trabajo pendiente

La parte experimental propia de esta revision queda pendiente. Lo que si se completo fue:

- Simulacion electrica de ambos canales.
- Esquematico KiCad actualizado.
- PCB con footprints revisados.
- Modelos 3D y vistas para documentacion.
- Validacion ERC/DRC sin errores.
- Paquete Gerber con taladros listo para fabricar.

Despues de fabricar la PCB, la validacion recomendada es:

1. Alimentar la tarjeta desde la B-Box o fuente equivalente y verificar rieles.
2. Medir la excitacion del SM-50 y confirmar los 10 V antes de conectar el sensor.
3. Probar el canal PT100 con resistencias patron o caja de decadas antes del sensor real.
4. Registrar la salida del PT100 frente a temperaturas conocidas y ajustar la curva de calibracion.
5. Probar el SM-50 con masas conocidas, evitando cargas laterales y momentos mecanicos.
6. Ajustar la ganancia del canal SM-50 si la salida se acerca demasiado a 10 V.
7. Repetir las mediciones para estimar repetibilidad, error y dispersion.

## Conclusiones

El proyecto avanzo desde una necesidad experimental del banco de eficiencia del LabCES hasta una tarjeta PCB documentada y lista para fabricacion. Las referencias previas sirvieron para entender el contexto del motor, el metodo IEEE 112, la instalacion de sensores y los problemas reales encontrados durante ensayos anteriores. Las hojas de datos y documentos tecnicos permitieron convertir ese contexto en decisiones concretas de diseno: excitacion estable para PT100, acondicionamiento de senales diferenciales con INA826, excitacion de 10 V para el SM-50, proteccion de entradas/salidas y seleccion de footprints compatibles con los componentes comprados.

La validacion experimental final no se reporta como realizada. En su lugar, se deja una validacion por simulacion, verificacion de diseno y referencia a la investigacion previa. Esto mantiene la trazabilidad honesta del proyecto: la PCB esta preparada para fabricarse y probarse, pero sus curvas definitivas de calibracion deben obtenerse con el hardware real en laboratorio.

## Bibliografia y referencias

- Ignacio Soto Montero, `Reporte_final_P.pdf`, "Pruebas de laboratorio para el calculo de eficiencia en motores trifasicos de induccion", archivo incluido en `Proyecto_eficiencia_LabCES-20260627T040051Z-3-001.zip`.
- `Caracterizacion_de_todo_los_sensores_y_lista_de_materiales.pdf`, archivo incluido en `Proyecto_eficiencia_LabCES-20260627T040051Z-3-001.zip`.
- Interface, `Interface-Book-2022-Edition.pdf`, archivo incluido en `Proyecto_eficiencia_LabCES-20260627T040051Z-3-001.zip`.
- Interface, `SM-S-Type.pdf`, hoja de datos del sensor SM S-Type, archivo local en `C:/Users/kenne/Downloads/`.
- Texas Instruments, INA826 datasheet: https://www.ti.com/lit/ds/symlink/ina826.pdf
- Texas Instruments, OPA2188 datasheet: https://www.ti.com/lit/ds/symlink/opa2188.pdf
- Texas Instruments, TPS7A49/TPS7A4901 datasheet: https://www.ti.com/lit/ds/symlink/tps7a49.pdf
- Texas Instruments, REF30/REF30E datasheet: https://www.ti.com/lit/ds/symlink/ref30e.pdf
- Documentacion interna del repositorio: `docs/PROCESO_DISENO_CHATGPT.md`, `docs/REFERENCIAS_TECNICAS.md`, `docs/VALIDACION.md` y `ProyectoPCB_LTspice_PT100_SM50/03_KICAD_LIBS/AUDITORIA_FOOTPRINTS.md`.
