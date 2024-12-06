# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

########################################################################
# Prepends directories to path, if they exist.
#      pathadd /path/to/dir            # add to PATH
# or   pathadd OTHERPATH /path/to/dir  # add to OTHERPATH
########################################################################
# If no variable name is supplied, just append to PATH
# otherwise append to that variable.
set _pa_varname = PATH;
set _pa_new_path = $_pa_args[1];

if ($#_pa_args > 1) then
    set _pa_varname = $_pa_args[1]
    set _pa_new_path = $_pa_args[2]
endif

# Check whether the variable is set yet.
set _pa_old_value = ""
eval set _pa_set = '$?'$_pa_varname
if ($_pa_set == 1) then
    eval set _pa_old_value='$'$_pa_varname
endif

# Do the actual prepending here, if it is a dir and not first in the path
if ( -d $_pa_new_path && $_pa_old_value\: !~ $_pa_new_path\:* ) then
    if ("x$_pa_old_value" == "x") then
        setenv $_pa_varname $_pa_new_path
    else
        setenv $_pa_varname $_pa_new_path\:$_pa_old_value
    endif
endif

unset _pa_args _pa_new_path _pa_old_value _pa_set _pa_varname
