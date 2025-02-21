# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

source $SPACK_ROOT/share/spack/setup-env.sh

LMOD_DIR=$(spack location -i lmod)

if [[ $LMOD_DIR ]] ; then
    source ${LMOD_DIR}/lmod/lmod/init/bash
    source $SPACK_ROOT/share/spack/setup-env.sh
fi
