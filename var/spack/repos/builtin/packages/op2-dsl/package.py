# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Op2Dsl(MakefilePackage, CudaPackage):
    """OP2 is a high-level embedded domain specific language for writing
    unstructured mesh algorithms with automatic parallelisation on multi-core
    and many-core architectures."""

    homepage = "https://op-dsl.github.io/"
    git = "https://github.com/OP-DSL/OP2-Common.git"

    maintainers("gihanmudalige", "reguly", "bozbez")

    version("master", branch="master")
    version("1.1.0", tag="v1.1.0", commit="22c13b425976e32a6c904f3a5a95ffb761680eb3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    build_directory = "op2"

    variant("mpi", default=False, description="Enable MPI support")

    variant(
        "parmetis", default=True, when="+mpi", description="Enable ParMETIS partitioning support"
    )

    variant(
        "scotch", default=True, when="+mpi", description="Enable PT-Scotch partitioning support"
    )

    depends_on("mpi", when="+mpi")

    depends_on("parmetis", when="+parmetis")
    depends_on("scotch", when="+scotch")

    depends_on("hdf5+fortran+mpi", when="+mpi")
    depends_on("hdf5+fortran~mpi", when="~mpi")

    def edit(self, spec, prefix):
        compiler_map = {
            "gcc": "gnu",
            "cce": "cray",
            "intel": "intel",
            "nvhpc": "nvhpc",
            "xl": "xl",
        }

        if self.spec.compiler.name in compiler_map:
            env["OP2_COMPILER"] = compiler_map[self.spec.compiler.name]

        if "+cuda" in self.spec and spec.variants["cuda_arch"].value[0] != "none":
            env["CUDA_GEN"] = ",".join(spec.variants["cuda_arch"].value)

    def install(self, spec, prefix):
        install_tree("op2/lib", prefix.lib)
        install_tree("op2/include", prefix.include)
        install_tree("op2/mod", prefix.mod)
