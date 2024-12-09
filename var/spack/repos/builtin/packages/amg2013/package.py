# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Amg2013(MakefilePackage):
    """AMG is a parallel algebraic multigrid solver for linear systems arising
    from problems on unstructured grids.  The driver provided with AMG
    builds linear systems for various 3-dimensional problems.
    """

    tags = ["proxy-app", "ecp-proxy-app"]

    homepage = "https://computing.llnl.gov/projects/co-design/amg2013"
    git = "https://github.com/LLNL/AMG.git"

    license("LGPL-2.1-or-later")

    version("develop", branch="master")
    version("1.2", tag="1.2", commit="3ada8a128e311543e84d9d66344ece77924127a8")
    version("1.1", tag="1.1", commit="09fe8a78baf6ba5eaef7d2804f7b653885d60fee")
    version("1.0", tag="1.0", commit="f5b864708ca3ef48a86e1e46fcb812cbbfa80c51")

    depends_on("c", type="build")  # generated

    variant("openmp", default=True, description="Build with OpenMP support")
    variant("optflags", default=False, description="Additional optimizations")
    variant("int64", default=False, description="Use 64-bit integers for global variables")

    depends_on("mpi")

    @property
    def build_targets(self):
        targets = []

        include_cflags = ["-DTIMER_USE_MPI"]
        include_lflags = ["-lm"]

        if self.spec.satisfies("+openmp"):
            include_cflags.append("-DHYPRE_USING_OPENMP")
            include_cflags.append(self.compiler.openmp_flag)
            include_lflags.append(self.compiler.openmp_flag)
            if self.spec.satisfies("+optflags"):
                include_cflags.append("-DHYPRE_USING_PERSISTENT_COMM")
                include_cflags.append("-DHYPRE_HOPSCOTCH")

        if self.spec.satisfies("+int64"):
            include_cflags.append("-DHYPRE_BIGINT")

        targets.append(f"INCLUDE_CFLAGS={' '.join(include_cflags)}")
        targets.append(f"INCLUDE_LFLAGS={' '.join(include_lflags)}")
        targets.append(f"CC={self.spec['mpi'].mpicc}")

        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("test/amg", prefix.bin)
        install_tree("docs", prefix.docs)
