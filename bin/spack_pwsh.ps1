# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

$Env:SPACK_PS1_PATH="$PSScriptRoot\..\share\spack\setup-env.ps1"
& (Get-Process -Id $pid).Path -NoExit {
     . $Env:SPACK_PS1_PATH ; 
    Push-Location $ENV:SPACK_ROOT
 }
