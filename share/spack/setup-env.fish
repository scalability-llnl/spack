# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


#################################################################################
#
# This file is part of Spack and sets up the spack environment for the friendly
# interactive shell (fish). This includes module support, and it also puts spack
# in your path. The script also checks that at least module support exists, and
# provides suggestions if it doesn't. Source it like this:
#
#    source /path/to/spack/share/spack/setup-env.fish
#
#################################################################################
# This is a wrapper around the spack command that forwards calls to 'spack load'
# and 'spack unload' to shell functions. This in turn allows them to be used to
# invoke environment modules functions.
#
# 'spack load' is smarter than just 'load' because it converts its arguments into
# a unique spack spec that is then passed to module commands. This allows the
# user to load packages without knowing all their installation details.
#
# e.g., rather than requiring a full spec for libelf, the user can type:
#
#     spack load libelf
#
# This will first find the available libelf modules and load a matching one. If
# there are two versions of libelf, the user would need to be more specific,
# e.g.:
#
#     spack load libelf@0.8.13
#
# This is very similar to how regular spack commands work and it avoids the need
# to come up with a user-friendly naming scheme for spack dotfiles.
#################################################################################

# prevent infinite recursion when spack shells out (e.g., on cray for modules)
if test -n "$_sp_initializing"
    exit 0
end
set -x _sp_initializing true


#
# Test for STDERR-NOCARET feature: if this is off, fish will redirect stderr to
# a file named in the string after `^`
#


if status test-feature stderr-nocaret
else
    echo "WARNING: you have not enabled the 'stderr-nocaret' feature."
    echo "This means that you have to escape the caret (^) character when defining specs."
    echo "Consider enabling stderr-nocaret: https://fishshell.com/docs/current/index.html#featureflags"
end



#
# SPACK wrapper function, preprocessing arguments and flags.
#


function spack -d "wrapper for the `spack` command"


#
# DEFINE SUPPORT FUNCTIONS HERE
#


#
# ALLOCATE_SP_SHARED, and DELETE_SP_SHARED allocate (and delete) temporary
# global variables
#


function allocate_sp_shared -d "allocate shared (global variables)"
    set -gx __sp_remaining_args
    set -gx __sp_subcommand_args
    set -gx __sp_module_args
    set -gx __sp_stat
    set -gx __sp_stdout
    set -gx __sp_stderr
end



function delete_sp_shared -d "deallocate shared (global variables)"
    set -e __sp_remaining_args
    set -e __sp_subcommand_args
    set -e __sp_module_args
    set -e __sp_stat
    set -e __sp_stdout
    set -e __sp_stderr
end




#
# STREAM_ARGS and SHIFT_ARGS: helper functions manipulating the `argv` array:
#   -> STREAM_ARGS: echos the `argv` array element-by-element
#   -> SHIFT_ARGS:  echos the `argv` array element-by-element starting with the
#                   second element. If `argv` has only one element, echo the
#                   empty string `""`.
# NOTE: while `stream_args` is not strictly necessary, it adds a nice symmetry
#       to `shift_args`
#

function stream_args -d "echos args as a stream"
    # return the elements of `$argv` as an array
    #  -> since we want to be able to call it as part of `set x (shift_args
    #     $x)`, we return these one-at-a-time using echo... this means that the
    #     sub-command stream will correctly concatenate the output into an array
    for elt in $argv
        echo $elt
    end
end


function shift_args -d "simulates bash shift"
    #
    # Returns argv[2..-1] (as an array)
    #  -> if argv has only 1 element, then returns the empty string. This
    #     simulates the behavior of bash `shift`
    #

    if test -z "$argv[2]"
        # there are no more element, returning the empty string
        echo ""
    else
        # return the next elements `$argv[2..-1]` as an array
        #  -> since we want to be able to call it as part of `set x (shift_args
        #     $x)`, we return these one-at-a-time using echo... this means that
        #     the sub-command stream will correctly concatenate the output into
        #     an array
        for elt in $argv[2..-1]
            echo $elt
        end
    end

end




#
# CAPTURE_ALL: helper function used to capture stdout, stderr, and status
#   -> CAPTURE_ALL: there is a bug in fish, that prevents stderr re-capture
#                   from nested command substitution:
#                   https://github.com/fish-shell/fish-shell/issues/6459
#

function capture_all
    begin;
        begin;
            eval $argv[1]
            set $argv[2] $status  # read sets the `status` flag => capture here
        end 2>| read -z __err
    end 1>| read -z __out

    # output arrays
    set $argv[3] (echo $__out | string split \n)
    set $argv[4] (echo $__err | string split \n)

    return 0
end




#
# GET_SP_FLAGS, and GET_MOD_ARGS: support functions for extracting arguments and
# flags. Note bash's `shift` operation is simulated by the `__sp_remaining_args`
# array which is roughly equivalent to `$@` in bash.
#

function get_sp_flags -d "return leading flags"
    #
    # Accumulate initial flags for main spack command. NOTE: Sets the external
    # array: `__sp_remaining_args` containing all unprocessed arguments.
    #

    # initialize argument counter
    set -l i 1

    # iterate over elements (`elt`) in `argv` array
    for elt in $argv

        # match element `elt` of `argv` array to check if it has a leading dash
        if echo $elt | string match -r -q "^-"
            # by echoing the current `elt`, the calling stream accumulates list
            # of valid flags. NOTE that this can also be done by adding to an
            # array, but fish functions can only return integers, so this is the
            # most elegant solution.
            echo $elt
        else
            # bash compatibility: stop when the match first fails. Upon failure,
            # we pack the remainder of `argv` into a global `__sp_remaining_args`
            # array (`i` tracks the index of the next element).
            set __sp_remaining_args (stream_args $argv[$i..-1])
            return
        end

        # increment argument counter: used in place of bash's `shift` command
        set -l i (math $i+1)

    end

    # if all elements in `argv` are matched, make sure that `__sp_remaining_args`
    # is deleted (this might be overkill...).
    set -e __sp_remaining_args
end



#
# CHECK_SP_FLAGS, CONTAINS_HELP_FLAGS, CHECK_ENV_ACTIVATE_FLAGS, and
# CHECK_ENV_DEACTIVATE_FLAGS: support functions for checking arguments and flags.
#

function check_sp_flags -d "check spack flags for h/V flags"
    #
    # Check if inputs contain h or V flags.
    #

    # combine argument array into single string (space seperated), to be passed
    # to regular expression matching (`string match -r`)
    set -l _a "$argv"

    # skip if called with blank input. Notes: [1] (cf. EOF)
    if test -n "$_a"
        if echo $_a | string match -r -q ".*h.*"
            return 0
        end
        if echo $_a | string match -r -q ".*V.*"
            return 0
        end
    end

    return 1
end



function match_flag -d "checks all combinations of flags ocurring inside of a string"

    # Remove leading and trailing spaces -- but we need to insert a "guard" (x)
    # so that eg. `string trim -h` doesn't trigger the help string for `string trim`
    set -l _a (string sub -s 2 (string trim "x$argv[1]"))
    set -l _b (string sub -s 2 (string trim "x$argv[2]"))

    if test -z "$_a"; or test -z "$_b"
        return 0
    end

    # surrounded by spaced
    if echo "$_a" | string match -r -q " +$_b +"
        return 0
    end

    # beginning of string + trailing space
    if echo "$_a" | string match -r -q "^$_b +"
        return 0
    end

    # end of string + leadingg space
    if echo "$_a" | string match -r -q " +$_b\$"
        return 0
    end

    # entire string
    if echo "$_a" | string match -r -q "^$_b\$"
        return 0
    end

    return 1

end



function check_env_activate_flags -d "check spack env subcommand flags for -h, --sh, --csh, or --fish"
    #
    # Check if inputs contain -h/--help, --sh, --csh, or --fish
    #

    # combine argument array into single string (space seperated), to be passed
    # to regular expression matching (`string match -r`)
    set -l _a "$argv"

    # skip if called with blank input. Notes: [1] (cf. EOF)
    if test -n "$_a"

        # looks for a single `-h`
        if match_flag $_a "-h"
            return 0
        end

        # looks for a single `--help`
        if match_flag $_a "--help"
            return 0
        end

        # looks for a single `--sh`
        if match_flag $_a "--sh"
            return 0
        end

        # looks for a single `--csh`
        if match_flag $_a "--csh"
            return 0
        end

        # looks for a single `--fish`
        if match_flag $_a "--fish"
            return 0
        end

        # looks for a single `--list`
        if match_flag $_a "--list"
            return 0
        end

    end

    return 1
end


function check_env_deactivate_flags -d "check spack env subcommand flags for --sh, --csh, or --fish"
    #
    # Check if inputs contain --sh, --csh, or --fish
    #

    # combine argument array into single string (space seperated), to be passed
    # to regular expression matching (`string match -r`)
    set -l _a "$argv"

    # skip if called with blank input. Notes: [1] (cf. EOF)
    if test -n "$_a"

        # looks for a single `--sh`
        if match_flag $_a "--sh"
            return 0
        end

        # looks for a single `--csh`
        if match_flag $_a "--csh"
            return 0
        end

        # looks for a single `--fish`
        if match_flag $_a "--fish"
            return 0
        end

    end

    return 1
end




#
# SPACK RUNNER function, this does all the work!
#


function spack_runner -d "Runner function for the `spack` wrapper"
    # Store DYLD_* variables from spack shell function
    # This is necessary because MacOS System Integrity Protection clears
    # variables that affect dyld on process start.
    for var in DYLD_LIBRARY_PATH DYLD_FALLBACK_LIBRARY_PATH
        if set -q $var
            set -gx SPACK_$var $$var
        end
    end

    #
    # Accumulate initial flags for main spack command
    #

    set __sp_remaining_args # remaining (unparsed) arguments
    set -l sp_flags (get_sp_flags $argv) # sets __sp_remaining_args


    #
    # h and V flags don't require further output parsing.
    #

    if check_sp_flags $sp_flags
        command spack $sp_flags $__sp_remaining_args
        return
    end


    #
    # Isolate subcommand and subcommand specs. Notes: [1] (cf. EOF)
    #

    set -l sp_subcommand ""

    if test -n "$__sp_remaining_args[1]"
        set sp_subcommand $__sp_remaining_args[1]
        set __sp_remaining_args (shift_args $__sp_remaining_args)  # simulates bash shift
    end

    set -l sp_spec $__sp_remaining_args


    #
    # Filter out cd, env, and load and unload. For any other commands, just run
    # the spack command as is.
    #

    switch $sp_subcommand

        # CASE: spack subcommand is `cd`: if the sub command arg is `-h`, nothing
        # further needs to be done. Otherwise, test the location referring the
        # subcommand and cd there (if it exists).

        case "cd"

            set -l sp_arg ""

            # Extract the first subcommand argument. Notes: [1] (cf. EOF)
            if test -n "$__sp_remaining_args[1]"
                set sp_arg $__sp_remaining_args[1]
                set __sp_remaining_args (shift_args $__sp_remaining_args) # simulates bash shift
            end

            # Notes: [2] (cf. EOF)
            if test "x$sp_arg" = "x-h"; or test "x$sp_arg" = "x--help"
                # nothing more needs to be done for `-h` or `--help`
                command spack cd -h
                return
            else
                # extract location using the subcommand (fish `(...)`)
                set -l LOC (command spack location $sp_arg $__sp_remaining_args)

                # test location and cd if exists:
                if test -d "$LOC"
                    cd $LOC
                    return
                else
                    return 1
                end

            end


        # CASE: spack subcommand is `env`. Here we get the spack runtime to
        # supply the appropriate shell commands for setting the environment
        # varibles. These commands are then run by fish (using the `capture_all`
        # function, instead of a command substitution).

        case "env"

            set -l sp_arg ""

            # Extract the first subcommand argument.  Notes: [1] (cf. EOF)
            if test -n "$__sp_remaining_args[1]"
                set sp_arg $__sp_remaining_args[1]
                set __sp_remaining_args (shift_args $__sp_remaining_args) # simulates bash shift
            end

            # Notes: [2] (cf. EOF)
            if test "x$sp_arg" = "x-h"; or test "x$sp_arg" = "x--help"
                # nothing more needs to be done for `-h` or `--help`
                command spack env -h
                return
            else
                switch $sp_arg
                    case "activate"
                        set -l _a (stream_args $__sp_remaining_args)

                        if check_env_activate_flags $_a
                            # no args or args contain -h/--help, --sh, or --csh: just execute
                            command spack env activate $_a
                            return
                        else
                            # actual call to activate: source the output
                            set -l sp_env_cmd "command spack $sp_flags env activate --fish $__sp_remaining_args"
                            capture_all $sp_env_cmd __sp_stat __sp_stdout __sp_stderr
                            eval $__sp_stdout
                            if test -n "$__sp_stderr"
                                echo -s \n$__sp_stderr 1>&2  # current fish bug: handle stderr manually
                            end
                            return $__sp_stat
                        end

                    case "deactivate"
                        set -l _a (stream_args $__sp_remaining_args)

                        if check_env_deactivate_flags $_a
                            # just  execute the command if --sh, --csh, or --fish are provided
                            command spack env deactivate $_a
                            return

                        # Test of further (unparsed arguments). Any other
                        # arguments are an error or help, so just run help
                        # -> TODO: This should throw and error but leave as is
                        #    for compatibility with setup-env.sh
                        # -> Notes: [1] (cf. EOF).
                        else if test -n "$__sp_remaining_args"
                            command spack env deactivate -h
                            return
                        else
                            # no args: source the output of the command
                            set -l sp_env_cmd "command spack $sp_flags env deactivate --fish"
                            capture_all $sp_env_cmd __sp_stat __sp_stdout __sp_stderr
                            if test $__sp_stat -ne 0
                                if test -n "$__sp_stderr"
                                    echo -s \n$__sp_stderr 1>&2  # current fish bug: handle stderr manually
                                end
                                return $__sp_stat
                            end
                            eval $__sp_stdout
                        end

                    case "*"
                        # if $__sp_remaining_args is empty, then don't include it
                        # as argument (otherwise it will be confused as a blank
                        # string input!)
                        if test -n "$__sp_remaining_args"
                            command spack env $sp_arg $__sp_remaining_args
                            return
                        else
                            command spack env $sp_arg
                            return
                        end
                end
            end


        # CASE: spack subcommand is either `load`, or `unload`. These statements
        # deal with the technical details of actually using modules. Especially
        # to deal with the substituting latest version numbers to the module
        # command.

        case "load" or "unload"

            set -l _a (stream_args $__sp_remaining_args)

            if check_env_activate_flags $_a
                # no args or args contain -h/--help, --sh, or --csh: just execute
                command spack $sp_flags $sp_subcommand $__sp_remaining_args
                return
            else
                # actual call to activate: source the output
                set -l sp_env_cmd "command spack $sp_flags $sp_subcommand --fish $__sp_remaining_args"
                capture_all $sp_env_cmd __sp_stat __sp_stdout __sp_stderr
                if test $__sp_stat -ne 0
                    if test -n "$__sp_stderr"
                        echo -s \n$__sp_stderr 1>&2  # current fish bug: handle stderr manually
                    end
                    return $__sp_stat
                end
                eval $__sp_stdout
            end


        # CASE: Catch-all

        case "*"
            command spack $argv
            return
    end
end




#
# RUN SPACK_RUNNER HERE
#


#
# Allocate temporary global variables used for return extra arguments from
# functions. NOTE: remember to call delete_sp_shared whenever returning from
# this function.
#

allocate_sp_shared


#
# Run spack command using the spack_runner.
#

spack_runner $argv
# Capture state of spack_runner (returned below)
set -l stat $status


#
# Delete temprary global variabels allocated in `allocated_sp_shared`.
#

delete_sp_shared



return $stat

end



#################################################################################
# Prepends directories to path, if they exist.
#      pathadd /path/to/dir            # add to PATH
# or   pathadd OTHERPATH /path/to/dir  # add to OTHERPATH
#################################################################################
function spack_pathadd -d "Add path to specified variable (defaults to PATH)"
    #
    # Adds (existing only) paths to specified (defaults to PATH)
    # variable. Does not warn attempting to add non-existing path. This is not a
    # bug because the MODULEPATH setup tries add all possible compatible systems
    # and therefore sp_multi_pathadd relies on this function failing silently.
    #

    # If no variable name is supplied, just append to PATH otherwise append to
    # that variable.
    #  -> Notes: [1] (cf. EOF).
    if test -n "$argv[2]"
        set pa_varname $argv[1]
        set pa_new_path $argv[2]
    else
        true # this is a bit of a strange hack! Notes: [3] (cf EOF).
        set pa_varname PATH
        set pa_new_path $argv[1]
    end

    set pa_oldvalue $$pa_varname

    # skip path is not existing directory
    #  -> Notes: [1] (cf. EOF).
    if test -d "$pa_new_path"

        # combine argument array into single string (space seperated), to be
        # passed to regular expression matching (`string match -r`)
        set -l _a "$pa_oldvalue"

        # skip path if it is already the first in the variable
        # note spaces in regular expression: we're matching to a space delimited
        # list of paths
        if not echo $_a | string match -q -r "^$pa_new_path *"
            if test -n "$pa_oldvalue"
                set $pa_varname $pa_new_path $pa_oldvalue
            else
                true # this is a bit of a strange hack! Notes: [3] (cf. EOF)
                set $pa_varname $pa_new_path
            end
        end
    end
end


function sp_multi_pathadd -d "Helper for adding module-style paths by incorporating compatible systems into pathadd" --inherit-variable _sp_compatible_sys_types
    #
    # Calls spack_pathadd in path inputs, adding all compatible system types
    # (sourced from $_sp_compatible_sys_types) to input paths.
    #

    for pth in $argv[2]
        for systype in $_sp_compatible_sys_types
            spack_pathadd $argv[1] "$pth/$systype"
        end
    end
end



#
# Figure out where this file is. Below code only needs to work in fish
#
set -l sp_source_file (status -f)  # name of current file



#
# Identify and lock the python interpreter
#
for cmd in "$SPACK_PYTHON" python3 python python2
    set -l _sp_python (command -v "$cmd")
    if test $status -eq 0
        set -x SPACK_PYTHON $_sp_python
        break
    end
end



#
# Find root directory and add bin to path.
#
set -l sp_share_dir (realpath (dirname $sp_source_file))
set -l sp_prefix (realpath (dirname (dirname $sp_share_dir)))
spack_pathadd PATH "$sp_prefix/bin"
set -xg SPACK_ROOT $sp_prefix



#
# No need to determine which shell is being used (obviously it's fish)
#
set -xg SPACK_SHELL "fish"
set -xg _sp_shell "fish"




if test -z "$SPACK_SKIP_MODULES"
    #
    # Check whether we need environment-variables (module) <= `use` is not available
    #
    set -l need_module "no"
    if not functions -q use; and not functions -q module
        set need_module "yes"
    end



    #
    # Make environment-modules available to shell
    #
    function sp_apply_shell_vars -d "applies expressions of the type `a='b'` as `set a b`"

        # convert `a='b' to array variable `a b`
        set -l expr_token (string trim -c "'" (string split "=" $argv))

        # run set command to takes, converting lists of type `a:b:c` to array
        # variables `a b c` by splitting around the `:` character
        set -xg $expr_token[1] (string split ":" $expr_token[2])
    end


    if test "$need_module" = "yes"
        set -l sp_shell_vars (command spack --print-shell-vars sh,modules)

        for sp_var_expr in $sp_shell_vars
            sp_apply_shell_vars $sp_var_expr
        end

        # _sp_module_prefix is set by spack --print-sh-vars
        if test "$_sp_module_prefix" != "not_installed"
            set -xg MODULE_PREFIX $_sp_module_prefix
            spack_pathadd PATH "$MODULE_PREFIX/bin"
        end

    else

        set -l sp_shell_vars (command spack --print-shell-vars sh)

        for sp_var_expr in $sp_shell_vars
            sp_apply_shell_vars $sp_var_expr
        end

    end

    if test "$need_module" = "yes"
        function module -d "wrapper for the `module` command to point at Spack's modules instance" --inherit-variable MODULE_PREFIX
            eval $MODULE_PREFIX/bin/modulecmd $SPACK_SHELL $argv
        end
    end



    #
    # set module system roots
    #

    # Search of MODULESPATHS by trying all possible compatible system types as
    # module roots.
    if test -z "$MODULEPATH"
        set -gx MODULEPATH
    end
    sp_multi_pathadd MODULEPATH $_sp_tcl_roots
end

# Add programmable tab completion for fish
#
set -l fish_version (string split '.' $FISH_VERSION)
if test $fish_version[1] -gt 3
    or test $fish_version[1] -eq 3
    and test $fish_version[2] -ge 2

    source $sp_share_dir/spack-completion.fish
end

#
# NOTES
#
# [1]: `test -n` requires exactly 1 argument. If `argv` is undefined, or if it
#      is an array, `test -n $argv` is unpredictable. Instead, encapsulate
#      `argv` in a string, and test the string.
#
# [2]: `test "$a" = "$b$` is dangerous if `a` and `b` contain flags at index 1,
#      as `test $a` can be interpreted as `test $a[1] $a[2..-1]`. Solution is to
#      prepend a non-flag character, eg: `test "x$a" = "x$b"`.
#
# [3]: When the test in the if statement fails, the `status` flag is set to 1.
#      `true` here manuallt resets the value of `status` to 0. Since `set`
#      passes `status` along, we thus avoid the function returning 1 by mistake.

# done: unset sentinel variable as we're no longer initializing
set -e _sp_initializing
