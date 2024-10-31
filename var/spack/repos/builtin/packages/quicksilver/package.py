# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Quicksilver(MakefilePackage):
    """Quicksilver is a proxy application that represents some elements of the
    Mercury workload.
    """

    tags = ["proxy-app"]

    homepage = "https://codesign.llnl.gov/quicksilver.php"
    url = "https://github.com/LLNL/Quicksilver/tarball/V1.0"
    git = "https://github.com/LLNL/Quicksilver.git"

    maintainers("richards12")

    version("master", branch="master")
    version("1.0", sha256="83371603b169ec75e41fb358881b7bd498e83597cd251ff9e5c35769ef22c59a")

    depends_on("cxx", type="build")  # generated

    variant("openmp", default=True, description="Build with OpenMP support")
    variant("mpi", default=True, description="Build with MPI support")

    depends_on("mpi", when="+mpi")

    build_directory = "src"

    @property
    def build_targets(self):
        targets = []
        spec = self.spec

        targets.append("CXXFLAGS={0}".format(self.compiler.cxx11_flag))

        if "+mpi" in spec:
            targets.append("CXX={0}".format(spec["mpi"].mpicxx))
        else:
            targets.append("CXX={0}".format(spack_cxx))

        if "+openmp+mpi" in spec:
            targets.append(
                "CPPFLAGS=-DHAVE_MPI -DHAVE_OPENMP {0}".format(self.compiler.openmp_flag)
            )
        elif "+openmp" in spec:
            targets.append("CPPFLAGS=-DHAVE_OPENMP {0}".format(self.compiler.openmp_flag))
        elif "+mpi" in spec:
            targets.append("CPPFLAGS=-DHAVE_MPI")

        if "+openmp" in self.spec:
            targets.append("LDFLAGS={0}".format(self.compiler.openmp_flag))

        return targets

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.doc)
        install("src/qs", prefix.bin)
        install("LICENSE.md", prefix.doc)
        install("README.md", prefix.doc)
        install_tree("Examples", prefix.Examples)
