# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zpares(MakefilePackage):
    """z-Pares is designed to compute a few eigenvalues
    and eigenvectors of sparse matrices."""

    homepage = "https://zpares.cs.tsukuba.ac.jp/"
    url = "http://zpares.cs.tsukuba.ac.jp/download/zpares_0.9.6a.tar.gz"

    license("BSD-3-Clause")

    version("0.9.6a", sha256="3c34257d249451b0b984abc985e296ebb73ae5331025f1b8ea08d50301c7cf9a")

    variant("mpi", default=False, description="Activates MPI support")
    variant("mumps", default=False, description="Activates MUMPS support")

    depends_on("mumps+mpi", when="+mumps+mpi")
    depends_on("mumps~mpi", when="+mumps~mpi")
    depends_on("lapack")
    depends_on("blas")
    depends_on("mpi", when="+mpi")

    def edit(self, spec, prefix):
        copy(join_path("Makefile.inc", "make.inc.gfortran.seq"), "make.inc")

    @property
    def build_targets(self):
        targets = []

        if "+mpi" in self.spec:
            targets.append("USE_MPI=1")
            targets.append("FC={0}".format(self.spec["mpi"].mpifc))
        else:
            targets.append("USE_MPI=0")
            targets.append("FC={0}".format(self.compiler.fc))

        if "+mumps" in self.spec:
            targets.append("USE_MUMPS=1")
            targets.append("FFLAG={0}".format(self.compiler.openmp_flag))
            targets.append("LFFLAG={0}".format(self.compiler.openmp_flag))
            targets.append("MUMPS_DIR={0}".format(self.spec["mumps"].prefix))
        else:
            targets.append("USE_MUMPS=0")

        targets.append("BLAS={0}".format(self.spec["blas"].libs.link_flags))
        targets.append("LAPACK={0}".format(self.spec["lapack"].libs.link_flags))

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.lib)
        mkdirp(prefix.include)

        install(join_path("lib", "*.a"), prefix.lib)
        install(join_path("include", "*.mod"), prefix.include)
