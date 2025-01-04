# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.build_systems.cmake
import spack.build_systems.makefile
from spack.package import *


class Babelstream(CMakePackage, CudaPackage, ROCmPackage, MakefilePackage):
    """Measure memory transfer rates to/from global device memory on GPUs.
    This benchmark is similar in spirit, and based on, the STREAM benchmark for CPUs."""

    homepage = "https://github.com/UoB-HPC/BabelStream"
    url = "https://github.com/UoB-HPC/BabelStream/archive/refs/tags/v5.0.tar.gz"
    git = "https://github.com/UoB-HPC/BabelStream.git"
    version("5.0", sha256="1a418203fbfd95595bdc66047e2e39d8f1bba95a49725c9ecb907caf1af2521f")
    version("4.0", sha256="a9cd39277fb15d977d468435eb9b894f79f468233f0131509aa540ffda4f5953")
    version("3.4", sha256="e34ee9d5ccdead019e3ea478333bcb7886117d600e5da8579a626f6ee34209cf")
    version("3.3", sha256="4c89c805b277d52776feeb7a8eef7985a0d9295ce3e0bb2333bf715f724723cf")
    version("3.2", sha256="20309b27ddd09ea37406bcc6f46fd32e9372bf3d145757e55938d19d69cdc49d")
    version("3.1", sha256="be69e6085e8966e12aa2df897eea6254b172e5adfa03de0adbb89bc3065f4fbe")
    version("3.0", sha256="776219c72e0fdc36f134e6975b68c7ab25f38206f8f8af84a6f9630648c24800")
    version("1.0", sha256="3cfb9e45601f1f249878355c72baa6e6a61f6c811f8716d60b83c7fb544e1d5c")
    version("main", branch="main")
    maintainers("tomdeakin", "kaanolgu", "tom91136")
    # Previous maintainers: "robj0nes"
    depends_on("cxx", type="build", when="languages=cxx")
    depends_on("fortran", type="build", when="languages=fortran")
    # Languages
    # in the future it could be possible to add other languages too
    variant(
        "languages",
        default="cxx",
        values=("cxx", "fortran"),
        description="Languages Babelstream Spack Package Support",
    )
    # Build System
    build_system(
        conditional("cmake", when="languages=cxx"),
        conditional("makefile", when="languages=fortran"),
        default="cmake",
    )
    with when("languages=cxx"):
        # Also supported variants are cuda and rocm (for HIP)
        # not included here because they are supplied via respective packages
        variant("sycl", default=False, description="Enable SYCL support")
        variant("sycl2020", default=False, description="Enable SYCL support")
        variant("omp", default=False, description="Enable OpenMP support")
        variant("ocl", default=False, description="Enable OpenCL support")
        variant("tbb", default=False, description="Enable TBB support")
        variant("acc", default=False, description="Enable OpenACC support")
        variant("hip", default=False, description="Enable HIP support")
        variant("thrust", default=False, description="Enable THRUST support")
        variant("raja", default=False, description="Enable RAJA support")
        variant("std", default=False, description="Enable STD support")

    # Some models need to have the programming model abstraction downloaded -
    # this variant enables a path to be provided.
    variant("dir", values=str, default="none", description="Enable Directory support")
    variant(
        "sycl2020_submodel",
        values=("usm", "acc"),
        when="+sycl2020",
        default="usm",
        description="SYCL2020 -> choose between usm and acc methods",
    )
    variant(
        "std_submodel",
        values=("data", "indices", "ranges"),
        when="+std",
        default="data",
        description="STD -> choose between data, indices and ranges models",
    )

    variant(
        "sycl2020_offload",
        values=("nvidia", "intel"),
        default="intel",
        when="+sycl2020",
        description="Offloading to NVIDIA GPU or not",
    )

    variant(
        "thrust_submodel",
        values=("cuda", "rocm"),
        default="cuda",
        when="+thrust",
        description="Which THRUST implementation to use",
    )
    variant(
        "thrust_backend",
        values=("cuda", "omp", "tbb"),
        default="cuda",
        when="+thrust",
        description="Which THRUST implementation to use",
    )

    # Kokkos variant
    variant("kokkos", default=False, description="Enable KOKKOS support")

    # STD conflicts
    conflicts("+std", when="%gcc@:10.1.0", msg="STD requires newer version of GCC")

    # CUDA conflict
    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="CUDA requires architecture to be specfied by cuda_arch=",
    )
    variant(
        "cuda_memory_mode",
        values=("default", "managed", "pagefault"),
        default="default",
        when="+cuda",
        description="Enable MEM Target for CUDA",
    )

    # OMP offload
    variant("omp_offload", default=False, when="+omp", description="Enable OpenMP Target")
    variant(
        "omp_flags",
        values=str,
        default="none",
        when="+omp",
        description="If OFFLOAD is enabled, this *overrides* the default offload flags",
    )
    conflicts(
        "omp_flags=none",
        when="+omp_offload",
        msg="OpenMP requires offload flags to be specfied by omp_flags=",
    )
    # Raja offload
    variant(
        "raja_offload",
        values=("cpu", "nvidia"),
        default="cpu",
        when="+raja",
        description="Enable RAJA Target [CPU or NVIDIA] / Offload with custom settings for OpenMP",
    )
    # std-* offload
    variant(
        "std_offload",
        values=("nvhpc", "none"),
        default="none",
        when="+std",
        description="Enable offloading support (via the non-standard `-stdpar`) "
        "for the new NVHPC SDK",
    )
    variant(
        "std_onedpl_backend",
        values=("openmp", "tbb", "dpcpp", "none"),
        default="none",
        when="+std",
        description="Implements policies using OpenMP,TBB or dpc++",
    )
    variant(
        "std_use_tbb",
        values=(True, False),
        default=False,
        when="+std",
        description="No-op if ONE_TBB_DIR is set. Link against an in-tree oneTBB "
        "via FetchContent_Declare, see top level CMakeLists.txt for details",
    )
    variant(
        "std_use_onedpl",
        values=(True, False),
        default=False,
        when="+std",
        description="Link oneDPL which implements C++17 executor policies "
        "(via execution_policy_tag) for different backends",
    )
    # hip memory mode
    variant(
        "hip_mem_mode",
        values=("default", "managed", "pagefault"),
        default="default",
        when="+hip",
        description="Enable MEM Target for HIP",
    )
    # tbb use vector
    variant(
        "tbb_use_vector",
        values=(True, False),
        default=False,
        when="+tbb",
        description="Whether to use std::vector<T> for storage or use aligned_alloc. "
        "C++ vectors are *zero* initialised where as aligned_alloc is "
        "uninitialised before first use.",
    )

    # Thrust Conflict
    depends_on("thrust", when="+thrust")
    depends_on("cuda", when="thrust_submodel=cuda")
    depends_on("cuda", when="+raja raja_offload=nvidia")
    depends_on("hip", when="+hip")
    depends_on("rocthrust", when="thrust_submodel=rocm")
    depends_on("intel-tbb", when="+std +std_use_tbb")
    depends_on("intel-oneapi-dpl", when="+std +std_use_onedpl")
    depends_on("intel-tbb", when="+std +std_use_onedpl")
    # TBB Dependency
    depends_on("intel-tbb", when="+tbb")

    variant(
        "tbb_partitioner",
        values=("auto", "affinity", "static", "simple"),
        default="auto",
        when="+tbb",
        description="Specifies how a loop template should partition its work among threads",
    )

    # Kokkos & RAJA Dependency
    cuda_archs = CudaPackage.cuda_arch_values
    for sm_ in cuda_archs:
        depends_on(
            "kokkos +cuda +wrapper cuda_arch={0}".format(sm_),
            when="kokkos_backend=cuda cuda_arch={0}".format(sm_),
        )
        depends_on(
            "raja +cuda cuda_arch={0}".format(sm_),
            when="raja_offload=nvidia cuda_arch={0}".format(sm_),
        )
    depends_on("kokkos +openmp", when="kokkos_backend=omp")
    depends_on("raja +openmp", when="raja_offload=cpu")

    # OpenCL Dependency
    variant(
        "ocl_backend",
        values=("amd", "cuda", "intel", "pocl", "none"),
        default="none",
        when="+ocl",
        description="Enable Backend Target for OpenCL",
    )
    variant(
        "kokkos_backend",
        values=("cuda", "omp", "none"),
        default="none",
        when="+kokkos",
        description="Enable Backend Target for kokkos",
    )
    conflicts(
        "ocl_backend=none",
        when="+ocl",
        msg="OpenCL implementation requires backend to be specfied by ocl_backend=",
    )
    # depends_on("rocm-opencl@6.0.2", when="+ocl ocl_backend=amd")
    depends_on("cuda", when="+ocl ocl_backend=cuda")
    depends_on("cuda", when="+sycl2020 sycl2020_offload=nvidia")
    depends_on("intel-oneapi-compilers", when="+ocl ocl_backend=intel")
    depends_on("pocl@1.5", when="+ocl ocl_backend=pocl")

    variant(
        "cuda_extra_flags",
        values=str,
        default="none",
        description="Additional CUDA Compiler flags to be provided",
    )

    # CMake specific dependency
    with when("build_system=cmake"):
        depends_on("cmake@3.14.0:", type="build")

    # This applies to all
    depends_on("opencl-c-headers", when="+ocl")

    # Fortran related configurations
    with when("languages=fortran"):
        implementation_vals = [
            "DoConcurrent",
            "Array",
            "OpenMP",
            "OpenMPWorkshare",
            "OpenMPTarget",
            "OpenMPTargetLoop",
            "OpenMPTaskloop",
            "OpenACC",
            "OpenACCArray",
            "CUDA",
            "CUDAKernel",
            "Sequential",
        ]
        variant(
            "foption",
            values=implementation_vals,
            default="Sequential",
            description="Implementation",
        )
        # The fortran Makefile is inside the src/fortran so we need to address this
        build_directory = "src/fortran"
        build_name = ""
        variant(
            "fortran_flags",
            values=str,
            default="none",
            description="Additional Fortran flags to be provided",
        )


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        model_list = [
            "sycl",
            "sycl2020",
            "omp",
            "cuda",
            "ocl",
            "tbb",
            "acc",
            "hip",
            "thrust",
            "raja",
            "std",
            "kokkos",
        ]
        # for +acc and +thrust the CudaPackage appends +cuda variant too so we need
        # to filter cuda from list e.g. we choose 'thrust'
        # from the list of ['cuda', 'thrust']
        model_names = [name for name in model_list if f"+{name}" in self.spec]
        print("model names : ", model_names)
        if len(model_names) > 1:
            model_names = [elem for elem in model_names if (elem != "cuda" and elem != "rocm")]
            if "std" in model_names[0]:
                args = ["-DMODEL=" + "std-" + self.spec.variants["std_submodel"].value]
            elif "sycl2020" in model_names[0]:  # this is for nvidia offload
                args = ["-DMODEL=" + "sycl2020-" + self.spec.variants["sycl2020_submodel"].value]
            else:
                args = ["-DMODEL=" + model_names[0]]
        else:
            # do some alterations here to append sub models too
            if "std" in model_names[0]:
                args = ["-DMODEL=" + "std-" + self.spec.variants["std_submodel"].value]
            elif "sycl2020" in model_names[0]:
                args = ["-DMODEL=" + "sycl2020-" + self.spec.variants["sycl2020_submodel"].value]
                print(args)
            elif "rocm" in model_names[0]:
                args = ["-DMODEL=hip"]
            else:
                args = ["-DMODEL=" + model_names[0]]
        if model_names[0] != "tbb" and model_names[0] != "thrust":
            args.append("-DCMAKE_CXX_COMPILER=" + spack_cxx)

        # ===================================
        #             ACC
        # ===================================
        """
        register_flag_optional(TARGET_DEVICE
        "[PGI/NVHPC only] This sets the `-target` flag, possible values are:
             gpu       - Globally set the target device to an NVIDIA GPU
             multicore - Globally set the target device to the host CPU
         Refer to `nvc++ --help` for the full list"
         register_flag_optional(CUDA_ARCH
        "[PGI/NVHPC only] Only applicable if `TARGET_DEVICE` is set to `gpu`.
         Nvidia architecture in ccXY format, for example, sm_70 becomes cc70,
         will be passed in via `-gpu=` (e.g `cc70`)
         Possible values are:
             cc35  - Compile for compute capability 3.5
             cc50  - Compile for compute capability 5.0
             cc60  - Compile for compute capability 6.0
             cc62  - Compile for compute capability 6.2
             cc70  - Compile for compute capability 7.0
             cc72  - Compile for compute capability 7.2
             cc75  - Compile for compute capability 7.5
             cc80  - Compile for compute capability 8.0
             ccall - Compile for all supported compute capabilities
         Refer to `nvc++ --help` for the full list"
        "")

register_flag_optional(TARGET_PROCESSOR
        "[PGI/NVHPC only] This sets the `-tp` (target processor) flag, possible values are:
             px          - Generic x86 Processor
             bulldozer   - AMD Bulldozer processor
             piledriver  - AMD Piledriver processor
             zen         - AMD Zen architecture (Epyc, Ryzen)
             zen2        - AMD Zen 2 architecture (Ryzen 2)
             sandybridge - Intel SandyBridge processor
             haswell     - Intel Haswell processor
             knl         - Intel Knights Landing processor
             skylake     - Intel Skylake Xeon processor
             host        - Link native version of HPC SDK cpu math library
             native      - Alias for -tp host
        Refer to `nvc++ --help` for the full list"
        "")
        """
        if self.spec.satisfies("+acc~kokkos~raja %nvhpc"):
            target_device = "gpu" if "cuda_arch" in self.spec.variants else "multicore"
            if "cuda_arch" in self.spec.variants:
                cuda_arch_list = self.spec.variants["cuda_arch"].value
                # the architecture value is only number so append cc_ to the name
                cuda_arch = "cc" + cuda_arch_list[0]
                # args.append(
                #     "-DCXX_EXTRA_FLAGS=" + "-target=" + target_device + "-gpu=" + cuda_arch
                # )
                args.append("-DCUDA_ARCH=" + cuda_arch)
            else:
                # get the cpu architecture value from user
                target_processor = str(self.spec.target)  # self.spec.variants["cpu_arch"].value[0]
                args.append("-DTARGET_PROCESSOR=" + target_processor)
                # args.append(
                #     "-DCXX_EXTRA_FLAGS="
                #     + "-target="
                #     + target_device
                #     + "-tp="
                #     + target_processor
                # )
            args.append("-DTARGET_DEVICE=" + target_device)
        # ===================================
        #    STDdata,STDindices,STDranges
        # ===================================

        if "+std" in self.spec:
            if self.spec.satisfies("+std_use_tbb"):
                args.append("-DCXX_EXTRA_FLAGS=-ltbb")
            if self.spec.satisfies("+std_use_onedpl"):
                # args.append("-DCXX_EXTRA_FLAGS=-ltbb")
                # args.append("-DCXX_EXTRA_FLAGS=-loneDPL")
                args.append(
                    "-DUSE_ONEDPL=" + self.spec.variants["std_onedpl_backend"].value.upper()
                )
            if self.spec.variants["std_offload"].value != "none":
                # the architecture value is only number so append cc_ to the name
                cuda_arch = "cc" + self.spec.variants["cuda_arch"].value[0]
                args.append("-DNVHPC_OFFLOAD=" + cuda_arch)

        # ===================================
        #             CUDA
        # ===================================
        if self.spec.satisfies("+cuda~kokkos~acc~omp~thrust~raja"):
            # Set up the cuda macros needed by the build
            cuda_arch_list = self.spec.variants["cuda_arch"].value
            # "-DCUDA_ARCH" requires sm_
            # the architecture value is only number so append sm_ to the name
            cuda_arch = "sm_" + cuda_arch_list[0]
            args.append("-DCUDA_ARCH=" + cuda_arch)
            cuda_dir = self.spec["cuda"].prefix
            cuda_comp = cuda_dir + "/bin/nvcc"
            args.append("-DCMAKE_CUDA_COMPILER=" + cuda_comp)
            args.append("-DMEM=" + self.spec.variants["cuda_memory_mode"].value.upper())
            if self.spec.variants["cuda_extra_flags"].value != "none":
                args.append("-DCUDA_EXTRA_FLAGS=" + self.spec.variants["cuda_extra_flags"].value)

        # ===================================
        #             OMP
        # ===================================
        # `~kokkos` option is there to prevent +kokkos +omp setting to use omp directly from here
        # Same applies for raja
        if self.spec.satisfies("+omp~kokkos~raja"):
            args.append("-DCMAKE_C_COMPILER=" + spack_cc)
            if self.spec.satisfies("~omp_offload"):
                args.append("-DOFFLOAD=" + "OFF")
                # Check if the omp_flags variant is not set to "none"
                args.append(
                    "-DCMAKE_CXX_FLAGS="
                    + self.pkg.compiler.openmp_flag
                    + " "
                    + (
                        self.spec.variants["omp_flags"].value
                        if self.spec.variants["omp_flags"].value != "none"
                        else ""
                    )
                )
            else:
                offload_args = ""
                args.append("-DOFFLOAD=ON")
                if "cuda_arch" in self.spec.variants:
                    if self.spec.satisfies("%nvhpc"):
                        cuda_arch = "cc" + self.spec.variants["cuda_arch"].value[0]
                        offload_args = " -mp=gpu;" + "-gpu=" + cuda_arch + " "
                    if self.spec.satisfies("%clang"):
                        cuda_arch = "sm_" + self.spec.variants["cuda_arch"].value[0]
                        offload_args = "-fopenmp;--offload-arch=" + cuda_arch
                elif ("amdgpu_target" in self.spec.variants) and (
                    self.spec.variants["amdgpu_target"].value != "none"
                ):
                    offload_args = (
                        ";--offload-arch=" + self.spec.variants["amdgpu_target"].value[0]
                    )

                args.append(
                    "-DOFFLOAD_FLAGS="
                    + self.pkg.compiler.openmp_flag
                    + ";"
                    + offload_args
                    + ";"
                    + self.spec.variants["omp_flags"].value
                )

        # ===================================
        #            SYCL
        # ===================================

        if "+sycl" in self.spec:
            if self.spec.satisfies("%oneapi"):
                # -fsycl flag is required for setting up sycl/sycl.hpp seems like
                #  it doesn't get it from the CMake file
                args.append("-DSYCL_COMPILER=ONEAPI-ICPX")
                args.append("-DCXX_EXTRA_FLAGS= -fsycl")
            elif self.spec.satisfies("%clang"):
                # this requires the clang inside oneapi installation
                args.append("-DSYCL_COMPILER=ONEAPI-Clang")
                args.append("-DCXX_EXTRA_FLAGS= -fsycl")
            else:
                args.append("-DSYCL_COMPILER=HIPSYCL")
                args.append("-DSYCL_COMPILER_DIR=" + self.spec.variants["dir"].value)
                args.append("-DCXX_EXTRA_FLAGS= -fsycl")

        # ===================================
        #              SYCL 2020
        # ===================================

        if "+sycl2020" in self.spec:
            if self.spec.satisfies("%oneapi"):
                # -fsycl flag is required for setting up sycl/sycl.hpp seems like
                #  it doesn't get it from the CMake file
                args.append("-DSYCL_COMPILER=ONEAPI-ICPX")
                args.append("-DCXX_EXTRA_FLAGS= -fsycl")
            elif self.spec.satisfies("%clang"):
                # this requires the clang inside oneapi installation
                args.append("-DSYCL_COMPILER=ONEAPI-Clang")
                args.append("-DCXX_EXTRA_FLAGS= -fsycl")
            else:
                args.append("-DSYCL_COMPILER=HIPSYCL")
                args.append("-DSYCL_COMPILER_DIR=" + self.spec.variants["dir"].value)
                args.append("-DCXX_EXTRA_FLAGS= -fsycl")
                # if self.spec.variants["flags"].value != "none":
            if self.spec.variants["sycl2020_offload"].value == "nvidia":
                cuda_dir = self.spec["cuda"].prefix
                cuda_arch = "sm_" + self.spec.variants["cuda_arch"].value[0]
                args.append(
                    "-DCXX_EXTRA_FLAGS="
                    + "-fsycl;-fsycl-targets=nvptx64-nvidia-cuda;"
                    + self.spec.target.optimization_flags(
                        self.spec.compiler.name, str(self.spec.compiler.version)
                    )
                    + " --cuda-path="
                    + cuda_dir
                )

        # ===================================
        #             HIP(ROCM)
        # ===================================

        if "+hip" in self.spec:
            hip_comp = self.spec["hip"].prefix + "/bin/hipcc"
            offload_arch = str(self.spec.variants["amdgpu_target"].value[0])

            args.append("-DCMAKE_CXX_COMPILER=" + hip_comp)
            args.append(f"-DCXX_EXTRA_FLAGS=--offload-arch={offload_arch} -O3")
            if str(self.spec.variants["hip_mem_mode"].value) != "none":
                args.append("-DMEM=" + self.spec.variants["hip_mem_mode"].value.upper())

        # ===================================
        #             TBB
        # ===================================

        if "+tbb" in self.spec:
            args.append("-DONE_TBB_DIR=" + self.spec["intel-tbb"].prefix + "/tbb/latest/")
            args.append("-DCXX_EXTRA_FLAGS=-ltbb")
            args.append("-DPARTITIONER=" + self.spec.variants["tbb_partitioner"].value.upper())
            if self.spec.satisfies("+tbb_use_vector"):
                args.append("-DUSE_VECTOR=ON")

        # ===================================
        #             OpenCL (ocl)
        # ===================================

        if "+ocl" in self.spec:
            if "cuda" in self.spec.variants["ocl_backend"].value:
                cuda_dir = self.spec["cuda"].prefix
                args.append("-DOpenCL_LIBRARY=" + cuda_dir + "/lib64/libOpenCL.so")
            elif "amd" in self.spec.variants["ocl_backend"].value:
                rocm_dir = self.spec["rocm-opencl"].prefix
                args.append("-DOpenCL_LIBRARY=" + rocm_dir + "/lib64/libOpenCL.so")
            elif "intel" in self.spec.variants["ocl_backend"].value:
                intel_lib = (
                    self.spec["intel-oneapi-compilers"].prefix
                    + "/compiler/"
                    + str(self.spec["intel-oneapi-compilers"].version)
                    + "/linux/lib/libOpenCL.so"
                )
                args.append("-DOpenCL_LIBRARY=" + intel_lib)
            elif "pocl" in self.spec.variants["ocl_backend"].value:
                pocl_lib = self.spec["pocl"].prefix + "/lib64/libOpenCL.so"
                args.append("-DOpenCL_LIBRARY=" + pocl_lib)

        # ===================================
        #             RAJA
        # ===================================

        if "+raja" in self.spec:
            args.append("-DCMAKE_C_COMPILER=" + spack_cc)
            args.append("-DRAJA_IN_PACKAGE=" + self.spec["raja"].prefix)
            if "nvidia" in self.spec.variants["raja_offload"].value:
                cuda_comp = self.spec["cuda"].prefix + "/bin/nvcc"
                args.append("-DTARGET=NVIDIA")
                cuda_arch = "sm_" + self.spec.variants["cuda_arch"].value[0]
                args.append("-DCUDA_ARCH=" + cuda_arch)

                args.append("-DENABLE_CUDA=ON")
                args.append("-DCUDA_TOOLKIT_ROOT_DIR=" + self.spec["cuda"].prefix)
                if self.spec.variants["cuda_extra_flags"].value != "none":
                    args.append(
                        "-DCMAKE_CUDA_FLAGS=" + self.spec.variants["cuda_extra_flags"].value
                    )

        # ===================================
        #             THRUST
        # ===================================

        if "+thrust" in self.spec:
            if "cuda" in self.spec.variants["thrust_submodel"].value:
                args.append("-DTHRUST_IMPL=" + self.spec.variants["thrust_submodel"].value.upper())

                args.append("-SDK_DIR=" + self.spec["thrust"].prefix + "/include")
                # this model uses CMAKE_CUDA_ARCHITECTURES which only requires number of cuda_arch
                # no need to append sm_ or cc_
                args.append("-DCUDA_ARCH=" + self.spec.variants["cuda_arch"].value[0])
                cuda_dir = self.spec["cuda"].prefix
                cuda_comp = cuda_dir + "/bin/nvcc"
                args.append("-DCMAKE_CUDA_COMPILER=" + cuda_comp)
                # args.append("-DCMAKE_CUDA_COMPILER=" + spack_cxx)
                # args.append("-DCMAKE_CUDA_FLAGS=-ccbin " + spack_cc)
                args.append("-DBACKEND=" + self.spec.variants["thrust_backend"].value.upper())
                if self.spec.variants["cuda_extra_flags"].value != "none":
                    args.append(
                        "-DCUDA_EXTRA_FLAGS=" + self.spec.variants["cuda_extra_flags"].value
                    )
            if "rocm" in self.spec.variants["thrust_submodel"].value:
                args.append("-DCMAKE_CXX_COMPILER=" + self.spec["hip"].hipcc)
                args.append("-DTHRUST_IMPL=" + self.spec.variants["thrust_submodel"].value.upper())
                args.append("-SDK_DIR=" + self.spec["rocthrust"].prefix)

        # ===================================
        #             kokkos
        # ===================================
        # kokkos implementation is versatile and it could use cuda or omp architectures as backend

        # The usage should be spack install babelstream +kokkos backend=[cuda or omp or none]
        if "+kokkos" in self.spec:
            args.append("-DCMAKE_C_COMPILER=" + spack_cc)
            args.append("-DKOKKOS_IN_PACKAGE=" + self.spec["kokkos"].prefix)
            if "cuda" in self.spec.variants["kokkos_backend"].value:
                # args.append("-DCMAKE_CXX_COMPILER=" + self.spec["cuda"].nvcc)
                args.append("-DCMAKE_CXX_COMPILER=" + spack_cxx)
                args.append("-DKokkos_ENABLE_CUDA=ON")
                int_cuda_arch = int(self.spec.variants["cuda_arch"].value[0])
                # arhitecture kepler optimisations
                if int_cuda_arch in (30, 32, 35, 37):
                    args.append("-D" + "Kokkos_ARCH_KEPLER" + str(int_cuda_arch) + "=ON")
                # arhitecture maxwell optimisations
                if int_cuda_arch in (50, 52, 53):
                    args.append("-D" + "Kokkos_ARCH_MAXWELL" + str(int_cuda_arch) + "=ON")
                # arhitecture pascal optimisations
                if int_cuda_arch in (60, 61):
                    args.append("-D" + "Kokkos_ARCH_PASCAL" + str(int_cuda_arch) + "=ON")
                # architecture volta optimisations
                if int_cuda_arch in (70, 72):
                    args.append("-D" + "Kokkos_ARCH_VOLTA" + str(int_cuda_arch) + "=ON")
                if int_cuda_arch == 75:
                    args.append("-DKokkos_ARCH_TURING75=ON")
                if int_cuda_arch == 80:
                    args.append("-DKokkos_ARCH_AMPERE80=ON")
            if "omp" in self.spec.variants["kokkos_backend"].value:
                args.append("-DKokkos_ENABLE_OPENMP=ON")

        # not in ["kokkos", "raja", "acc", "hip"] then compiler forced true
        if set(model_list).intersection(["kokkos", "raja", "acc", "hip"]) is True:
            args.append("-DCMAKE_CXX_COMPILER_FORCED=True")

        return args


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    build_directory = "src/fortran"

    # Generate Compiler Specific includes
    def edit(self, pkg, spec, prefix):
        config = {
            "FC": pkg.compiler.fc,
            "FCFLAGS": "",
            "ARCH": spec.target.family,
            "DOCONCURRENT_FLAG": "",
            "ARRAY_FLAG": "",
            "OPENMP_FLAG": "",
            "OPENACC_FLAG": "",
            "CUDA_FLAG": "",
            "SEQUENTIAL_FLAG": "",
        }
        # Dictionary mapping compiler names to unsupported options
        unsupported_options = {
            "arm": ["CUDA", "CUDAKernel", "OpenACC", "OpenACCArray"],
            "aocc": ["CUDA", "CUDAKernel"],
            "cce": ["CUDA", "CUDAKernel"],
            "gcc": ["CUDA", "CUDAKernel"],
            "nvhpc": ["OpenMPTaskloop"],
            "oneapi": ["CUDA", "CUDAKernel", "OpenACC", "OpenACCArray"],
            "fj": ["CUDA", "CUDAKernel", "OpenACC"],
        }

        # Check if spec.compiler.name is in the unsupported_options dictionary
        unsupported_value = self.spec.variants["foption"].value
        compiler_name = spec.compiler.name
        unsupported = any(
            unsupported_value in options
            for options in unsupported_options.get(compiler_name, [])
            if options == unsupported_value
        )
        if unsupported:
            raise InstallError(
                f"{unsupported_value} is not supported by the {compiler_name} compiler"
            )
        # ===================================
        #               ARM
        # ===================================
        if spec.compiler.name == "arm":
            fortran_flags = (
                "-std=f2018 " + pkg.compiler.opt_flags[4] + " -Wall -Wno-unused-variable"
            )
            fortran_flags += self.spec.target.optimization_flags(
                self.spec.compiler.name, str(self.spec.compiler.version)
            )

            config["FCFLAGS"] = fortran_flags
            config["DOCONCURRENT_FLAG"] = pkg.compiler.openmp_flag  # libomp.so required
            config["ARRAY_FLAG"] = pkg.compiler.openmp_flag  # libomp.so required
            config["OPENMP_FLAG"] = pkg.compiler.openmp_flag  # libomp.so required
            config["OPENACC_FLAG"] = "-fopenacc"

        # ===================================
        #               AMD
        # ===================================
        if spec.compiler.name == "aocc":
            fortran_flags = (
                "-std=f2018 " + pkg.compiler.opt_flags[3] + " -Wall -Wno-unused-variable"
            )
            config["FCFLAGS"] = fortran_flags
            config["DOCONCURRENT_FLAG"] = pkg.compiler.openmp_flag  # libomp.so required
            config["ARRAY_FLAG"] = pkg.compiler.openmp_flag  # libomp.so required
            config["OPENMP_FLAG"] = pkg.compiler.openmp_flag  # libomp.so required
            config["OPENACC_FLAG"] = "-fopenacc"

        # ===================================
        #               CRAY
        # ===================================
        if spec.compiler.name == "cce":
            fortran_flags = "-e F -O3"
            config["FCFLAGS"] = fortran_flags
            config["DOCONCURRENT_FLAG"] = "-h thread_do_concurrent -DCRAY_THREAD_DOCONCURRENT"
            config["ARRAY_FLAG"] = "-h autothread"
            config["OPENMP_FLAG"] = pkg.compiler.openmp_flag
            config["OPENACC_FLAG"] = "-h acc"  # for cpu only -h omp

        # ===================================
        #               GCC
        # ===================================
        if spec.compiler.name == "gcc":
            fortran_flags = "-std=f2018 -O3 "
            fortran_flags += "-Wall -Wno-unused-dummy-argument -Wno-unused-variable "
            fortran_flags += self.spec.target.optimization_flags(
                self.spec.compiler.name, str(self.spec.compiler.version)
            )

            config["FCFLAGS"] = fortran_flags
            config["DOCONCURRENT_FLAG"] = "-ftree-parallelize-loops=4"
            config["OPENMP_FLAG"] = pkg.compiler.openmp_flag
            config["OPENACC_FLAG"] = "-fopenacc"

        # ===================================
        #               NVHPC
        # ===================================
        if spec.compiler.name == "nvhpc":
            fortran_flags = pkg.compiler.opt_flags[4]  # for -O3
            # FCFLAGS	:= -O3 -Minform=inform -Minfo=all
            fortran_flags += " -Minform=warn "
            TARGET = "gpu"  # target = "multicore"
            config["TARGET"] = TARGET
            if "cuda_arch" in self.spec.variants:
                cuda_arch_list = self.spec.variants["cuda_arch"].value
                # the architecture value is only number so append sm_ to the name
                cuda_arch = "cc" + cuda_arch_list[0]
            GPUFLAG = " -gpu=" + cuda_arch
            fortran_flags += "-tp=" + str(spec.target)
            # this is to allow apples-to-apples comparison with DC in non-DC GPU impls
            # set exactly one of these pairs!
            # MANAGED = "-DUSE_MANAGED -gpu=managed"
            # DEVICE=""
            # ------------
            DEVICE = "-DUSE_DEVICE -cuda -gpu=nomanaged"
            MANAGED = ""
            config["FCFLAGS"] = fortran_flags
            config["DOCONCURRENT_FLAG"] = GPUFLAG + " -stdpar=" + TARGET + " " + DEVICE
            config["ARRAY_FLAG"] = GPUFLAG + " -stdpar=" + TARGET + " " + MANAGED
            config["OPENMP_FLAG"] = GPUFLAG + " -mp=" + TARGET + " " + MANAGED
            config["OPENACC_FLAG"] = GPUFLAG + " -acc=" + TARGET + " " + MANAGED
            config["CUDA_FLAG"] = GPUFLAG + " -cuda -acc=gpu" + " " + MANAGED

        # ===================================
        #               ONEAPI
        # ===================================
        if spec.compiler.name == "oneapi":
            fortran_flags = "-std18 -Ofast -xHOST -qopt-zmm-usage=low"
            if config["FC"] == "ifort":
                fortran_flags += "-qopt-streaming-stores=always"

            config["DOCONCURRENT_FLAG"] = "-qopenmp" + (
                "-parallel" if config["FC"] == "ifort" else ""
            )
            config["ARRAY_FLAG"] = "-qopenmp" + ("-parallel" if config["FC"] == "ifort" else "")
            config["OPENMP_FLAG"] = "-qopenmp" + (
                "-fopenmp-targets=spir64 -DUSE_FLOAT=1" if config["FC"] == "ifx" else ""
            )
            config["FCFLAGS"] = fortran_flags

        # ===================================
        #               FJ
        # ===================================
        if spec.compiler.name == "fj":
            fortran_flags = "-X08 -Kfast -KA64FX -KSVE -KARMV8_3_A -Kzfill=100 "
            fortran_flags += "-Kprefetch_sequential=soft "
            fortran_flags += "-Kprefetch_line=8 -Kprefetch_line_L2=16 -Koptmsg=2 "
            # FJ Fortran system_clock is low resolution
            fortran_flags += "-Keval -DUSE_OMP_GET_WTIME=1 "

            config["FCFLAGS"] = fortran_flags
            config["DOCONCURRENT_FLAG"] = "-Kparallel,reduction -DNOTSHARED"
            config["ARRAY_FLAG"] = "-Kparallel,reduction"
            config["OPENMP_FLAG"] = pkg.compiler.openmp_flag

        with open(self.build_directory + "/make.inc." + spec.compiler.name, "w+") as inc:
            for key in config:
                inc.write("{0} = {1}\n".format(key, config[key]))

    def setup_build_environment(self, env):
        ######################################
        # Build and Installation Directories #
        ######################################

        # The environment variable ESMF_DIR must be set to the full pathname
        # of the top level ESMF directory before building the framework.
        env.set("COMPILER", self.spec.compiler.name)
        env.set("IMPLEMENTATION", self.spec.variants["foption"].value)
        # DEBUG
        # print(self.spec.variants["foption"].value)
        # print(self.spec.compiler.version)
        # print(platform.machine())
        # This creates a testing tree (if one doesn't already exist) and
        # copies the binaries from `src/fortran` to `SpackPackage/bin`.
        # This allows you to use the testing tree independently of the
        # source tree in the future.
        # print(pkg.compiler.cc_pic_flag)

    @property
    def build_name(self):
        compiler_prefix = self.spec.compiler.name
        implementation_prefix = self.spec.variants["foption"].value
        return "{}.{}.{}".format("BabelStream", compiler_prefix, implementation_prefix)

    def install(self, pkg, spec, prefix):
        mkdir(prefix.bin)
        install(self.build_directory + "/" + self.build_name, prefix.bin)
        # To check the make.inc file generated
        install_tree(self.build_directory, prefix.lib)
