@ECHO OFF
setlocal EnableDelayedExpansion
:: (c) 2021 Lawrence Livermore National Laboratory
:: To use this file independently of Spack's installer, execute this script in its directory, or add the
:: associated bin directory to your PATH. Invoke to launch Spack Shell.
::
:: source_dir/spack/bin/spack_cmd.bat
::
pushd %~dp0..\..
set SPACK_ROOT=%CD%
pushd %CD%\..
set spackinstdir=%CD%
popd


:: Check if Python is on the PATH
if not defined python_pf_ver (
(for /f "delims=" %%F in ('where python.exe') do (
                                                    set "python_pf_ver=%%F"
                                                    goto :found_python
                                                  ) ) 2> NUL
)
:found_python
if not defined python_pf_ver (
    :: If not, look for Python from the Spack installer
    :get_builtin
    (for /f "tokens=*" %%g in ('dir /b /a:d "!spackinstdir!\Python*"') do (
        set "python_ver=%%g")) 2> NUL

    if not defined python_ver (
        echo Python was not found on your system.
        echo Please install Python or add Python to your PATH.
    ) else (
        set "py_path=!spackinstdir!\!python_ver!"
        set "py_exe=!py_path!\python.exe"
    )
    goto :exitpoint
) else (
    :: Python is already on the path
    set "py_exe=!python_pf_ver!"
    (for /F "tokens=* USEBACKQ" %%F in (
        `"!py_exe!" --version`) do (set "output=%%F")) 2>NUL
    if not "!output:Microsoft Store=!"=="!output!" goto :get_builtin
    goto :exitpoint
)
:exitpoint
endlocal & (
    set "SPACK_ROOT=%SPACK_ROOT%"
    set "spackinstdir=%spackinstdir%"
    set "py_path=%py_path%"
    set "py_exe=%py_exe%"
)

set "PATH=%SPACK_ROOT%\bin\;%PATH%"
if defined py_path (
    set "PATH=%py_path%;%PATH%"
)

if defined py_exe (
    "%py_exe%" "%SPACK_ROOT%\bin\haspywin.py"
)

if not defined EDITOR (
   set EDITOR=notepad
)

@echo **********************************************************************
@echo ** Spack Package Manager
@echo **********************************************************************

IF "%1"=="" GOTO CONTINUE
set
GOTO:EOF

:continue
title Spack
set PROMPT=[spack] %PROMPT%
