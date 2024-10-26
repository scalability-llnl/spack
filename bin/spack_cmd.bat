@ECHO OFF
:: (c) 2021 Lawrence Livermore National Laboratory
:: To use this file independently of Spack's installer, execute this script in its directory, or add the
:: associated bin directory to your PATH. Invoke to launch Spack Shell.
::
:: source_dir/spack/bin/spack_cmd.bat
::

call "%~dp0..\share\spack\setup-env.bat"
pushd %SPACK_ROOT%
%comspec% /K
