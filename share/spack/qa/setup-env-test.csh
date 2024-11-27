#!/bin/csh
#
# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# This tests that Spack's setup-env.csh init script works.
#
# There are limited tests here so far, as we haven't ported the unit test
# functions we have for sh/bash/zsh/fish to csh.
#

# -----------------------------------------------------------------------
# Setup test environment and do some preliminary checks
# -----------------------------------------------------------------------

# find spack but don't call it SPACK_ROOT -- we want to ensure that
# setup-env.csh sets that.
set QA_DIR = `dirname $0`
set SPACK_DIR = `cd $QA_DIR/../../.. && pwd`

# Make sure no environment is active, and SPACK_ROOT is not set
unsetenv SPACK_ENV
unsetenv SPACK_ROOT

# Source setup-env.sh before tests
source "$SPACK_DIR/share/spack/setup-env.csh"

echo -n "SPACK_ROOT is set..."
if (! $?SPACK_ROOT) then
    echo "FAIL"
    echo "Error: SPACK_ROOT not set by setup-env.csh"
    exit 1
else
    echo "SUCCESS"
endif

echo -n "SPACK_ROOT is set correctly..."
if ("$SPACK_ROOT" != "$SPACK_DIR") then
    echo "FAIL"
    echo "Error: SPACK_ROOT not set correctly by setup-env.csh"
    echo "    Expected: '$SPACK_DIR'"
    echo "    Found:    '$SPACK_ROOT'"
    exit 1
else
    echo "SUCCESS"
endif

echo -n "spack is in the path..."
set spack_script = `which \spack`
if ("$spack_script" != "$SPACK_DIR/bin/spack") then
    echo "FAIL"
    echo "Error: could not find spack after sourcing."
    echo "    Expected: '$SPACK_DIR/bin/spack'"
    echo "    Found:    '$spack_script'"
    exit 1
else
    echo "SUCCESS"
endif

echo -n "spack is aliased to something after sourcing..."
set spack_alias = `which spack`
if ("$spack_alias" !~ 'spack: aliased to '*) then
    echo "FAIL"
    echo "Error: spack not aliased after sourcing."
    echo "    Expected: 'spack: aliased to [...]'"
    echo "    Found:    '$spack_alias'"
    exit 1
else
    echo "SUCCESS"
endif

echo "SUCCESS"
exit 0
