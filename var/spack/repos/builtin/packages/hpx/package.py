# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Hpx(CMakePackage, CudaPackage, ROCmPackage):
    """C++ runtime system for parallel and distributed applications."""

    homepage = "https://hpx.stellar-group.org/"
    url = "https://github.com/STEllAR-GROUP/hpx/archive/v0.0.0.tar.gz"
    git = "https://github.com/STEllAR-GROUP/hpx.git"
    maintainers("msimberg", "albestro", "teonnik", "hkaiser", "diehlpk")

    license("BSL-1.0")

    tags = ["e4s"]

    version("master", branch="master")
    version("stable", tag="stable", commit="103a7b8e3719a0db948d1abde29de0ff91e070be")
    version("1.10.0", sha256="5720ed7d2460fa0b57bd8cb74fa4f70593fe8675463897678160340526ec3c19")
    version("1.9.1", sha256="1adae9d408388a723277290ddb33c699aa9ea72defadf3f12d4acc913a0ff22d")
    version("1.9.0", sha256="2a8dca78172fbb15eae5a5e9facf26ab021c845f9c09e61b1912e6cf9e72915a")
    version("1.8.1", sha256="2fc4c10f55e2e6bcdc6f6ff950e26c6d8e218e138fdbd885ee71ccf5c5549054")
    version("1.8.0", sha256="93f147ab7cf0ab4161f37680ea720d3baeb86540a95382f2fb591645b2a9b135")
    version("1.7.1", sha256="008a0335def3c551cba31452eda035d7e914e3e4f77eec679eea070ac71bd83b")
    version("1.7.0", sha256="05099b860410aa5d8a10d6915b1a8818733aa1aa2d5f2b9774730ca7e6de5fac")
    version("1.6.0", sha256="4ab715613c1e1808edc93451781cc9bc98feec4e422ccd4322858a680f6d9017")
    version("1.5.1", sha256="b2f9358ce2a9446b9d8fb1998c30913e7199b007aa82e46d0aa05c763331c635")
    version("1.5.0", sha256="de2901d8ae017592c513e0af9cf58de295abc9802e55ece00424cbd8a3801920")
    version("1.4.1", sha256="965dabe44d17480e326d92da4eec56722d98b33943c53d2b0f8f4655cb208023")
    version("1.4.0", sha256="241a1c47fafba751848fac12446e7bf4ad3d342d5eb2fa1ef94dd904acc329ed")
    version("1.3.0", sha256="cd34da674064c4cc4a331402edbd65c5a1f8058fb46003314ca18fa08423c5ad")
    version("1.2.1", sha256="8cba9b48e919035176d3b7bbfc2c110df6f07803256626f1dad8d9dde16ab77a")
    version("1.2.0", sha256="20942314bd90064d9775f63b0e58a8ea146af5260a4c84d0854f9f968077c170")
    version("1.1.0", sha256="1f28bbe58d8f0da600d60c3a74a644d75ac777b20a018a5c1c6030a470e8a1c9")

    depends_on("cxx", type="build")

    generator("ninja")

    map_cxxstd = lambda cxxstd: "2a" if cxxstd == "20" else cxxstd
    cxxstds = ("11", "14", "17", "20")
    variant(
        "cxxstd",
        default="17",
        values=cxxstds,
        description="Use the specified C++ standard when building.",
    )

    variant(
        "malloc",
        default="tcmalloc",
        description="Define which allocator will be linked in",
        values=("system", "jemalloc", "mimalloc", "tbbmalloc", "tcmalloc"),
    )

    variant(
        "max_cpu_count",
        default="auto",
        description="Max number of OS-threads for HPX applications",
        values=lambda x: isinstance(x, str) and (x.isdigit() or x == "auto"),
    )

    instrumentation_values = ("apex", "google_perftools", "papi", "valgrind", "thread_debug")
    variant(
        "instrumentation",
        values=any_combination_of(*instrumentation_values),
        description="Add support for various kind of instrumentation",
    )

    variant(
        "networking",
        values=any_combination_of("tcp", "mpi").with_default("tcp"),
        description="Support for networking through parcelports",
    )

    default_generic_coroutines = True
    if sys.platform.startswith("linux") or sys.platform == "win32":
        default_generic_coroutines = False
    variant(
        "generic_coroutines",
        default=default_generic_coroutines,
        description="Use Boost.Context as the underlying coroutines"
        " context switch implementation.",
    )

    variant("tools", default=False, description="Build HPX tools")
    variant("examples", default=False, description="Build examples")
    variant("async_mpi", default=False, description="Enable MPI Futures.")
    variant("async_cuda", default=False, description="Enable CUDA Futures.")

    # Build dependencies
    depends_on("python", type=("build", "test", "run"))
    depends_on("pkgconfig", type="build")
    depends_on("git", type="build")
    depends_on("cmake", type="build")

    # Other dependecies
    depends_on("hwloc")
    depends_on(Boost.with_default_variants)
    depends_on("boost +context", when="+generic_coroutines")
    for cxxstd in cxxstds:
        depends_on("boost cxxstd={0}".format(map_cxxstd(cxxstd)), when="cxxstd={0}".format(cxxstd))

    with when("@1.7:"):
        for cxxstd in cxxstds:
            depends_on(f"asio cxxstd={map_cxxstd(cxxstd)}", when=f"cxxstd={cxxstd}")

    depends_on("gperftools", when="malloc=tcmalloc")
    depends_on("jemalloc", when="malloc=jemalloc")
    depends_on("mimalloc", when="malloc=mimalloc")
    depends_on("tbb", when="malloc=tbbmalloc")

    depends_on("mpi", when="networking=mpi")
    depends_on("mpi", when="+async_mpi")

    depends_on("cuda", when="+async_cuda")

    depends_on("otf2", when="instrumentation=apex")
    depends_on("gperftools", when="instrumentation=google_perftools")
    depends_on("papi", when="instrumentation=papi")
    depends_on("valgrind", when="instrumentation=valgrind")

    # Only ROCm or CUDA maybe be enabled at once
    conflicts("+rocm", when="+cuda")

    # Restrictions for 1.9.X
    with when("@1.9:"):
        conflicts("%gcc@:8")
        conflicts("%clang@:9")

    # Restrictions for 1.8.X
    with when("@1.8:"):
        conflicts("cxxstd=14")
        conflicts("%gcc@:7")
        conflicts("%clang@:8")
        depends_on("cuda@11:", when="+cuda")

    # Restrictions for 1.7.X
    with when("@1.7:"):
        depends_on("cmake@3.18.0:", type="build")
        depends_on("boost@1.71.0:")
        depends_on("asio@1.12.0:")
        conflicts("%gcc@:6")
        conflicts("%clang@:6")

    # Restrictions for 1.6.X
    conflicts("+rocm", when="@:1.5")

    # Restrictions for 1.5.x
    conflicts("cxxstd=11", when="@1.5:")

    # Restrictions for 1.2.X
    with when("@:1.2.1"):
        depends_on("cmake@3.9.0:", type="build")
        depends_on("boost@1.62.0:")
        depends_on("hwloc@1.11:")

    # Restrictions before 1.2
    with when("@:1.1.0"):
        depends_on("boost@1.55.0:")
        depends_on("hwloc@1.6:")

    # Patches and one-off conflicts

    # Certain Asio headers don't compile with nvcc from 1.17.0 onwards with
    # C++17. Starting with CUDA 11.3 they compile again.
    conflicts("^asio@1.17.0:", when="+cuda cxxstd=17 ^cuda@:11.2")

    # Starting from ROCm 5.0.0 hipcc miscompiles asio 1.17.0 and newer
    conflicts("^asio@1.17.0:", when="+rocm ^hip@5:")

    # Boost and HIP don't work together in certain versions:
    # https://github.com/boostorg/config/issues/392. Boost 1.78.0 and HPX 1.8.0
    # both include a fix.
    conflicts("^boost@:1.77.0", when="@:1.7 +rocm")

    # libstdc++ has a broken valarray in some versions that clang/hipcc refuses
    # to compile:
    # https://github.com/spack/spack/issues/38104
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=103022
    conflicts("%gcc@9.1:9.4", when="+rocm")
    conflicts("%gcc@10.1:10.3", when="+rocm")
    conflicts("%gcc@11.2", when="+rocm")

    # boost 1.73.0 build problem with HPX 1.4.0 and 1.4.1
    # https://github.com/STEllAR-GROUP/hpx/issues/4728#issuecomment-640685308
    depends_on("boost@:1.72.0", when="@:1.4")

    # COROUTINES
    # ~generic_coroutines conflict is not fully implemented
    # for additional information see:
    # https://github.com/spack/spack/pull/17654
    # https://github.com/STEllAR-GROUP/hpx/issues/4829
    depends_on("boost+context", when="+generic_coroutines")

    _msg_generic_coroutines_platform = "This platform requires +generic_coroutines"
    conflicts("~generic_coroutines", when="platform=darwin", msg=_msg_generic_coroutines_platform)

    _msg_generic_coroutines_target = "This target requires +generic_coroutines"
    conflicts("~generic_coroutines", when="target=aarch64:", msg=_msg_generic_coroutines_target)
    conflicts("~generic_coroutines", when="target=arm:", msg=_msg_generic_coroutines_target)

    # Patches APEX
    patch("git_external.patch", when="@1.3.0 instrumentation=apex")
    patch("mimalloc_no_version_requirement.patch", when="@:1.8.0 malloc=mimalloc")

    def url_for_version(self, version):
        if version >= Version("1.9.0"):
            return "https://github.com/STEllAR-GROUP/hpx/archive/v{}.tar.gz".format(version)
        return "https://github.com/STEllAR-GROUP/hpx/archive/{}.tar.gz".format(version)

    def instrumentation_args(self):
        args = []
        for value in self.instrumentation_values:
            condition = "instrumentation={0}".format(value)
            args.append(self.define("HPX_WITH_{0}".format(value.upper()), condition in self.spec))
        return args

    def cmake_args(self):
        spec, args = self.spec, []

        format_max_cpu_count = lambda max_cpu_count: (
            "" if max_cpu_count == "auto" else max_cpu_count
        )
        args += [
            self.define("HPX_WITH_CXX{0}".format(spec.variants["cxxstd"].value), True),
            self.define_from_variant("HPX_WITH_MALLOC", "malloc"),
            self.define_from_variant("HPX_WITH_CUDA", "cuda"),
            self.define_from_variant("HPX_WITH_HIP", "rocm"),
            self.define_from_variant("HPX_WITH_TOOLS", "tools"),
            self.define_from_variant("HPX_WITH_EXAMPLES", "examples"),
            self.define_from_variant("HPX_WITH_ASYNC_MPI", "async_mpi"),
            self.define_from_variant("HPX_WITH_ASYNC_CUDA", "async_cuda"),
            self.define("HPX_WITH_TESTS", self.run_tests),
            self.define("HPX_WITH_NETWORKING", "networking=none" not in spec),
            self.define("HPX_WITH_PARCELPORT_TCP", spec.satisfies("networking=tcp")),
            self.define("HPX_WITH_PARCELPORT_MPI", spec.satisfies("networking=mpi")),
            self.define(
                "HPX_WITH_MAX_CPU_COUNT",
                format_max_cpu_count(spec.variants["max_cpu_count"].value),
            ),
            self.define_from_variant("HPX_WITH_GENERIC_CONTEXT_COROUTINES", "generic_coroutines"),
            self.define("BOOST_ROOT", spec["boost"].prefix),
            self.define("HWLOC_ROOT", spec["hwloc"].prefix),
            self.define("HPX_WITH_BOOST_ALL_DYNAMIC_LINK", True),
            self.define("BUILD_SHARED_LIBS", True),
            self.define("HPX_DATASTRUCTURES_WITH_ADAPT_STD_TUPLE", False),
        ]

        # Enable unity builds when available
        if spec.satisfies("@1.7:"):
            args += [self.define("HPX_WITH_UNITY_BUILD", True)]

        # HIP support requires compiling with hipcc
        if self.spec.satisfies("+rocm"):
            args += [self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc)]
            if self.spec.satisfies("^cmake@3.21.0:3.21.2"):
                args += [self.define("__skip_rocmclang", True)]

        # Instrumentation
        args += self.instrumentation_args()

        if spec.satisfies("instrumentation=thread_debug"):
            args += [
                self.define("HPX_WITH_THREAD_DEBUG_INFO", True),
                self.define("HPX_WITH_LOGGING", True),
            ]

        if spec.satisfies("instrumentation=apex"):
            args += [
                self.define("APEX_WITH_OTF2", True),
                self.define("OTF2_ROOT", spec["otf2"].prefix),
            ]

            # it seems like there was a bug in the default version of APEX in 1.5.x
            if spec.satisfies("@1.5"):
                args += [self.define("HPX_WITH_APEX_TAG", "v2.3.0")]

        return args
