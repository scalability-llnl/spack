# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NimrodAai(CMakePackage):
    """NIMROD infrastructure for FEM evaluation, integration and linear algebra
    solves with device accelerated computing through OpenACC and abstract types
    enabled by modern Fortran.
    """

    homepage = "https://gitlab.com/NIMRODteam/open/nimrod-abstract"
    url = "https://gitlab.com/NIMRODteam/open/nimrod-abstract/-/archive/24.2/nimrod-abstract-24.2.tar.gz"
    git = "https://gitlab.com/NIMRODteam/open/nimrod-abstract.git"

    maintainers("jacobrking")

    version("main", branch="main")
    version("24.2", sha256="1dd4d51426f141c058e25cb29870eaf15e0edfb44d80df94e7c65c850ca78eda")
    version("23.9", sha256="34f7ee00bbbe9a6d08304473e8893af9bd94af8dbd0bbd50b8b441057023e179")
    version("23.6", sha256="de7e5c5cc2ad97dc0e66628d29c8153fa807821a316eb9aa8ee21a39c69df800")

    depends_on("fortran", type="build")  # generated

    variant("debug", default=False, description="Whether to enable debug code")
    variant("openacc", default=False, description="Whether to enable OpenACC")
    variant(
        "openacc_autocompare", default=False, description="Whether to enable OpenACC autocompare"
    )
    variant("enable_shared", default=True, description="Whether to build and use shared libraries")
    variant("mpi", default=False, description="Whether to enable MPI")
    variant("time_level1", default=False, description="Whether to add timings at level 1")
    variant("time_level2", default=False, description="Whether to add timings at level 2")
    variant("nvtx_profile", default=False, description="Whether to enable NVTX profiling")
    variant("openacc_cc", default="native", description="OpenACC compute capability")
    variant(
        "trap_fp_exceptions",
        default=False,
        description="Whether to enable trapping of floating point exceptions",
    )

    depends_on("cmake", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("hdf5+fortran~mpi", when="~mpi")
    depends_on("hdf5+fortran+mpi", when="+mpi")

    def cmake_args(self):
        args = [
            self.define_from_variant("DEBUG", "debug"),
            self.define_from_variant("ENABLE_OPENACC", "openacc"),
            self.define_from_variant("ENABLE_MPI", "mpi"),
            self.define_from_variant("ENABLE_SHARED", "enable_shared"),
            self.define_from_variant("NVTX_PROFILE", "nvtx_profile"),
            self.define_from_variant("TIME_LEVEL1", "time_level1"),
            self.define_from_variant("TIME_LEVEL2", "time_level2"),
            self.define_from_variant("TRAP_FP_EXCEPTIONS", "trap_fp_exceptions"),
        ]
        if "+openacc" in self.spec:
            addl_args = [
                self.define_from_variant("ENABLE_OPENACC_AUTOCOMPARE", "openacc_autocompare"),
                self.define_from_variant("OPENACC_CC", "openacc_cc"),
            ]
            args.append(addl_args)
        return args

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check(self):
        with working_dir(self.builder.build_directory):
            ctest("--output-on-failure")
