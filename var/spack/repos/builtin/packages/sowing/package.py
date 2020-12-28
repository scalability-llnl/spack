# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sowing(AutotoolsPackage):
    """Sowing generates Fortran interfaces and documentation for PETSc
       and MPICH.
    """

    homepage = "http://www.mcs.anl.gov/petsc/index.html"
    url = "http://ftp.mcs.anl.gov/pub/petsc/externalpackages/sowing-1.1.23-p1.tar.gz"

    version('1.1.26-p1', sha256='fa0bd07295e5d768f2c33c8ab32205cc6411d42cb40bde0700fb57f9ee31c3d9')
    version('1.1.25-p1', sha256='c3a5bb170fffeeb1405ec4c3a048744a528d2bef24de29b6ac5e970cfeaddab5')
    version('1.1.23-p1', sha256='3e36f59e06fccbbf7b78d185c5654edaf70cf76f1c584bcbf08c39d7f29125e8')

    def build(self, spec, prefix):
        make('ALL', parallel=False)
