# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# A testing framework for any POSIX-compatible shell.
#

# ------------------------------------------------------------------------
# Functions for color output.
# ------------------------------------------------------------------------

# Colors for output
red='\033[1;31m'
cyan='\033[1;36m'
green='\033[1;32m'
reset='\033[0m'

echo_red() {
    printf "${red}$*${reset}\n"
}

echo_green() {
    printf "${green}$*${reset}\n"
}

echo_msg() {
    printf "${cyan}$*${reset}\n"
}

# ------------------------------------------------------------------------
# Generic functions for testing shell code.
# ------------------------------------------------------------------------

# counts of test successes and failures.
success=0
errors=0

# Print out a header for a group of tests.
title() {
    echo
    echo_msg "$@"
    echo_msg "---------------------------------"
}

# echo FAIL in red text; increment failures
fail() {
    echo_red FAIL
    errors=$((errors+1))
}

#
# Echo SUCCESS in green; increment successes
#
pass() {
    echo_green SUCCESS
    success=$((success+1))
}

#
# Run a command and suppress output unless it fails.
# On failure, echo the exit code and output.
#
succeeds() {
    printf "'%s' succeeds ... " "$*"
    output=$("$@" 2>&1)
    err="$?"

    if [ "$err" != 0 ]; then
        fail
        echo_red "Command failed with error $err."
        if [ -n "$output" ]; then
            echo_msg "Output:"
            echo "$output"
        else
            echo_msg "No output."
        fi
    else
        pass
    fi
}

#
# Run a command and suppress output unless it succeeds.
# If the command succeeds, echo the output.
#
fails() {
    printf "'%s' fails ... " "$*"
    output=$("$@" 2>&1)
    err="$?"

    if [ "$err" = 0 ]; then
        fail
        echo_red "Command failed with error $err."
        if [ -n "$output" ]; then
            echo_msg "Output:"
            echo "$output"
        else
            echo_msg "No output."
        fi
    else
        pass
    fi
}

#
# Ensure that a string is in the output of a command.
# Suppresses output on success.
# On failure, echo the exit code and output.
#
contains() {
    string="$1"
    shift

    printf "'%s' output contains '$string' ... " "$*"
    output=$("$@" 2>&1)
    err="$?"

    if [ "${output#*$string}" = "${output}" ]; then
        fail
        echo_red "Command exited with error $err."
        echo_red "'$string' was not in output."
        if [ -n "$output" ]; then
            echo_msg "Output:"
            echo "$output"
        else
            echo_msg "No output."
        fi
    else
        pass
    fi
}

#
# Ensure that a string is not in the output of a command. The command must have a 0 exit
# status to guard against false positives. Suppresses output on success.
# On failure, echo the exit code and output.
#
does_not_contain() {
    string="$1"
    shift

    printf "'%s' output does not contain '$string' ... " "$*"
    output=$("$@" 2>&1)
    err="$?"

    if [ "$err" != 0 ]; then
        fail
    elif [ "${output#*$string}" = "${output}" ]; then
        pass
        return
    else
        fail
        echo_red "'$string' was in the output."
    fi
    if [ -n "$output" ]; then
        echo_msg "Output:"
        echo "$output"
    else
        echo_msg "No output."
    fi
}

#
# Ensure that a variable is set.
#
is_set() {
    printf "'%s' is set ... " "$1"
    if eval "[ -z \${${1:-}+x} ]"; then
        fail
        echo_msg "$1 was not set!"
    else
        pass
    fi
}

#
# Ensure that a variable is not set.
# Fails and prints the value of the variable if it is set.
#
is_not_set() {
    printf "'%s' is not set ... " "$1"
    if eval "[ ! -z \${${1:-}+x} ]"; then
        fail
        echo_msg "$1 was set:"
        echo "    $1"
    else
        pass
    fi
}

#
# Report the number of tests that succeeded and failed on exit.
#
teardown() {
    if [ "$?" != 0 ]; then
        trapped_error=true
    else
        trapped_error=false
    fi

    if type cleanup &> /dev/null
    then
        cleanup
    fi

    echo
    echo "$success tests succeeded."
    echo "$errors tests failed."

    if [ "$trapped_error" = true ]; then
        echo "Exited due to an error."
    fi

    if [ "$errors" = 0 ] && [ "$trapped_error" = false ]; then
        pass
        exit 0
    else
        fail
        exit 1
    fi
}

trap teardown EXIT
