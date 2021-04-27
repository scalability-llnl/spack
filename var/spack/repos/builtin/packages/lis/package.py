# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Lis(AutotoolsPackage):
    """Lis (Library of Iterative Solvers for linear systems,
       pronounced [lis]) is a parallel software library for
       solving discretized linear equations and eigenvalue
       problems that arise in the numerical solution of partial
       differential equations using iterative methods."""

    homepage = "https://www.ssisc.org/lis/index.en.html"
    url      = "https://www.ssisc.org/lis/dl/lis-2.0.27.zip"

    version('2.0.27', sha256='85f32f4abbc94d1b40b22c10b915170271b19822b6aa6939b1cb295f6e455237')

    variant('mpi', default=False, description='Build with MPI library')
    variant('omp', default=False, description='Build with openMP library')
    variant('f90', default=False, description='enable FORTRAN 90 compatible interfaces')

    depends_on('mpi', when='+mpi')

    def configure_args(self):
        config_args = []
        config_args.extend(self.enable_or_disable('mpi'))
        config_args.extend(self.enable_or_disable('omp'))
        config_args.extend(self.enable_or_disable('f90'))

        if self.spec.satisfies('%fj'):
            config_args.append('CLIBS=-lm')
            config_args.append('FCLDFLAGS=-mlcmain=main')

        return config_args
