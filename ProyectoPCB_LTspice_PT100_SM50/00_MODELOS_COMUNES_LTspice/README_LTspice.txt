LTspice - Proyecto PCB: PT100 + SM-50
=======================================

Archivos incluidos
------------------
1) PT100_1CH_40a130_ideal.cir
   - Valida un canal PT100 de 40 C a 130 C.
   - Usa Iexc = 1 mA.
   - Resta V_RTD(40 C) = 115.4 mV.
   - Modela el INA828 como una fuente behavioral ideal.
   - Salida esperada: aprox. -4.5 V a +4.37 V.

2) SM50_1CH_bridge_ideal.cir
   - Valida un canal SM-50 como puente Wheatstone de 350 ohm.
   - Excitacion: +5 V y -5 V, total 10 V.
   - Sensibilidad: 3 mV/V.
   - Fondo de escala: aprox. 30 mV diferencial.
   - Usa la ganancia final:
       RG=340 ohm -> G≈146.3 -> salida FS≈+/-4.39 V

3) Sistema_4sensores_3PT100_1SM50_ideal.cir
   - Valida la version final con 3 PT100 y 1 SM-50.
   - Editar T1, T2, T3 y LoadFrac al inicio del archivo.

Como correrlos
--------------
1. Abrir LTspice.
2. File > Open.
3. Seleccionar un archivo .cir.
4. Click en Run.
5. Para ver resultados numericos:
   View > SPICE Error Log.
6. Para graficar:
   - PT100: hacer click en nodos out, out_filt, nPT.
   - SM-50: graficar V(sp,sn), V(out), V(out_filt).

Notas importantes
-----------------
- Estos archivos NO usan el modelo real del INA828. Se usa un INA ideal para validar calculos,
  rangos, ganancias y saturacion.
- Cuando estos resultados den bien, el siguiente paso es reemplazar BINA por el subcircuito real
  del INA828 y revisar el orden de pines del .subckt.
- El objetivo es evitar el problema de los simbolos sin etiquetas y validar primero el comportamiento
  matematico del acondicionamiento.
