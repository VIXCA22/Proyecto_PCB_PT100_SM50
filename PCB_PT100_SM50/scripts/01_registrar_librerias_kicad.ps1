# 01_registrar_librerias_kicad.ps1
# Copia/crea tablas fp-lib-table y sym-lib-table en el proyecto KiCad.
# Ejecutar desde PowerShell. Cierra KiCad antes de correrlo.

Add-Type -AssemblyName System.Windows.Forms

$dialog = New-Object System.Windows.Forms.FolderBrowserDialog
$dialog.Description = "Selecciona la carpeta del proyecto KiCad donde esta el .kicad_pro"
if ($dialog.ShowDialog() -ne "OK") {
    Write-Host "Cancelado."
    exit
}
$ProjectDir = $dialog.SelectedPath
$PackDir = Split-Path $PSScriptRoot -Parent

Write-Host "Proyecto KiCad:" $ProjectDir
Write-Host "Pack:" $PackDir

# Crear carpetas destino si no existen
$DestSymbols = Join-Path $ProjectDir "symbols"
$DestFootprints = Join-Path $ProjectDir "footprints"
$DestPretty = Join-Path $DestFootprints "ProyectoPCB.pretty"
$Dest3D = Join-Path $ProjectDir "3dmodels"
$DestOutputs = Join-Path $ProjectDir "outputs"
New-Item -ItemType Directory -Force -Path $DestSymbols,$DestPretty,$Dest3D,$DestOutputs | Out-Null

# Copiar contenido del pack al proyecto, sin borrar lo existente
Copy-Item -Path (Join-Path $PackDir "symbols\*.kicad_sym") -Destination $DestSymbols -ErrorAction SilentlyContinue
Copy-Item -Path (Join-Path $PackDir "footprints\ProyectoPCB.pretty\*.kicad_mod") -Destination $DestPretty -ErrorAction SilentlyContinue
Copy-Item -Path (Join-Path $PackDir "3dmodels\*.step") -Destination $Dest3D -ErrorAction SilentlyContinue
Copy-Item -Path (Join-Path $PackDir "3dmodels\*.wrl") -Destination $Dest3D -ErrorAction SilentlyContinue

# Crear fp-lib-table especifico del proyecto
$FpTable = Join-Path $ProjectDir "fp-lib-table"
$FpContent = @"
(fp_lib_table
  (lib (name "ProyectoPCB")(type "KiCad")(uri "`${KIPRJMOD}/footprints/ProyectoPCB.pretty")(options "")(descr "Footprints especificos del proyecto PCB PT100 SM50"))
)
"@
Set-Content -Path $FpTable -Value $FpContent -Encoding UTF8
Write-Host "fp-lib-table creado/actualizado."

# Crear sym-lib-table si hay simbolos .kicad_sym
$SymLibs = Get-ChildItem -Path $DestSymbols -Filter "*.kicad_sym" -ErrorAction SilentlyContinue
if ($SymLibs.Count -gt 0) {
    $SymTable = Join-Path $ProjectDir "sym-lib-table"
    $lines = @()
    $lines += "(sym_lib_table"
    foreach ($lib in $SymLibs) {
        $name = [System.IO.Path]::GetFileNameWithoutExtension($lib.Name)
        $lines += "  (lib (name `"$name`" )(type `"KiCad`" )(uri `"`${KIPRJMOD}/symbols/$($lib.Name)`" )(options `"`" )(descr `"Simbolos del proyecto`"))"
    }
    $lines += ")"
    Set-Content -Path $SymTable -Value $lines -Encoding UTF8
    Write-Host "sym-lib-table creado con $($SymLibs.Count) libreria(s)."
} else {
    Write-Host "No hay .kicad_sym en symbols/. Solo se registro la libreria de footprints."
}

Write-Host "Listo. Reabre KiCad."
