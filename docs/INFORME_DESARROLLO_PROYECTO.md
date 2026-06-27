# Informe de desarrollo del proyecto

Fecha de redaccion: 2026-06-27.

## Proyecto

Este proyecto consistio en disenar y documentar una tarjeta de circuito impreso para el acondicionamiento de las senales de un sensor de temperatura PT100 y un sensor de carga/torque SM-50, pensada para integrarse al sistema de medicion de un motor trifasico de induccion del LabCES. La tarjeta se planteo como una etapa intermedia entre los sensores instalados en el banco y la interfaz de adquisicion, por lo que el diseno se enfoco en entregar senales de voltaje limpias, protegidas y dentro de rangos utiles para la B-Box o el sistema de adquisicion disponible.

El punto de partida fue una investigacion previa de LabCES orientada al calculo de eficiencia de motores mediante el estandar IEEE 112, metodo C. En ese trabajo se identifico la necesidad de medir temperatura, velocidad, potencia y carga para estimar la eficiencia del motor bajo distintos puntos de operacion. Tambien se documento que la temperatura se midio con sensores RTD instalados en los bobinados del estator y que la senal de carga requeria una revision cuidadosa, ya que durante pruebas previas el comportamiento del sensor no fue suficientemente confiable. Por esa razon, esta PCB se trabajo como una mejora de acondicionamiento y documentacion, no como una prueba experimental final del banco.

## Fuentes usadas

| Fuente | Uso en el proyecto |
| --- | --- |
| `Proyecto_PCB_TODO_con_referencias.zip/00_INDICE_DE_ARCHIVOS.txt` | Indice del paquete completo de referencias, memorias, capturas, datasheets y bibliografia. |
| `Proyecto_PCB_TODO_con_referencias.zip/00_REFERENCIAS_IMPORTANTES.txt` | Bibliografia principal en formato LaTeX/bibitem para defender el proyecto. |
| `Proyecto_PCB_TODO_con_referencias.zip/calculos_memorias/memoria_calculo_PCB0.docx` | Memoria preliminar de calculo para PT100 y SM-50; usada para documentar la evolucion de los parametros. |
| `Proyecto_PCB_TODO_con_referencias.zip/referencias_bibliografia/fuentes_pcb_sensores_motor.pdf` | Marco bibliografico sobre PCB de acondicionamiento, sensores de torque/temperatura y motores de induccion. |
| `Proyecto_PCB_TODO_con_referencias.zip/instrumentacion_puentes_adc/sloa034.pdf` | Referencia de TI para acondicionamiento de sensores resistivos en puente Wheatstone. |
| `Proyecto_PCB_TODO_con_referencias.zip/instrumentacion_puentes_adc/sboa247a.pdf` | Referencia de TI para amplificacion de puentes de galgas extensiometricas en una sola alimentacion. |
| `Proyecto_PCB_TODO_con_referencias.zip/instrumentacion_puentes_adc/an43f.pdf` | Nota de Analog Devices sobre circuitos de puente. |
| `Proyecto_PCB_TODO_con_referencias.zip/instrumentacion_puentes_adc/an96fa.pdf` | Nota de Analog Devices sobre medicion de puentes con ADC delta-sigma y consideraciones de ruido/resolucion. |
| `Proyecto_PCB_TODO_con_referencias.zip/datasheets_sensores/Electrical_Wiring_Diagram.pdf` | Cableado de celdas de carga Interface, colores de cable, excitacion y senales. |
| `Proyecto_PCB_TODO_con_referencias.zip/pcb_kicad_ruido_fabricacion/User-Manual-BoomBox.pdf` | Especificaciones practicas de entradas analogicas BoomBox/B-Box, RJ45, Cat5e, alimentacion de sensores y limites de entrada. |
| `Proyecto_eficiencia_LabCES-20260627T040051Z-3-001.zip/Reporte_final_P.pdf` | Contexto del banco de LabCES, estandar IEEE 112, metodo C, sensores usados y problemas encontrados en pruebas previas. |
| `Proyecto_eficiencia_LabCES-20260627T040051Z-3-001.zip/Caracterizacion_de_todo_los_sensores_y_lista_de_materiales.pdf` | Datos experimentales previos de PT100, salida de instrumentacion y prueba de carga. |
| `Proyecto_eficiencia_LabCES-20260627T040051Z-3-001.zip/Interface-Book-2022-Edition.pdf` | Fundamento general de celdas de carga, galgas extensiometricas, excitacion, sensibilidad y errores de montaje. |
| `C:/Users/kenne/Downloads/SM-S-Type.pdf` | Datos del sensor SM S-Type: salida nominal 3.0 mV/V, puente de 350 ohm y excitacion maxima de 15 VDC. |
| `docs/simulacion/pt100_sweep_ng_20260625.csv` | Valores usados para las graficas del canal PT100. |
| `docs/simulacion/sm50_sweep_positive_ng_20260625.csv` | Valores usados para las graficas del canal SM-50. |
| `PCB_PT100_SM50/COMPONENTES_A_USAR_KICAD.csv` | Lista base de componentes, bloques funcionales y MPN seleccionados. |
| `ProyectoPCB_LTspice_PT100_SM50/03_KICAD_LIBS/AUDITORIA_FOOTPRINTS.md` | Trazabilidad de simbolos, footprints, modelos 3D y fuentes primarias revisadas. |
| `docs/VALIDACION.md` | Resultado final de ERC, DRC y paquete de fabricacion. |

El paquete `Proyecto_PCB_TODO_con_referencias.zip` se uso como fuente documental, pero no se agrego completo al repositorio para evitar subir archivos pesados y duplicados. En el repositorio se conserva la sintesis tecnica, los datos numericos regenerables y los archivos finales de diseno.

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

### Evolucion desde la memoria de calculo preliminar

La memoria `memoria_calculo_PCB0.docx` fue importante para fijar el razonamiento inicial: calcular la sensibilidad del PT100, estimar autocalentamiento, separar offset de variacion util, calcular ganancia del amplificador de instrumentacion, y dimensionar el canal SM-50 desde una senal de puente de aproximadamente 30 mV a escala completa. Sin embargo, esa memoria corresponde a una etapa previa del proyecto y no todos sus valores quedaron iguales en la revision final.

La diferencia principal es el destino de la senal. En la memoria preliminar se penso en aprovechar un ADC de 3.3 V directamente, mientras que el proyecto final se adapto a la BoomBox/B-Box, que permite entradas analogicas diferenciales de hasta el orden de 10 V y entrega alimentacion de sensores por el cable analogico. Por eso el canal SM-50 final usa una ganancia mayor que la memoria preliminar, para aprovechar mejor el rango de entrada de la B-Box sin exceder el limite de 10 V. En el PT100 se redujo la corriente de excitacion a 0.5 mA para disminuir autocalentamiento y mantener una respuesta de voltaje compatible con el rango documentado en simulacion.

| Aspecto | Memoria preliminar | Revision final en repo |
| --- | --- | --- |
| PT100, corriente de excitacion | 1 mA | 0.5 mA, definida por REF3012 de 1.25 V y RSET de 2.49 kohm |
| PT100, salida objetivo | 0 a 3.3 V hacia ADC | Aproximadamente 2.33 a 3.22 V hacia B-Box en el barrido 0-100 degC |
| PT100, amplificador | INA828 como opcion inicial | INA826/OPA2188 segun BOM y simbolos finales |
| SM-50, sensibilidad base | 3 mV/V con 10 V, es decir cerca de 30 mV FS | Igual: 3 mV/V, puente de 350 ohm y excitacion de 10 V |
| SM-50, ganancia calculada | Cerca de 100 V/V para salida de 3.3 V | Cerca de 306 V/V en LTspice con RG = 162 ohm, para salida real menor a 10 V |
| Interfaz de adquisicion | ADC generico de 3.3 V | BoomBox/B-Box con entrada analogica diferencial, RJ45 y alimentacion +/-15 V |

Esta evolucion no se considera una contradiccion, sino una decision de integracion: se conservaron los fundamentos de sensibilidad, filtrado y amplificacion diferencial, pero se recalcularon rangos para la interfaz real de adquisicion.

### 3. Diseno del esquematico en KiCad

Despues de validar rangos en LTspice, el circuito se traslado a KiCad. El esquematico final se organizo por bloques funcionales: alimentacion, proteccion, canal PT100, canal SM-50, filtrado y salida hacia la B-Box.

En el bloque de alimentacion se considero la disponibilidad de rieles desde la B-Box y la necesidad de una excitacion regulada para el SM-50. El regulador TPS7A4901 se selecciono para generar la referencia de excitacion positiva de 10 V del puente, manteniendo un margen adecuado frente al maximo permitido por el sensor. En el bloque PT100 se incorporo una referencia REF3012 de 1.25 V para establecer la corriente de excitacion. El uso de OPA2188 se justifico por su baja deriva, mientras que el INA826 se uso como amplificador de instrumentacion para senales diferenciales pequenas.

El manual de la BoomBox/B-Box reforzo la decision de usar conectores RJ45 blindados y cable Cat5e para la interfaz analogica. La entrada analogica puede configurarse como diferencial de alta impedancia o como entrada de baja impedancia, incluye ganancia y filtro programable, y el conector entrega rieles de alimentacion para sensores. Para el diseno de esta PCB se tomaron como restricciones practicas los rieles +/-15 V disponibles por el cable y los limites de entrada de aproximadamente +/-10 V en modo diferencial, por lo que las salidas acondicionadas se mantuvieron por debajo de 10 V.

| Pin RJ45 BoomBox analogica | Funcion reportada en manual |
| ---: | --- |
| 1, 2 | +15 V para sensores |
| 3, 6 | 0 V |
| 4 | Entrada positiva / entrada de corriente |
| 5 | Entrada negativa / tierra |
| 7, 8 | -15 V para sensores |

El diagrama de cableado de Interface para celdas de carga tambien justifico mantener una entrada diferencial con lineas de excitacion y senal separadas. En la PCB se llevo esa idea al conector SM-50 de 4 hilos: `+EXC_SM50`, `-EXC_SM50`, `SENP_SM50` y `SENN_SM50`.

| Bloque | Decision tomada | Justificacion |
| --- | --- | --- |
| PT100 | Excitacion de aproximadamente 0.5 mA | Reduce autocalentamiento y genera una caida medible sobre el RTD. |
| PT100 | REF3012 como referencia de 1.25 V | Permite definir la corriente con una resistencia precisa. |
| PT100 | OPA2188 como operacional de precision | Baja deriva, adecuado para senales lentas de temperatura. |
| PT100/SM-50 | INA826 como amplificador diferencial | Su ganancia se define con una sola resistencia: `G = 1 + 49.4 kohm/RG`. |
| SM-50 | Excitacion de 10 V | Compatible con la hoja del SM S-Type y produce cerca de 30 mV a escala completa. |
| SM-50 | Rango de salida cercano a 0-10 V | Facilita la lectura por la B-Box sin exceder el limite esperado. |
| Entradas/salidas | Filtros RC y proteccion | Reducen ruido y protegen ante transitorios o manipulacion del banco. |

Las notas de aplicacion SLOA034 y SBOA247A respaldan la arquitectura usada para el SM-50: un puente Wheatstone genera una senal diferencial pequena, el amplificador de instrumentacion rechaza el modo comun y la ganancia se elige para escalar la senal al rango de lectura. La nota AN96 se uso como advertencia de diseno: aumentar la ganancia solo para llenar todo el ADC no siempre mejora la resolucion, porque tambien entran ruido, deriva y limitaciones del frente analogico. En este proyecto la ganancia se eligio con una restriccion practica: no saturar la entrada de la B-Box y dejar margen hasta 10 V.

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

- `Proyecto_PCB_TODO_con_referencias.zip`, paquete completo de referencias bibliograficas, memoria de calculo, datasheets, capturas, notas de instrumentacion y documentos de PCB/fabricacion.
- `memoria_calculo_PCB0.docx`, "Memoria de calculo PCB de Acondicionamiento de Senal Sensores PT100 y SM-50", archivo incluido en `Proyecto_PCB_TODO_con_referencias.zip`.
- `fuentes_pcb_sensores_motor.pdf`, "Fuentes para el desarrollo de una PCB de acondicionamiento de sensores de torque y temperatura en motores de induccion", archivo incluido en `Proyecto_PCB_TODO_con_referencias.zip`.
- Ignacio Soto Montero, `Reporte_final_P.pdf`, "Pruebas de laboratorio para el calculo de eficiencia en motores trifasicos de induccion", archivo incluido en `Proyecto_eficiencia_LabCES-20260627T040051Z-3-001.zip`.
- `Caracterizacion_de_todo_los_sensores_y_lista_de_materiales.pdf`, archivo incluido en `Proyecto_eficiencia_LabCES-20260627T040051Z-3-001.zip`.
- Interface, `Interface-Book-2022-Edition.pdf`, archivo incluido en `Proyecto_eficiencia_LabCES-20260627T040051Z-3-001.zip`.
- Interface, `SM-S-Type.pdf`, hoja de datos del sensor SM S-Type, archivo local en `C:/Users/kenne/Downloads/`.
- Interface, `Electrical_Wiring_Diagram.pdf`, diagrama electrico y cableado de celdas de carga, archivo incluido en `Proyecto_PCB_TODO_con_referencias.zip`.
- imperix, `User-Manual-BoomBox.pdf`, manual de la plataforma BoomBox/B-Box, archivo incluido en `Proyecto_PCB_TODO_con_referencias.zip`.
- Texas Instruments, "Signal Conditioning Wheatstone Resistive Bridge Sensors", SLOA034: https://www.ti.com/lit/an/sloa034/sloa034.pdf
- Texas Instruments, "Single-Supply Strain Gauge Bridge Amplifier Circuit", SBOA247A: https://www.ti.com/lit/pdf/sboa247
- Analog Devices, "AN-43: Bridge Circuits": https://www.analog.com/en/resources/app-notes/an-43f.html
- Analog Devices, "AN-96: Delta Sigma ADC Bridge Measurement Techniques": https://www.analog.com/en/resources/app-notes/an-96fa.html
- Texas Instruments, INA826 datasheet: https://www.ti.com/lit/ds/symlink/ina826.pdf
- Texas Instruments, OPA2188 datasheet: https://www.ti.com/lit/ds/symlink/opa2188.pdf
- Texas Instruments, TPS7A49/TPS7A4901 datasheet: https://www.ti.com/lit/ds/symlink/tps7a49.pdf
- Texas Instruments, REF30/REF30E datasheet: https://www.ti.com/lit/ds/symlink/ref30e.pdf
- Documentacion interna del repositorio: `docs/PROCESO_DISENO_CHATGPT.md`, `docs/REFERENCIAS_TECNICAS.md`, `docs/VALIDACION.md` y `ProyectoPCB_LTspice_PT100_SM50/03_KICAD_LIBS/AUDITORIA_FOOTPRINTS.md`.
