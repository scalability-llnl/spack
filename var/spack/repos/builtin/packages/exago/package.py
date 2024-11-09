# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Exago(CMakePackage, CudaPackage, ROCmPackage):
    """ExaGO is a package for solving large-scale power grid optimization
    problems on parallel and distributed architectures, particularly targeted
    for exascale machines."""

    homepage = "https://github.com/pnnl/ExaGO"
    git = "https://github.com/pnnl/ExaGO.git"
    maintainers("ryandanehy", "cameronrutherford", "pelesh")

    version(
        "1.6.0", tag="v1.6.0", commit="159cd173572280ac0f6f094a71dcc3ebeeb34076", submodules=True
    )
    version(
        "1.5.1", tag="v1.5.1", commit="84e9faf9d9dad8d851075eba26038338d90e6d3a", submodules=True
    )
    version(
        "1.5.0", tag="v1.5.0", commit="227f49573a28bdd234be5500b3733be78a958f15", submodules=True
    )
    version(
        "1.4.1", tag="v1.4.1", commit="ea607c685444b5f345bfdc9a59c345f0f30adde2", submodules=True
    )
    version(
        "1.4.0", tag="v1.4.0", commit="4f4c3fdb40b52ace2d6ba000e7f24b340ec8e886", submodules=True
    )
    version(
        "1.3.0", tag="v1.3.0", commit="58b039d746a6eac8e84b0afc01354cd58caec485", submodules=True
    )
    version(
        "1.2.0", tag="v1.2.0", commit="255a214ec747b7bdde7a6d8151c083067b4d0907", submodules=True
    )
    version(
        "1.1.2", tag="v1.1.2", commit="db3bb16e19c09e01402071623258dae4d13e5133", submodules=True
    )
    version(
        "1.1.1", tag="v1.1.1", commit="0e0a3f27604876749d47c06ec71daaca4b270df9", submodules=True
    )
    version(
        "1.1.0", tag="v1.1.0", commit="dc8dd85544ff1b55a64a3cbbbdf12b8a0c6fdaf6", submodules=True
    )
    version("1.0.0", tag="v1.0.0", commit="230d7df2f384f68b952a1ea03aad41431eaad283")
    version("0.99.2", tag="v0.99.2", commit="56961641f50827b3aa4c14524f2f978dc48b9ce5")
    version("0.99.1", tag="v0.99.1", commit="0ae426c76651ba5a9dbcaeb95f18d1b8ba961690")
    version("main", branch="main", submodules=True)
    version("develop", branch="develop", submodules=True)
    version(
        "snapshot.5-18-2022",
        tag="5-18-2022-snapshot",
        commit="3eb58335db71bb72341153a7867eb607402067ca",
        submodules=True,
    )
    version("kpp2", tag="kpp2", commit="1da764d80a2db793f4c43ca50e50981f7ed3880a", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Progrmming model options
    variant("mpi", default=True, description="Enable/Disable MPI")
    variant("raja", default=False, description="Enable/Disable RAJA")
    variant("python", default=True, when="@1.4:", description="Enable/Disable Python bindings")
    variant("logging", default=True, description="Enable/Disable spdlog based logging")

    conflicts(
        "+python", when="+ipopt+rocm", msg="Python bindings require -fPIC with Ipopt for rocm."
    )

    # Adds ExaGO's python wrapper to PYTHONPATH
    extends("python", when="+python")

    # Solver options
    variant("hiop", default=False, description="Enable/Disable HiOp")
    variant("ipopt", default=False, description="Enable/Disable IPOPT")

    conflicts(
        "~hiop~ipopt @:1.4",
        msg="ExaGO needs at least one solver enabled. PFLOW only mode is supported in 1.5+",
    )
    # You can use Python with PFLOW if desired ~ipopt~hiop
    conflicts(
        "~hiop~ipopt+python @:1.5.0",
        msg="ExaGO Python wrapper requires at least one solver enabled.",
    )
    conflicts(
        "+hiop~mpi ^hiop@1.0.0:~mpi",
        when="@1.5.1:1.6.1",
        msg="#18 - builds with hiop and without MPI cause compile time errors",
    )
    conflicts("+python~mpi", msg="#16 - Python wrapper requires MPI enabled")
    # Dependencies
    depends_on("python@3.6:3.10", when="@1.3.0:1.5+python")
    depends_on("py-pytest", type=("build", "run"), when="@1.5.0:+python")
    depends_on("py-mpi4py", when="@1.3.0:+mpi+python")
    depends_on("pkgconfig", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("blas")
    depends_on("ipopt~mumps", when="+ipopt")
    depends_on("cuda", when="+cuda")
    depends_on("raja", when="+raja")
    depends_on("umpire", when="+raja")
    depends_on("cmake@3.18:", type="build")

    # Profiling
    depends_on(
        "hiop+deepchecking build_type=RelWithDebInfo", when="+hiop build_type=RelWithDebInfo"
    )
    depends_on("hiop~deepchecking  build_type=Release ", when="+hiop build_type=Release ")

    # Control the package's build-type depending on the release or debug flag
    for pkg in [
        ("raja", "raja"),
        ("umpire", "raja"),
        ("magma", "hiop+cuda"),
        ("magma", "hiop+rocm"),
        ("camp", "raja"),
    ]:
        depends_on(
            "{0} build_type=Release".format(pkg[0]), when="+{0} build_type=Release".format(pkg[1])
        )
        depends_on(
            "{0} build_type=RelWithDebInfo".format(pkg[0]),
            when="+{0} build_type=RelWithDebInfo".format(pkg[1]),
        )

    with when("+hiop"):
        depends_on("hiop")
        with when("build_type=Release"):
            depends_on("hiop build_type=Release")
            depends_on("ginkgo build_type=Release", when="^hiop+ginkgo")
        with when("build_type=Debug"):
            depends_on("hiop build_type=RelWithDebInfo")
            depends_on("ginkgo build_type=Debug", when="^hiop+ginkgo")

    # depends_on("hpctoolkit", when="with_profiling=hpctoolkit")
    # depends_on("tau", when="with_profiling=tau")
    # ^ need to depend when both hpctoolkit and tau

    # HiOp dependency logic
    depends_on("hiop@0.3.99:", when="@0.99:+hiop")
    depends_on("hiop@0.5.1:", when="@1.1.0:+hiop")
    depends_on("hiop@0.5.3:", when="@1.3.0:+hiop")
    depends_on("hiop@0.7.0:1.0.0", when="@1.5.0:1.6.0+hiop")
    depends_on("hiop@1.0.1:", when="@develop:+hiop")

    depends_on("hiop~mpi", when="+hiop~mpi")
    depends_on("hiop+mpi", when="+hiop+mpi")

    # RAJA dependency logic
    # ExaGO will support +raja~hiop in the future
    depends_on("hiop+raja", when="+hiop+raja")
    # This is duplicated from HiOp
    # RAJA > 0.14 and Umpire > 6.0 require c++ std 14
    # We are working on supporting newer Umpire/RAJA versions
    depends_on("raja@0.14.0:0.14 +shared", when="@1.1.0:+raja")
    depends_on("umpire@6.0.0:6", when="@1.1.0:+raja")
    depends_on("camp@0.2.3:0.2", when="@1.1.0:+raja")
    # This is no longer a requirement in RAJA > 0.14
    depends_on("umpire+cuda~shared", when="+raja+cuda ^raja@:0.14")

    depends_on("petsc@3.13:3.14", when="@:1.2")
    depends_on("petsc@3.16", when="@1.3:1.4")
    depends_on("petsc@3.18:3.19", when="@1.5")
    depends_on("petsc@3.19:", when="@1.6:")

    depends_on("petsc~mpi", when="~mpi")

    for arch in CudaPackage.cuda_arch_values:
        cuda_dep = "+cuda cuda_arch={0}".format(arch)
        depends_on("hiop {0}".format(cuda_dep), when=cuda_dep)
        depends_on("raja {0}".format(cuda_dep), when="+raja {0}".format(cuda_dep))
        depends_on("umpire {0}".format(cuda_dep), when="+raja {0}".format(cuda_dep))
        depends_on("camp {0}".format(cuda_dep), when="+raja {0}".format(cuda_dep))

    for arch in ROCmPackage.amdgpu_targets:
        rocm_dep = "+rocm amdgpu_target={0}".format(arch)
        depends_on("hiop {0}".format(rocm_dep), when=rocm_dep)
        depends_on("raja {0}".format(rocm_dep), when="+raja {0}".format(rocm_dep))
        depends_on("umpire {0}".format(rocm_dep), when="+raja {0}".format(rocm_dep))
        depends_on("camp {0}".format(rocm_dep), when="+raja {0}".format(rocm_dep))

    # CMake patches to support ~python and ~testing
    patch("exago-1.6.0.patch", when="@1.6.0")
    patch("exago-1.5.0.patch", when="@1.5.0:1.5.1")
    patch("exago-1.3.0.patch", when="@1.3.0:1.4.1")
    patch("exago-1.1.0.patch", when="@1.1.0:1.2.0")

    flag_handler = build_system_flags

    def cmake_args(self):
        args = []
        spec = self.spec

        if self.spec.satisfies("~mpi"):
            args.append(self.define("CMAKE_C_COMPILER", os.environ["CC"]))
            args.append(self.define("CMAKE_CXX_COMPILER", os.environ["CXX"]))
        else:
            args.append(self.define("CMAKE_C_COMPILER", spec["mpi"].mpicc))
            args.append(self.define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx))
            args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))
            args.append(self.define("MPI_CXX_COMPILER", spec["mpi"].mpicxx))
            if spec.satisfies("+cuda"):
                args.append(self.define("MPI_CXX_HEADER_DIR", spec["mpi"].prefix.include))

        # NOTE: If building with spack develop on a cluster, you may want to
        # change the ctest launch command to use your job scheduler like so:
        #
        # args.append(
        #     self.define('EXAGO_CTEST_LAUNCH_COMMAND', 'srun -t 10:00'))

        args.extend(
            [
                self.define("EXAGO_ENABLE_GPU", "+cuda" in spec or "+rocm" in spec),
                self.define("PETSC_DIR", spec["petsc"].prefix),
                self.define("EXAGO_RUN_TESTS", self.run_tests),
                self.define("LAPACK_LIBRARIES", spec["lapack"].libs + spec["blas"].libs),
                self.define_from_variant("EXAGO_ENABLE_CUDA", "cuda"),
                self.define_from_variant("EXAGO_ENABLE_HIP", "rocm"),
                self.define_from_variant("EXAGO_ENABLE_LOGGING", "logging"),
                self.define_from_variant("EXAGO_ENABLE_MPI", "mpi"),
                self.define_from_variant("EXAGO_ENABLE_RAJA", "raja"),
                self.define_from_variant("EXAGO_ENABLE_HIOP", "hiop"),
                self.define_from_variant("EXAGO_ENABLE_IPOPT", "ipopt"),
                self.define_from_variant("EXAGO_ENABLE_PYTHON", "python"),
            ]
        )

        if spec.satisfies("+cuda"):
            cuda_arch_list = spec.variants["cuda_arch"].value
            if cuda_arch_list[0] != "none":
                args.append(self.define("CMAKE_CUDA_ARCHITECTURES", cuda_arch_list))

        # NOTE: if +rocm, some HIP CMake variables may not be set correctly.
        # Namely, HIP_CLANG_INCLUDE_PATH. If the configure phase fails due to
        # this variable being undefined, adding the following line typically
        # resolves this issue:
        #
        # args.append(
        #     self.define('HIP_CLANG_INCLUDE_PATH',
        #         '/opt/rocm-X.Y.Z/llvm/lib/clang/14.0.0/include/'))
        if spec.satisfies("+rocm"):
            args.append(self.define("CMAKE_CXX_COMPILER", spec["hip"].hipcc))

            rocm_arch_list = spec.variants["amdgpu_target"].value
            if rocm_arch_list[0] != "none":
                args.append(self.define("GPU_TARGETS", rocm_arch_list))
                args.append(self.define("AMDGPU_TARGETS", rocm_arch_list))

        return args
