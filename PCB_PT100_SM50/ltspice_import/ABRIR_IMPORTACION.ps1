$ProjectDir = "C:\Users\kenne\Documents\KiCad\PCB_PT100_SM50\PCB_PT100_SM50"
$ImportRoot = "C:\Users\kenne\Documents\KiCad\PCB_PT100_SM50\PCB_PT100_SM50\ltspice_import"
$KicadPro = "C:\Users\kenne\Documents\KiCad\PCB_PT100_SM50\PCB_PT100_SM50\PCB_PT100_SM50.kicad_pro"

Start-Process explorer.exe "$ImportRoot"

$PossibleKiCad = @(
    "C:\Program Files\KiCad\9.0\bin\kicad.exe",
    "C:\Program Files\KiCad\bin\kicad.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($PossibleKiCad) {
    Start-Process $PossibleKiCad "$KicadPro"
} else {
    Start-Process "$KicadPro"
}
