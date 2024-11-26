# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hpccg(MakefilePackage):
    """Proxy Application. Intended to be the 'best approximation
    to an unstructured implicit finite element or finite volume
    application in 800 lines or fewer.'
    """

    homepage = "https://mantevo.org/about/applications/"
    url = "https://downloads.mantevo.org/releaseTarballs/miniapps/HPCCG/HPCCG-1.0.tar.gz"

    tags = ["proxy-app"]

    version("1.0", sha256="5be1b8cc3246811bfc9d6d7072be29455777d61b585675512ae52043ea64cefc")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Build with MPI support")
    variant("openmp", default=True, description="Build with OpenMP support")

    # Optional dependencies
    depends_on("mpi", when="+mpi")

    @property
    def build_targets(self):
        targets = []

        if self.spec.satisfies("+mpi"):
            targets.append("CXX={0}".format(self.spec["mpi"].mpicxx))
            targets.append("LINKER={0}".format(self.spec["mpi"].mpicxx))
            targets.append("USE_MPI=-DUSING_MPI")
        else:
            targets.append("CXX=c++")
            targets.append("LINKER=c++")

        if self.spec.satisfies("+openmp"):
            targets.append("USE_OMP=-DUSING_OMP")
            targets.append("OMP_FLAGS={0}".format(self.compiler.openmp_flag))

        # Remove Compiler Specific Optimization Flags
        if "%gcc" not in self.spec:
            targets.append("CPP_OPT_FLAGS=")

        return targets

    def install(self, spec, prefix):
        # Manual installation
        mkdirp(prefix.bin)
        mkdirp(prefix.doc)

        install("test_HPCCG", prefix.bin)
        install("README", prefix.doc)
        install("weakScalingRunScript", prefix.bin)
        install("strongScalingRunScript", prefix.bin)
