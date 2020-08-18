# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import imp
import os
import spack.util.environment as env_utils

class Mpi(Package):
    """Virtual package for the Message Passing Interface."""
    homepage = 'https://www.mpi-forum.org/'
    virtual = True

    run_env_variables = ['MPICC', 'MPICXX', 'MPIF77', 'MPIF90']
    dep_spec_variables = ['mpicc', 'mpicxx', 'mpif77', 'mpifc']

    def check_interface(self, provider):
        pass
