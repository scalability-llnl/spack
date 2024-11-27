$ErrorActionPreference = "SilentlyContinue"
Write-Output F|xcopy .\share\spack\qa\configuration\windows_config.yaml "$env:USERPROFILE\.spack\windows\config.yaml"
# The line below prevents the _spack_root symlink from causing issues with cyclic symlinks on Windows
(Get-Item '.\lib\spack\docs\_spack_root').Delete()
./share/spack/setup-env.ps1