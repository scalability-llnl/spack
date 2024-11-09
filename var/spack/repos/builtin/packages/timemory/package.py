# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
#
# ----------------------------------------------------------------------------

from spack.package import *


class Timemory(CMakePackage, PythonExtension):
    """Modular profiling toolkit and suite of libraries and tools
    for C/C++/Fortran/CUDA/Python"""

    homepage = "https://timemory.readthedocs.io/en/latest/"
    git = "https://github.com/NERSC/timemory.git"
    maintainers("jrmadsen")

    license("MIT")

    version("master", branch="master", submodules=True)
    version("develop", branch="develop", submodules=True)
    version("3.2.3", commit="d535e478646e331a4c65cfd8c8f759c9a363ccc9", submodules=True)
    version("3.2.2", commit="4725f4e4a3eea3b80b50a01ea088b5d5a1cf40ab", submodules=True)
    version("3.2.1", commit="76ff978d9b1568b7f88a3de82bb84a2042003630", submodules=True)
    version("3.2.0", commit="2bdd28e87224558060e27da90f9b6fcfb20dd324", submodules=True)
    version("3.1.0", commit="b12de7eeed699d820693fecd6136daff744f21b6", submodules=True)
    version("3.0.1", commit="ef638e1cde90275ce7c0e12fc4902c27bcbdeefd", submodules=True)
    version("3.0.0", commit="b36b1673b2c6b7ff3126d8261bef0f8f176c7beb", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")
    variant("static", default=False, description="Build static libraries")
    variant("pic", default=True, description="Build position independent code")
    variant("install_headers", default=True, description="Install headers")
    variant("install_config", default=True, description="Install cmake configuration files")
    variant("python", default=False, description="Enable Python support")
    variant(
        "python_hatchet",
        default=False,
        description="Build Python hatchet submodule " "(does not conflict with py-hatchet)",
    )
    variant(
        "python_line_profiler",
        default=False,
        description=(
            "Build timemorys extended version of py-line-profiler "
            "(does not conflict with py-line-profiler)"
        ),
    )
    variant(
        "python_deps",
        default=False,
        description="Install non-critical python dependencies "
        "(may significantly increase spack install time)",
    )
    variant("mpi", default=False, description="Enable support for MPI aggregation")
    variant("nccl", default=False, description="Enable support for wrapping NCCL functions")
    variant("tau", default=False, description="Enable TAU support")
    variant("papi", default=False, description="Enable PAPI support")
    variant("cuda", default=False, description="Enable CUDA support")
    variant("cupti", default=False, description="Enable CUPTI support")
    variant("tools", default=True, description="Build/install extra tools")
    variant("vtune", default=False, description="Enable VTune support")
    variant("upcxx", default=False, description="Enable UPC++ support")
    variant("gotcha", default=False, description="Enable GOTCHA support")
    variant("likwid", default=False, description="Enable LIKWID CPU marker API support (perfmon)")
    variant(
        "likwid_nvmon", default=False, description="Enable LIKWID GPU marker API support (nvmon)"
    )
    variant("caliper", default=False, description="Enable Caliper support")
    variant("dyninst", default=False, description="Build dynamic instrumentation tools")
    variant("examples", default=False, description="Build/install examples")
    variant("gperftools", default=False, description="Enable gperftools support")
    variant(
        "kokkos_tools",
        default=False,
        description=(
            "Build generic kokkos-tools libraries, e.g. " "kp_timemory, kp_timemory_filter"
        ),
    )
    variant(
        "kokkos_build_config",
        default=False,
        description=(
            "Build pre-configured (i.e. dedicated) kokkos-tools "
            "libraries, e.g. kp_timemory_cpu_flops"
        ),
    )
    variant(
        "cuda_arch",
        default="auto",
        description="CUDA architecture name",
        values=(
            "auto",
            "kepler",
            "kepler30",
            "kepler32",
            "kepler35",
            "kepler37",
            "tesla",
            "maxwell",
            "maxwell50",
            "maxwell52",
            "maxwell53",
            "pascal",
            "pascal60",
            "pascal61",
            "volta",
            "volta70",
            "volta72",
            "turing",
            "turing75",
            "ampere",
            "ampere80",
            "ampere86",
        ),
        multi=True,
    )
    variant(
        "cpu_target",
        default="auto",
        description=("Build for specific cpu architecture (specify " "cpu-model)"),
    )
    variant(
        "use_arch",
        default=False,
        description=(
            "Build all of timemory w/ cpu_target architecture "
            "flags (default: roofline toolkit only)"
        ),
    )
    variant(
        "tls_model",
        default="global-dynamic",
        description="Thread-local static model",
        multi=False,
        values=("global-dynamic", "local-dynamic", "initial-exec", "local-exec"),
    )
    variant("lto", default=False, description="Build with link-time optimization")
    variant(
        "statistics",
        default=True,
        description=("Build components w/ support for statistics " "(min/max/stddev)"),
    )
    variant(
        "extra_optimizations",
        default=True,
        description="Build timemory with extra optimization flags",
    )
    variant(
        "cxxstd",
        default="14",
        description="C++ language standard",
        values=("14", "17", "20"),
        multi=False,
    )
    variant(
        "cudastd",
        default="14",
        description="CUDA language standard",
        values=("14", "17"),
        multi=False,
    )
    variant(
        "unity_build",
        default=True,
        description="Build with CMAKE_UNITY_BUILD=ON for faster builds "
        "but larger memory consumption",
    )
    variant(
        "mpip_library", default=False, description="Build stand-alone timemory-mpip GOTCHA library"
    )
    variant("ompt", default=False, description=("Enable OpenMP tools support"))
    variant("ompt_library", default=False, description="Build stand-alone timemory-ompt library")
    variant("allinea_map", default=False, description="Enable Allinea ARM-MAP support")
    variant(
        "require_packages",
        default=True,
        description=("find_package(...) resulting in NOTFOUND " "generates error"),
    )
    variant("compiler", default=True, description="Enable compiler instrumentation support")
    variant(
        "ert",
        default=True,
        description="Enable extern templates for empirical roofline toolkit (ERT)",
    )

    extends("python", when="+python")
    depends_on("cmake@3.15:", type="build")
    depends_on("python@3:", when="+python", type=("build", "run"))
    depends_on("py-cython", when="+python_hatchet", type=("build"))
    depends_on("py-cython", when="+python_line_profiler", type=("build"))
    depends_on("pil", when="+python+python_deps", type=("run"))
    depends_on("py-numpy", when="+python+python_deps", type=("run"))
    depends_on("py-hatchet", when="+python+python_deps", type=("run"))
    depends_on("py-matplotlib", when="+python+python_deps", type=("run"))
    depends_on("py-mpi4py", when="+python+mpi+python_deps", type=("run"))
    depends_on("py-pandas", when="+python_deps+python_hatchet", type=("run"))
    depends_on("py-pydot", when="+python_deps+python_hatchet", type=("run"))
    depends_on("py-pyyaml", when="+python_deps+python_hatchet", type=("run"))
    depends_on("py-multiprocess", when="+python_deps+python_hatchet", type=("run"))
    depends_on("mpi", when="+mpi")
    depends_on("nccl", when="+nccl")
    depends_on("tau", when="+tau")
    depends_on("papi", when="+papi")
    depends_on("cuda", when="+cuda")
    depends_on("cuda", when="+cupti")
    depends_on("upcxx", when="+upcxx")
    depends_on("likwid", when="+likwid~likwid_nvmon")
    depends_on("likwid+cuda", when="+likwid+likwid_nvmon")
    depends_on("gotcha", when="+gotcha")
    depends_on("caliper", when="+caliper")
    depends_on("dyninst", when="+dyninst")
    depends_on("gperftools", when="+gperftools")
    depends_on("intel-parallel-studio", when="+vtune")
    depends_on("arm-forge", when="+allinea_map")

    conflicts(
        "+python",
        when="~shared~static",
        msg="+python requires building shared or static libraries",
    )
    conflicts(
        "~pic",
        "~shared+static+python",
        msg="Python bindings cannot be be linked to static libs w/o +pic",
    )
    conflicts("+python_deps", when="~python")
    conflicts("+cupti", when="~cuda", msg="CUPTI requires CUDA")
    conflicts("+kokkos_tools", when="~tools", msg="+kokkos_tools requires +tools")
    conflicts(
        "+kokkos_build_config",
        when="~tools~kokkos_tools",
        msg="+kokkos_build_config requires +tools+kokkos_tools",
    )
    conflicts(
        "tls_model=local-dynamic", when="+python", msg="+python require tls_model=global-dynamic"
    )
    conflicts(
        "tls_model=initial-exec", when="+python", msg="+python require tls_model=global-dynamic"
    )
    conflicts(
        "tls_model=local-exec", when="+python", msg="+python require tls_model=global-dynamic"
    )
    conflicts("+nccl", when="~gotcha", msg="+nccl requires +gotcha")
    conflicts(
        "+nccl", when="~shared~static", msg="+nccl requires building shared or static libraries"
    )
    conflicts("+mpip_library", when="~mpi", msg="+mpip_library requires +mpi")
    conflicts("+mpip_library", when="~gotcha", msg="+mpip_library requires +gotcha")
    conflicts(
        "+mpip_library",
        when="~shared~static",
        msg="+mpip_library requires building shared or static libraries",
    )
    conflicts("+ompt_library", when="~ompt", msg="+ompt_library requires +ompt")
    conflicts(
        "+ompt_library",
        when="~shared~static",
        msg="+ompt_library requires building shared or static libraries",
    )
    conflicts("+likwid_nvmon", when="~likwid", msg="+likwid_nvmon requires +likwid")

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define("SPACK_BUILD", True),
            self.define("TIMEMORY_BUILD_OMPT", False),  # disable submodule
            self.define("TIMEMORY_BUILD_PYTHON", True),
            self.define("TIMEMORY_BUILD_GOTCHA", False),  # disable submodule
            self.define("TIMEMORY_BUILD_CALIPER", False),  # disable submodule
            self.define("TIMEMORY_BUILD_TESTING", False),
            self.define("TIMEMORY_USE_MPI_LINK_FLAGS", False),
            self.define("CMAKE_INSTALL_RPATH_USE_LINK_PATH", True),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("BUILD_STATIC_LIBS", "static"),
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
            self.define_from_variant("CMAKE_CUDA_STANDARD", "cudastd"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            self.define_from_variant("CpuArch_TARGET", "cpu_target"),
            self.define_from_variant("TIMEMORY_TLS_MODEL", "tls_model"),
            self.define_from_variant("TIMEMORY_UNITY_BUILD", "unity_build"),
            self.define_from_variant("TIMEMORY_REQUIRE_PACKAGES", "require_packages"),
            self.define_from_variant("TIMEMORY_INSTALL_HEADERS", "install_headers"),
            self.define_from_variant("TIMEMORY_INSTALL_CONFIG", "install_config"),
            self.define_from_variant("TIMEMORY_BUILD_ERT", "ert"),
            self.define_from_variant("TIMEMORY_BUILD_COMPILER_INSTRUMENTATION", "compiler"),
            self.define_from_variant("TIMEMORY_BUILD_LTO", "lto"),
            self.define_from_variant("TIMEMORY_BUILD_TOOLS", "tools"),
            self.define_from_variant("TIMEMORY_BUILD_EXAMPLES", "examples"),
            self.define_from_variant("TIMEMORY_BUILD_NCCLP_LIBRARY", "nccl"),
            self.define_from_variant("TIMEMORY_BUILD_MALLOCP_LIBRARY", "gotcha"),
            self.define_from_variant("TIMEMORY_BUILD_MPIP_LIBRARY", "mpip_library"),
            self.define_from_variant("TIMEMORY_BUILD_OMPT_LIBRARY", "ompt_library"),
            self.define_from_variant("TIMEMORY_BUILD_KOKKOS_TOOLS", "kokkos_tools"),
            self.define_from_variant("TIMEMORY_BUILD_KOKKOS_CONFIG", "kokkos_build_config"),
            self.define_from_variant("TIMEMORY_BUILD_EXTRA_OPTIMIZATIONS", "extra_optimizations"),
            self.define_from_variant("TIMEMORY_BUILD_PYTHON_HATCHET", "python_hatchet"),
            self.define_from_variant(
                "TIMEMORY_BUILD_PYTHON_LINE_PROFILER", "python_line_profiler"
            ),
            self.define_from_variant("TIMEMORY_USE_MPI", "mpi"),
            self.define_from_variant("TIMEMORY_USE_TAU", "tau"),
            self.define_from_variant("TIMEMORY_USE_ARCH", "use_arch"),
            self.define_from_variant("TIMEMORY_USE_PAPI", "papi"),
            self.define_from_variant("TIMEMORY_USE_OMPT", "ompt"),
            self.define_from_variant("TIMEMORY_USE_CUDA", "cuda"),
            self.define_from_variant("TIMEMORY_USE_NCCL", "nccl"),
            self.define_from_variant("TIMEMORY_USE_CUPTI", "cupti"),
            self.define_from_variant("TIMEMORY_USE_VTUNE", "vtune"),
            self.define_from_variant("TIMEMORY_USE_UPCXX", "upcxx"),
            self.define_from_variant("TIMEMORY_USE_PYTHON", "python"),
            self.define_from_variant("TIMEMORY_USE_GOTCHA", "gotcha"),
            self.define_from_variant("TIMEMORY_USE_LIKWID", "likwid"),
            self.define_from_variant("TIMEMORY_USE_LIKWID_PERFMON", "likwid"),
            self.define_from_variant("TIMEMORY_USE_LIKWID_NVMON", "likwid_nvmon"),
            self.define_from_variant("TIMEMORY_USE_DYNINST", "dyninst"),
            self.define_from_variant("TIMEMORY_USE_CALIPER", "caliper"),
            self.define_from_variant("TIMEMORY_USE_GPERFTOOLS", "gperftools"),
            self.define_from_variant("TIMEMORY_USE_STATISTICS", "statistics"),
            self.define_from_variant("TIMEMORY_USE_ALLINEA_MAP", "allinea_map"),
        ]

        if "+mpi" in spec:
            args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))
            args.append(self.define("MPI_CXX_COMPILER", spec["mpi"].mpicxx))

        if "+cuda" in spec:
            # newer versions use 'TIMEMORY_CUDA_ARCH'
            key = "CUDA_ARCH" if spec.satisfies("@:3.0.1") else "TIMEMORY_CUDA_ARCH"
            args.append(self.define_from_variant(key, "cuda_arch"))
            args.append(self.define_from_variant("CMAKE_CUDA_STANDARD", "cudastd"))

        return args
