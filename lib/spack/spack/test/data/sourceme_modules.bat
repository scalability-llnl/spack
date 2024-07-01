@echo off
setlocal

rem C:\lib\spack\spack\test\data
rem
rem Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
rem Spack Project Developers. See the top-level COPYRIGHT file for details.
rem
rem SPDX-License-Identifier: (Apache-2.0 OR MIT)

:_module_raw val_1

exit /b 0

:module
exit /b 0

:ml
exit /b 0

set "_module_raw=call :_module_raw"
set "mod=call :mod"
set "ml=call :ml"

set MODULES_AUTO_HANDLING=1
set __MODULES_LMCONFLICT=bar^&foo
set NEW_VAR=new
