param ($systemFolder, $shortcut)

$start = [System.Environment]::GetFolderPath("$systemFolder")
Invoke-Item "$start\Programs\Spack\$shortcut"
