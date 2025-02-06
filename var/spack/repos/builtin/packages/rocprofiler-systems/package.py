# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RocprofilerSystems(CMakePackage):
    """Application Profiling, Tracing, and Analysis"""

    homepage = "https://github.com/ROCm/rocprofiler-systems"
    git = "https://github.com/ROCm/rocprofiler-systems.git"
    url = "https://github.com/ROCm/rocprofiler-systems/archive/refs/tags/rocm-6.3.1.tar.gz"

    maintainers("dgaliffiAMD", "afzpatel", "srekolam", "renjithravindrankannath", "jrmadsen")

    license("MIT")

    version("amd-mainline", branch="amd-mainline", submodules=True)
    version("amd-staging", branch="amd-staging", submodules=True)
    version(
        "6.3.2",
        git="https://github.com/ROCm/rocprofiler-systems",
        tag="rocm-6.3.2",
        commit="2fd5fbbef941ff219a1ecef702f8cfaae6e8e5ba",
        submodules=True,
    )
    version(
        "6.3.1",
        git="https://github.com/ROCm/rocprofiler-systems",
        tag="rocm-6.3.1",
        commit="04a84dd0b0df3dfd61f7765696e0e474ec29f10b",
        submodules=True,
    )

    version(
        "6.3.0",
        git="https://github.com/ROCm/rocprofiler-systems",
        tag="rocm-6.3.0",
        commit="71a5e271b5e07efd2948fb6e7b451db5e8e40cb8",
        submodules=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "rocm",
        default=True,
        description="Enable ROCm API, kernel tracing, and GPU HW counters support",
    )
    variant("strip", default=False, description="Faster binary instrumentation, worse debugging")
    variant(
        "python", default=False, description="Enable support for Python function profiling and API"
    )
    variant("papi", default=True, description="Enable HW counters support via PAPI")
    variant("ompt", default=True, description="Enable OpenMP Tools support")
    variant(
        "tau",
        default=False,
        description="Enable support for using TAU markers in omnitrace instrumentation",
    )
    variant(
        "caliper",
        default=False,
        description="Enable support for using Caliper markers in omnitrace instrumentation",
    )
    variant(
        "perfetto_tools",
        default=False,
        description="Install perfetto tools (e.g. traced, perfetto)",
    )
    variant(
        "mpi",
        default=False,
        description=(
            "Enable intercepting MPI functions and aggregating output during finalization "
            "(requires target application to use same MPI installation)"
        ),
    )
    variant(
        "mpi_headers",
        default=True,
        description=(
            "Enable intercepting MPI functions but w/o support for aggregating output "
            "(target application can use any MPI installation)"
        ),
    )

    extends("python", when="+python")

    # hard dependencies
    depends_on("cmake@3.16:", type="build")
    depends_on("dyninst@11.0.1:", type=("build", "run"))
    depends_on("libunwind", type=("build", "run"))
    depends_on("papi+shared", when="+papi")
    depends_on("mpi", when="+mpi")
    depends_on("tau", when="+tau")
    depends_on("caliper", when="+caliper")
    depends_on("python@3:", when="+python", type=("build", "run"))
    depends_on("dyninst@12:", when="+rocm")
    depends_on("m4", when="+rocm")
    depends_on("texinfo", when="+rocm")
    depends_on("libunwind", when="+rocm")
    depends_on("autoconf", when="+rocm")
    depends_on("automake", when="+rocm")
    depends_on("libtool", when="+rocm")
    with when("+rocm"):
        for ver in ["6.3.0", "6.3.1", "6.3.2"]:
            depends_on(f"rocm-smi-lib@{ver}", when=f"@{ver}")
            depends_on(f"hip@{ver}", when=f"@{ver}")
            depends_on(f"roctracer-dev@{ver}", when=f"@{ver}")
            depends_on(f"rocprofiler-dev@{ver}", when=f"@{ver}")

            patch("add_cstdint.patch", when="%gcc@13:")

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define("SPACK_BUILD", True),
            self.define("ROCPROFSYS_BUILD_PAPI", False),
            self.define("ROCPROFSYS_BUILD_PYTHON", True),
            self.define("ROCPROFSYS_BUILD_LIBUNWIND", False),
            self.define("ROCPROFSYS_BUILD_STATIC_LIBGCC", False),
            self.define("ROCPROFSYS_BUILD_STATIC_LIBSTDCXX", False),
            self.define_from_variant("ROCPROFSYS_BUILD_LTO", "ipo"),
            self.define_from_variant("ROCPROFSYS_USE_HIP", "rocm"),
            self.define_from_variant("ROCPROFSYS_USE_MPI", "mpi"),
            self.define_from_variant("ROCPROFSYS_USE_OMPT", "ompt"),
            self.define_from_variant("ROCPROFSYS_USE_PAPI", "papi"),
            self.define_from_variant("ROCPROFSYS_USE_RCCL", "rocm"),
            self.define_from_variant("ROCPROFSYS_USE_ROCM_SMI", "rocm"),
            self.define_from_variant("ROCPROFSYS_USE_ROCTRACER", "rocm"),
            self.define_from_variant("ROCPROFSYS_USE_ROCPROFILER", "rocm"),
            self.define_from_variant("ROCPROFSYS_USE_PYTHON", "python"),
            self.define_from_variant("ROCPROFSYS_USE_MPI_HEADERS", "mpi_headers"),
            self.define_from_variant("ROCPROFSYS_STRIP_LIBRARIES", "strip"),
            self.define_from_variant("ROCPROFSYS_INSTALL_PERFETTO_TOOLS", "perfetto_tools"),
            # timemory arguments
            self.define("TIMEMORY_UNITY_BUILD", False),
            self.define("TIMEMORY_BUILD_CALIPER", False),
            self.define_from_variant("TIMEMORY_USE_TAU", "tau"),
            self.define_from_variant("TIMEMORY_USE_CALIPER", "caliper"),
        ]

        if "+tau" in spec:
            tau_root = spec["tau"].prefix
            args.append(self.define("TAU_ROOT_DIR", tau_root))

        if "+mpi" in spec:
            args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))
            args.append(self.define("MPI_CXX_COMPILER", spec["mpi"].mpicxx))

        if spec.satisfies("@6.3:"):
            args.append(self.define("dl_LIBRARY", "dl"))
            args.append(
                self.define("libunwind_INCLUDE_DIR", self.spec["libunwind"].prefix.include)
            )
        if spec.satisfies("%gcc@13:"):
            self.define("ROCPROFSYS_BUILD_DYNINST", True),
            self.define("DYNINST_BUILD_TBB", True),
        else:
            self.define("ROCPROFSYS_BUILD_DYNINST", False),
        return args

    def flag_handler(self, name, flags):
        if self.spec.satisfies("@6.3:"):
            if name == "ldflags":
                flags.append("-lintl")
        return (flags, None, None)

    def setup_build_environment(self, env):
        if "+tau" in self.spec:
            import glob

            # below is how TAU_MAKEFILE is set in packages/tau/package.py
            pattern = join_path(self.spec["tau"].prefix.lib, "Makefile.*")
            files = glob.glob(pattern)
            if files:
                env.set("TAU_MAKEFILE", files[0])
