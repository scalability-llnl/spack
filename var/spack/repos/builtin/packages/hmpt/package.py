# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class Hmpt(Package):
    """HMPT is HPE's implementation of 
    the Message Passing Interface (MPI) standard.
 
    Note: HMPT is proprietry software. Spack will search your
    current directory for the download file. Alternatively, add this file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = ""

    provides('mpi')
    provides('mpi@:3.0', when='@3:')
    provides('mpi@:1.3', when='@1:')

    filter_compiler_wrappers(
        'mpicc', 'mpicxx', 'mpif77', 'mpif90', 'mpif77', 'mpif08', relative_root='bin'
    )

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('MPICC',  join_path(self.prefix.bin, 'mpicc'))
        spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpicxx'))
        spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
        spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

        spack_env.set('MPICC_CC', spack_cc)
        spack_env.set('MPICXX_CXX', spack_cxx)
        spack_env.set('MPIF90_F90', spack_fc)

    def setup_dependent_package(self, module, dependent_spec):
        if 'platform=cray' in self.spec:
            self.spec.mpicc = spack_cc
            self.spec.mpicxx = spack_cxx
            self.spec.mpifc = spack_fc
            self.spec.mpif77 = spack_f77
        else:
            self.spec.mpicc = join_path(self.prefix.bin, 'mpicc')
            self.spec.mpicxx = join_path(self.prefix.bin, 'mpicxx')
            self.spec.mpifc = join_path(self.prefix.bin, 'mpif90')
            self.spec.mpif77 = join_path(self.prefix.bin, 'mpif77')

    @property
    def fetcher(self):
        msg = """This package is intended to be a placeholder for HPE's
        system-provided, MPT MPI library

        Add to your packages.yaml (changing the /opt/ path to match 
        where MPT is actually installed):

        packages:
          hmpt:
            paths:
              hmpt@2.20: /opt/
            buildable: False

        """
        raise InstallError(msg)

    def install(self, spec, prefix):
        pass

