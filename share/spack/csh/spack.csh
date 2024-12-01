# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

########################################################################
# This is a wrapper around the spack command that forwards calls to
# 'spack load' and 'spack unload' to shell functions.  This in turn
# allows them to be used to invoke environment-modules functions.
#
# 'spack load' is smarter than just 'load' because it converts its
# arguments into a unique Spack spec that is then passed to environment-modules
# commands.  This allows the user to use packages without knowing all
# their installation details.
#
# e.g., rather than requiring a full spec for libelf, the user can type:
#
#     spack load libelf
#
# This will first find the available libelf module file and use a
# matching one.  If there are two versions of libelf, the user would
# need to be more specific, e.g.:
#
#     spack load libelf@0.8.13
#
# This is very similar to how regular spack commands work and it
# avoids the need to come up with a user-friendly naming scheme for
# spack module files.
########################################################################
# Store DYLD_* variables from spack shell function
# This is necessary because MacOS System Integrity Protection clears
# variables that affect dyld on process start.
if ( ${?DYLD_LIBRARY_PATH} ) then
    setenv SPACK_DYLD_LIBRARY_PATH $DYLD_LIBRARY_PATH
endif
if ( ${?DYLD_FALLBACK_LIBRARY_PATH} ) then
    setenv SPACK_DYLD_FALLBACK_LIBRARY_PATH $DYLD_FALLBACK_LIBRARY_PATH
endif

# accumulate initial flags for main spack command
set _sp_flags = ""
while ( $#_sp_args > 0 )
    if ( "$_sp_args[1]" !~ "-*" ) break
    set _sp_flags = "$_sp_flags $_sp_args[1]"
    shift _sp_args
end

# h and V flags don't require further output parsing.
if ( "$_sp_flags" =~ *h* || "$_sp_flags" =~ *V* ) then
    \spack $_sp_flags $_sp_args
    goto _sp_end
endif

# Set up args -- we want a subcommand and a spec.
set _sp_subcommand=""
set _sp_spec=""
if ($#_sp_args > 0) then
    set _sp_subcommand = ($_sp_args[1])
endif
if ($#_sp_args > 1) then
    set _sp_spec = ($_sp_args[2-])
endif

# Run subcommand
switch ($_sp_subcommand)
case cd:
    shift _sp_args  # get rid of 'cd'

    set _sp_arg=""
    if ($#_sp_args > 0) then
        set _sp_arg = ($_sp_args[1])
    endif
    shift _sp_args

    if ( "$_sp_arg" == "-h" || "$_sp_args" == "--help" ) then
        \spack cd -h
    else
        cd `\spack location $_sp_arg $_sp_args`
    endif
    breaksw
case env:
    shift _sp_args  # get rid of 'env'

    set _sp_arg=""
    if ($#_sp_args > 0) then
        set _sp_arg = ($_sp_args[1])
    endif

    if ( "$_sp_arg" == "-h" || "$_sp_arg" == "--help" ) then
        \spack env -h
    else
        switch ($_sp_arg)
            case activate:
                set _sp_env_arg=""
                if ($#_sp_args > 1) then
                    set _sp_env_arg = ($_sp_args[2])
                endif

                # Space needed here to differentiate between `-h`
                # argument and environments with "-h" in the name.
                if ( "$_sp_env_arg" == "" || \
                     "$_sp_args" =~ "* --sh*" || \
                     "$_sp_args" =~ "* --csh*" || \
                     "$_sp_args" =~ "* -h*" || \
                     "$_sp_args" =~ "* --help*" ) then
                    # No args or args contain --sh, --csh, or -h/--help: just execute.
                    \spack $_sp_flags env $_sp_args
                else
                    shift _sp_args  # consume 'activate' or 'deactivate'
                    # Actual call to activate: source the output.
                    eval `\spack $_sp_flags env activate --csh $_sp_args`
                endif
                breaksw
            case deactivate:
                set _sp_env_arg=""
                if ($#_sp_args > 1) then
                    set _sp_env_arg = ($_sp_args[2])
                endif

                # Space needed here to differentiate between `--sh`
                # argument and environments with "--sh" in the name.
                if ( "$_sp_args" =~ "* --sh*" || \
                     "$_sp_args" =~ "* --csh*" ) then
                    # Args contain --sh or --csh: just execute.
                    \spack $_sp_flags env $_sp_args
                else if ( "$_sp_env_arg" != "" ) then
                    # Any other arguments are an error or -h/--help: just run help.
                    \spack $_sp_flags env deactivate -h
                else
                    # No args: source the output of the command.
                    eval `\spack $_sp_flags env deactivate --csh`
                endif
                breaksw
            default:
                \spack $_sp_flags env $_sp_args
                breaksw
        endsw
    endif
    breaksw

case load:
case unload:
    # Get --sh, --csh, -h, or --help arguments.
    # Space needed here to differentiate between `-h`
    # argument and specs with "-h" in the name.
    if ( " $_sp_spec" =~ "* --sh*" || \
         " $_sp_spec" =~ "* --csh*" || \
         " $_sp_spec" =~ "* --list*" || \
         " $_sp_spec" =~ "* -h*" || \
         " $_sp_spec" =~ "* --help*") then
        # Args contain --sh, --csh, or -h/--help: just execute.
        \spack $_sp_flags $_sp_subcommand $_sp_spec
    else
        # Otherwise, eval with csh.
        eval `\spack $_sp_flags $_sp_subcommand --csh $_sp_spec || \
             echo "exit 1"`
    endif
    breaksw

default:
    \spack $_sp_flags $_sp_args
    breaksw
endsw

_sp_end:
unset _sp_args _sp_full_spec _sp_sh_cmd _sp_spec _sp_subcommand _sp_flags
unset _sp_arg _sp_env_arg
