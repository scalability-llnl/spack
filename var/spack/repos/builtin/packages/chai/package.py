# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import socket

from spack.package import *

from .blt import llnl_link_helpers


class Chai(CachedCMakePackage, CudaPackage, ROCmPackage):
    """
    Copy-hiding array interface for data migration between memory spaces
    """

    homepage = "https://github.com/LLNL/CHAI"
    git = "https://github.com/LLNL/CHAI.git"
    tags = ["ecp", "e4s", "radiuss"]

    maintainers("davidbeckingsale", "adayton1", "adrienbernede")

    license("BSD-3-Clause")

    version("develop", branch="develop", submodules=False)
    version(
        "2024.07.0",
        tag="v2024.07.0",
        commit="df7741f1dbbdc5fff5f7d626151fdf1904e62b19",
        submodules=False,
    )
    version(
        "2024.02.2",
        tag="v2024.02.2",
        commit="5ba0944d862513f600432c34b009824875df27e5",
        submodules=False,
    )
    version(
        "2024.02.1",
        tag="v2024.02.1",
        commit="7597134729bd3a38b45b67b4dfbf7f199d8106f3",
        submodules=False,
    )
    version(
        "2024.02.0",
        tag="v2024.02.0",
        commit="31773a2f0d30f3f64c82939f60fc4da32cf33261",
        submodules=False,
    )
    version(
        "2023.06.0",
        tag="v2023.06.0",
        commit="6fe3470ad020303530af2f3dbbfe18826bd3319b",
        submodules=False,
    )
    version(
        "2022.10.0",
        tag="v2022.10.0",
        commit="9510efd33b06e4443b15447eebb7dad761822654",
        submodules=False,
    )
    version(
        "2022.03.0",
        tag="v2022.03.0",
        commit="f0b809de1ac194376866b3ac0f5933d4146ec09e",
        submodules=False,
    )
    version(
        "2.4.0", tag="v2.4.0", commit="77d22da28187245a2c5454cf471c0c352bd98ad7", submodules=True
    )
    version(
        "2.3.0", tag="v2.3.0", commit="42f3fbcc0b966227b40b4467dc919a4c24f07196", submodules=True
    )
    version(
        "2.2.2", tag="v2.2.2", commit="56e75fc0f805b2746f3992af0c00c474513e3b24", submodules=True
    )
    version(
        "2.2.1", tag="v2.2.1", commit="c912f583828ea5963850816e3e232cc45608ccf7", submodules=True
    )
    version(
        "2.2.0", tag="v2.2.0", commit="18536c61a4817db6b3b3025f35e2dd3ae532330c", submodules=True
    )
    version(
        "2.1.1", tag="v2.1.1", commit="496911e00d15c350560860f7964cd5fb5ab7f515", submodules=True
    )
    version(
        "2.1.0", tag="v2.1.0", commit="fff02768068a64970b34760a1041585319edee87", submodules=True
    )
    version(
        "2.0.0", tag="v2.0.0", commit="63139cf45443b1266950826b165e042c7679b557", submodules=True
    )
    version(
        "1.2.0", tag="v1.2.0", commit="7bb5bc12e4508db45910d8e2b98444687da7ebf6", submodules=True
    )
    version(
        "1.1.0", tag="v1.1.0", commit="907d5f40d653a73955387067799913397807adf3", submodules=True
    )
    version("1.0", tag="v1.0", commit="501a098ad879dc8deb4a74fcfe8c08c283a10627", submodules=True)

    depends_on("cxx", type="build")  # generated

    # Patching Umpire for dual BLT targets import changed MPI target name in Umpire link interface
    # We propagate the patch here.
    patch("change_mpi_target_name_umpire_patch.patch", when="@2022.10.0:2023.06.0")

    variant("enable_pick", default=False, description="Enable pick method")
    variant(
        "separable_compilation",
        default=True,
        description="Build with CUDA_SEPARABLE_COMPILATION flag on ",
    )
    variant("shared", default=True, description="Build Shared Libs")
    variant("mpi", default=False, description="Enable MPI support")
    variant("raja", default=False, description="Build plugin for RAJA")
    variant("examples", default=True, description="Build examples.")
    variant("openmp", default=False, description="Build using OpenMP")
    # TODO: figure out gtest dependency and then set this default True
    # and remove the +tests conflict below.
    variant(
        "tests",
        default="none",
        values=("none", "basic", "benchmarks"),
        multi=False,
        description="Tests to run",
    )

    depends_on("cmake", type="build")
    depends_on("cmake@3.23:", type="build", when="@2024.07.0:")
    depends_on("cmake@3.14:", type="build", when="@2022.03.0:2024.2")
    depends_on("cmake@3.9:", type="build", when="+cuda")
    depends_on("cmake@3.8:", type="build")

    depends_on("blt", type="build")
    depends_on("blt@0.6.2:", type="build", when="@2024.02.1:")
    depends_on("blt@0.6.1", type="build", when="@2024.02.0")
    depends_on("blt@0.5.3", type="build", when="@2023.06.0")
    depends_on("blt@0.5.2:0.5.3", type="build", when="@2022.10.0")
    depends_on("blt@0.5.0:0.5.3", type="build", when="@2022.03.0")
    depends_on("blt@0.4.1:0.5.3", type="build", when="@2.4.0")
    depends_on("blt@0.4.0:0.5.3", type="build", when="@2.3.0")
    depends_on("blt@0.3.6:0.5.3", type="build", when="@:2.2.2")
    conflicts("^blt@:0.3.6", when="+rocm")

    depends_on("umpire")
    depends_on("umpire@2024.07.0:", when="@2024.07.0:")
    depends_on("umpire@2024.02.1", when="@2024.02.1")
    depends_on("umpire@2024.02.0", when="@2024.02.0")
    depends_on("umpire@2023.06.0", when="@2023.06.0")
    depends_on("umpire@2022.10.0:2023.06.0", when="@2022.10.0")
    depends_on("umpire@2022.03.0:2023.06.0", when="@2022.03.0")
    depends_on("umpire@6.0.0", when="@2.4.0")
    depends_on("umpire@4.1.2", when="@2.2.0:2.3.0")

    depends_on("umpire+mpi", when="+mpi")

    with when("+cuda"):
        depends_on("umpire+cuda")
        for sm_ in CudaPackage.cuda_arch_values:
            depends_on("umpire+cuda cuda_arch={0}".format(sm_), when="cuda_arch={0}".format(sm_))
        with when("@2024.02.0:"):
            depends_on("umpire~fmt_header_only")

    with when("+rocm"):
        depends_on("umpire+rocm")
        for arch in ROCmPackage.amdgpu_targets:
            depends_on(
                "umpire+rocm amdgpu_target={0}".format(arch), when="amdgpu_target={0}".format(arch)
            )

    with when("+raja"):
        depends_on("raja~openmp", when="~openmp")
        depends_on("raja+openmp", when="+openmp")
        depends_on("raja@2024.07.0:", when="@2024.07.0:")
        depends_on("raja@2024.02.2", when="@2024.02.2")
        depends_on("raja@2024.02.1", when="@2024.02.1")
        depends_on("raja@2024.02.0", when="@2024.02.0")
        depends_on("raja@2023.06.0", when="@2023.06.0")
        depends_on("raja@2022.10.0:2023.06.0", when="@2022.10.0")
        depends_on("raja@2022.03.0:2023.06.0", when="@2022.03.0")
        depends_on("raja@0.14.0", when="@2.4.0")
        depends_on("raja@0.13.0", when="@2.3.0")
        depends_on("raja@0.12.0", when="@2.2.0:2.2.2")

        with when("+cuda"):
            depends_on("raja+cuda")
            for sm_ in CudaPackage.cuda_arch_values:
                depends_on("raja+cuda cuda_arch={0}".format(sm_), when="cuda_arch={0}".format(sm_))
        with when("+rocm"):
            depends_on("raja+rocm")
            for arch in ROCmPackage.amdgpu_targets:
                depends_on(
                    "raja+rocm amdgpu_target={0}".format(arch),
                    when="amdgpu_target={0}".format(arch),
                )

    depends_on("mpi", when="+mpi")

    def _get_sys_type(self, spec):
        sys_type = spec.architecture
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        return sys_type

    @property
    def cache_name(self):
        hostname = socket.gethostname()
        if "SYS_TYPE" in env:
            hostname = hostname.rstrip("1234567890")
        return "{0}-{1}-{2}@{3}-{4}.cmake".format(
            hostname,
            self._get_sys_type(self.spec),
            self.spec.compiler.name,
            self.spec.compiler.version,
            self.spec.dag_hash(8),
        )

    def initconfig_compiler_entries(self):
        spec = self.spec
        compiler = self.compiler
        # Default entries are already defined in CachedCMakePackage, inherit them:
        entries = super().initconfig_compiler_entries()

        if spec.satisfies("+rocm"):
            entries.insert(0, cmake_cache_path("CMAKE_CXX_COMPILER", spec["hip"].hipcc))

        llnl_link_helpers(entries, spec, compiler)

        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec
        entries = super().initconfig_hardware_entries()

        entries.append("#------------------{0}".format("-" * 30))
        entries.append("# Package custom hardware settings")
        entries.append("#------------------{0}\n".format("-" * 30))

        if spec.satisfies("+cuda"):
            entries.append(cmake_cache_option("ENABLE_CUDA", True))
            if spec.satisfies("+separable_compilation"):
                entries.append(cmake_cache_option("CMAKE_CUDA_SEPARABLE_COMPILATION", True))
                entries.append(cmake_cache_option("CUDA_SEPARABLE_COMPILATION", True))
        else:
            entries.append(cmake_cache_option("ENABLE_CUDA", False))

        if spec.satisfies("+rocm"):
            entries.append(cmake_cache_option("ENABLE_HIP", True))
        else:
            entries.append(cmake_cache_option("ENABLE_HIP", False))

        return entries

    def initconfig_mpi_entries(self):
        spec = self.spec

        entries = super(Chai, self).initconfig_mpi_entries()
        entries.append(cmake_cache_option("ENABLE_MPI", spec.satisfies("+mpi")))

        return entries

    def initconfig_package_entries(self):
        spec = self.spec
        entries = []

        option_prefix = "CHAI_" if spec.satisfies("@2022.03.0:") else ""

        # TPL locations
        entries.append("#------------------{0}".format("-" * 60))
        entries.append("# TPLs")
        entries.append("#------------------{0}\n".format("-" * 60))

        # - BLT
        entries.append(cmake_cache_path("BLT_SOURCE_DIR", spec["blt"].prefix))

        # - RAJA
        if spec.satisfies("+raja"):
            entries.append(cmake_cache_option("{}ENABLE_RAJA_PLUGIN".format(option_prefix), True))
            entries.append(cmake_cache_path("RAJA_DIR", spec["raja"].prefix))
        else:
            entries.append(cmake_cache_option("{}ENABLE_RAJA_PLUGIN".format(option_prefix), False))

        # - Umpire
        entries.append(cmake_cache_path("umpire_DIR", spec["umpire"].prefix))

        # Build options
        entries.append("#------------------{0}".format("-" * 60))
        entries.append("# Build Options")
        entries.append("#------------------{0}\n".format("-" * 60))

        entries.append(cmake_cache_string("CMAKE_BUILD_TYPE", spec.variants["build_type"].value))
        entries.append(cmake_cache_option("BUILD_SHARED_LIBS", spec.satisfies("+shared")))

        # Generic options that have a prefixed equivalent in CHAI CMake
        entries.append(cmake_cache_option("ENABLE_OPENMP", spec.satisfies("+openmp")))
        entries.append(cmake_cache_option("ENABLE_EXAMPLES", spec.satisfies("+examples")))
        entries.append(cmake_cache_option("ENABLE_DOCS", False))
        if spec.satisfies("tests=benchmarks"):
            # BLT requires ENABLE_TESTS=True to enable benchmarks
            entries.append(cmake_cache_option("ENABLE_BENCHMARKS", True))
            entries.append(cmake_cache_option("ENABLE_TESTS", True))
        else:
            entries.append(cmake_cache_option("ENABLE_TESTS", not spec.satisfies("tests=none")))

        # Prefixed options that used to be name without one
        entries.append(
            cmake_cache_option(
                "{}ENABLE_PICK".format(option_prefix), spec.satisfies("+enable_pick")
            )
        )

        return entries

    def cmake_args(self):
        return []
