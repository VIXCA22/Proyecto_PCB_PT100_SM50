.include ".\lib\sub\INA828.LIB"
.include ".\lib\sub\OPAx188.LIB"
.include ".\lib\sub\TPS7A3301.lib"
.include ".\lib\sub\tps7a4701_trans.lib"

* Modelo ideal REF3012 / REF30E para LTspice
* Orden de pines esperado: IN GND OUT
.subckt REF3012_IDEAL IN GND OUT
RIN IN GND 1G
VREF OUT GND DC 1.25
.ends REF3012_IDEAL


* ============================================================
* Modelo ideal REF30E1 para LTspice
* Referencia de precision ideal de 1.25 V
* Orden de pines: IN GND OUT
* IN  = entrada desde +15V_BBOX
* GND = tierra analogica
* OUT = VREF_1V25
* ============================================================
.subckt REF30E1_IDEAL IN GND OUT
RIN IN GND 1G
VREF OUT GND DC 1.25
.ends REF30E1_IDEAL

.include ".\lib\sub\PT100_clean.lib"

* ============================================================
* OPA_IDEAL para depuracion LTspice
* Orden de pines:
* IN+ IN- VCC VEE OUT
* ============================================================
.SUBCKT OPA_IDEAL INP INM VCC VEE OUT
RINP INP 0 1G
RINM INM 0 1G
BOUT OUT 0 V=limit(1e6*(V(INP)-V(INM)), V(VEE)+0.1, V(VCC)-0.1)
.ENDS OPA_IDEAL


* ============================================================
* Alias opamp2 ideal para depurar
* Orden de pines: IN+ IN- V+ V- OUT
* ============================================================
.SUBCKT opamp2 INP INM VCC VEE OUT
RINP INP 0 1G
RINM INM 0 1G
BOUT OUT 0 V=limit(1e6*(V(INP)-V(INM)), V(VEE)+0.1, V(VCC)-0.1)
.ENDS opamp2


* ============================================================
* UniversalOpamp2 ideal para depuracion PT100
* Orden de pines: IN+ IN- V+ V- OUT
* ============================================================
.SUBCKT UniversalOpamp2 INP INM VCC VEE OUT
RINP INP 0 1G
RINM INM 0 1G
BOUT OUT 0 V=limit(1e6*(V(INP)-V(INM)), V(VEE)+0.1, V(VCC)-0.1)
.ENDS UniversalOpamp2

