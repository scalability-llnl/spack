# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class QmdProgress(CMakePackage):
    """PROGRESS: Parallel, Rapid O(N) and Graph-based Recursive Electronic
    Structure Solver.
    This library is focused on the development of general solvers that are
    commonly used in quantum chemistry packages."""

    homepage = "https://qmd-progress.readthedocs.io/"
    url = "https://github.com/lanl/qmd-progress/archive/refs/tags/v1.2.0.tar.gz"
    git = "https://github.com/lanl/qmd-progress.git"

    maintainers("jeanlucf22")

    version("master", branch="master")
    version("1.2.0", sha256="d41708f0e9c12d0e421a9fa883f8b12478cf4faa7453703143f32c093626638e")
    version("1.1.0", sha256="757d2606d7b7f38e7f8f491bf7369b88de55062bae0b12a9928f0a5acae993bd")
    version("1.0.0", sha256="eed87e68b4a1533a3ed70c1662feca4ac890b985f3326fc94522c2f71f198fdc")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("graphlib", default=False, description="Build with Metis Suppport")
    variant("mpi", default=True, description="Build with MPI Support")
    variant("shared", default=True, description="Build shared libs")
    variant("benchmarks", default=True, description="Build with benchmark drivers")

    depends_on("bml")
    depends_on("mpi", when="+mpi")
    depends_on("metis", when="+graphlib")

    def cmake_args(self):
        spec = self.spec
        args = ["-DCMAKE_Fortran_FLAGS=-ffree-line-length-none"]
        if "+shared" in spec:
            args.append("-DBUILD_SHARED_LIBS=ON")
        else:
            args.append("-DBUILD_SHARED_LIBS=OFF")
        if "+mpi" in spec:
            args.append("-DPROGRESS_MPI=yes")
            args.append("-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc)
            args.append("-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx)
            args.append("-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc)
        else:
            args.append("-DPROGRESS_MPI=no")
        if "+graphlib" in spec:
            args.append("-DPROGRESS_GRAPHLIB=yes")
        else:
            args.append("-DPROGRESS_GRAPHLIB=no")
        if "+benchmarks" in spec:
            args.append("-DPROGRESS_BENCHMARKS=yes")

        return args
