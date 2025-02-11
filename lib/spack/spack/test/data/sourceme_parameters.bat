@echo off
rem "C:\lib\spack\spack\test\data
rem
rem Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
rem Spack Project Developers. See the top-level COPYRIGHT file for details.
rem
rem SPDX-License-Identifier: (Apache-2.0 OR MIT)

if "%1" == "intel64" (
    set FOO=intel64
) else (
    set FOO=default
)
