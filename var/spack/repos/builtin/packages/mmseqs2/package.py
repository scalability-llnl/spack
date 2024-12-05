# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Mmseqs2(CMakePackage):
    """MMseqs2 (Many-against-Many sequence searching) is a software suite to
    search and cluster huge protein and nucleotide sequence sets"""

    homepage = "https://github.com/soedinglab/MMseqs2"
    url = "https://github.com/soedinglab/MMseqs2/archive/refs/tags/14-7e284.tar.gz"

    license("GPL-3.0-only")

    version("15-6f452", sha256="7115ac5a7e2a49229466806aaa760d00204bb08c870e3c231b00e525c77531dc")
    version("14-7e284", sha256="a15fd59b121073fdcc8b259fc703e5ce4c671d2c56eb5c027749f4bd4c28dfe1")
    version("13-45111", sha256="6444bb682ebf5ced54b2eda7a301fa3e933c2a28b7661f96ef5bdab1d53695a2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("openmp", default=False, description="build with OpenMP support")
    variant("mpi", default=False, description="build with MPI support")

    depends_on("zstd")
    depends_on("mpi", when="+mpi")

    # patch to support building with gcc@13:
    patch(
        "https://github.com/soedinglab/MMseqs2/commit/3e43617.patch?full_index=1",
        sha256="673737ac545260e7800ca191c6eee14feef3318d9cfa5005db32bd2ab3c006fe",
        when="@:14 %gcc@13:",
        level=1,
    )

    # apple-clang will build with +openmp with llvm-openmp as a dependency
    # however when running with real data, it threw segmentation faults
    conflicts("%apple-clang", when="+openmp")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append("-DVERSION_OVERRIDE=%s" % self.spec.version)
        args.append("-DUSE_SYSTEM_ZSTD=1")
        if "~openmp" in spec:
            args.append("-DREQUIRE_OPENMP=0")
        if "~mpi" in spec:
            args.append("-DHAVE_MPI=0")
        return args
