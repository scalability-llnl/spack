#################################################################################
# This file is part of Spack's fish (friendly interactive shell) support
# Ported from bash (setup-env.sh) by Johannes Blaschke,
#                                    johannes@blaschke.science
#################################################################################



#################################################################################
#
# This file is part of Spack and sets up the spack environment for the friendly
# interactive shell (fish). This includes dotkit support, module support, and it
# also puts spack in your path. The script also checks that at least module
# support exists, and provides suggestions if it doesn't. Source it like this:
#
#    . /path/to/spack/share/spack/setup-env.fish
#
#################################################################################
# This is a wrapper around the spack command that forwards calls to 'spack use'
# and 'spack unuse' to shell functions. This in turn allows them to be used to
# invoke dotkit functions.
#
# 'spack use' is smarter than just 'use' because it converts its arguments into
# a unique spack spec that is then passed to dotkit commands. This allows the
# user to use packages without knowing all their installation details.
#
# e.g., rather than requiring a full spec for libelf, the user can type:
#
#     spack use libelf
#
# This will first find the available libelf dotkits and use a matching one. If
# there are two versions of libelf, the user would need to be more specific,
# e.g.:
#
#     spack use libelf@0.8.13
#
# This is very similar to how regular spack commands work and it avoids the need
# to come up with a user-friendly naming scheme for spack dotfiles.
#################################################################################






function shift_args -d "simulates bash shift"
    #
    # Returns argv[2..-1] (as an array)
    #  -> if argv has only 1 element, then returns the empty string
    # simulates the behavior of bash `shift`
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





function get_sp_flags -d "return leading flags"
    #
    # accumulate initial flags for main spack command
    #

    # initialize argument counter
    set i 0

    # iterate over elements (`elt`) in `argv` array
    for elt in $argv

        # # increment argument counter: used in place of bash's `shift` command
        # set i (math $i+1)

        # match element `elt` of `argv` array to check if it has a leading dash
        if echo $elt | string match -r -q "^-"
            # by echoing the current `elt`, the calling stream accumulates list
            # of valid flags. NOTE that this can also be done by adding to an
            # array, but fish functions can only return integers, so this is the
            # most elegant solution.
            echo $elt
        else
            # bash compatibility: stop when the match first fails. Upon failure,
            # we pack the remainder of `argv` into a global `remaining_args`
            # array (`i` tracks the index of the next element).
            set -x remaining_args (shift_args $argv[$i..-1])
            return
        end

        # increment argument counter: used in place of bash's `shift` command
        set i (math $i+1)

    end

    # if all elements in `argv` are matched, make sure that `remaining_args` is
    # initialized to an empty array (this might be overkill...).
    set -x remaining_args ""
end



function get_mod_args -d "return submodule flags"

    set -x sp_subcommand_args ""
    set -x sp_module_args ""

    # initialize argument counter
    set i 0

    for elt in $argv

        # # increment argument counter: used in place of bash's `shift` command
        # set i (math $i+1)

        if echo $elt | string match -r -q "^-"

            if test "$elt" = "-r" -o "$elt" = "--dependencies"
                set -x sp_subcommand_args $sp_subcommand_args $elt
            else
                set -x sp_module_args $sp_module_args $elt
            end

        else
            # bash compatibility: stop when the match first fails. Upon failure,
            # we pack the remainder of `argv` into a global `remaining_args`
            # array (`i` tracks the index of the next element).
            set -x remaining_args (shift_args $argv[$i..-1])
        end

        # increment argument counter: used in place of bash's `shift` command
        set i (math $i+1)

    end
end





function check_sp_flags -d "check spack flags for h/V flags"

    # check if inputs contain h or V flags.

    # skip if called with blank input
    #  -> bit of a hack: test -n requires exactly 1 argument. If `argv` is
    #     undefined, or if it is an array, `test -n $argv` is unpredictable.
    #     Instead, encapsulate `argv` in a string, and test the string instead.
    if test -n "$argv"
        if echo $argv | string match -r -q ".*h.*"
            return 0
        end
        if echo $argv | string match -r -q ".*V.*"
            return 0
        end
    end

    return 1
end



#
# save raw arguments into an array before butchering them
#

set args $argv



#
# accumulate initial flags for main spack command
#

set remaining_args "" # remaining (unparsed) arguments
set sp_flags (get_sp_flags $argv)



#
# h and V flags don't require further output parsing.
#

if check_sp_flags $sp_flags
    command spack $sp_flags $remaining_args
end



#
# isolate subcommand and subcommand specs
#  -> bit of a hack: test -n requires exactly 1 argument. If `argv` is
#     undefined, or if it is an array, `test -n $argv` is unpredictable.
#     Instead, encapsulate `argv` in a string, and test the string instead.
#

set sp_subcommand ""

if test -n "$remaining_args[1]"
    set -x sp_subcommand $remaining_args[1]
    set -x remaining_args (shift_args $remaining_args)     # simulates bash shift
end

set sp_spec $remaining_args



#
# Filter out use and unuse. For any other commands, just run the command.
#

switch $sp_subcommand

    # CASE: spack subcommand is `cd`: if the sub command arg is `-h`, nothing
    # further needs to be done. Otherwise, test the location referring the
    # subcommand and cd there (if it exists).

    case "cd"

        set sp_arg ""

        # Extract the first subcommand argument:
        # -> bit of a hack: test -n requires exactly 1 argument. If `argv` is
        #    undefined, or if it is an array, `test -n $argv` is unpredictable.
        #    Instead, encapsulate `argv` in a string, and test the string
        #    instead.
        if test -n "$remaining_args[1]"
            set sp_arg $remaining_args[1]
            set -x remaining_args (shift_args $remaining_args)     # simulates bash shift
        end

        if test $sp_arg = "-h"
            # nothing more needs to be done for `-h`
            command spack cd -h
        else
            # extract location using the subcommand (fish `(...)`)
            set LOC (spack location $sp_arg $remaining_args)

            # test location and cd if exists:
            if test -d "$LOC"
                cd $LOC
            else
                exit 1
            end

        end

        exit 0


    # CASE: spack subcommand is either `use`, `unuse`, `load`, or `unload`.
    # These statements deal with the technical details of actually using
    # modules.

    case "use" or "unuse" or "load" or "unload"

        # Shift any other args for use off before parsing spec.
        set sp_subcommand_args ""
        set sp_module_args ""

        get_mod_args $remaining_args

        set sp_spec $remaining_args


        # Here the user has run use or unuse with a spec. Find a matching spec
        # using 'spack module find', then use the appropriate module tool's
        # commands to add/remove the result from the environment. If spack
        # module command comes back with an error, do nothing.
end



# temporary debugging statements

echo "sp_flags = $sp_flags"
echo "remaining_args = $remaining_args"
echo "sp_subcommand = $sp_subcommand"
echo "sp_subcommand_args = $sp_subcommand"
echo "sp_module_args = $sp_module_args"
echo "sp_spec = $sp_spec"
