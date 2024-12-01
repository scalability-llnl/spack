# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bml(CMakePackage):
    """The basic matrix library (bml) is an implementation of various matrix data
    formats (dense and sparse) and their associated algorithms for basic
    matrix operations used electronic structure solvers."""

    homepage = "https://lanl.github.io/bml/"
    url = "https://github.com/lanl/bml/archive/refs/tags/v2.2.0.tar.gz"
    git = "https://github.com/lanl/bml.git"

    maintainers("jeanlucf22")

    license("BSD-3-Clause")

    version("master", branch="master")
    version("2.2.0", sha256="41703eee605bcb0ce3bcb5dde5914363aaa382393138ab24f02acf84f670fad0")
    version("2.1.2", sha256="d5bb4726759eb35ec66fae7b6ce8b4978cee33fa879aed314bf7aa1fa7eece91")
    version("2.1.1", sha256="412cdc1609e8d66d4a47799806c0974ed3f84c25f09132ad2821a173e8d89261")
    version("2.1.0", sha256="f95f0289d055a91d8499e2a37f785f69ca3b86dc6cf16726ee6c433b8b8a7f62")
    version("2.0.1", sha256="ffb590b745888bbf1ff1892e920c29dd3edd7b29405ade3a738df4db5b1e2370")
    version("2.0.0", sha256="dd9454f825605ee849b68e80bf28c2eaec0d0dd1d491807895352eb08e616bd9")
    version("1.3.1", sha256="d9cbf95467f7a97d0eaa5a1a7a16481a160464c930a593bce4f2a32b012e2c24")
    version("1.3.0", sha256="c2d3de0021b314b3fbdaa5445b96109dc22b1ae5c78363eac08fbde692ffe1ad")
    version("1.2.3", sha256="8106b8ba3d1fb402b98fcfb0110e00ac18264b240b47320268888fc27971aeab")
    version("1.2.2", sha256="babc2fd0229397e418be00f3691277e86f549b5a23cadbcee66078595e9176a0")
    version("1.1.0", sha256="a90ede19d80ed870f0bf1588875a9f371484d89006a7296010d8d791da3eac33")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Build shared libs")
    variant("mpi", default=True, description="Build with MPI Support")

    conflicts("+mpi", when="@:1.2.2")

    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi", when="+mpi")
    depends_on("python", type="build")

    def cmake_args(self):
        args = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
        spec = self.spec
        if spec.satisfies("+mpi"):
            args.append("-DBML_MPI=True")
            args.append("-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc)
            args.append("-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx)
            args.append("-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc)
        else:
            args.append("-DBML_MPI=False")
        return args
