# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

Push-Location $PSScriptRoot/../..
$Env:SPACK_ROOT = $PWD.Path
Push-Location $PWD/..
$Env:spackinstdir = $PWD.Path
Pop-Location

Set-Variable -Name python_pf_ver -Value (Get-Command -Name python -ErrorAction SilentlyContinue).Path

# If python_pf_ver is not defined, we cannot find Python on the Path
# We next look for Spack vendored copys
if ($null -eq $python_pf_ver)
{
    $python_pf_ver_list = Resolve-Path -Path "$PWD\Python*"
    if ($python_pf_ver_list.Length -gt 0)
    {
        $py_path = $python_pf_ver_list[$python_pf_ver_list.Length-1].Path
        $py_exe = "$py_path\python.exe"
    }
    else {
        Write-Error -Message "Python was not found on system"
        Write-Output "Please install Python or add Python to the PATH"
    }
}
else{
    Set-Variable -Name py_exe -Value $python_pf_ver
}

if (!$null -eq $py_path)
{
    $Env:Path = "$py_path;$Env:Path"
}

if (!$null -eq $py_exe)
{
    & "$py_exe" "$Env:SPACK_ROOT\bin\haspywin.py"
}

$Env:Path = "$Env:SPACK_ROOT\bin;$Env:Path"
if ($null -eq $Env:EDITOR)
{
    $Env:EDITOR = "notepad"
}

# Set spack shell so we can detect powershell context
$Env:SPACK_SHELL="pwsh"

doskey /exename=powershell.exe spack=$Env:SPACK_ROOT\bin\spack.ps1 $args

Write-Output "*****************************************************************"
Write-Output "**************** Spack Package Manager **************************"
Write-Output "*****************************************************************"

function global:prompt
{
    $pth = $(Convert-Path $(Get-Location)) | Split-Path -leaf
    "[spack] PS $pth>"
}
[system.console]::title = "Spack"
Pop-Location

