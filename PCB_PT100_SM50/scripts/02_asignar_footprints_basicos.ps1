# 02_asignar_footprints_basicos.ps1
# Asigna footprints a R, C y conectores genericos en archivos .kicad_sch.
# Cierra KiCad antes de correrlo. Hace respaldo automatico.

Add-Type -AssemblyName System.Windows.Forms

$dialog = New-Object System.Windows.Forms.OpenFileDialog
$dialog.Filter = "KiCad schematic (*.kicad_sch)|*.kicad_sch"
$dialog.Title = "Seleccione el esquematico principal de KiCad"
if ($dialog.ShowDialog() -ne "OK") {
    Write-Host "Cancelado."
    exit
}

$MainSch = $dialog.FileName
$ProjectDir = Split-Path $MainSch -Parent
$SchFiles = Get-ChildItem -Path $ProjectDir -Filter "*.kicad_sch"
$BackupDir = Join-Path $ProjectDir ("backup_footprints_" + (Get-Date -Format "yyyyMMdd_HHmmss"))
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null

function Set-FootprintByLibId {
    param([string]$Text,[string]$LibId,[string]$Footprint)
    $pattern = '(?s)(\(symbol\s+\(lib_id\s+"' + [regex]::Escape($LibId) + '".*?\(property\s+"Footprint"\s+")([^"]*)(")'
    return ([regex]$pattern).Replace($Text, {
        param($m)
        if ([string]::IsNullOrWhiteSpace($m.Groups[2].Value)) { $m.Groups[1].Value + $Footprint + $m.Groups[3].Value } else { $m.Value }
    })
}

foreach ($file in $SchFiles) {
    Copy-Item $file.FullName (Join-Path $BackupDir $file.Name)
    $text = Get-Content $file.FullName -Raw

    $text = Set-FootprintByLibId $text "Device:C" "Capacitor_SMD:C_0805_2012Metric"
    $text = Set-FootprintByLibId $text "Device:R" "Resistor_SMD:R_0805_2012Metric"
    $text = Set-FootprintByLibId $text "Device:Polyfuse" "Fuse:Fuse_1812_4532Metric"
    $text = Set-FootprintByLibId $text "Device:Fuse" "Fuse:Fuse_1812_4532Metric"
    $text = Set-FootprintByLibId $text "Connector_Generic:Conn_01x03" "ProyectoPCB:AST0250304"
    $text = Set-FootprintByLibId $text "Connector_Generic:Conn_01x04" "ProyectoPCB:AST0250404"
    $text = Set-FootprintByLibId $text "Connector:RJ45_Shielded" "ProyectoPCB:2250066-1"

    Set-Content -Path $file.FullName -Value $text -Encoding UTF8
    Write-Host "Procesado:" $file.Name
}

Write-Host "Listo. Respaldo en:" $BackupDir
Write-Host "Abre KiCad y revisa Tools -> Assign Footprints."
