# Proyecto KiCad - PCB PT100 y SM-50

Esta carpeta contiene el diseno KiCad principal de la tarjeta de acondicionamiento de senales para sensores PT100 y SM-50.

## Archivos principales

| Archivo o carpeta | Uso |
| --- | --- |
| `PCB_PT100_SM50.kicad_pro` | Proyecto KiCad principal. |
| `PCB_PT100_SM50.kicad_sch` | Esquematico del circuito de acondicionamiento. |
| `PCB_PT100_SM50.kicad_pcb` | Layout de la PCB. |
| `symbols/` | Librerias de simbolos locales. |
| `footprints/` | Huellas locales usadas por la PCB. |
| `3d/` | Modelos 3D vinculados a las huellas. |
| `bom/` | Lista de materiales y referencia de compra. |
| `docs/` | Imagenes y soporte visual del diseno. |
| `outputs/` | Reportes de validacion generados por KiCad. |

## Estado de validacion

El cierre de validacion documentado fue generado con KiCad 9 y no reporta violaciones:

```text
../docs/validacion/erc_final_20260626.rpt
../docs/validacion/drc_final_20260626.rpt
```

La carpeta `outputs/` conserva reportes locales intermedios del PCB. Los reportes anteriores con warnings eran de sincronizacion de librerias, no de conexion electrica. Se registro la libreria faltante `ProyectoPCB` y se dejo la regla `lib_symbol_mismatch` en `ignore` porque varios simbolos fueron ajustados localmente para el esquematico.

## Uso rapido

1. Abrir `PCB_PT100_SM50.kicad_pro` en KiCad 9.
2. Revisar el esquematico y correr ERC.
3. Revisar el PCB y correr DRC antes de fabricar.
4. Usar las librerias locales incluidas en `sym-lib-table` y `fp-lib-table`.

## Nota sobre LTspice

Los archivos `.asy` y `.lib` pertenecen a simulacion LTspice. No se deben importar como simbolos o footprints KiCad; para KiCad se usan `.kicad_sym`, `.kicad_mod` y modelos `.step/.wrl`.
