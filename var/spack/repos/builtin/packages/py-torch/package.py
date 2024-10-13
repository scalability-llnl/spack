# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.operating_systems.mac_os import macos_version
from spack.package import *


class PyTorch(PythonPackage, CudaPackage, ROCmPackage):
    """Tensors and Dynamic neural networks in Python with strong GPU acceleration."""

    homepage = "https://pytorch.org/"
    git = "https://github.com/pytorch/pytorch.git"
    submodules = True

    maintainers("adamjstewart")

    # Exact set of modules is version- and variant-specific, just attempt to import the
    # core libraries to ensure that the package was successfully installed.
    import_modules = ["torch", "torch.autograd", "torch.nn", "torch.utils"]

    license("BSD-3-Clause")

    version("main", branch="main")
    version("2.4.1", tag="v2.4.1", commit="ee1b6804381c57161c477caa380a840a84167676")
    version("2.4.0", tag="v2.4.0", commit="d990dada86a8ad94882b5c23e859b88c0c255bda")
    version("2.3.1", tag="v2.3.1", commit="63d5e9221bedd1546b7d364b5ce4171547db12a9")
    version("2.3.0", tag="v2.3.0", commit="97ff6cfd9c86c5c09d7ce775ab64ec5c99230f5d")
    version("2.2.2", tag="v2.2.2", commit="39901f229520a5256505ec24782f716ee7ddc843")
    version("2.2.1", tag="v2.2.1", commit="6c8c5ad5eaf47a62fafbb4a2747198cbffbf1ff0")
    version("2.2.0", tag="v2.2.0", commit="8ac9b20d4b090c213799e81acf48a55ea8d437d6")
    version("2.1.2", tag="v2.1.2", commit="a8e7c98cb95ff97bb30a728c6b2a1ce6bff946eb")
    version("2.1.1", tag="v2.1.1", commit="4c55dc50355d5e923642c59ad2a23d6ad54711e7")
    version("2.1.0", tag="v2.1.0", commit="7bcf7da3a268b435777fe87c7794c382f444e86d")
    version("2.0.1", tag="v2.0.1", commit="e9ebda29d87ce0916ab08c06ab26fd3766a870e5")
    version("2.0.0", tag="v2.0.0", commit="c263bd43e8e8502d4726643bc6fd046f0130ac0e")
    version("1.13.1", tag="v1.13.1", commit="49444c3e546bf240bed24a101e747422d1f8a0ee")
    version("1.13.0", tag="v1.13.0", commit="7c98e70d44abc7a1aead68b6ea6c8adc8c554db5")
    version("1.12.1", tag="v1.12.1", commit="664058fa83f1d8eede5d66418abff6e20bd76ca8")
    version("1.12.0", tag="v1.12.0", commit="67ece03c8cd632cce9523cd96efde6f2d1cc8121")
    version("1.11.0", tag="v1.11.0", commit="bc2c6edaf163b1a1330e37a6e34caf8c553e4755")
    version("1.10.2", tag="v1.10.2", commit="71f889c7d265b9636b93ede9d651c0a9c4bee191")
    version("1.10.1", tag="v1.10.1", commit="302ee7bfb604ebef384602c56e3853efed262030")
    version("1.10.0", tag="v1.10.0", commit="36449ea93134574c2a22b87baad3de0bf8d64d42")
    version("1.9.1", tag="v1.9.1", commit="dfbd030854359207cb3040b864614affeace11ce")
    version("1.9.0", tag="v1.9.0", commit="d69c22dd61a2f006dcfe1e3ea8468a3ecaf931aa")
    version("1.8.2", tag="v1.8.2", commit="e0495a7aa104471d95dc85a1b8f6473fbcc427a8")
    version("1.8.1", tag="v1.8.1", commit="56b43f4fec1f76953f15a627694d4bba34588969")
    version("1.8.0", tag="v1.8.0", commit="37c1f4a7fef115d719104e871d0cf39434aa9d56")
    version("1.7.1", tag="v1.7.1", commit="57bffc3a8e4fee0cce31e1ff1f662ccf7b16db57")
    version("1.7.0", tag="v1.7.0", commit="e85d494707b835c12165976b8442af54b9afcb26")
    version("1.6.0", tag="v1.6.0", commit="b31f58de6fa8bbda5353b3c77d9be4914399724d")
    version("1.5.1", tag="v1.5.1", commit="3c31d73c875d9a4a6ea8a843b9a0d1b19fbe36f3")
    version("1.5.0", tag="v1.5.0", commit="4ff3872a2099993bf7e8c588f7182f3df777205b")
    version("1.4.1", tag="v1.4.1", commit="74044638f755cd8667bedc73da4dbda4aa64c948")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    is_darwin = sys.platform == "darwin"

    # All options are defined in CMakeLists.txt.
    # Some are listed in setup.py, but not all.
    variant("debug", default=False, description="Build with debugging support")
    variant("caffe2", default=False, description="Build Caffe2", when="@1.7:")
    variant("test", default=False, description="Build C++ test binaries")
    variant("cuda", default=not is_darwin, description="Use CUDA")
    variant("rocm", default=False, description="Use ROCm")
    variant("cudnn", default=not is_darwin, description="Use cuDNN", when="+cuda")
    variant("fbgemm", default=True, description="Use FBGEMM (quantized 8-bit server operators)")
    variant("kineto", default=True, description="Use Kineto profiling library", when="@1.8:")
    variant("magma", default=not is_darwin, description="Use MAGMA", when="+cuda")
    variant("metal", default=is_darwin, description="Use Metal for Caffe2 iOS build")
    variant(
        "mps",
        default=is_darwin and macos_version() >= Version("12.3"),
        description="Use MPS for macOS build (requires full Xcode suite)",
        when="@1.12: platform=darwin",
    )
    variant("nccl", default=True, description="Use NCCL", when="+cuda platform=linux")
    variant("nccl", default=True, description="Use NCCL", when="+rocm platform=linux")
    # Requires AVX2: https://discuss.pytorch.org/t/107518
    variant("nnpack", default=True, description="Use NNPACK", when="target=x86_64_v3:")
    variant("numa", default=True, description="Use NUMA", when="platform=linux")
    variant("numpy", default=True, description="Use NumPy")
    variant("openmp", default=True, description="Use OpenMP for parallel code")
    variant("qnnpack", default=True, description="Use QNNPACK (quantized 8-bit operators)")
    variant("valgrind", default=True, description="Use Valgrind", when="@1.8: platform=linux")
    variant("xnnpack", default=True, description="Use XNNPACK", when="@1.5:")
    variant("mkldnn", default=True, description="Use MKLDNN")
    variant("distributed", default=True, description="Use distributed")
    variant("mpi", default=True, description="Use MPI for Caffe2", when="+distributed")
    variant("ucc", default=False, description="Use UCC", when="@1.13: +distributed")
    variant("gloo", default=True, description="Use Gloo", when="+distributed")
    variant("tensorpipe", default=True, description="Use TensorPipe", when="@1.6: +distributed")
    variant("onnx_ml", default=True, description="Enable traditional ONNX ML API", when="@1.5:")
    variant(
        "breakpad",
        default=True,
        description="Enable breakpad crash dump library",
        when="@1.10:1.11",
    )
    # py-torch has strict dependencies on old protobuf/py-protobuf versions that
    # cause problems with other packages that require newer versions of protobuf
    # and py-protobuf --> provide an option to use the internal/vendored protobuf.
    variant("custom-protobuf", default=False, description="Use vendored protobuf")

    conflicts("+cuda+rocm")
    conflicts("+tensorpipe", when="+rocm ^hip@:5.1", msg="TensorPipe not supported until ROCm 5.2")
    conflicts("+breakpad", when="target=ppc64:")
    conflicts("+breakpad", when="target=ppc64le:")

    # https://github.com/pytorch/pytorch/issues/77811
    conflicts("+qnnpack", when="platform=darwin target=aarch64:")

    # https://github.com/pytorch/pytorch/issues/97397
    conflicts(
        "~tensorpipe",
        when="@1.8: +distributed",
        msg="TensorPipe must be enabled with +distributed",
    )

    # https://github.com/pytorch/pytorch/issues/100991
    conflicts("%apple-clang@14:", when="@:1")

    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )

    # Required dependencies
    # Based on PyPI wheel availability
    with default_args(type=("build", "link", "run")):
        depends_on("python@3.8:3.12", when="@2.2:")
        depends_on("python@3.8:3.11", when="@2.0:2.1")
        depends_on("python@:3.10", when="@1.11:1")
        depends_on("python@:3.9", when="@1.7.1:1.10")
        depends_on("python@:3.8", when="@1.4:1.7.0")

    # CMakelists.txt
    with default_args(type="build"):
        depends_on("cmake@3.18:", when="@2:")
        depends_on("cmake@3.13:", when="@1.11:")
        depends_on("cmake@3.10:", when="@1.10:")
        depends_on("cmake@3.5:")
        depends_on("ninja@1.5:")

    with default_args(type=("build", "run")):
        # setup.py
        depends_on("py-filelock", when="@2:")
        depends_on("py-typing-extensions@4.8:", when="@2.2:")
        depends_on("py-typing-extensions@3.6.2.1:", when="@1.7:")
        depends_on("py-sympy", when="@2:")
        depends_on("py-networkx", when="@2:")
        depends_on("py-jinja2", when="@2:")
        depends_on("py-fsspec", when="@2.1:")

        # pyproject.toml
        depends_on("py-setuptools")
        depends_on("py-astunparse", when="@1.13:")
        depends_on("py-numpy@1.16.6:")
        # https://github.com/pytorch/pytorch/issues/107302
        depends_on("py-numpy@:1", when="@:2.2")
        depends_on("py-pyyaml")
        depends_on("py-requests", when="@1.13:")

    # Undocumented dependencies
    depends_on("py-tqdm", type="run")
    depends_on("blas")
    depends_on("lapack")

    # Third party dependencies
    depends_on("fp16@2020-05-14", when="@1.6:")
    depends_on("fxdiv@2020-04-17", when="@1.6:")
    # https://github.com/pytorch/pytorch/issues/60332
    # depends_on("xnnpack@2024-02-29", when="@2.3:+xnnpack")
    # depends_on("xnnpack@2022-12-21", when="@2.0:2.2+xnnpack")
    # depends_on("xnnpack@2022-02-16", when="@1.12:1+xnnpack")
    # depends_on("xnnpack@2021-06-21", when="@1.10:1.11+xnnpack")
    # depends_on("xnnpack@2021-02-22", when="@1.8:1.9+xnnpack")
    # depends_on("xnnpack@2020-03-23", when="@1.6:1.7+xnnpack")
    depends_on("benchmark", when="@1.6:+test")
    depends_on("cpuinfo@2023-11-04", when="@2.3:")
    depends_on("cpuinfo@2023-01-13", when="@2.1:2.2")
    depends_on("cpuinfo@2022-08-19", when="@1.13:2.0")
    depends_on("cpuinfo@2020-12-17", when="@1.8:1.12")
    depends_on("cpuinfo@2020-06-11", when="@1.6:1.7")
    depends_on("eigen")
    depends_on("gloo@2023-12-03", when="@2.3:+gloo")
    depends_on("gloo@2023-05-19", when="@2.1:2.2+gloo")
    depends_on("gloo@2023-01-17", when="@2.0+gloo")
    depends_on("gloo@2022-05-18", when="@1.13:1+gloo")
    depends_on("gloo@2021-05-21", when="@1.10:1.12+gloo")
    depends_on("gloo@2021-05-04", when="@1.9+gloo")
    depends_on("gloo@2020-09-18", when="@1.7:1.8+gloo")
    depends_on("gloo@2020-03-17", when="@1.6+gloo")
    depends_on("gloo+cuda", when="@1.6:+gloo+cuda")
    depends_on("gloo+libuv", when="@1.6: platform=darwin")
    depends_on("nccl", when="+nccl+cuda")
    # https://github.com/pytorch/pytorch/issues/60331
    # depends_on("onnx@1.16.0", when="@2.3:+onnx_ml")
    # depends_on("onnx@1.15.0", when="@2.2+onnx_ml")
    # depends_on("onnx@1.14.1", when="@2.1+onnx_ml")
    # depends_on("onnx@1.13.1", when="@2.0+onnx_ml")
    # depends_on("onnx@1.12.0", when="@1.13:1+onnx_ml")
    # depends_on("onnx@1.11.0", when="@1.12+onnx_ml")
    # depends_on("onnx@1.10.1_2021-10-08", when="@1.11+onnx_ml")
    # depends_on("onnx@1.10.1", when="@1.10+onnx_ml")
    # depends_on("onnx@1.8.0_2020-11-03", when="@1.8:1.9+onnx_ml")
    # depends_on("onnx@1.7.0_2020-05-31", when="@1.6:1.7+onnx_ml")
    with when("~custom-protobuf"):
        depends_on("protobuf@3.13.0", when="@1.10:")
        depends_on("protobuf@3.11.4", when="@1.6:1.9")
        depends_on("protobuf@3.6.1", when="@1.1:1.5")
        depends_on("protobuf@3.5.0", when="@1.0")
        with default_args(type=("build", "run")):
            depends_on("py-protobuf@3.13", when="@1.10:")
            depends_on("py-protobuf@3.11", when="@1.6:1.9")
            depends_on("py-protobuf@3.6", when="@1.1:1.5")
            depends_on("py-protobuf@3.5", when="@1.0")
    depends_on("psimd@2020-05-17", when="@1.6:")
    depends_on("pthreadpool@2023-08-29", when="@2.2:")
    depends_on("pthreadpool@2021-04-13", when="@1.9:2.1")
    depends_on("pthreadpool@2020-10-05", when="@1.8")
    depends_on("pthreadpool@2020-06-15", when="@1.6:1.7")
    with default_args(type=("build", "link", "run")):
        depends_on("py-pybind11@2.12.0:", when="@2.3:")
        depends_on("py-pybind11@2.11.0:", when="@2.1:2.2")
        depends_on("py-pybind11@2.10.1:", when="@2.0")
        depends_on("py-pybind11@2.10.0:", when="@1.13:1")
        depends_on("py-pybind11@2.6.2:", when="@1.8:1.12")
        depends_on("py-pybind11@2.3.0:", when="@:1.7")
    depends_on("sleef@3.6.0_2024-03-20", when="@2.4:")
    depends_on("sleef@3.5.1_2020-12-22", when="@1.8:2.3")
    depends_on("sleef@3.4.0_2019-07-30", when="@1.6:1.7")

    # Optional dependencies
    with default_args(type=("build", "link", "run")):
        # cmake/public/cuda.cmake
        depends_on("cuda@11:", when="@2.4:+cuda")
        # https://github.com/pytorch/pytorch/issues/122169
        depends_on("cuda@11:12.3", when="@2.0:2.3+cuda")
        depends_on("cuda@10.2:12.3", when="@1.11:1+cuda")
        # https://discuss.pytorch.org/t/compiling-1-10-1-from-source-with-gcc-11-and-cuda-11-5/140971
        depends_on("cuda@10.2:11.4", when="@1.10+cuda")
        depends_on("cuda@9.2:11.4", when="@1.6:1.9+cuda")
        depends_on("cuda@9:11.4", when="@:1.5+cuda")
    # https://github.com/pytorch/pytorch#prerequisites
    # https://github.com/pytorch/pytorch/issues/119400
    depends_on("cudnn@8.5:9.0", when="@2.3:+cudnn")
    depends_on("cudnn@7:8", when="@1.6:2.2+cudnn")
    depends_on("cudnn@7", when="@:1.5+cudnn")
    depends_on("magma+cuda", when="+magma+cuda")
    depends_on("magma+rocm", when="+magma+rocm")
    depends_on("numactl", when="+numa")
    depends_on("llvm-openmp", when="%apple-clang +openmp")
    depends_on("valgrind", when="+valgrind")
    with when("+rocm"):
        depends_on("hsa-rocr-dev")
        depends_on("hip")
        depends_on("rccl", when="+nccl")
        depends_on("rocprim")
        depends_on("hipcub")
        depends_on("rocthrust")
        depends_on("roctracer-dev")
        depends_on("rocrand")
        depends_on("hipsparse")
        depends_on("hipfft")
        depends_on("rocfft")
        depends_on("rocblas")
        depends_on("miopen-hip")
        depends_on("rocminfo")
    depends_on("mpi", when="+mpi")
    depends_on("ucc", when="+ucc")
    depends_on("ucx", when="+ucc")
    depends_on("mkl", when="+mkldnn")

    # Test dependencies
    with default_args(type="test"):
        depends_on("py-hypothesis")
        depends_on("py-six")
        depends_on("py-psutil")

    # Historical dependencies
    with default_args(type=("build", "run")):
        depends_on("mkl@2021.1.1:2021.4.0", when="@2.3 platform=windows")
        depends_on("py-cffi", when="@:1")
        depends_on("py-future", when="@1.5:1")
        depends_on("py-six", when="@1.13:1")

    conflicts("%gcc@:9.3", when="@2.2:", msg="C++17 support required")

    # https://github.com/pytorch/pytorch/issues/90448
    patch(
        "https://github.com/pytorch/pytorch/pull/97270.patch?full_index=1",
        sha256="beb3fb57746cf8443f5caa6e08b2f8f4d4822c1e11e0c912134bd166c6a0ade7",
        when="@1.10:2.0",
    )

    # Fix BLAS being overridden by MKL
    # https://github.com/pytorch/pytorch/issues/60328
    patch(
        "https://github.com/pytorch/pytorch/pull/59220.patch?full_index=1",
        sha256="6d5717267f901e8ee493dfacd08734d9bcc48ad29a76ca9ef702368e96bee675",
        when="@:1.11",
    )

    # Fixes build on older systems with glibc <2.12
    patch(
        "https://github.com/pytorch/pytorch/pull/55063.patch?full_index=1",
        sha256="2229bcbf20fbe88aa9f7318f89c126ec7f527875ffe689a763c78abfa127a65c",
        when="@:1.8.1",
    )

    # https://github.com/pytorch/pytorch/issues/70297
    patch(
        "https://github.com/google/breakpad/commit/605c51ed96ad44b34c457bbca320e74e194c317e.patch?full_index=1",
        sha256="694d83db3a2147d543357f22ba5c8d5683d0ed43e693d42bca8f24ec50080f98",
        when="+breakpad",
        working_dir="third_party/breakpad",
    )

    # Fixes CMake configuration error when XNNPACK is disabled
    # https://github.com/pytorch/pytorch/pull/35607
    # https://github.com/pytorch/pytorch/pull/37865
    patch("xnnpack.patch", when="@1.5")

    # Fixes build error when ROCm is enabled for pytorch-1.5 release
    patch("rocm.patch", when="@1.5+rocm")

    # Fixes compilation with Clang 9.0.0 and Apple Clang 11.0.3
    # https://github.com/pytorch/pytorch/pull/37086
    patch(
        "https://github.com/pytorch/pytorch/commit/e921cd222a8fbeabf5a3e74e83e0d8dfb01aa8b5.patch?full_index=1",
        sha256="0f3ad037a95af9d34b1d085050c1e7771fd00f0b89e5b3a276097b7c9f4fabf8",
        when="@:1.5",
    )

    # Fixes 'FindOpenMP.cmake'
    # to detect openmp settings used by Fujitsu compiler.
    patch("detect_omp_of_fujitsu_compiler.patch", when="%fj")

    # Fixes to build with fujitsu-ssl2
    patch("fj-ssl2_1.11.patch", when="@1.11:^fujitsu-ssl2")
    patch("fj-ssl2_1.10.patch", when="@1.10^fujitsu-ssl2")
    patch("fj-ssl2_1.9.patch", when="@1.9^fujitsu-ssl2")
    patch("fj-ssl2_1.8.patch", when="@1.8^fujitsu-ssl2")
    patch("fj-ssl2_1.6-1.7.patch", when="@1.6:1.7^fujitsu-ssl2")
    patch("fj-ssl2_1.3-1.5.patch", when="@:1.5^fujitsu-ssl2")

    # Fix compilation of +distributed~tensorpipe
    # https://github.com/pytorch/pytorch/issues/68002
    patch(
        "https://github.com/pytorch/pytorch/commit/c075f0f633fa0136e68f0a455b5b74d7b500865c.patch?full_index=1",
        sha256="41271e494a3a60a65a8dd45ac053d1a6e4e4d5b42c2dac589ac67524f61ac41e",
        when="@1.10.0+distributed~tensorpipe",
    )

    # Use patches from IBM's Open CE to enable building on Power systems
    # 01xx patches are specific to open-ce, we only include 03xx patches used in meta.yaml
    # https://github.com/open-ce/pytorch-feedstock
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.7.4/pytorch-1.10/recipe/0302-cpp-extension.patch",
        sha256="ecb3973fa7d0f4c8f8ae40433f3ca5622d730a7b16f6cb63325d1e95baff8aa2",
        when="@1.10:1.11 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.7.4/pytorch-1.10/recipe/0311-PR66085-Remove-unused-dump-method-from-VSX-vec256-methods.patch",
        sha256="f05db59f3def4c4215db7142d81029c73fe330c660492159b66d65ca5001f4d1",
        when="@1.10 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.7.4/pytorch-1.10/recipe/0312-PR67331-Dummpy-VSX-bfloat16-implementation.patch",
        sha256="860b64afa85f5e6647ebc3c91d5a0bb258784770900c9302c3599c98d5cff1ee",
        when="@1.10 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.7.4/pytorch-1.10/recipe/0313-add-missing-vsx-dispatch.patch",
        sha256="7393c2bc0b6d41ecc813c829a1e517bee864686652e91f174cb7bcdfb10ba451",
        when="@1.10 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.7.4/pytorch-1.10/recipe/0314-fix-nullpointer-error.patch",
        sha256="b9cff8966f316f58514c66a403b7a6786be3cdb252f1380a6b91c722686a4097",
        when="@1.10 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.7.4/pytorch-1.12/recipe/0302-cpp-extension.patch",
        sha256="2fac519cca8997f074c263505657ff867e7ba2d6637fc8bda99c70a99be0442a",
        when="@1.12 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.8.0/pytorch-1.13/recipe/0302-cpp-extension.patch",
        sha256="a54db63640b90e5833cc1099c0935572f5297d2d8625f62f01ac1fda79ed4569",
        when="@1.13 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.9.0/pytorch-2.0/recipe/0309-fallback-to-cpu_kernel-with-VSX.patch",
        sha256="27f41c8d6cb61e69e761be62f03dc1ce023cbca34926e3ba559996821a7ce726",
        when="@2.0 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.9.0/pytorch-2.0/recipe/0310-PR100149.patch",
        sha256="1adbd38a9cc1611f1caaa325614695f4349d9ffd236332e0d8f0de5a3880f4dd",
        when="@2.0 arch=ppc64le:",
    )
    patch(
        "https://github.com/open-ce/pytorch-feedstock/raw/open-ce-v1.10.0/pytorch-2.0/recipe/0311-PR104956.patch",
        sha256="be27c906924a21be198a3ea6c459739a1daa8b8b89045af339dafa4cd6f90d6c",
        when="@2.0 arch=ppc64le:",
    )
    conflicts("arch=ppc64le:", when="@:1.9")

    # Cherry-pick a patch to allow earlier versions of PyTorch to work with CUDA 11.4
    patch(
        "https://github.com/pytorch/pytorch/commit/c74c0c571880df886474be297c556562e95c00e0.patch?full_index=1",
        sha256="8ff7d285e52e4718bad1ca01ceb3bb6471d7828329036bb94222717fcaa237da",
        when="@:1.9.1 ^cuda@11.4.100:",
    )

    # PyTorch does not build with GCC 12 (fixed in 2.0)
    # See: https://github.com/pytorch/pytorch/issues/77614
    patch(
        "https://github.com/facebookincubator/gloo/commit/4a5e339b764261d20fc409071dc7a8b8989aa195.patch?full_index=1",
        sha256="dc8b3a9bea4693f32d6850ea2ce6ce75e1778538bfba464b50efca92bac425e3",
        when="@:1 %gcc@12:",
        working_dir="third_party/gloo",
    )

    # PyTorch does not build on Linux >=6.0.3 (fixed in master)
    # See: https://github.com/facebookincubator/gloo/issues/345
    patch(
        "https://github.com/facebookincubator/gloo/commit/10909297fedab0a680799211a299203e53515032.patch?full_index=1",
        sha256="8e6e9a44e0533ba4303a95a651b1934e5d73632cab08cc7d5a9435e1e64aa424",
        when="@:1",
        working_dir="third_party/gloo",
    )

    # Some missing includes
    # See: https://github.com/pytorch/pytorch/pull/100036
    patch(
        "https://patch-diff.githubusercontent.com/raw/pytorch/pytorch/pull/100036.patch?full_index=1",
        sha256="65060b54c31196b26dcff29bbb178fd17d5677e8481a2a06002c0ca4dd37b3d0",
        when="@2.0.0:2.0.1",
    )
    # See: https://github.com/pytorch/pytorch/pull/100049
    patch(
        "https://patch-diff.githubusercontent.com/raw/pytorch/pytorch/pull/100049.patch?full_index=1",
        sha256="673056141c0ea6ff4411f65a26f1a9d7a7c49ad8fe034a01ef0d56ba8a7a9386",
        when="@2.0.0:2.0.1",
    )

    # Use correct OpenBLAS include path under prefix
    patch(
        "https://patch-diff.githubusercontent.com/raw/pytorch/pytorch/pull/110063.patch?full_index=1",
        sha256="23fb4009f7337051fc5303927ff977186a5af960245e7212895406477d8b2f66",
        when="@:2.1",
    )

    patch(
        "https://github.com/pytorch/FBGEMM/commit/da01a59556fec9776733bf20aea8fe8fb29cdd3d.patch?full_index=1",
        sha256="97d8bd43f8cd8bb203dab3480d609c08499224acaca9915f2bdeb23c62350fb1",
        when="@2.0.1 +fbgemm",
        working_dir="third_party/fbgemm",
    )

    @when("@1.5.0:")
    def patch(self):
        # https://github.com/pytorch/pytorch/issues/52208
        filter_file(
            "torch_global_deps PROPERTIES LINKER_LANGUAGE C",
            "torch_global_deps PROPERTIES LINKER_LANGUAGE CXX",
            "caffe2/CMakeLists.txt",
        )

    def torch_cuda_arch_list(self, env):
        if "+cuda" in self.spec:
            torch_cuda_arch = CudaPackage.compute_capabilities(
                self.spec.variants["cuda_arch"].value
            )
            env.set("TORCH_CUDA_ARCH_LIST", ";".join(torch_cuda_arch))

    def setup_build_environment(self, env):
        """Set environment variables used to control the build.

        PyTorch's ``setup.py`` is a thin wrapper around ``cmake``.
        In ``tools/setup_helpers/cmake.py``, you can see that all
        environment variables that start with ``BUILD_``, ``USE_``,
        or ``CMAKE_``, plus a few more explicitly specified variable
        names, are passed directly to the ``cmake`` call. Therefore,
        most flags defined in ``CMakeLists.txt`` can be specified as
        environment variables.
        """

        def enable_or_disable(variant, keyword="USE", var=None):
            """Set environment variable to enable or disable support for a
            particular variant.

            Parameters:
                variant (str): the variant to check
                keyword (str): the prefix to use for enabling/disabling
                var (str): CMake variable to set. Defaults to variant.upper()
            """
            if var is None:
                var = variant.upper()

            if "+" + variant in self.spec:
                env.set(keyword + "_" + var, "ON")
            elif "~" + variant in self.spec:
                env.set(keyword + "_" + var, "OFF")

        # Build in parallel to speed up build times
        env.set("MAX_JOBS", make_jobs)

        # Spack logs have trouble handling colored output
        env.set("COLORIZE_OUTPUT", "OFF")

        enable_or_disable("test", keyword="BUILD")
        enable_or_disable("caffe2", keyword="BUILD")

        enable_or_disable("cuda")
        if "+cuda" in self.spec:
            env.set("CUDA_TOOLKIT_ROOT_DIR", self.spec["cuda"].prefix)  # Linux/macOS
            env.set("CUDA_HOME", self.spec["cuda"].prefix)  # Linux/macOS
            env.set("CUDA_PATH", self.spec["cuda"].prefix)  # Windows
            self.torch_cuda_arch_list(env)

            if self.spec.satisfies("%clang"):
                for flag in self.spec.compiler_flags["cxxflags"]:
                    if "gcc-toolchain" in flag:
                        env.set("CMAKE_CUDA_FLAGS", "=-Xcompiler={0}".format(flag))

        enable_or_disable("rocm")
        if "+rocm" in self.spec:
            env.set("PYTORCH_ROCM_ARCH", ";".join(self.spec.variants["amdgpu_target"].value))
            env.set("HSA_PATH", self.spec["hsa-rocr-dev"].prefix)
            env.set("ROCBLAS_PATH", self.spec["rocblas"].prefix)
            env.set("ROCFFT_PATH", self.spec["rocfft"].prefix)
            env.set("HIPFFT_PATH", self.spec["hipfft"].prefix)
            env.set("HIPSPARSE_PATH", self.spec["hipsparse"].prefix)
            env.set("HIP_PATH", self.spec["hip"].prefix)
            env.set("HIPRAND_PATH", self.spec["rocrand"].prefix)
            env.set("ROCRAND_PATH", self.spec["rocrand"].prefix)
            env.set("MIOPEN_PATH", self.spec["miopen-hip"].prefix)
            if "+nccl" in self.spec:
                env.set("RCCL_PATH", self.spec["rccl"].prefix)
            env.set("ROCPRIM_PATH", self.spec["rocprim"].prefix)
            env.set("HIPCUB_PATH", self.spec["hipcub"].prefix)
            env.set("ROCTHRUST_PATH", self.spec["rocthrust"].prefix)
            env.set("ROCTRACER_PATH", self.spec["roctracer-dev"].prefix)
            if self.spec.satisfies("^hip@5.2.0:"):
                env.set("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip)

        enable_or_disable("cudnn")
        if "+cudnn" in self.spec:
            # cmake/Modules_CUDA_fix/FindCUDNN.cmake
            env.set("CUDNN_INCLUDE_DIR", self.spec["cudnn"].prefix.include)
            env.set("CUDNN_LIBRARY", self.spec["cudnn"].libs[0])

        # Flash attention has very high memory requirements that may cause the build to fail
        # https://github.com/pytorch/pytorch/issues/111526
        # https://github.com/pytorch/pytorch/issues/124018
        env.set("USE_FLASH_ATTENTION", "OFF")

        enable_or_disable("fbgemm")
        enable_or_disable("kineto")
        enable_or_disable("magma")
        enable_or_disable("metal")
        enable_or_disable("mps")
        enable_or_disable("breakpad")

        enable_or_disable("nccl")
        if "+cuda+nccl" in self.spec:
            env.set("NCCL_LIB_DIR", self.spec["nccl"].libs.directories[0])
            env.set("NCCL_INCLUDE_DIR", self.spec["nccl"].prefix.include)

        # cmake/External/nnpack.cmake
        enable_or_disable("nnpack")

        enable_or_disable("numa")
        if "+numa" in self.spec:
            # cmake/Modules/FindNuma.cmake
            env.set("NUMA_ROOT_DIR", self.spec["numactl"].prefix)

        # cmake/Modules/FindNumPy.cmake
        enable_or_disable("numpy")
        # cmake/Modules/FindOpenMP.cmake
        enable_or_disable("openmp")
        enable_or_disable("qnnpack")
        enable_or_disable("qnnpack", var="PYTORCH_QNNPACK")
        enable_or_disable("valgrind")
        enable_or_disable("xnnpack")
        enable_or_disable("mkldnn")
        enable_or_disable("distributed")
        enable_or_disable("mpi")
        enable_or_disable("ucc")
        # cmake/Modules/FindGloo.cmake
        enable_or_disable("gloo")
        enable_or_disable("tensorpipe")

        if "+debug" in self.spec:
            env.set("DEBUG", "ON")
        else:
            env.set("DEBUG", "OFF")

        if "+onnx_ml" in self.spec:
            env.set("ONNX_ML", "ON")
        elif "~onnx_ml" in self.spec:
            env.set("ONNX_ML", "OFF")

        if not self.spec.satisfies("@main"):
            env.set("PYTORCH_BUILD_VERSION", self.version)
            env.set("PYTORCH_BUILD_NUMBER", 0)

        # BLAS to be used by Caffe2
        # Options defined in cmake/Dependencies.cmake and cmake/Modules/FindBLAS.cmake
        if self.spec["blas"].name == "atlas":
            env.set("BLAS", "ATLAS")
            env.set("WITH_BLAS", "atlas")
            env.set("Atlas_ROOT_DIR", self.spec["atlas"].prefix)
        elif self.spec["blas"].name in ["blis", "amdblis"]:
            env.set("BLAS", "BLIS")
            env.set("WITH_BLAS", "blis")
            env.set("BLIS_HOME", self.spec["blas"].prefix)
        elif self.spec["blas"].name == "eigen":
            env.set("BLAS", "Eigen")
        elif self.spec["lapack"].name in ["libflame", "amdlibflame"]:
            env.set("BLAS", "FLAME")
            env.set("WITH_BLAS", "FLAME")
        elif self.spec["blas"].name in ["intel-mkl", "intel-parallel-studio", "intel-oneapi-mkl"]:
            env.set("BLAS", "MKL")
            env.set("WITH_BLAS", "mkl")
            # help find MKL
            if self.spec["mkl"].name == "intel-oneapi-mkl":
                env.set("INTEL_MKL_DIR", self.spec["mkl"].prefix.mkl.latest)
            else:
                env.set("INTEL_MKL_DIR", self.spec["mkl"].prefix.mkl)
        elif self.spec["blas"].name == "openblas":
            env.set("BLAS", "OpenBLAS")
            env.set("WITH_BLAS", "open")
            env.set("OpenBLAS_HOME", self.spec["openblas"].prefix)
        elif self.spec["blas"].name == "veclibfort":
            env.set("BLAS", "vecLib")
            env.set("WITH_BLAS", "veclib")
        elif self.spec["blas"].name == "fujitsu-ssl2":
            env.set("BLAS", "SSL2")
            env.set("WITH_BLAS", "ssl2")
        else:
            env.set("BLAS", "Generic")
            env.set("WITH_BLAS", "generic")

        # Don't use vendored third-party libraries when possible
        # env.set("USE_SYSTEM_LIBS", "ON")
        env.set("USE_SYSTEM_BENCHMARK", "ON")
        env.set("USE_SYSTEM_CPUINFO", "ON")
        env.set("USE_SYSTEM_EIGEN_INSTALL", "ON")
        env.set("USE_SYSTEM_FP16", "ON")
        env.set("USE_SYSTEM_FXDIV", "ON")
        env.set("USE_SYSTEM_GLOO", "ON")
        env.set("USE_SYSTEM_NCCL", "ON")
        # https://github.com/pytorch/pytorch/issues/60331
        # env.set("USE_SYSTEM_ONNX", "ON")
        env.set("USE_SYSTEM_PSIMD", "ON")
        env.set("USE_SYSTEM_PTHREADPOOL", "ON")
        env.set("USE_SYSTEM_PYBIND11", "ON")
        env.set("USE_SYSTEM_SLEEF", "ON")
        env.set("USE_SYSTEM_UCC", "ON")
        # https://github.com/pytorch/pytorch/issues/60332
        # env.set("USE_SYSTEM_XNNPACK", "ON")

        if self.spec.satisfies("+custom-protobuf"):
            env.set("BUILD_CUSTOM_PROTOBUF", "ON")
        else:
            env.set("BUILD_CUSTOM_PROTOBUF", "OFF")

    def setup_run_environment(self, env):
        self.torch_cuda_arch_list(env)

    @run_before("install")
    def build_amd(self):
        if "+rocm" in self.spec:
            python(os.path.join("tools", "amd_build", "build_amd.py"))

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def install_test(self):
        with working_dir("test"):
            python("run_test.py")

    @property
    def cmake_prefix_paths(self):
        cmake_prefix_paths = [join_path(python_platlib, "torch", "share", "cmake")]
        return cmake_prefix_paths
