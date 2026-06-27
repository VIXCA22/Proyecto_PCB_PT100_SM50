# Revisión de footprints y modelos 3D - 2026-06-23

Proyecto revisado: `C:\Users\kenne\Documents\KiCad\PCB_PT100_SM50`

## Cambios aplicados

- `ProyectoPCB:2250066-1`
  - Huella corregida contra el dibujo oficial Bel Fuse / TRP `C-2250066`.
  - Se ajustó la fila de pines 2/4/6/8 para que no quede espejada respecto al layout sugerido.
  - Se agregaron los 2 taladros NPTH de 3.2 mm para postes plásticos.
  - Se corrigieron taladros de señal a 0.89 mm y blindaje a 1.57 mm.
  - Modelo 3D: `${KIPRJMOD}/3d/2250066-1.stp`, offset `Z=5.75`, escala `(1 1 1)`.
  - Nota: el STEP del ZIP local del RJ45 parece renderizar solo subpartes/elementos metálicos, no un cuerpo completo claramente visible del jack.

- `ProyectoPCB:SMF12CT1G_SC88_SOT363`
  - Se agregó modelo 3D local `${KIPRJMOD}/3d/SOT-363-6_2P2X1P35_ONS.step`.

- `ProyectoPCB_Footprints:PPTC_1812L050_30PR_1812`
  - Se agregó modelo 3D 1812 global de KiCad a la librería y a las 4 instancias colocadas.

- `ProyectoPCB_Footprints:Bourns_3296W_1_102LF`
  - Se corrigió la huella custom al orden físico `1-3-2` indicado por Bourns para 3296W-1.

- `ProyectoPCB_Footprints:REF3012AIDBZR_SOT-23-3`
  - Se agregó modelo 3D local `${KIPRJMOD}/3d/DBZ0003A.stp`.

- `ProyectoPCB_Footprints:TPS7A4901DGNT_HVSSOP-8-EP`
  - Se agregó modelo 3D local `${KIPRJMOD}/3d/DGN0008G.stp`.

- Terminales METZ
  - Se agregaron huellas locales:
    - `TerminalBlock_METZ_AST0250304_1x03_P5.00mm`
    - `TerminalBlock_METZ_AST0250404_1x04_P5.00mm`

## Respaldos creados

- `backup_footprints_20260623_212949`
- `PCB_PT100_SM50_before_board_sync_*.kicad_pcb`

## Validación

- KiCad CLI detectado: `9.0.7`.
- El PCB abre con `kicad-cli pcb drc`.
- DRC después de la sincronización RJ45/modelos:
  - 27 violaciones.
  - 124 ítems sin conectar.

## Pendientes importantes

- El RJ45 `J_BBOX_SM50` ahora usa los postes reales del fabricante. Uno de esos NPTH queda demasiado cerca del mounting hole `H2`. Hay que mover `H2`, mover ligeramente el RJ45, o cambiar la estrategia mecánica del mounting hole.
- Al corregir el RJ45, los pines 2/4/6/8 quedaron en la posición real del fabricante. Revisa o vuelve a rutear las conexiones de ambos RJ45 antes de fabricar.
- El esquemático aún tiene `TRIM_PT100` y `TRIM_SM50` apuntando al footprint stock de KiCad. La huella custom corregida ya está disponible como `ProyectoPCB_Footprints:Bourns_3296W_1_102LF`.
- Los conectores de terminal colocados siguen siendo Phoenix 5.00 mm. Las huellas METZ correctas ya están agregadas, pero no se cambiaron las instancias colocadas para no alterar la mecánica sin revisar.

## Fuentes usadas

- Bel Fuse / TRP drawing `C-2250066`, `dr-mag-2250066.pdf`.
- Bourns 3296 datasheet: `https://www.bourns.com/docs/product-datasheets/3296.pdf`.
- Modelos 3D STEP desde los ZIP locales de `C:\Users\kenne\Downloads\Footprints`.
