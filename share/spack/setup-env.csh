# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# This file is part of Spack and sets up the spack environment for
# csh and tcsh.  This includes environment modules and lmod support, and
# it also puts spack in your path.  Source it like this:
#
#    source /path/to/spack/share/spack/setup-env.csh
#

# prevent infinite recursion when spack shells out (e.g., on cray for modules)
if ($?_sp_initializing) then
    exit 0
endif
setenv _sp_initializing true

# find SPACK_ROOT.
# csh/tcsh don't have a built-in way to do this, but both keep files
# they are sourcing open. We use /proc on linux and lsof on macs to
# find this script's full path in the current process's open files.

# figure out a command to list open files
if (-d /proc/$$/fd) then
    set _sp_lsof = "ls -l /proc/$$/fd"
else
    which lsof > /dev/null
    if ($? == 0) then
        set _sp_lsof = "lsof -p $$"
    endif
endif

# filter this script out of list of open files
if ( $?_sp_lsof ) then
    set _sp_source_file = `$_sp_lsof | sed -e 's/^[^/]*//' | grep "/setup-env.csh"`
endif

# This script is in $SPACK_ROOT/share/spack; get the root with dirname
if ($?_sp_source_file) then
    set _sp_share_spack = `dirname "$_sp_source_file"`
    set _sp_share = `dirname "$_sp_share_spack"`
    setenv SPACK_ROOT `dirname "$_sp_share"`
endif

if (! $?SPACK_ROOT) then
    echo "==> Error: setup-env.csh couldn't figure out where spack lives."
    echo "    Set SPACK_ROOT to the root of your spack installation and try again."
    exit 1
endif

# Command aliases point at separate source files
set _spack_source_file = $SPACK_ROOT/share/spack/setup-env.csh
set _spack_share_dir = $SPACK_ROOT/share/spack
alias spack          'set _sp_args = (\!*); source $_spack_share_dir/csh/spack.csh'
alias spacktivate    'spack env activate'
alias _spack_pathadd 'set _pa_args = (\!*) && source $_spack_share_dir/csh/pathadd.csh'

# Identify and lock the python interpreter
if (! $?SPACK_PYTHON) then
    setenv SPACK_PYTHON ""
endif
foreach cmd ("$SPACK_PYTHON" python3 python python2)
    set status=`which "$cmd" >& /dev/null; echo $?`
    if ($status == 0) then
        setenv SPACK_PYTHON `which "$cmd"`
        break
    endif
end

# Set variables needed by this script
_spack_pathadd PATH "$SPACK_ROOT/bin"
eval `spack --print-shell-vars csh`

# Set up module search paths in the user environment
set tcl_roots = `echo $_sp_tcl_roots:q | sed 's/:/ /g'`
set compatible_sys_types = `echo $_sp_compatible_sys_types:q | sed 's/:/ /g'`
foreach tcl_root ($tcl_roots:q)
    foreach systype ($compatible_sys_types:q)
        _spack_pathadd MODULEPATH "$tcl_root/$systype"
    end
end

# done: unset sentinel variable as we're no longer initializing
unsetenv _sp_initializing
