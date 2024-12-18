# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sowing(AutotoolsPackage):
    """Sowing generates Fortran interfaces and documentation for PETSc
    and MPICH.
    """

    homepage = "https://bitbucket.org/petsc/pkg-sowing"
    url = "https://ftp.mcs.anl.gov/pub/petsc/externalpackages/sowing-1.1.23-p1.tar.gz"
    git = "https://bitbucket.org/petsc/pkg-sowing"
    maintainers("balay")

    version("master", branch="master")
    version("1.1.26-p8", sha256="2ef4d6db2075230247306e3d0194ffb3e4591aeb05bd244647c72dc1a4e52994")
    version("1.1.26-p1", sha256="fa0bd07295e5d768f2c33c8ab32205cc6411d42cb40bde0700fb57f9ee31c3d9")
    version("1.1.25-p1", sha256="c3a5bb170fffeeb1405ec4c3a048744a528d2bef24de29b6ac5e970cfeaddab5")
    version("1.1.23-p1", sha256="3e36f59e06fccbbf7b78d185c5654edaf70cf76f1c584bcbf08c39d7f29125e8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    def build(self, spec, prefix):
        make("ALL", parallel=False)
