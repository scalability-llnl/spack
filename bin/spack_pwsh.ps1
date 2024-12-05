# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

$Env:SPACK_PS1_PATH="$PSScriptRoot\..\share\spack\setup-env.ps1"
& (Get-Process -Id $pid).Path -NoExit {
     . $Env:SPACK_PS1_PATH ; 
    Push-Location $ENV:SPACK_ROOT
 }
