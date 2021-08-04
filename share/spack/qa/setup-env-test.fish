#!/usr/bin/env fish
#
# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# This script tests that Spack's setup-env.fish init script works.
#


function allocate_testing_global -d "allocate global variables used for testing"

    # Colors for output
    set -gx __spt_red '\033[1;31m'
    set -gx __spt_cyan '\033[1;36m'
    set -gx __spt_green '\033[1;32m'
    set -gx __spt_reset '\033[0m'

    # counts of test successes and failures.
    set -gx __spt_success 0
    set -gx __spt_errors 0
end


function delete_testing_global -d "deallocate global variables used for testing"

    set -e __spt_red
    set -e __spt_cyan
    set -e __spt_green
    set -e __spt_reset

    set -e __spt_success
    set -e __spt_errors
end

# ------------------------------------------------------------------------
# Functions for color output.
# ------------------------------------------------------------------------


function echo_red
    printf "$__spt_red$argv$__spt_reset\n"
end

function echo_green
    printf "$__spt_green$argv$__spt_reset\n"
end

function echo_msg
    printf "$__spt_cyan$argv$__spt_reset\n"
end



# ------------------------------------------------------------------------
# Generic functions for testing fish code.
# ------------------------------------------------------------------------


# Print out a header for a group of tests.
function title

    echo
    echo_msg "$argv"
    echo_msg "---------------------------------"

end

# echo FAIL in red text; increment failures
function fail
    echo_red FAIL
    set __spt_errors (math $__spt_errors+1)
end

# echo SUCCESS in green; increment successes
function pass
    echo_green SUCCESS
    set __spt_success (math $__spt_success+1)
end


#
# Run a command and suppress output unless it fails.
# On failure, echo the exit code and output.
#
function spt_succeeds
    printf "'$argv' succeeds ... "

    set -l output (eval $argv 2>&1)

    if test $status -ne 0
        fail
        echo_red "Command failed with error $status"
        if test -n "$output"
            echo_msg "Output:"
            echo "$output"
        else
            echo_msg "No output."
        end
    else
        pass
    end
end


#
# Run a command and suppress output unless it succeeds.
# If the command succeeds, echo the output.
#
function spt_fails
    printf "'$argv' fails ... "

    set -l output (eval $argv 2>&1)

    if test $status -eq 0
        fail
        echo_red "Command failed with error $status"
        if test -n "$output"
            echo_msg "Output:"
            echo "$output"
        else
            echo_msg "No output."
        end
    else
        pass
    end
end


#
# Ensure that a string is in the output of a command.
# Suppresses output on success.
# On failure, echo the exit code and output.
#
function spt_contains
    set -l target_string $argv[1]
    set -l remaining_args $argv[2..-1]

    printf "'$remaining_args' output contains '$target_string' ... "

    set -l output (eval $remaining_args 2>&1)

    if not echo "$output" | string match -q -r ".*$target_string.*"
        fail
        echo_red "Command exited with error $status"
        echo_red "'$target_string' was not in output."
        if test -n "$output"
            echo_msg "Output:"
            echo "$output"
        else
            echo_msg "No output."
        end
    else
        pass
    end
end


#
# Ensure that a variable is set.
#
function is_set
    printf "'$argv[1]' is set ... "

    if test -z "$$argv[1]"
        fail
        echo_msg "'$argv[1]' was not set!"
    else
        pass
    end
end


#
# Ensure that a variable is not set.
# Fails and prints the value of the variable if it is set.
#
function is_not_set
    printf "'$argv[1]' is not set ... "

    if test -n "$$argv[1]"
        fail
        echo_msg "'$argv[1]' was set!"
        echo "    $$argv[1]"
    else
        pass
    end
end



# -----------------------------------------------------------------------
# Setup test environment and do some preliminary checks
# -----------------------------------------------------------------------

# Make sure no environment is active
set -e SPACK_ENV
true # ignore failing `set -e`

# Source setup-env.sh before tests
set -gx QA_DIR (dirname (status --current-filename))
source $QA_DIR/../setup-env.fish



# -----------------------------------------------------------------------
# Instead of invoking the module and cd commands, we print the arguments that
# Spack invokes the command with, so we can check that Spack passes the expected
# arguments in the tests below.
#
# We make that happen by defining the fish functions below. NOTE: these overwrite
# existing functions => define them last
# -----------------------------------------------------------------------


function module
    echo "module $argv"
end

function cd
    echo "cd $argv"
end


allocate_testing_global



# -----------------------------------------------------------------------
# Let the testing begin!
# -----------------------------------------------------------------------


title "Testing setup-env.fish with $_sp_shell"

# spack command is now available
spt_succeeds which spack


# create a fake mock package install and store its location for later
title "Setup"
echo "Creating a mock package installation"
spack -m install --fake a

# create a test environment for testing environment commands
echo "Creating a mock environment"
spack env create spack_test_env

# ensure that we uninstall b on exit
function spt_cleanup

    set trapped_error false
    if test $status -ne 0
        set trapped_error true
    end

    echo "Removing test environment before exiting."
    spack env deactivate 2>&1 > /dev/null
    spack env rm -y spack_test_env

    title "Cleanup"
    echo "Removing test packages before exiting."
    spack -m uninstall -yf b a

    echo
    echo "$__spt_success tests succeeded."
    echo "$__spt_errors tests failed."

    if test "$trapped_error" = false
        echo "Exited due to an error."
    end

    if test "$__spt_errors" -eq 0
        if test "$trapped_error" = false
            pass
            exit 0
        else
            fail
            exit 1
        end
    else
        fail
        exit 1
    end

    delete_testing_global
end

trap spt_cleanup EXIT



# -----------------------------------------------------------------------
# Test all spack commands with special env support
# -----------------------------------------------------------------------
title 'Testing `spack`'
spt_contains 'usage: spack ' spack
spt_contains "usage: spack " spack -h
spt_contains "usage: spack " spack help
spt_contains "usage: spack " spack -H
spt_contains "usage: spack " spack help --all

title 'Testing `spack cd`'
spt_contains "usage: spack cd " spack cd -h
spt_contains "usage: spack cd " spack cd --help
spt_contains "cd $b_install" spack cd -i b

title 'Testing `spack module`'
spt_contains "usage: spack module " spack -m module -h
spt_contains "usage: spack module " spack -m module --help
spt_contains "usage: spack module " spack -m module

title 'Testing `spack load`'
set _b_loc (spack -m location -i b)
set _b_ld $_b_loc"/lib"
set _a_loc (spack -m location -i a)
set _a_ld $_a_loc"/lib"

spt_contains "set -gx LD_LIBRARY_PATH $_b_ld" spack -m load --only package --fish b
spt_succeeds spack -m load b
# test a variable MacOS clears and one it doesn't for recursive loads
spt_contains "set -gx LD_LIBRARY_PATH $_a_ld:$_b_ld" spack -m load --fish a
spt_contains "set -gx LIBRARY_PATH $_a_ld:$_b_ld" spack -m load --fish a
spt_succeeds spack -m load --only dependencies a
spt_succeeds spack -m load --only package a
spt_fails spack -m load d
spt_contains "usage: spack load " spack -m load -h
spt_contains "usage: spack load " spack -m load -h d
spt_contains "usage: spack load " spack -m load --help

title 'Testing `spack unload`'
spack -m load b a  # setup
# spt_contains "module unload $b_module" spack -m unload b
spt_succeeds spack -m unload b
spt_succeeds spack -m unload --all
spack -m unload --all # cleanup
spt_fails spack -m unload -l
# spt_contains "module unload -l --arg $b_module" spack -m unload -l --arg b
spt_fails spack -m unload d
spt_contains "usage: spack unload " spack -m unload -h
spt_contains "usage: spack unload " spack -m unload -h d
spt_contains "usage: spack unload " spack -m unload --help

title 'Testing `spack env`'
spt_contains "usage: spack env " spack env -h
spt_contains "usage: spack env " spack env --help

title 'Testing `spack env list`'
spt_contains " spack env list " spack env list -h
spt_contains " spack env list " spack env list --help

title 'Testing `spack env activate`'
spt_contains "No such environment:" spack env activate no_such_environment
spt_contains "usage: spack env activate " spack env activate
spt_contains "usage: spack env activate " spack env activate -h
spt_contains "usage: spack env activate " spack env activate --help

title 'Testing `spack env deactivate`'
spt_contains "Error: No environment is currently active" spack env deactivate
spt_contains "usage: spack env deactivate " spack env deactivate no_such_environment
spt_contains "usage: spack env deactivate " spack env deactivate -h
spt_contains "usage: spack env deactivate " spack env deactivate --help

title 'Testing activate and deactivate together'
echo "Testing 'spack env activate spack_test_env'"
spack env activate spack_test_env
is_set SPACK_ENV

echo "Testing 'spack env deactivate'"
spack env deactivate
is_not_set SPACK_ENV

echo "Testing 'spack env activate spack_test_env'"
spack env activate spack_test_env
is_set SPACK_ENV

echo "Testing 'despacktivate'"
despacktivate
is_not_set SPACK_ENV

#
# NOTE: `--prompt` on fish does nothing => currently not implemented.
#

# echo "Testing 'spack env activate --prompt spack_test_env'"
# spack env activate --prompt spack_test_env
# is_set SPACK_ENV
# is_set SPACK_OLD_PS1
#
# echo "Testing 'despacktivate'"
# despacktivate
# is_not_set SPACK_ENV
# is_not_set SPACK_OLD_PS1
