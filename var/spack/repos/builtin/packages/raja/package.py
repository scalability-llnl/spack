# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import socket

from spack.package import *

from .blt import llnl_link_helpers


# Starting with 2022.03.0, the only submodule we want to fetch is tpl/desul
# since there is no package for it. Other RAJA submodules are defined as
# dependencies.
def submodules(package):
    submodules = []
    submodules.append("tpl/desul")
    return submodules


class Raja(CachedCMakePackage, CudaPackage, ROCmPackage):
    """RAJA Parallel Framework."""

    homepage = "https://github.com/LLNL/RAJA"
    git = "https://github.com/LLNL/RAJA.git"
    tags = ["radiuss", "e4s"]

    maintainers("davidbeckingsale", "adrienbernede")

    license("BSD-3-Clause")

    version("develop", branch="develop", submodules=submodules)
    version("main", branch="main", submodules=submodules)
    version(
        "2024.07.0",
        tag="v2024.07.0",
        commit="4d7fcba55ebc7cb972b7cc9f6778b48e43792ea1",
        submodules=submodules,
    )
    version(
        "2024.02.2",
        tag="v2024.02.2",
        commit="593f756b14ac57ded33ee61d8d2292d4beb840e6",
        submodules=submodules,
    )
    version(
        "2024.02.1",
        tag="v2024.02.1",
        commit="3ada0950b0774ec907d30a9eceaf6af7478b833b",
        submodules=submodules,
    )
    version(
        "2024.02.0",
        tag="v2024.02.0",
        commit="82d1b926ada0fbb15a4a6e0adadc30c715cfda7b",
        submodules=submodules,
    )
    version(
        "2023.06.1",
        tag="v2023.06.1",
        commit="9b5f61edf3aa1e6fdbc9a4b30828c81504639963",
        submodules=submodules,
    )
    version(
        "2023.06.0",
        tag="v2023.06.0",
        commit="e330b2560747d5417cd7bd265fab3fb91d32ecbd",
        submodules=submodules,
    )
    version(
        "2022.10.5",
        tag="v2022.10.5",
        commit="3774f51339459bbbdb77055aa23f82919b6335b6",
        submodules=submodules,
    )
    version(
        "2022.10.4",
        tag="v2022.10.4",
        commit="c2a6b1740759ae3ae7c85b35e20dbffbe235355d",
        submodules=submodules,
    )
    version(
        "2022.03.0",
        tag="v2022.03.0",
        commit="4351fe6a50bd579511a625b017c9e054885e7fd2",
        submodules=submodules,
    )
    version(
        "0.14.0",
        tag="v0.14.0",
        commit="357933a42842dd91de5c1034204d937fce0a2a44",
        submodules="True",
    )
    version(
        "0.13.0",
        tag="v0.13.0",
        commit="3047fa720132d19ee143b1fcdacaa72971f5988c",
        submodules="True",
    )
    version(
        "0.12.1",
        tag="v0.12.1",
        commit="9cb6370bb2868e35ebba23cdce927f5f7f9da530",
        submodules="True",
    )
    version(
        "0.12.0",
        tag="v0.12.0",
        commit="32d92e38da41cc8d4db25ec79b9884a73a0cb3a1",
        submodules="True",
    )
    version(
        "0.11.0",
        tag="v0.11.0",
        commit="0502b9b69c4cb60aa0afbdf699b555c76cb18f22",
        submodules="True",
    )
    version(
        "0.10.1",
        tag="v0.10.1",
        commit="be91e040130678b1350dbda56cc352433db758bd",
        submodules="True",
    )
    version(
        "0.10.0",
        tag="v0.10.0",
        commit="53cb89cf788d28bc4ed2b4e6f75483fdd26024aa",
        submodules="True",
    )
    version(
        "0.9.0", tag="v0.9.0", commit="df7ca1fa892b6ac4147c614d2d739d5022f63fc7", submodules="True"
    )
    version(
        "0.8.0", tag="v0.8.0", commit="8d19a8c2cbac611de6f92ad8852b9f3454b27e63", submodules="True"
    )
    version(
        "0.7.0", tag="v0.7.0", commit="caa33b371b586dfae3d8569caee91c5eddfd7b31", submodules="True"
    )
    version(
        "0.6.0", tag="v0.6.0", commit="cc7a97e8b4e52c3de820c9dfacd358822a147871", submodules="True"
    )
    version(
        "0.5.3", tag="v0.5.3", commit="1ca35c0ed2a43a3fa9c6cd70c5d25f16d88ecd8c", submodules="True"
    )
    version(
        "0.5.2", tag="v0.5.2", commit="4d5c3d5d7f311838855f7010810610349e729f64", submodules="True"
    )
    version(
        "0.5.1", tag="v0.5.1", commit="bf340abe5199d7e051520913c9a7a5de336b5820", submodules="True"
    )
    version(
        "0.5.0", tag="v0.5.0", commit="9b539d84fdad049f65caeba836f41031f5baf4cc", submodules="True"
    )
    version(
        "0.4.1", tag="v0.4.1", commit="3618cfe95d6a442fa50fbe7bfbcf654cf9f800b9", submodules="True"
    )
    version(
        "0.4.0", tag="v0.4.0", commit="31b2a48192542c2da426885baa5af0ed57606b78", submodules="True"
    )

    depends_on("cxx", type="build")  # generated

    # export targets when building pre-2.4.0 release with BLT 0.4.0+
    patch(
        "https://github.com/LLNL/RAJA/commit/eca1124ee4af380d6613adc6012c307d1fd4176b.patch?full_index=1",
        sha256="12bb78c00b6683ad3e7fd4e3f87f9776bae074b722431b79696bc862816735ef",
        when="@:0.13.0 ^blt@0.4:",
    )

    # Backward compatibility is stopped from ROCm 6.0
    # Future relase will have the change from PR https://github.com/LLNL/RAJA/pull/1568
    patch(
        "https://github.com/LLNL/RAJA/commit/406eb8dee05a41eb32c421c375688a4863b60642.patch?full_index=1",
        sha256="d9ce5ef038555cbccb330a9016b7be77e56ae0660583cba955dab9d0297a4b07",
        when="^hip@6.0",
    )

    variant("openmp", default=False, description="Build OpenMP backend")
    variant("shared", default=False, description="Build shared libs")
    variant("desul", default=False, description="Build desul atomics backend")
    variant("vectorization", default=False, description="Build SIMD/SIMT intrinsics support")
    variant(
        "omptask", default=False, description="Build OpenMP task variants of internal algorithms"
    )
    variant("omptarget", default=False, description="Build OpenMP on target device support")
    variant("sycl", default=False, description="Build sycl backend")

    variant("plugins", default=False, description="Enable runtime plugins")
    variant("examples", default=True, description="Build examples.")
    variant("exercises", default=True, description="Build exercises.")
    # TODO: figure out gtest dependency and then set this default True
    # and remove the +tests conflict below.
    variant("tests", default=False, description="Build tests")

    # we don't use variants to express the failing test, we only add a variant to
    # define whether we want to run all the tests (including those known to fail)
    # or only the passing ones.
    variant(
        "run-all-tests",
        default=False,
        description="Run all the tests, including those known to fail.",
    )

    depends_on("blt", type="build")
    depends_on("blt@0.6.2:", type="build", when="@2024.02.1:")
    depends_on("blt@0.6.1", type="build", when="@2024.02.0")
    depends_on("blt@0.5.3", type="build", when="@2023.06.0:2023.06.1")
    depends_on("blt@0.5.2:0.5.3", type="build", when="@2022.10.5")
    depends_on("blt@0.5.0:0.5.3", type="build", when="@0.14.1:2022.10.4")
    depends_on("blt@0.4.1", type="build", when="@0.14.0")
    depends_on("blt@0.4.0:0.4.1", type="build", when="@0.13.0")
    depends_on("blt@0.3.6:0.4.1", type="build", when="@:0.12.0")
    conflicts("^blt@:0.3.6", when="+rocm")

    depends_on("camp")
    depends_on("camp+openmp", when="+openmp")
    depends_on("camp+omptarget", when="+omptarget")
    depends_on("camp+sycl", when="+sycl")
    depends_on("camp@2024.07.0:", when="@2024.02.2:")
    depends_on("camp@2024.02.1", when="@2024.02.1")
    depends_on("camp@2024.02.0", when="@2024.02.0")
    depends_on("camp@2023.06.0", when="@2023.06.0:2023.06.1")
    depends_on("camp@2022.10.1:2023.06.0", when="@2022.10.3:2022.10.5")
    depends_on("camp@2022.10.0:2023.06.0", when="@2022.10.0:2022.10.2")
    depends_on("camp@2022.03.2", when="@2022.03.0:2022.03.1")
    depends_on("camp@0.2.2:0.2.3", when="@0.14.0")
    depends_on("camp@0.1.0", when="@0.10.0:0.13.0")

    depends_on("cmake@3.23:", when="@2024.07.0:", type="build")
    depends_on("cmake@3.23:", when="@2022.10.0:2024.02.2+rocm", type="build")
    depends_on("cmake@3.20:", when="@2022.10.0:2024.02.2", type="build")
    depends_on("cmake@3.20:", when="@:2022.03+rocm", type="build")
    depends_on("cmake@3.14:", when="@:2022.03", type="build")

    depends_on("llvm-openmp", when="+openmp %apple-clang")

    depends_on("rocprim", when="+rocm")
    with when("+rocm @0.12.0:"):
        depends_on("camp+rocm")
        for arch in ROCmPackage.amdgpu_targets:
            depends_on(
                "camp+rocm amdgpu_target={0}".format(arch), when="amdgpu_target={0}".format(arch)
            )
        conflicts("+openmp", when="@:2022.03")

    with when("+cuda @0.12.0:"):
        depends_on("camp+cuda")
        for sm_ in CudaPackage.cuda_arch_values:
            depends_on("camp +cuda cuda_arch={0}".format(sm_), when="cuda_arch={0}".format(sm_))

    conflicts("+omptarget +rocm")
    conflicts("+sycl +omptarget")
    conflicts("+sycl +rocm")
    conflicts(
        "+sycl",
        when="@:2024.02.99",
        msg="Support for SYCL was introduced in RAJA after 2024.02 release, "
        "please use a newer release.",
    )

    def _get_sys_type(self, spec):
        sys_type = spec.architecture
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        return sys_type

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libRAJA", root=self.prefix, shared=shared, recursive=True)

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

        entries.append(cmake_cache_option("ENABLE_OPENMP", spec.satisfies("+openmp")))

        if spec.satisfies("+cuda"):
            entries.append(cmake_cache_option("ENABLE_CUDA", True))
        else:
            entries.append(cmake_cache_option("ENABLE_CUDA", False))

        if spec.satisfies("+rocm"):
            entries.append(cmake_cache_option("ENABLE_HIP", True))
            hipcc_flags = []
            if self.spec.satisfies("@0.14.0:"):
                hipcc_flags.append("-std=c++14")
            entries.append(cmake_cache_string("HIP_HIPCC_FLAGS", " ".join(hipcc_flags)))
        else:
            entries.append(cmake_cache_option("ENABLE_HIP", False))

        return entries

    def initconfig_package_entries(self):
        spec = self.spec
        entries = []

        option_prefix = "RAJA_" if spec.satisfies("@0.14.0:") else ""

        # TPL locations
        entries.append("#------------------{0}".format("-" * 60))
        entries.append("# TPLs")
        entries.append("#------------------{0}\n".format("-" * 60))

        entries.append(cmake_cache_path("BLT_SOURCE_DIR", spec["blt"].prefix))
        if "camp" in self.spec:
            entries.append(cmake_cache_path("camp_DIR", spec["camp"].prefix))

        # Build options
        entries.append("#------------------{0}".format("-" * 60))
        entries.append("# Build Options")
        entries.append("#------------------{0}\n".format("-" * 60))

        entries.append(cmake_cache_string("CMAKE_BUILD_TYPE", spec.variants["build_type"].value))
        entries.append(cmake_cache_option("BUILD_SHARED_LIBS", spec.satisfies("+shared")))

        entries.append(cmake_cache_option("RAJA_ENABLE_DESUL_ATOMICS", spec.satisfies("+desul")))

        entries.append(
            cmake_cache_option("RAJA_ENABLE_VECTORIZATION", spec.satisfies("+vectorization"))
        )

        entries.append(cmake_cache_option("RAJA_ENABLE_OPENMP_TASK", spec.satisfies("+omptask")))

        entries.append(
            cmake_cache_option("RAJA_ENABLE_TARGET_OPENMP", spec.satisfies("+omptarget"))
        )

        entries.append(cmake_cache_option("RAJA_ENABLE_SYCL", spec.satisfies("+sycl")))

        # C++17
        if spec.satisfies("@2024.07.0:") and spec.satisfies("+sycl"):
            entries.append(cmake_cache_string("BLT_CXX_STD", "c++17"))
        # C++14
        elif spec.satisfies("@0.14.0:"):
            entries.append(cmake_cache_string("BLT_CXX_STD", "c++14"))

            if spec.satisfies("+desul"):
                if spec.satisfies("+cuda"):
                    entries.append(cmake_cache_string("CMAKE_CUDA_STANDARD", "14"))

        entries.append(
            cmake_cache_option("RAJA_ENABLE_RUNTIME_PLUGINS", spec.satisfies("+plugins"))
        )

        if spec.satisfies("+omptarget"):
            entries.append(
                cmake_cache_string(
                    "BLT_OPENMP_COMPILE_FLAGS", "-fopenmp;-fopenmp-targets=nvptx64-nvidia-cuda"
                )
            )
            entries.append(
                cmake_cache_string(
                    "BLT_OPENMP_LINK_FLAGS", "-fopenmp;-fopenmp-targets=nvptx64-nvidia-cuda"
                )
            )

        entries.append(
            cmake_cache_option(
                "{}ENABLE_EXAMPLES".format(option_prefix), spec.satisfies("+examples")
            )
        )
        if spec.satisfies("@0.14.0:"):
            entries.append(
                cmake_cache_option(
                    "{}ENABLE_EXERCISES".format(option_prefix), spec.satisfies("+exercises")
                )
            )
        else:
            entries.append(cmake_cache_option("ENABLE_EXERCISES", spec.satisfies("+exercises")))

        # TODO: Treat the workaround when building tests with spack wrapper
        #       For now, removing it to test CI, which builds tests outside of wrapper.
        # Work around spack adding -march=ppc64le to SPACK_TARGET_ARGS which
        # is used by the spack compiler wrapper.  This can go away when BLT
        # removes -Werror from GTest flags
        #
        # if self.spec.satisfies("%clang target=ppc64le:")
        #   or (not self.run_tests and not spec.satisfies("+tests")):
        if not self.run_tests and not spec.satisfies("+tests"):
            entries.append(cmake_cache_option("ENABLE_TESTS", False))
        else:
            entries.append(cmake_cache_option("ENABLE_TESTS", True))
            if not spec.satisfies("+run-all-tests"):
                if spec.satisfies("%clang@12.0.0:13.9.999"):
                    entries.append(
                        cmake_cache_string(
                            "CTEST_CUSTOM_TESTS_IGNORE",
                            "test-algorithm-sort-OpenMP.exe;test-algorithm-stable-sort-OpenMP.exe",
                        )
                    )
                excluded_tests = [
                    "test-algorithm-sort-Cuda.exe",
                    "test-algorithm-stable-sort-Cuda.exe",
                    "test-algorithm-sort-OpenMP.exe",
                    "test-algorithm-stable-sort-OpenMP.exe",
                ]
                if spec.satisfies("+cuda %clang@12.0.0:13.9.999"):
                    entries.append(
                        cmake_cache_string("CTEST_CUSTOM_TESTS_IGNORE", ";".join(excluded_tests))
                    )
                if spec.satisfies("+cuda %xl@16.1.1.12"):
                    entries.append(
                        cmake_cache_string(
                            "CTEST_CUSTOM_TESTS_IGNORE",
                            "test-algorithm-sort-Cuda.exe;test-algorithm-stable-sort-Cuda.exe",
                        )
                    )

        entries.append(cmake_cache_option("RAJA_HOST_CONFIG_LOADED", True))

        return entries

    def cmake_args(self):
        return []

    @property
    def build_relpath(self):
        """Relative path to the cmake build subdirectory."""
        return join_path("..", self.builder.build_dirname)

    @run_after("install")
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to a
        relative install test subdirectory for use during `spack test run`."""
        # Now copy the relative files
        cache_extra_test_sources(self, self.build_relpath)

        # Ensure the path exists since relying on a relative path at the
        # same level as the normal stage source path.
        mkdirp(install_test_root(self))

    @property
    def _extra_tests_path(self):
        # TODO: The tests should be converted to re-build and run examples
        # TODO: using the installed libraries.
        return join_path(install_test_root(self), self.build_relpath, "bin")

    def run_example(self, exe, expected):
        """run and check outputs of the example"""
        with working_dir(self._extra_tests_path):
            example = which(exe)
            if example is None:
                raise SkipTest(f"{exe} was not built")

            out = example(output=str.split, error=str.split)
            check_outputs(expected, out)

    def test_line_of_sight(self):
        """check line of sight example"""
        self.run_example(
            "ex5_line-of-sight_solution",
            [r"C-style sequential", r"RAJA sequential", r"result -- PASS"],
        )

    def test_stencil_offset_layout(self):
        """check stencil offset layout"""
        self.run_example(
            "ex6_stencil-offset-layout_solution", [r"RAJA Views \(permuted\)", r"result -- PASS"]
        )

    def test_tiled_matrix(self):
        """check tiled matrix transpose"""
        self.run_example(
            "ex8_tiled-matrix-transpose_solution",
            [r"C-version", r"RAJA sequential", r"result -- PASS"],
        )

    def test_dynamic_tile(self):
        """check kernel dynamic tile"""
        self.run_example("kernel-dynamic-tile", [r"Running index", r"(24,24)"])

    def test_plugin_example(self):
        """check plugin example"""
        self.run_example("plugin-example", [r"Launching host kernel for the 10 time"])

    def test_matrix_multiply(self):
        """check batched matrix multiple tutorial"""
        self.run_example(
            "tut_batched-matrix-multiply", [r"batched matrix multiplication", r"result -- PASS"]
        )

    def test_wave_equation(self):
        """check wave equation"""
        self.run_example("wave-eqn", [r"Max Error = 2", r"Evolved solution to time"])
