Proyecto PCB LTspice - PT100 y SM-50

Se eliminaron archivos generados por LTspice (.net, .raw, .log, .db) para evitar rutas antiguas.

Para PT100 abra:
  01_SENSOR_PT100/PT100_1CH_robusto.asc

El include principal es relativo:
  .include ".\proyecto_pcb_sensor_pt100.inc"

Si aparece una ruta antigua, borre el .net generado y vuelva a correr desde el .asc.

KiCad / footprints:
  Se agrego una libreria local en:
    03_KICAD_LIBS/

  Para usarla abra:
    01_SENSOR_PT100/Sensor_PT100.kicad_pro

  KiCad tomara las tablas locales:
    01_SENSOR_PT100/fp-lib-table
    01_SENSOR_PT100/sym-lib-table

  La guia de asignacion esta en:
    03_KICAD_LIBS/FOOTPRINTS_ASIGNADOS.md

  Cruce contra la orden de compra DigiKey 99915123:
    03_KICAD_LIBS/CRUCE_ORDEN_COMPRA_DK99915123.md

  Los modelos 3D de fabricante copiados desde los ZIPs estan en:
    03_KICAD_LIBS/3dmodels/

  Detalle de modelos STEP/STP:
    03_KICAD_LIBS/MODELOS_3D_FABRICANTE.md

  Auditoria de que esta verificado y que queda pendiente:
    03_KICAD_LIBS/AUDITORIA_FOOTPRINTS.md

  Importante: INA826 e INA828 no son pin-compatibles. Use el simbolo KiCad exacto
  del integrado que va a montar, no solo un footprint SOIC-8 generico.

  Nota de compra: las borneras METZ AST0250304/AST0250404 son de paso 5.00 mm.
  El conector 2250066-1 de la orden es Bel Fuse/TRP; su footprint local se llama
  RJ45_BelFuse_2250066-1.
