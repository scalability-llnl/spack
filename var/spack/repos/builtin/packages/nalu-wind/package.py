# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


def _parse_float(val):
    try:
        return float(val) > 0.0
    except ValueError:
        return False


class NaluWind(CMakePackage, CudaPackage, ROCmPackage):
    """Nalu-Wind: Wind energy focused variant of Nalu."""

    homepage = "https://nalu-wind.readthedocs.io"
    git = "https://github.com/exawind/nalu-wind.git"
    url = "https://github.com/Exawind/nalu-wind/archive/refs/tags/v2.0.0.tar.gz"

    maintainers("jrood-nrel", "psakievich")

    tags = ["ecp", "ecp-apps"]

    version("master", branch="master", submodules=True)
    version("2.1.0", tag="v2.1.0", submodules=True)
    version("2.0.0", tag="v2.0.0", submodules=True)

    variant("pic", default=True, description="Position independent code")
    variant(
        "abs_tol",
        default=1.0e-15,
        values=_parse_float,
        description="Absolute tolerance for regression tests",
    )
    variant(
        "rel_tol",
        default=1.0e-12,
        values=_parse_float,
        description="Relative tolerance for regression tests",
    )
    variant("openfast", default=False, description="Compile with OpenFAST support")
    variant("tioga", default=False, description="Compile with Tioga support")
    variant("hypre", default=True, description="Compile with Hypre support")
    variant("trilinos-solvers", default=False, description="Compile with Trilinos Solvers support")
    variant("catalyst", default=False, description="Compile with Catalyst support")
    variant("shared", default=True, description="Build shared libraries")
    variant("fftw", default=False, description="Compile with FFTW support")
    variant("fsi", default=False, description="Enable fluid-structure-interaction models")
    variant("boost", default=False, description="Enable Boost integration")
    variant("gpu-aware-mpi", default=False, description="gpu-aware-mpi")
    variant("wind-utils", default=False, description="Build wind-utils")
    variant("umpire", default=False, description="Enable Umpire")
    variant(
        "tests", default=False, description="Enable regression tests and clone the mesh submodule"
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="+openfast")

    depends_on("mpi")
    depends_on("yaml-cpp@0.6.0:0.7.0")
    depends_on("openfast@4.0.0:+cxx+netcdf", when="+fsi")
    depends_on("trilinos@15.1.1", when="@=2.1.0")
    depends_on("trilinos@13.4.1", when="@=2.0.0")
    depends_on("hypre@2.29.0:", when="@2.0.0:+hypre")
    depends_on(
        "trilinos@13:+exodus+tpetra+zoltan+stk~superlu-dist~superlu+hdf5+shards~hypre+gtest "
        "gotype=long cxxstd=17"
    )
    depends_on("trilinos~cuda~wrapper", when="~cuda")
    depends_on("openfast@2.6.0: +cxx", when="+openfast")
    depends_on("tioga@1.0.0:", when="+tioga")
    depends_on("hypre@2.18.2: ~int64+mpi~superlu-dist", when="+hypre")
    depends_on("trilinos+muelu+belos+amesos2+ifpack2", when="+trilinos-solvers")
    depends_on("kokkos-nvcc-wrapper", type="build", when="+cuda")
    depends_on("trilinos-catalyst-ioss-adapter", when="+catalyst")
    depends_on("fftw+mpi", when="+fftw")
    depends_on("nccmp")
    depends_on("boost +filesystem +iostreams cxxstd=14", when="+boost")
    depends_on("hypre+gpu-aware-mpi", when="+gpu-aware-mpi")
    depends_on("hypre+umpire", when="+umpire")
    depends_on("trilinos~shared", when="+trilinos-solvers")
    # indirect dependency needed to make original concretizer work
    depends_on("netcdf-c+parallel-netcdf")

    for _arch in CudaPackage.cuda_arch_values:
        depends_on(
            "trilinos~shared+cuda+cuda_rdc+wrapper cuda_arch={0}".format(_arch),
            when="+cuda cuda_arch={0}".format(_arch),
        )
        depends_on(
            "hypre@2.30.0: +cuda cuda_arch={0}".format(_arch),
            when="+hypre+cuda cuda_arch={0}".format(_arch),
        )
    for _arch in ROCmPackage.amdgpu_targets:
        depends_on(
            "trilinos~shared+rocm+rocm_rdc amdgpu_target={0}".format(_arch),
            when="+rocm amdgpu_target={0}".format(_arch),
        )
        depends_on(
            "hypre@2.30.0: +rocm amdgpu_target={0}".format(_arch),
            when="+hypre+rocm amdgpu_target={0}".format(_arch),
        )

    conflicts(
        "~hypre~trilinos-solvers",
        msg="nalu-wind: Must enable at least one of the linear-solvers: hypre or trilinos-solvers",
    )
    conflicts(
        "+shared",
        when="+cuda",
        msg="invalid device functions are generated with shared libs and cuda",
    )
    conflicts(
        "+shared",
        when="+rocm",
        msg="invalid device functions are generated with shared libs and rocm",
    )
    conflicts("+cuda", when="+rocm")
    conflicts("+rocm", when="+cuda")
    conflicts("^hypre+cuda", when="~cuda")
    conflicts("^hypre+rocm", when="~rocm")
    conflicts("^hypre+sycl")
    conflicts("^trilinos+cuda", when="~cuda")
    conflicts("^trilinos+rocm", when="~rocm")
    conflicts("+shared", when="+trilinos-solvers")

    def setup_dependent_run_environment(self, env, dependent_spec):
        spec = self.spec
        if spec.satisfies("+cuda") or spec.satisfies("+rocm"):
            env.set("CUDA_LAUNCH_BLOCKING", "1")
            env.set("CUDA_MANAGED_FORCE_DEVICE_ALLOC", "1")
            env.set("HIP_LAUNCH_BLOCKING", "1")
            env.set("HIP_MANAGED_FORCE_DEVICE_ALLOC", "1")

    def setup_build_environment(self, env):
        spec = self.spec
        env.append_flags("CXXFLAGS", "-DUSE_STK_SIMD_NONE")
        if spec.satisfies("+cuda"):
            env.set("OMPI_CXX", self.spec["kokkos-nvcc-wrapper"].kokkos_cxx)
            env.set("MPICH_CXX", self.spec["kokkos-nvcc-wrapper"].kokkos_cxx)
            env.set("MPICXX_CXX", self.spec["kokkos-nvcc-wrapper"].kokkos_cxx)
        if spec.satisfies("+rocm"):
            env.append_flags("CXXFLAGS", "-fgpu-rdc")

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx),
            self.define("Trilinos_DIR", spec["trilinos"].prefix),
            self.define("YAML_DIR", spec["yaml-cpp"].prefix),
            self.define("CMAKE_CXX_STANDARD", "17"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            self.define_from_variant("ENABLE_CUDA", "cuda"),
            self.define_from_variant("ENABLE_WIND_UTILS", "wind-utils"),
            self.define_from_variant("ENABLE_BOOST", "boost"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("ENABLE_OPENFAST", "openfast"),
            self.define_from_variant("ENABLE_TIOGA", "tioga"),
            self.define_from_variant("ENABLE_HYPRE", "hypre"),
            self.define_from_variant("ENABLE_TRILINOS_SOLVERS", "trilinos-solvers"),
            self.define_from_variant("ENABLE_PARAVIEW_CATALYST", "catalyst"),
            self.define_from_variant("ENABLE_FFTW", "fftw"),
            self.define_from_variant("ENABLE_UMPIRE", "umpire"),
            self.define_from_variant("ENABLE_TESTS", "tests"),
        ]

        if spec.satisfies("+openfast"):
            args.append(self.define("OpenFAST_DIR", spec["openfast"].prefix))
            args.append(self.define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc))

        if spec.satisfies("+tioga"):
            args.append(self.define("TIOGA_DIR", spec["tioga"].prefix))

        if spec.satisfies("+hypre"):
            args.append(self.define("HYPRE_DIR", spec["hypre"].prefix))

        if spec.satisfies("+catalyst"):
            args.append(
                self.define(
                    "PARAVIEW_CATALYST_INSTALL_PATH", spec["trilinos-catalyst-ioss-adapter"].prefix
                )
            )

        if spec.satisfies("+fftw"):
            args.append(self.define("FFTW_DIR", spec["fftw"].prefix))

        args.append(self.define("ENABLE_TESTS", self.run_tests))
        if self.run_tests:
            args.extend(
                [
                    self.define("TEST_TOLERANCE", spec.variants["abs_tol"].value),
                    self.define("TEST_REL_TOL", spec.variants["rel_tol"].value),
                ]
            )

        if spec.satisfies("+umpire"):
            args.append(self.define("UMPIRE_DIR", spec["umpire"].prefix))

        if spec.satisfies("+rocm"):
            args.append(self.define("CMAKE_CXX_COMPILER", spec["hip"].hipcc))
            args.append(self.define("ENABLE_ROCM", True))
            targets = spec.variants["amdgpu_target"].value
            args.append(self.define("GPU_TARGETS", ";".join(str(x) for x in targets)))

        if "darwin" in spec.architecture:
            args.append(self.define("CMAKE_MACOSX_RPATH", "ON"))

        return args

    @run_before("cmake")
    def add_submodules(self):
        if self.run_tests or self.spec.satisfies("+wind-utils"):
            git = which("git")
            git("submodule", "update", "--init", "--recursive")
