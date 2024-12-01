# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Pflogger(CMakePackage):
    """A parallel Fortran logger (based on the design of the Python logger)"""

    homepage = "https://github.com/Goddard-Fortran-Ecosystem/pFlogger"
    url = "https://github.com/Goddard-Fortran-Ecosystem/pFlogger/archive/refs/tags/v1.6.1.tar.gz"
    list_url = "https://github.com/Goddard-Fortran-Ecosystem/pFlogger/tags"
    git = "https://github.com/Goddard-Fortran-Ecosystem/pFlogger.git"

    maintainers("mathomp4", "tclune")

    license("Apache-2.0")

    version("develop", branch="develop")
    version("main", branch="main")

    version("1.15.0", sha256="454f05731a3ba50c7ae3ef9463b642c53248ae84ccb3b93455ef2ae2b6858235")
    version("1.14.0", sha256="63422493136f66f61d5148b7b1d278b1e5ca76bd37c578e45e4ae0e967351823")
    version("1.13.2", sha256="934e573134f7f1a22b14eb582ea38dd68eb9dccb10526bfabe51229efe106352")
    version("1.13.1", sha256="d2246d1bf3e5186045ae84c52656168856f693f743700f473cf3d1c99eecae02")
    version("1.13.0", sha256="d46b61162496e227d2982bcdfe9b2c8af6a5734d0fbad9305b1a1547abeac06e")
    version("1.12.0", sha256="ff29b0ce4baf50675edb69c3c7493be5410839b5f81e3ce5405f04925503fb0d")
    version("1.11.0", sha256="bf197b6f223a75c7d3eee23888cdde204b5aea053c308852a3f8f677784b8899")
    version("1.10.0", sha256="8e25564699c0adcbe9a23fded6637668ce659480b39420be5a4c8181cd44ad53")
    version("1.9.5", sha256="baa3ebb83962f1b6c8c5b0413fe9d02411d3e379c76b8c190112e158c10ac0ac")
    version("1.9.3", sha256="f300fab515a25b728889ef6c2ab64aa90e7f94c98fd8190dd11a9b1ebd38117a")
    version("1.9.2", sha256="783879eb1326a911f6e22c016e8530644ed0d315660405f2b43df42ba8670acc")
    version("1.9.1", sha256="918965f5a748a3a62e54751578f5935a820407b988b8455f7f25c266b5b7fe3c")
    version("1.9.0", sha256="aacd9b7e188bee3a54a4e681adde32e3bd95bb556cbbbd2c725c81aca5008003")
    version("1.8.0", sha256="28ce9ac8af374253b6dfd8f53f8fd271c787d432645ec9bc6a5a01601dc56e19")
    version("1.6.1", sha256="114a15daa7994ab7d4eea463c3a9b8fe7df3da7d07a0004b5c40cf155e374916")

    depends_on("fortran", type="build")

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )

    variant("mpi", default=False, description="Enable MPI")

    # pFlogger needs careful versioning to build
    depends_on("gftl@:1.5", when="@:1.6")
    depends_on("gftl-shared@:1.3", when="@:1.6")
    depends_on("yafyaml@1.0-beta5", when="@:1.6")

    depends_on("gftl@1.6:", when="@1.8:")
    depends_on("gftl-shared@1.4:", when="@1.8:")
    depends_on("yafyaml@1.0-beta8:", when="@1.8:")

    depends_on("gftl@1.8.1:", when="@1.9:")
    depends_on("gftl-shared@1.5:", when="@1.9:")
    depends_on("yafyaml@1.0.4:", when="@1.9:")

    depends_on("mpi", when="+mpi")

    # Using pFlogger with MPICH 4 is only supported from version 1.11
    conflicts("^mpich@4:", when="@:1.10")

    # pflogger only works with the Fujitsu compiler from 1.13.0 onwards
    conflicts(
        "%fj",
        when="@:1.12",
        msg="pFlogger only works with the Fujitsu compiler from version 1.13.0 onwards",
    )

    depends_on("cmake@3.12:", type="build")

    def cmake_args(self):
        spec = self.spec
        args = []

        if spec.satisfies("+mpi"):
            args.extend(["-DCMAKE_Fortran_COMPILER=%s" % spec["mpi"].mpifc])

        # From version 1.12 on, there is an `ENABLE_MPI` option that
        # defaults to `ON`. If we don't want MPI, we need to set it to
        # `OFF`
        if spec.satisfies("@1.12: ~mpi"):
            args.append("-DENABLE_MPI=OFF")

        return args
