# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

source $SPACK_ROOT/share/spack/setup-env.sh

LMOD_DIR=$(spack location -i lmod)

if [[ $LMOD_DIR ]] ; then
    source ${LMOD_DIR}/lmod/lmod/init/bash
    source $SPACK_ROOT/share/spack/setup-env.sh
fi
