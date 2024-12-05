# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Ghost(CMakePackage, CudaPackage):
    """GHOST: a General, Hybrid and Optimized Sparse Toolkit.
    This library provides highly optimized building blocks for implementing
    sparse iterative eigenvalue and linear solvers multi- and manycore
    clusters and on heterogenous CPU/GPU machines. For an iterative solver
    library using these kernels, see the phist package.
    """

    homepage = "https://www.bitbucket.org/essex/ghost/"
    git = "https://bitbucket.org/essex/ghost/ghost.git"

    maintainers("jthies")

    license("BSD-3-Clause")

    version("develop", branch="devel")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("mpi", default=True, description="enable/disable MPI")
    variant("scotch", default=False, description="enable/disable matrix reordering with PT-SCOTCH")
    variant("zoltan", default=False, description="enable/disable matrix reordering with Zoltan")

    # ###################### Dependencies ##########################

    # Everything should be compiled position independent (-fpic)
    depends_on("cmake@3.5:", type="build")
    depends_on("hwloc")
    depends_on("blas")
    depends_on("mpi", when="+mpi")
    depends_on("scotch", when="+scotch")
    depends_on("zoltan", when="+zoltan")

    conflicts("^hwloc@2:")

    def cmake_args(self):
        spec = self.spec
        # note: we require the cblas_include_dir property from the blas
        # provider, this is implemented at least for intel-mkl and
        # netlib-lapack
        args = [
            self.define_from_variant("GHOST_ENABLE_MPI", "mpi"),
            self.define_from_variant("GHOST_USE_CUDA", "cuda"),
            self.define_from_variant("GHOST_USE_SCOTCH", "scotch"),
            self.define_from_variant("GHOST_USE_ZOLTAN", "zoltan"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            "-DCBLAS_INCLUDE_DIR:STRING=%s" % format(spec["blas"].headers.directories[0]),
            "-DBLAS_LIBRARIES=%s" % spec["blas:c"].libs.joined(";"),
        ]
        return args

    def check(self):
        make("test")
