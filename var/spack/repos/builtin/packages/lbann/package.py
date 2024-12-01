# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import socket

import spack.platforms.cray
from spack.package import *


class Lbann(CachedCMakePackage, CudaPackage, ROCmPackage):
    """LBANN: Livermore Big Artificial Neural Network Toolkit.  A distributed
    memory, HPC-optimized, model and data parallel training toolkit for deep
    neural networks.
    """

    homepage = "https://software.llnl.gov/lbann/"
    url = "https://github.com/LLNL/lbann/archive/v0.91.tar.gz"
    git = "https://github.com/LLNL/lbann.git"
    tags = ["ecp", "radiuss"]

    maintainers("bvanessen")

    license("Apache-2.0")

    version("develop", branch="develop")
    version("benchmarking", branch="benchmarking")
    version("0.104", sha256="a847c7789082ab623ed5922ab1248dd95f5f89d93eed44ac3d6a474703bbc0bf")
    version("0.103", sha256="9da1bf308f38323e30cb07f8ecf8efa05c7f50560e8683b9cd961102b1b3e25a")
    version(
        "0.102",
        sha256="3734a76794991207e2dd2221f05f0e63a86ddafa777515d93d99d48629140f1a",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )
    variant(
        "deterministic",
        default=False,
        description="Builds with support for deterministic execution",
    )
    variant(
        "distconv",
        default=False,
        sticky=True,
        description="Builds with support for spatial, filter, or channel "
        "distributed convolutions",
    )
    variant(
        "dtype",
        default="float",
        sticky=True,
        description="Type for floating point representation of weights",
        values=("float", "double"),
    )
    variant("fft", default=False, description="Support for FFT operations")
    variant("half", default=False, description="Builds with support for FP16 precision data types")
    variant("nvprof", default=False, description="Build with region annotations for NVPROF")
    variant(
        "numpy", default=False, description="Builds with support for processing NumPy data files"
    )
    variant(
        "vision",
        default=False,
        description="Builds with support for image processing data with OpenCV",
    )
    variant("vtune", default=False, description="Builds with support for Intel VTune")
    variant("onednn", default=False, description="Support for OneDNN")
    variant("onnx", default=False, description="Support for exporting models into ONNX format")
    variant(
        "nvshmem", default=False, sticky=True, description="Support for NVSHMEM", when="+distconv"
    )
    variant(
        "python",
        default=True,
        sticky=True,
        description="Support for Python extensions (e.g. Data Reader)",
    )
    variant(
        "pfe",
        default=True,
        sticky=True,
        description="Python Frontend for generating and launching models",
    )
    variant("boost", default=False, description="Enable callbacks that use Boost libraries")
    variant("asan", default=False, description="Build with support for address-sanitizer")
    variant("unit_tests", default=False, description="Support for unit testing")
    variant("caliper", default=False, description="Support for instrumentation with caliper")
    variant(
        "shared", default=True, sticky=True, description="Enables the build of shared libraries"
    )

    # LBANN benefits from high performance linkers, but passing these in as command
    # line options forces the linker flags to unnecessarily propagate to all
    # dependent packages. Don't include gold or lld as dependencies
    variant("gold", default=False, description="Use gold high performance linker")
    variant("lld", default=False, description="Use lld high performance linker")
    # Don't expose this a dependency until Spack can find the external properly
    # depends_on('binutils+gold', type='build', when='+gold')

    patch("lbann_v0.104_build_cleanup.patch", when="@0.104:")

    # Variant Conflicts
    conflicts("~cuda", when="+nvprof")
    conflicts("~cuda", when="+nvshmem")
    conflicts("+cuda", when="+rocm", msg="CUDA and ROCm support are mutually exclusive")

    requires("%clang", when="+lld")

    conflicts("+lld", when="+gold")
    conflicts("+gold", when="platform=darwin", msg="gold does not work on Darwin")
    conflicts("+lld", when="platform=darwin", msg="lld does not work on Darwin")

    depends_on("cmake@3.17.0:", type="build")
    depends_on("cmake@3.21.0:", type="build", when="@0.103:")

    # Specify the core libraries: Hydrogen, DiHydrogen, Aluminum
    depends_on("hydrogen@1.5.3:")
    depends_on("aluminum@1.4.1:")
    depends_on("dihydrogen@0.2.0:")

    # Align the following variants across Hydrogen and DiHydrogen
    forwarded_variants = ["cuda", "rocm", "half", "nvshmem"]
    for v in forwarded_variants:
        if v != "nvshmem":
            depends_on("hydrogen +{0}".format(v), when="+{0}".format(v))
            depends_on("hydrogen ~{0}".format(v), when="~{0}".format(v))
        if v != "al" and v != "half":
            depends_on("dihydrogen +{0}".format(v), when="+{0}".format(v))
            depends_on("dihydrogen ~{0}".format(v), when="~{0}".format(v))
        if v == "cuda" or v == "rocm":
            depends_on("aluminum +{0} +nccl".format(v), when="+{0}".format(v))

    # Add Hydrogen variants
    depends_on("hydrogen +openmp +shared +int64")
    depends_on("hydrogen build_type=Debug", when="build_type=Debug")

    # Add DiHydrogen variants
    depends_on("dihydrogen +distconv", when="+distconv")
    depends_on("dihydrogen@develop", when="@develop")

    # Add Aluminum variants
    depends_on("aluminum@master", when="@develop")

    # Note that while Aluminum typically includes the dependency for the AWS OFI
    # plugins, if Aluminum is pre-built, LBANN needs to make sure that the module
    # is loaded
    with when("+cuda"):
        if spack.platforms.cray.slingshot_network():
            depends_on("aws-ofi-nccl")  # Note: NOT a CudaPackage

    with when("+rocm"):
        if spack.platforms.cray.slingshot_network():
            depends_on("aws-ofi-rccl")

    depends_on("hdf5+mpi", when="+distconv")

    for arch in CudaPackage.cuda_arch_values:
        depends_on("hydrogen cuda_arch=%s" % arch, when="+cuda cuda_arch=%s" % arch)
        depends_on("aluminum cuda_arch=%s" % arch, when="+cuda cuda_arch=%s" % arch)
        depends_on("dihydrogen cuda_arch=%s" % arch, when="+cuda cuda_arch=%s" % arch)
        depends_on("nccl cuda_arch=%s" % arch, when="+cuda cuda_arch=%s" % arch)
        depends_on("hwloc cuda_arch=%s" % arch, when="+cuda cuda_arch=%s" % arch)

    # variants +rocm and amdgpu_targets are not automatically passed to
    # dependencies, so do it manually.
    for val in ROCmPackage.amdgpu_targets:
        depends_on("hydrogen amdgpu_target=%s" % val, when="+rocm amdgpu_target=%s" % val)
        depends_on("aluminum amdgpu_target=%s" % val, when="+rocm amdgpu_target=%s" % val)
        depends_on("dihydrogen amdgpu_target=%s" % val, when="+rocm amdgpu_target=%s" % val)
        depends_on(f"hwloc amdgpu_target={val}", when=f"+rocm amdgpu_target={val}")

    depends_on("roctracer-dev", when="+rocm +distconv")

    depends_on("cudnn@8.0.2:", when="+cuda")
    depends_on("cutensor", when="+cuda")
    depends_on("hipcub", when="+rocm")
    depends_on("mpi")
    depends_on("hwloc@1.11:")
    depends_on("hwloc +cuda +nvml ~rocm", when="+cuda")
    depends_on("hwloc@2.3.0: +rocm ~cuda", when="+rocm")
    depends_on("hiptt", when="+rocm")

    depends_on("half", when="+half")

    depends_on("fftw@3.3: +openmp", when="+fft")

    # LBANN wraps OpenCV calls in OpenMP parallel loops, build without OpenMP
    # Additionally disable video related options, they incorrectly link in a
    # bad OpenMP library when building with clang or Intel compilers
    depends_on(
        "opencv@4.1.0: build_type=RelWithDebInfo +highgui "
        "+imgcodecs +imgproc +jpeg +png +tiff +fast-math ~cuda",
        when="+vision",
    )

    # Note that for Power systems we want the environment to add +powerpc
    # When using a GCC compiler
    depends_on("opencv@4.1.0: +powerpc", when="+vision %gcc arch=ppc64le:")

    depends_on("cnpy", when="+numpy")
    depends_on("nccl", when="@0.94:0.98.2 +cuda")

    # Note that conduit defaults to +fortran +parmetis +python, none of which are
    # necessary by LBANN: you may want to disable those options in your
    # packages.yaml
    depends_on("conduit@0.6.0: +hdf5")

    # LBANN can use Python in two modes 1) as part of an extensible framework
    # and 2) to drive the front end model creation and launch

    # Core library support for Python Data Reader and extensible interface
    depends_on("python@3: +shared", type=("run"), when="@:0.90,0.99: +python")
    extends("python", when="+python")

    # Python front end and possible extra packages
    depends_on("python@3: +shared", type=("build", "run"), when="+pfe")
    extends("python", when="+pfe")
    depends_on("py-setuptools", type="build", when="+pfe")
    depends_on("py-protobuf@3.10.0:4.21.12", type=("build", "run"), when="+pfe")

    depends_on("protobuf@3.10.0:3.21.12")
    depends_on("zlib-api", when="^protobuf@3.11.0:")

    # using cereal@1.3.1 and above requires changing the
    # find_package call to lowercase, so stick with :1.3.0
    depends_on("cereal@:1.3.0")
    depends_on("catch2@2.9.0:2.99.999", when="+unit_tests", type=("build", "test"))
    depends_on("clara")

    depends_on("llvm-openmp", when="%apple-clang")

    depends_on("onednn cpu_runtime=omp gpu_runtime=none", when="+onednn")
    depends_on("onnx", when="+onnx")
    depends_on("nvshmem", when="+nvshmem")

    depends_on("spdlog@1.11.0:1.12.0")
    depends_on("zstr")

    depends_on("caliper+adiak+mpi", when="+caliper")

    generator("ninja")

    def setup_build_environment(self, env):
        env.append_flags("CXXFLAGS", "-fno-omit-frame-pointer")
        if self.spec.satisfies("%apple-clang"):
            env.append_flags("CPPFLAGS", self.compiler.openmp_flag)
            env.append_flags("CFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("CXXFLAGS", self.spec["llvm-openmp"].headers.include_flags)
            env.append_flags("LDFLAGS", self.spec["llvm-openmp"].libs.ld_flags)

    def _get_sys_type(self, spec):
        sys_type = spec.architecture
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        return sys_type

    @property
    def libs(self):
        shared = True if self.spec.satisfies("+shared") else False
        return find_libraries("liblbann", root=self.prefix, shared=shared, recursive=True)

    @property
    def cache_name(self):
        hostname = socket.gethostname()
        # Get a hostname that has no node identifier
        hostname = hostname.rstrip("1234567890-")
        return "LBANN_{0}_{1}-{2}-{3}@{4}.cmake".format(
            hostname,
            self.spec.version,
            self._get_sys_type(self.spec),
            self.spec.compiler.name,
            self.spec.compiler.version,
        )

    def initconfig_compiler_entries(self):
        spec = self.spec
        entries = super().initconfig_compiler_entries()
        entries.append(cmake_cache_string("CMAKE_CXX_STANDARD", "17"))
        entries.append(cmake_cache_option("BUILD_SHARED_LIBS", spec.satisfies("+shared")))
        if not spec.satisfies("^cmake@3.23.0"):
            # There is a bug with using Ninja generator in this version
            # of CMake
            entries.append(cmake_cache_option("CMAKE_EXPORT_COMPILE_COMMANDS", True))

        entries.append(cmake_cache_string("CMAKE_INSTALL_RPATH_USE_LINK_PATH", "ON"))
        linker_flags = "-Wl,--disable-new-dtags"
        entries.append(cmake_cache_string("CMAKE_EXE_LINKER_FLAGS", linker_flags))
        entries.append(cmake_cache_string("CMAKE_SHARED_LINKER_FLAGS", linker_flags))

        # Use lld high performance linker
        if spec.satisfies("+lld"):
            entries.append(
                cmake_cache_string(
                    "CMAKE_EXE_LINKER_FLAGS", "{0} -fuse-ld=lld".format(linker_flags)
                )
            )
            entries.append(
                cmake_cache_string(
                    "CMAKE_SHARED_LINKER_FLAGS", "{0} -fuse-ld=lld".format(linker_flags)
                )
            )

        # Use gold high performance linker
        if spec.satisfies("+gold"):
            entries.append(
                cmake_cache_string(
                    "CMAKE_EXE_LINKER_FLAGS", "{0} -fuse-ld=gold".format(linker_flags)
                )
            )
            entries.append(
                cmake_cache_string(
                    "CMAKE_SHARED_LINKER_FLAGS", "{0} -fuse-ld=gold".format(linker_flags)
                )
            )

        # Set the generator in the cached config
        if self.spec.satisfies("generator=make"):
            entries.append(cmake_cache_string("CMAKE_GENERATOR", "Unix Makefiles"))
        if self.spec.satisfies("generator=ninja"):
            entries.append(cmake_cache_string("CMAKE_GENERATOR", "Ninja"))
            entries.append(
                cmake_cache_string(
                    "CMAKE_MAKE_PROGRAM", "{0}/ninja".format(spec["ninja"].prefix.bin)
                )
            )

        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec
        entries = super().initconfig_hardware_entries()

        if spec.satisfies("+cuda"):
            if self.spec.satisfies("%clang"):
                for flag in self.spec.compiler_flags["cxxflags"]:
                    if "gcc-toolchain" in flag:
                        entries.append(
                            cmake_cache_string("CMAKE_CUDA_FLAGS", "-Xcompiler={0}".format(flag))
                        )
            if spec.satisfies("^cuda@11.0:"):
                entries.append(cmake_cache_string("CMAKE_CUDA_STANDARD", "17"))
            else:
                entries.append(cmake_cache_string("CMAKE_CUDA_STANDARD", "14"))

            entries.append(self.define_cmake_cache_from_variant("LBANN_WITH_NVPROF", "nvprof"))

            if spec.satisfies("%cce") and spec.satisfies("^cuda+allow-unsupported-compilers"):
                entries.append(
                    cmake_cache_string("CMAKE_CUDA_FLAGS", "-allow-unsupported-compiler")
                )

        return entries

    def initconfig_package_entries(self):
        spec = self.spec
        entries = []
        entries = [
            "#------------------{0}".format("-" * 60),
            "# LBANN",
            "#------------------{0}\n".format("-" * 60),
        ]

        cmake_variant_fields = [
            ("LBANN_WITH_CNPY", "numpy"),
            ("LBANN_DETERMINISTIC", "deterministic"),
            ("LBANN_WITH_ADDRESS_SANITIZER", "asan"),
            ("LBANN_WITH_BOOST", "boost"),
            ("LBANN_WITH_CALIPER", "caliper"),
            ("LBANN_WITH_NVSHMEM", "nvshmem"),
            ("LBANN_WITH_FFT", "fft"),
            ("LBANN_WITH_ONEDNN", "onednn"),
            ("LBANN_WITH_ONNX", "onnx"),
            ("LBANN_WITH_EMBEDDED_PYTHON", "python"),
            ("LBANN_WITH_PYTHON_FRONTEND", "pfe"),
            ("LBANN_WITH_UNIT_TESTING", "unit_tests"),
            ("LBANN_WITH_VISION", "vision"),
            ("LBANN_WITH_VTUNE", "vtune"),
        ]

        for opt, val in cmake_variant_fields:
            entries.append(self.define_cmake_cache_from_variant(opt, val))

        entries.append(cmake_cache_option("LBANN_WITH_ALUMINUM", True))
        entries.append(cmake_cache_option("LBANN_WITH_CONDUIT", True))
        entries.append(cmake_cache_option("LBANN_WITH_HWLOC", True))
        entries.append(
            cmake_cache_option("LBANN_WITH_ROCTRACER", spec.satisfies("+rocm +distconv"))
        )
        entries.append(cmake_cache_option("LBANN_WITH_TBINF", False))
        entries.append(
            cmake_cache_string("LBANN_DATATYPE", "{0}".format(spec.variants["dtype"].value))
        )
        entries.append(cmake_cache_option("protobuf_MODULE_COMPATIBLE", True))

        if spec.satisfies("+pfe ^python"):
            entries.append(cmake_cache_path("LBANN_PFE_PYTHON_EXECUTABLE", python.path))
            entries.append(
                cmake_cache_string("LBANN_PFE_PYTHONPATH", env["PYTHONPATH"])
            )  # do NOT need to sub ; for : because
            # value will only be interpreted by
            # a shell, which expects :

        # Add support for OpenMP with external (Brew) clang
        if spec.satisfies("%clang platform=darwin"):
            clang = self.compiler.cc
            clang_bin = os.path.dirname(clang)
            clang_root = os.path.dirname(clang_bin)
            entries.append(cmake_cache_string("OpenMP_CXX_FLAGS", "-fopenmp=libomp"))
            entries.append(cmake_cache_string("OpenMP_CXX_LIB_NAMES", "libomp"))
            entries.append(
                cmake_cache_string(
                    "OpenMP_libomp_LIBRARY", "{0}/lib/libomp.dylib".format(clang_root)
                )
            )

        entries.append(cmake_cache_option("LBANN_WITH_DIHYDROGEN", True))
        entries.append(self.define_cmake_cache_from_variant("LBANN_WITH_DISTCONV", "distconv"))

        # IF IBM ESSL is used it needs help finding the proper LAPACK libraries
        if self.spec.satisfies("^essl"):
            entries.append(
                cmake_cache_string(
                    "LAPACK_LIBRARIES",
                    "%s;-llapack;-lblas"
                    % ";".join("-l{0}".format(lib) for lib in self.spec["essl"].libs.names),
                )
            )
            entries.append(
                cmake_cache_string(
                    "BLAS_LIBRARIES",
                    "%s;-lblas"
                    % ";".join("-l{0}".format(lib) for lib in self.spec["essl"].libs.names),
                )
            )

        return entries
