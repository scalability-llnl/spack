# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack.package import *


class VtkM(CMakePackage, CudaPackage, ROCmPackage):
    """VTK-m is a toolkit of scientific visualization algorithms for emerging
    processor architectures. VTK-m supports the fine-grained concurrency for
    data analysis and visualization algorithms required to drive extreme scale
    computing by providing abstract models for data and execution that can be
    applied to a variety of algorithms across many different processor
    architectures."""

    homepage = "https://m.vtk.org/"
    maintainers("kmorel", "vicentebolea")

    url = "https://github.com/Kitware/VTK-m/archive/refs/tags/v2.2.0.tar.gz"
    git = "https://github.com/Kitware/VTK-m.git"
    tags = ["e4s"]

    test_requires_compiler = True

    version("master", branch="master")
    version("release", branch="release")
    version(
        "2.2.0",
        sha256="f40d6b39ca1bcecd232571c92ce606627811909f4e21972d1823e605f686bcf5",
        preferred=True,
    )
    version("2.1.0", sha256="7b224f1f91e5ef140e193338bf091133b1e9f40d323bccdc8bb80bfc2675e6ea")
    version("2.0.0", sha256="21c8b2cb8f3d4116a4f90c1d08c9f5e27b25c7a0951f7b403eced94576f84880")
    version("1.9.0", sha256="f9862d9d24deae32063ba1ea3d9a42900ac0cdd7f98412d960249a7cac35d47f")
    version("1.8.0", sha256="17f875e62b4c412574109af9b1bdbedbef49ab8797b113b69b21e6cfc64077d4")
    version("1.7.1", sha256="c623895edde050f79d2d48e1abbaf4d537eaf544bc12bae0d4350614eb888011")
    version("1.7.0", sha256="c334ce01aa1e6a506c9395789d41dc80c62234c3108506021b0cb104ba2eba7a")
    version("1.6.0", sha256="6ab2124e51a2fbfcf2a90587d7b242e39afe08e75ea497a953c865741be3cc79")
    version("1.5.5", commit="d2d1c854adc8c0518802f153b48afd17646b6252")
    version("1.5.4", commit="bbba2a1967b271cc393abd043716d957bca97972")
    version("1.5.3", commit="a3b8525ef97d94996ae843db0dd4f675c38e8b1e")
    version("1.5.2", commit="c49390f2537c5ba8cf25bd39aa5c212d6eafcf61")
    version("1.5.1", sha256="c6652fc03c9648b06f856231c270fc832e527d633d4bf6a9600b2175172f0a27")
    version("1.5.0", sha256="d4ffc6f1176c1fda41852a3e8b83650b6765205b829b70f014f4100dd51161b8")
    version("1.4.0", sha256="c70a9a19058dd32f15b1845b4bb40c0d3ad2b3916267c434e62cd3f6f256c1e6")
    version("1.3.0", sha256="2d05a6545abfaa7594ef344389617fdca48c7f5ebddc617038544317b70ba19e")
    version("1.2.0", sha256="44596e88b844e7626248fb8e96a38be25a0e585a22256b1c859208b23ef45171")
    version("1.1.0", sha256="55f42c417d3a41893230b2fd3b5c192daeee689a2193de10bf22a1ef5c24c7ad")

    depends_on("cxx", type="build")  # generated

    variant("shared", default=False, description="build shared libs")

    variant("doubleprecision", default=True, description="enable double precision")
    variant("logging", default=False, when="@1.3:", description="build logging support")
    variant(
        "virtuals",
        default=False,
        description="enable support for deprecated virtual functions",
        when="@:1.9",
    )
    variant("mpi", default=False, when="@1.3:", description="build mpi support")
    variant("rendering", default=True, description="build rendering support")
    variant("64bitids", default=False, description="enable 64 bits ids")
    variant("testlib", default=False, when="@1.7:", description="build test library")
    variant("fpic", default=False, description="build fpic support")
    variant("examples", default=True, when="@1.8:", description="Install builtin examples")

    # Device variants
    # CudaPackage provides cuda variant
    # ROCmPackage provides rocm variant
    variant("kokkos", default=False, when="@1.6:", description="build using Kokkos backend")
    variant(
        "cuda_native", default=True, description="build using native cuda backend", when="+cuda"
    )
    variant(
        "openmp",
        default=(sys.platform != "darwin"),
        when="@1.3:",
        description="build openmp support",
    )
    variant("tbb", default=(sys.platform == "darwin"), description="build TBB support")

    depends_on("cmake@3.12:", type="build")  # CMake >= 3.12
    depends_on("cmake@3.18:", when="+rocm", type="build")  # CMake >= 3.18

    conflicts("%gcc@:4.10", msg="vtk-m requires gcc >= 5. Please install a newer version")
    conflicts("%gcc@11:", when="@:1.5.2", msg="DIY has a issue building with gcc 11")

    depends_on("cuda@10.1.0:", when="+cuda_native")
    depends_on("tbb", when="+tbb")
    depends_on("mpi", when="+mpi")
    depends_on("llvm-openmp", when="+openmp %apple-clang")

    # VTK-m uses the default Kokkos backend
    depends_on("kokkos", when="+kokkos")
    depends_on("kokkos@3.7:3.9", when="@2.0 +kokkos")
    # VTK-m native CUDA and Kokkos CUDA backends are not compatible
    depends_on("kokkos ~cuda", when="+kokkos +cuda +cuda_native")
    depends_on("kokkos +cuda", when="+kokkos +cuda ~cuda_native")
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on(
            "kokkos cuda_arch=%s" % cuda_arch,
            when="+kokkos +cuda ~cuda_native cuda_arch=%s" % cuda_arch,
        )
    # VTK-m uses the Kokkos HIP backend.
    # If Kokkos provides multiple backends, the HIP backend may or
    # may not be used for VTK-m depending on the default selected by Kokkos
    depends_on("kokkos +rocm", when="+kokkos +rocm")
    # Propagate AMD GPU target to kokkos for +rocm
    for amdgpu_value in ROCmPackage.amdgpu_targets:
        depends_on(
            "kokkos amdgpu_target=%s" % amdgpu_value,
            when="+kokkos +rocm amdgpu_target=%s" % amdgpu_value,
        )

    depends_on("hip@3.7:", when="+rocm")
    # CUDA thrust is already include in the CUDA pkg
    depends_on("rocthrust", when="@2.2: +kokkos+rocm ^cmake@3.24:")

    # The rocm variant is only valid options for >= 1.7. It would be better if
    # this could be expressed as a when clause to disable the rocm variant,
    # but that is not currently possible since when clauses are stacked,
    # not overwritten.
    conflicts("+rocm", when="@:1.6")
    conflicts("+rocm", when="+cuda")
    conflicts("+rocm", when="~kokkos", msg="VTK-m does not support HIP without Kokkos")
    conflicts("+rocm", when="+virtuals", msg="VTK-m does not support virtual functions with ROCm")

    # Can build +shared+cuda after @1.7:
    conflicts("+shared", when="@:1.6 +cuda_native")
    conflicts("+cuda~cuda_native~kokkos", msg="Cannot have +cuda without a cuda device")
    conflicts("+cuda~cuda_native", when="@:1.5", msg="Cannot have +cuda without a cuda device")

    conflicts("+cuda", when="cuda_arch=none", msg="vtk-m +cuda requires that cuda_arch be set")

    # Patch
    patch("diy-include-cstddef.patch", when="@1.5.3:1.8.0")

    # VTK-M PR#3215
    # https://gitlab.kitware.com/vtk/vtk-m/-/merge_requests/3215
    patch("vtkm-mr3215-ext-geom-fix.patch", when="@2.1")

    # VTK-M PR#2972
    # https://gitlab.kitware.com/vtk/vtk-m/-/merge_requests/2972
    patch("vtkm-cuda-swap-conflict-pr2972.patch", when="@1.9 +cuda ^cuda@12:")

    # VTK-M PR#3160
    # https://gitlab.kitware.com/vtk/vtk-m/-/merge_requests/3160
    patch("mr3160-rocthrust-fix.patch", when="@2.1")

    # VTK-M PR#3258
    # https://gitlab.kitware.com/vtk/vtk-m/-/merge_requests/3258
    patch("mr3258-fix-typo-thrust-dependency-with-rocm.patch", when="@2.2:")

    # VTK-M PR#3259
    # https://gitlab.kitware.com/vtk/vtk-m/-/merge_requests/3259
    patch("mr3259-thrust-is_arithmetic-fix.patch", when="@2.0.0:2.2.0 +cuda ^cuda@12.6:")

    # Disable Thrust patch that is no longer needed in modern Thrust
    patch(
        "https://github.com/Kitware/VTK-m/commit/4a4466e7c8cd44d2be2bd3fe6f359faa8e9547aa.patch?full_index=1",
        sha256="58dc104ba05ec99c359eeec3ac094cdb071053a4250f4ad9d72ef6a356c4346e",
        when="@1.6.0:2.1 +cuda ^cuda@12.5:",
    )

    def cmake_args(self):
        spec = self.spec
        options = []
        gpu_name_table = {
            "30": "kepler",
            "32": "kepler",
            "35": "kepler",
            "50": "maxwell",
            "52": "maxwell",
            "53": "maxwell",
            "60": "pascal",
            "61": "pascal",
            "62": "pascal",
            "70": "volta",
            "72": "turing",
            "75": "turing",
            "80": "ampere",
            "86": "ampere",
        }
        with working_dir("spack-build", create=True):
            is_release = spec.variants["build_type"].value == "Release"
            options = [
                self.define("VTKm_ENABLE_TESTING", False),
                self.define("VTKm_NO_ASSERT", is_release),
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define_from_variant("VTKm_ENABLE_KOKKOS", "kokkos"),
                self.define_from_variant("VTKm_ENABLE_LOGGING", "logging"),
                self.define_from_variant("VTKm_ENABLE_MPI", "mpi"),
                self.define_from_variant("VTKm_ENABLE_OPENMP", "openmp"),
                self.define_from_variant("VTKm_ENABLE_RENDERING", "rendering"),
                self.define_from_variant("VTKm_ENABLE_TBB", "tbb"),
                self.define_from_variant("VTKm_ENABLE_TESTING_LIBRARY", "testlib"),
                self.define_from_variant("VTKm_INSTALL_EXAMPLES", "examples"),
                self.define_from_variant("VTKm_NO_DEPRECATED_VIRTUAL", "virtuals"),
                self.define_from_variant("VTKm_USE_64BIT_IDS", "64bitids"),
                self.define_from_variant("VTKm_USE_DOUBLE_PRECISION", "doubleprecision"),
                self.define(
                    "VTKm_USE_DEFAULT_TYPES_FOR_ASCENT", "~64bitids +doubleprecision" in spec
                ),
            ]

            if "+tbb" in spec:
                # vtk-m detectes tbb via TBB_ROOT env var
                os.environ["TBB_ROOT"] = spec["tbb"].prefix

            if "+kokkos" in spec and "+rocm" in spec and spec.satisfies("^kokkos@4:"):
                options.append(f"-DCMAKE_CXX_COMPILER:BOOL={spec['hip'].prefix.bin.hipcc}")

            # Support for relocatable code
            if "~shared" in spec and "+fpic" in spec:
                options.append("-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON")

            # cuda support
            if "+cuda_native" in spec:
                options.append("-DVTKm_ENABLE_CUDA:BOOL=ON")
                options.append("-DCMAKE_CUDA_HOST_COMPILER={0}".format(env["SPACK_CXX"]))

                if spec.satisfies("@1.9.0:") and spec.satisfies("^cmake@3.18:"):
                    options.append(self.builder.define_cuda_architectures(self))

                else:
                    # VTKm_CUDA_Architecture only accepts a single CUDA arch
                    num_cuda_arch = spec.variants["cuda_arch"].value[0]
                    str_cuda_arch = str()

                    try:
                        str_cuda_arch = gpu_name_table[num_cuda_arch]
                    except KeyError:
                        raise InstallError(
                            f"cuda_arch={num_cuda_arch} needs cmake>=3.18 & VTK-m>=1.9.0"
                        )
                    options.append(f"-DVTKm_CUDA_Architecture={str_cuda_arch}")

            else:
                options.append("-DVTKm_ENABLE_CUDA:BOOL=OFF")

            # hip support
            if "+rocm" in spec:
                options.append(self.builder.define_hip_architectures(self))

        return options

    def test_smoke_test(self):
        """Build and run ctests"""
        spec = self.spec

        if "+examples" not in spec:
            raise SkipTest("Package must be installed with +examples")

        testdir = "smoke_test_build"
        with working_dir(testdir, create=True):
            cmake = Executable(spec["cmake"].prefix.bin.cmake)
            ctest = Executable(spec["cmake"].prefix.bin.ctest)
            cmakeExampleDir = spec["vtk-m"].prefix.share.doc.VTKm.examples.smoke_test

            cmake(*([cmakeExampleDir, "-DVTKm_ROOT=" + spec["vtk-m"].prefix]))
            cmake(*(["--build", "."]))
            ctest(*(["--verbose"]))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        self.test_smoke_test()
