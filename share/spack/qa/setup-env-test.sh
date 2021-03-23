#!/bin/sh
#
# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# This script tests that Spack's setup-env.sh init script works.
#
# The tests are portable to bash, zsh, and bourne shell, and can be run
# in any of these shells.
#

export QA_DIR=$(dirname "$0")
export SHARE_DIR=$(cd "$QA_DIR/.." && pwd)
export SPACK_ROOT=$(cd "$QA_DIR/../../.." && pwd)

. "$QA_DIR/test-framework.sh"

# -----------------------------------------------------------------------
# Instead of invoking the module commands, we print the
# arguments that Spack invokes the command with, so we can check that
# Spack passes the expected arguments in the tests below.
#
# We make that happen by defining the sh functions below.
# -----------------------------------------------------------------------
module() {
    echo module "$@"
}

# -----------------------------------------------------------------------
# Setup test environment and do some preliminary checks
# -----------------------------------------------------------------------

# Make sure no environment is active
unset SPACK_ENV

# Fail on undefined variables
set -u

# Source setup-env.sh before tests
. "$SHARE_DIR/setup-env.sh"

# Bash should expand aliases even when non-interactive
if [ -n "${BASH:-}" ]; then
    shopt -s expand_aliases
fi

title "Testing setup-env.sh with $_sp_shell"

# Spack command is now available
succeeds which spack

# Mock cd command (intentionally define only AFTER setup-env.sh)
cd() {
    echo cd "$@"
}

# Create a fake mock package install and store its location for later
title "Setup"
echo "Creating a mock package installation"
spack -m install --fake a
a_install=$(spack location -i a)
a_module=$(spack -m module tcl find a)

b_install=$(spack location -i b)
b_module=$(spack -m module tcl find b)

# Create a test environment for testing environment commands
echo "Creating a mock environment"
spack env create spack_test_env
test_env_location=$(spack location -e spack_test_env)

# Ensure that we uninstall b on exit
cleanup() {
    echo "Removing test environment before exiting."
    spack env deactivate 2>&1 > /dev/null
    spack env rm -y spack_test_env

    title "Cleanup"
    echo "Removing test packages before exiting."
    spack -m uninstall -yf b a
}

# -----------------------------------------------------------------------
# Test all spack commands with special env support
# -----------------------------------------------------------------------
title 'Testing `spack`'
contains 'usage: spack ' spack
contains "usage: spack " spack -h
contains "usage: spack " spack help
contains "usage: spack " spack -H
contains "usage: spack " spack help --all

title 'Testing `spack cd`'
contains "usage: spack cd " spack cd -h
contains "usage: spack cd " spack cd --help
contains "cd $b_install" spack cd -i b

title 'Testing `spack module`'
contains "usage: spack module " spack -m module -h
contains "usage: spack module " spack -m module --help
contains "usage: spack module " spack -m module

title 'Testing `spack load`'
contains "export LD_LIBRARY_PATH=$(spack -m location -i b)/lib" spack -m load --only package --sh b
succeeds spack -m load b
fails spack -m load -l
# test a variable MacOS clears and one it doesn't for recursive loads
contains "export LD_LIBRARY_PATH=$(spack -m location -i a)/lib:$(spack -m location -i b)/lib" spack -m load --sh a
succeeds spack -m load --only dependencies a
succeeds spack -m load --only package a
fails spack -m load d
contains "usage: spack load " spack -m load -h
contains "usage: spack load " spack -m load -h d
contains "usage: spack load " spack -m load --help

title 'Testing `spack unload`'
spack -m load b a  # setup
succeeds spack -m unload b
succeeds spack -m unload --all
spack -m unload --all # cleanup
fails spack -m unload -l
fails spack -m unload d
contains "usage: spack unload " spack -m unload -h
contains "usage: spack unload " spack -m unload -h d
contains "usage: spack unload " spack -m unload --help

title 'Testing `spack env`'
contains "usage: spack env " spack env -h
contains "usage: spack env " spack env --help

title 'Testing `spack env list`'
contains " spack env list " spack env list -h
contains " spack env list " spack env list --help

title 'Testing `spack env activate`'
contains "No such environment:" spack env activate no_such_environment
contains "usage: spack env activate " spack env activate
contains "usage: spack env activate " spack env activate -h
contains "usage: spack env activate " spack env activate --help

title 'Testing `spack env deactivate`'
contains "Error: No environment is currently active" spack env deactivate
contains "usage: spack env deactivate " spack env deactivate no_such_environment
contains "usage: spack env deactivate " spack env deactivate -h
contains "usage: spack env deactivate " spack env deactivate --help

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

echo "Testing 'spack env activate --prompt spack_test_env'"
spack env activate --prompt spack_test_env
is_set SPACK_ENV
is_set SPACK_OLD_PS1

echo "Testing 'despacktivate'"
despacktivate
is_not_set SPACK_ENV
is_not_set SPACK_OLD_PS1
