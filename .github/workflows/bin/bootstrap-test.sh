#!/bin/bash
set -e
source share/spack/setup-env.sh
$PYTHON bin/spack bootstrap disable github-actions-v0.5
$PYTHON bin/spack bootstrap disable spack-install
$PYTHON bin/spack $SPACK_FLAGS solve zlib
tree $BOOTSTRAP/store
exit 0
