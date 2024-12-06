#!/bin/bash
#
# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# This script ensures that Spack can help users edit an environment's
# manifest file even when it has invalid configuration.
#

export QA_DIR=$(dirname "$0")
export SHARE_DIR=$(cd "$QA_DIR/.." && pwd)

# Include convenience functions
. "$QA_DIR/test-framework.sh"
. "$QA_DIR/setup.sh"

# Source setup-env.sh before tests
. "$SHARE_DIR/setup-env.sh"

env_cfg=""

function cleanup {
  # Regardless of whether the test fails or succeeds, we can't remove the
  # environment without restoring spack.yaml to match the schema
  if [ ! -z "env_cfg" ]; then
    echo "\
spack:
  specs: []
  view: False
" > "$env_cfg"
  fi

  spack env deactivate
  spack env rm -y broken-cfg-env
}

trap cleanup EXIT

spack env create broken-cfg-env
echo "Activating test environment"
spack env activate broken-cfg-env
env_cfg=`spack config --scope=env:broken-cfg-env edit --print-file`
# Save this, so we can make sure it is reported correctly when the environment
# contains broken configuration
orig_manifest_path="$env_cfg"

echo "Environment config file: $env_cfg"
# Make sure we got a manifest file path
contains "spack.yaml" echo "$env_cfg"

# Create an invalid packages.yaml configuration for the environment
echo "\
spack:
  specs: []
  view: False
  packages:
    what:
" > "$env_cfg"

echo "Try 'spack config edit' with broken environment"
manifest_path=`spack config edit --print-file`
# Re-run command for coverage purposes
$coverage_run $(which spack) config edit --print-file

if [ $orig_manifest_path = $manifest_path ]; then
  pass
else
  fail
fi

