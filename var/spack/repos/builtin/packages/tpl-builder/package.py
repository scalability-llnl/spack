# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TplBuilder(CMakePackage, CudaPackage, ROCmPackage):
    """A CMake wrapper for dependencies used by SAMRApps and AMP."""

    homepage = "https://github.com/AdvancedMultiPhysics/TPL-builder"
    git = "https://github.com/AdvancedMultiPhysics/TPL-builder.git"

    maintainers("bobby-philip", "gllongo", "rbberger")

    license("UNKNOWN")

    version("master", branch="master")
    version("2.1.0", tag="2.1.0", commit="f2018b32623ea4a2f61fd0e7f7087ecb9b955eb5")

    variant("stacktrace", default=False, description="Build with support for Stacktrace")
    variant("lapack", default=False, description="Build with support for lapack")
    variant("hypre", default=False, description="Build with support for hypre")
    variant("kokkos", default=False, description="Build with support for Kokkos")
    variant("mpi", default=False, description="Build with MPI support")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant("shared", default=False, description="Build shared libraries")

    depends_on("git", type="build")

    depends_on("stacktrace", when="+stacktrace")
    depends_on("stacktrace+mpi", when="+stacktrace+mpi")

    depends_on("hypre", when="+hypre")
    depends_on("kokkos", when="+kokkos")

    depends_on("kokkos+cuda+cuda_constexpr", when="+kokkos+cuda")
    depends_on("kokkos+rocm", when="+kokkos+rocm")
    depends_on("hypre+cuda+unified-memory", when="+hypre+cuda")
    depends_on("hypre+rocm", when="+hypre+rocm")

    depends_on("hypre~shared", when="~shared+hypre")
    depends_on("hypre+shared", when="+shared+hypre")
    depends_on("blas", when="+lapack")
    depends_on("lapack", when="+lapack")

    requires("+lapack", when="+hypre")

    for _flag in list(CudaPackage.cuda_arch_values):
        depends_on(f"hypre cuda_arch={_flag}", when=f"+hypre+cuda cuda_arch={_flag}")
        depends_on(f"kokkos cuda_arch={_flag}", when=f"+kokkos+cuda cuda_arch={_flag}")

    for _flag in ROCmPackage.amdgpu_targets:
        depends_on(f"hypre amdgpu_target={_flag}", when=f"+hypre+rocm amdgpu_target={_flag}")
        depends_on(f"kokkos amdgpu_target={_flag}", when=f"+kokkos+rocm amdgpu_target={_flag}")

    # MPI related dependencies
    depends_on("mpi", when="+mpi")

    phases = ["cmake", "build"]

    def cmake_args(self):
        spec = self.spec

        options = [
            self.define("INSTALL_DIR", spec.prefix),
            self.define("DISABLE_ALL_TESTS", True),
            self.define("CXX_STD", "17"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("ENABLE_SHARED", "shared"),
            self.define("ENABLE_STATIC", not spec.variants["shared"].value),
            self.define_from_variant("USE_MPI", "mpi"),
            self.define("MPI_SKIP_SEARCH", False),
            self.define_from_variant("USE_OPENMP", "openmp"),
            self.define("DISABLE_GOLD", True),
        ]

        if spec.satisfies("+cuda"):
            cuda_arch = spec.variants["cuda_arch"].value
            cuda_flags = ["-extended-lambda", "--expt-relaxed-constexpr"]
            if cuda_arch[0] != "none":
                options.extend(
                    [
                        self.define("USE_CUDA", True),
                        self.define(
                            "CMAKE_CUDA_COMPILER", join_path(spec["cuda"].prefix.bin, "nvcc")
                        ),
                        self.define("CMAKE_CUDA_ARCHITECTURES", cuda_arch),
                        self.define("CMAKE_CUDA_FLAGS", " ".join(cuda_flags)),
                    ]
                )

        if spec.satisfies("+rocm"):
            amdgpu_target = spec.variants["amdgpu_target"].value
            if amdgpu_target[0] != "none":
                options.extend(
                    [
                        self.define("USE_HIP", True),
                        self.define(
                            "CMAKE_HIP_COMPILER",
                            join_path(spec["llvm-amdgpu"].prefix.bin, "amdclang++"),
                        ),
                        self.define("CMAKE_HIP_ARCHITECTURES", amdgpu_target),
                        self.define("CMAKE_HIP_FLAGS", ""),
                    ]
                )

        tpl_list = []

        if spec.satisfies("+lapack"):
            tpl_list.append("LAPACK")
            if spec.satisfies("^[virtuals=lapack] intel-mkl"):
                options.append(self.define("LAPACK_INSTALL_DIR", spec["lapack"].prefix.mkl))
            elif spec.satisfies("^[virtuals=lapack] intel-oneapi-mkl"):
                options.append(
                    self.define(
                        "LAPACK_INSTALL_DIR", spec["intel-oneapi-mkl"].package.component_prefix
                    )
                )
            else:
                options.append(self.define("LAPACK_INSTALL_DIR", spec["lapack"].prefix))

            blas, lapack = spec["blas"].libs, spec["lapack"].libs
            options.extend(
                [
                    self.define("BLAS_LIBRARY_NAMES", ";".join(blas.names)),
                    self.define("BLAS_LIBRARY_DIRS", ";".join(blas.directories)),
                    self.define("LAPACK_LIBRARY_NAMES", ";".join(lapack.names)),
                    self.define("LAPACK_LIBRARY_DIRS", ";".join(lapack.directories)),
                ]
            )

        for vname in ("stacktrace", "hypre", "kokkos"):
            if spec.satisfies(f"+{vname}"):
                tpl_list.append(vname.upper())
                options.append(self.define(f"{vname.upper()}_INSTALL_DIR", spec[vname].prefix))

        options.append(self.define("TPL_LIST", ";".join(tpl_list)))
        return options

    @run_after("build")
    def filter_compilers(self):
        kwargs = {"ignore_absent": True, "backup": False, "string": True}
        filenames = [join_path(self.prefix, "TPLsConfig.cmake")]

        filter_file(spack_cc, self.compiler.cc, *filenames, **kwargs)
        filter_file(spack_cxx, self.compiler.cxx, *filenames, **kwargs)
        filter_file(spack_fc, self.compiler.fc, *filenames, **kwargs)
