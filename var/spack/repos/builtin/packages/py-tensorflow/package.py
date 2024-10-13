# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import sys
import tempfile

from spack.build_environment import optimization_flags
from spack.package import *

rocm_dependencies = [
    "hip",
    "rocrand",
    "rocblas",
    "rocfft",
    "hipfft",
    "rccl",
    "hipsparse",
    "rocprim",
    "llvm-amdgpu",
    "hsa-rocr-dev",
    "rocminfo",
    "hipsolver",
    "hiprand",
    "rocsolver",
    "hipsolver",
    "hipblas",
    "hipcub",
    "rocm-core",
    "roctracer-dev",
    "miopen-hip",
]


class PyTensorflow(Package, CudaPackage, ROCmPackage, PythonExtension):
    """TensorFlow is an open source machine learning framework for everyone."""

    homepage = "https://www.tensorflow.org"
    url = "https://github.com/tensorflow/tensorflow/archive/v2.3.1.tar.gz"
    git = "https://github.com/tensorflow/tensorflow.git"

    maintainers("adamjstewart", "aweits")
    import_modules = ["tensorflow"]

    license("Apache-2.0")

    version("2.17.0", sha256="9cc4d5773b8ee910079baaecb4086d0c28939f024dd74b33fc5e64779b6533dc")
    version("2.16.2", sha256="023849bf253080cb1e4f09386f5eb900492da2288274086ed6cfecd6d99da9eb")
    version("2.16.1", sha256="c729e56efc945c6df08efe5c9f5b8b89329c7c91b8f40ad2bb3e13900bd4876d")
    version(
        "2.16.1-rocm-enhanced",
        sha256="e1b63b1b5d5b014194ed33113c7fa7f26ecb8d36333282b8c550e795e0eb31c6",
        url="https://github.com/ROCm/tensorflow-upstream/archive/refs/tags/v2.16.1-rocm-enhanced.tar.gz",
    )
    version("2.15.1", sha256="f36416d831f06fe866e149c7cd752da410a11178b01ff5620e9f265511ed57cf")
    version("2.15.0", sha256="9cec5acb0ecf2d47b16891f8bc5bc6fbfdffe1700bdadc0d9ebe27ea34f0c220")
    version("2.14.1", sha256="6b31ed347ed7a03c45b906aa41628ac91c3db7c84cb816971400d470e58ba494")
    version(
        "2.14-rocm-enhanced",
        git="https://github.com/ROCm/tensorflow-upstream.git",
        branch="r2.14-rocm-enhanced-nohipblaslt-build",
    )
    version("2.14.0", sha256="ce357fd0728f0d1b0831d1653f475591662ec5bca736a94ff789e6b1944df19f")
    version("2.13.1", sha256="89c07aebd4f41fbe0d08cc88aef00305542134f2f16d3b62918dc3c1182f33e2")
    version("2.13.0", sha256="e58c939079588623e6fa1d054aec2f90f95018266e0a970fd353a5244f5173dc")
    version("2.12.1", sha256="6bc4600cc0b88e9e40f1800096f5bddbbd3b6e5527a030dea631b87f2ae46b5b")
    version("2.12.0", sha256="c030cb1905bff1d2446615992aad8d8d85cbe90c4fb625cee458c63bf466bc8e")
    version("2.11.1", sha256="624ed1cc170cdcc19e8a15d8cdde989a9a1c6b0534c90b38a6b2f06fb2963e5f")
    version(
        "2.11.0-rocm-enhanced",
        sha256="0c4ee8d83bc72215cbc1a5cd3e88cde1a9cf7304237d3e3d8d105ff09827d903",
        url="https://github.com/ROCmSoftwarePlatform/tensorflow-upstream/archive/refs/tags/v2.11.0-rocm-enhanced.tar.gz",
    )
    version("2.11.0", sha256="99c732b92b1b37fc243a559e02f9aef5671771e272758aa4aec7f34dc92dac48")
    version("2.10.1", sha256="622a92e22e6f3f4300ea43b3025a0b6122f1cc0e2d9233235e4c628c331a94a3")
    version("2.10.0", sha256="b5a1bb04c84b6fe1538377e5a1f649bb5d5f0b2e3625a3c526ff3a8af88633e8")
    version("2.9.3", sha256="59d09bd00eef6f07477eea2f50778582edd4b7b2850a396f1fd0c646b357a573")
    version("2.9.2", sha256="8cd7ed82b096dc349764c3369331751e870d39c86e73bbb5374e1664a59dcdf7")
    version("2.9.1", sha256="6eaf86ead73e23988fe192da1db68f4d3828bcdd0f3a9dc195935e339c95dbdc")
    version("2.9.0", sha256="8087cb0c529f04a4bfe480e49925cd64a904ad16d8ec66b98e2aacdfd53c80ff")
    version("2.8.4", sha256="c08a222792bdbff9da299c7885561ee27b95d414d1111c426efac4ccdce92cde")
    version("2.8.3", sha256="4b7ecbe50b36887e1615bc2a582cb86df1250004d8bb540e18336d539803b5a7")
    version("2.8.2", sha256="b3f860c02c22a30e9787e2548ca252ab289a76b7778af6e9fa763d4aafd904c7")
    version("2.8.1", sha256="4b487a63d6f0c1ca46a2ac37ba4687eabdc3a260c222616fa414f6df73228cec")
    version("2.8.0", sha256="66b953ae7fba61fd78969a2e24e350b26ec116cf2e6a7eb93d02c63939c6f9f7")
    version(
        "2.7.4-rocm-enhanced",
        sha256="45b79c125edfdc008274f1b150d8b5a53b3ff4713fd1ad1ff4738f515aad8191",
        url="https://github.com/ROCmSoftwarePlatform/tensorflow-upstream/archive/refs/tags/v2.7.4-rocm-enhanced.tar.gz",
    )
    version("2.7.4", sha256="75b2e40a9623df32da16d8e97528f5e02e4a958e23b1f2ee9637be8eec5d021b")
    version("2.7.3", sha256="b576c2e124cd6d4d04cbfe985430a0d955614e882172b2258217f0ec9b61f39b")
    version("2.7.2", sha256="b3c8577f3b7cc82368ff7f9315821d506abd2f716ea6692977d255b7d8bc54c0")
    version("2.7.1", sha256="abebe2cf5ca379e18071693ca5f45b88ade941b16258a21cc1f12d77d5387a21")
    version("2.7.0", sha256="bb124905c7fdacd81e7c842b287c169bbf377d29c74c9dacc04f96c9793747bb")
    version("2.6.5", sha256="305da42845ac584a42494e521c92a88ce92ee47d93022d4c0bb45180b5c19a8c")
    version("2.6.4", sha256="6a9e54f46039ef0a6f0a1adf19befa510044d3203d1e124dba8318ec4b1e0210")
    version("2.6.3", sha256="7a71dde0987677b9512b202eb6ae119e0e308b1ea15b66dcfce001a44873997b")
    version("2.6.2", sha256="e68c1d346fc3d529653530ca346b2c62f5b31bd4fcca7ffc9c65bb39ab2f6ed3")
    version("2.6.1", sha256="8e457f617bc2eb43de2a51900e7922b60a8107e2524b2576438f1acccee1d043")
    version("2.6.0", sha256="41b32eeaddcbc02b0583660bcf508469550e4cd0f86b22d2abe72dfebeacde0f")
    version("2.5.3", sha256="58d69b7163f7624debc243750976d27fa7dddbc6fb7c5215aec94732bcc670e1")
    version("2.5.2", sha256="bcccc6ba0b8ac1d10d3302f766eed71911acecc0bc43d0bd27d97a1e7ce275a8")
    version("2.5.1", sha256="8d2728e155a3aa6befd9cb3d0980fabd25e2142d124f8f6b6c78cdf17ff79da5")
    version("2.5.0", sha256="233875ea27fc357f6b714b2a0de5f6ff124b50c1ee9b3b41f9e726e9e677b86c")
    version("2.4.4", sha256="f1abc3ed92c3ce955db2a7db5ec422a3a98f015331183194f97b99fe77a09bb4")
    version("2.4.3", sha256="cafd520c753f8755a9eb1262932f685dc722d8658f08373f8ec88d8acd58d7d4")
    version("2.4.2", sha256="edc88da97277906513d53eeee57997a2036fa32ac1f1937730301764fa06cdc0")
    version("2.4.1", sha256="f681331f8fc0800883761c7709d13cda11942d4ad5ff9f44ad855e9dc78387e0")
    version("2.4.0", sha256="26c833b7e1873936379e810a39d14700281125257ddda8cd822c89111db6f6ae")
    version("2.3.4", sha256="195947838b0918c15d79bc6ed85ff714b24d6d564b4d07ba3de0b745a2f9b656")
    version("2.3.3", sha256="b91e5bcd373b942c4a62c6bcb7ff6f968b1448152b82f54a95dfb0d8fb9c6093")
    version("2.3.2", sha256="21a703d2e68cd0677f6f9ce329198c24fd8203125599d791af9f1de61aadf31f")
    version("2.3.2", sha256="21a703d2e68cd0677f6f9ce329198c24fd8203125599d791af9f1de61aadf31f")
    version("2.3.1", sha256="ee534dd31a811f7a759453567257d1e643f216d8d55a25c32d2fbfff8153a1ac")
    version("2.3.0", sha256="2595a5c401521f20a2734c4e5d54120996f8391f00bb62a57267d930bce95350")
    version("2.2.3", sha256="5e6c779ca8392864d436d88893461dcce783c3a8d46dcb2b2f2ee8ece3cc4538")
    version("2.2.2", sha256="fb4b5d26c5b983350f7ce8297b71176a86a69e91faf66e6ebb1e58538ad3bb51")
    version("2.2.1", sha256="e6a28e64236d729e598dbeaa02152219e67d0ac94d6ed22438606026a02e0f88")
    version("2.2.0", sha256="69cd836f87b8c53506c4f706f655d423270f5a563b76dc1cfa60fbc3184185a3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mkl", default=False, description="Build with MKL support")
    variant("jemalloc", default=False, description="Build with jemalloc as malloc support")
    variant("gcp", default=False, description="Build with Google Cloud Platform support")
    variant("hdfs", default=False, description="Build with Hadoop File System support")
    variant("aws", default=False, description="Build with Amazon AWS Platform support")
    variant("xla", default=sys.platform != "darwin", description="Build with XLA JIT support")
    variant("gdr", default=False, description="Build with GDR support")
    variant("verbs", default=False, description="Build with libverbs support")
    variant("ngraph", default=False, description="Build with Intel nGraph support")
    variant("opencl", default=False, description="Build with OpenCL SYCL support")
    variant("computecpp", default=False, description="Build with ComputeCPP support")
    variant(
        "tensorrt", default=False, description="Build with TensorRT support"
    )  # TODO: enable when TensorRT in Spack
    variant("cuda", default=sys.platform != "darwin", description="Build with CUDA support")
    variant(
        "nccl", default=sys.platform.startswith("linux"), description="Enable NVIDIA NCCL support"
    )
    variant("mpi", default=False, description="Build with MPI support")
    variant("android", default=False, description="Configure for Android builds")
    variant("ios", default=False, description="Build with iOS support (macOS only)")
    variant("monolithic", default=False, description="Static monolithic build")
    variant("numa", default=False, description="Build with NUMA support")
    variant(
        "dynamic_kernels",
        default=sys.platform.startswith("linux"),
        description="Build kernels into separate shared objects",
    )

    extends("python")

    with default_args(type="build"):
        # See .bazelversion
        depends_on("bazel@6.5.0", when="@2.16:")
        depends_on("bazel@6.1.0", when="@2.14:2.15")
        depends_on("bazel@5.3.0", when="@2.11:2.13")
        depends_on("bazel@5.1.1", when="@2.10")
        # See _TF_MIN_BAZEL_VERSION and _TF_MAX_BAZEL_VERSION in configure.py
        depends_on("bazel@4.2.2:5.99.0", when="@2.9")
        depends_on("bazel@4.2.1:4.99.0", when="@2.8")
        depends_on("bazel@3.7.2:4.99.0", when="@2.7")
        depends_on("bazel@3.7.2:3.99.0", when="@2.5:2.6")
        depends_on("bazel@3.1.0:3.99.0", when="@2.3:2.4")
        depends_on("bazel@2.0.0", when="@2.2")

        # tensorflow/tools/pip_package/build_pip_package.sh
        depends_on("patchelf", when="@2.13: platform=linux")
        # https://github.com/tensorflow/tensorflow/issues/60179#issuecomment-1491238631
        depends_on("coreutils", when="@2.13: platform=darwin")

        depends_on("swig")
        depends_on("py-pip")
        depends_on("py-wheel")

    with default_args(type=("build", "run")):
        # Python support based on wheel availability
        depends_on("python@3.9:3.12", when="@2.16:")
        depends_on("python@3.9:3.11", when="@2.14:2.15")
        depends_on("python@3.8:3.11", when="@2.12:2.13")
        depends_on("python@:3.10", when="@2.8:2.11")
        depends_on("python@:3.9", when="@2.5:2.7")
        depends_on("python@:3.8", when="@2.2:2.4")

        # Listed under REQUIRED_PACKAGES in tensorflow/tools/pip_package/setup.py
        depends_on("py-absl-py@1:", when="@2.9:")
        depends_on("py-absl-py@0.4:", when="@2.7:2.8")
        depends_on("py-absl-py@0.10:0", when="@2.4:2.6")
        depends_on("py-absl-py@0.7:", when="@:2.3")
        depends_on("py-astunparse@1.6:", when="@2.7:")
        depends_on("py-astunparse@1.6.3:1.6", when="@2.4:2.6")
        depends_on("py-astunparse@1.6.3", when="@2.2:2.3")
        depends_on("py-flatbuffers@24.3.25:", when="@2.17:")
        depends_on("py-flatbuffers@23.5.26:", when="@2.14:")
        depends_on("py-flatbuffers@23.1.21:", when="@2.13")
        depends_on("py-flatbuffers@2:", when="@2.10:2.12")
        depends_on("py-flatbuffers@1.12:1", when="@2.9")
        depends_on("py-flatbuffers@1.12:", when="@2.8")
        depends_on("py-flatbuffers@1.12:2", when="@2.7")
        depends_on("py-flatbuffers@1.12", when="@2.4:2.6")
        depends_on("py-gast@0.2.1:0.4,0.5.3:", when="@2.14:")
        depends_on("py-gast@0.2.1:0.4.0", when="@2.9:2.13")
        depends_on("py-gast@0.2.1:", when="@2.8")
        depends_on("py-gast@0.2.1:0.4", when="@2.7")
        depends_on("py-gast@0.4.0", when="@2.5:2.6")
        depends_on("py-gast@0.3.3", when="@2.2:2.4")
        depends_on("py-gast@0.2.2", when="@:2.1")
        depends_on("py-google-pasta@0.1.1:", when="@2.7:")
        depends_on("py-google-pasta@0.2:0", when="@2.4:2.6")
        depends_on("py-google-pasta@0.1.8:", when="@2.2:2.3")
        depends_on("py-google-pasta@0.1.6:", when="@:2.1")
        depends_on("py-h5py@3.10:", when="@2.16:")
        depends_on("py-h5py@2.9:", when="@2.7:2.15")
        depends_on("py-h5py@3.1", when="@2.5:2.6")
        depends_on("py-h5py@2.10", when="@2.2:2.4")
        depends_on("py-h5py@:2.10.0", when="@2.1.3:2.1")
        # propagate the mpi variant setting for h5py/hdf5 to avoid unexpected crashes
        depends_on("py-h5py+mpi", when="@2.1.3:+mpi")
        depends_on("py-h5py~mpi", when="@2.1.3:~mpi")
        depends_on("hdf5+mpi", when="@2.1.3:+mpi")
        depends_on("hdf5~mpi", when="@2.1.3:~mpi")
        depends_on("py-libclang@13:", when="@2.9:")
        depends_on("py-libclang@9.0.1:", when="@2.7:2.8")
        depends_on("py-ml-dtypes@0.3.1:0.4", when="@2.17:")
        depends_on("py-ml-dtypes@0.3.1:0.3", when="@2.15.1:2.16")
        depends_on("py-ml-dtypes@0.2", when="@2.15.0")
        depends_on("py-ml-dtypes@0.2.0", when="@2.14")
        depends_on("py-numpy@1.23.5:", when="@2.14:")
        depends_on("py-numpy@1.22:1.24.3", when="@2.13:")
        depends_on("py-numpy@1.22:1.23", when="@2.12")
        depends_on("py-numpy@1.20:", when="@2.8:2.11")
        depends_on("py-numpy@1.14.5:", when="@2.7")
        depends_on("py-numpy@1.19.2:1.19", when="@2.4:2.6")
        # https://github.com/tensorflow/tensorflow/issues/40688
        depends_on("py-numpy@1.16.0:1.18", when="@:2.3")
        # https://github.com/tensorflow/tensorflow/issues/67291
        depends_on("py-numpy@:1")
        depends_on("py-opt-einsum@2.3.2:", when="@:2.3,2.7:")
        depends_on("py-opt-einsum@3.3", when="@2.4:2.6")
        depends_on("py-packaging", when="@2.9:")
        depends_on("py-protobuf@3.20.3:4.20,4.21.6:4", when="@2.12:")
        depends_on("py-protobuf@3.9.2:", when="@2.3:2.11")
        depends_on("py-protobuf@3.8.0:", when="@:2.2")
        # https://github.com/protocolbuffers/protobuf/issues/10051
        # https://github.com/tensorflow/tensorflow/issues/56266
        depends_on("py-protobuf@:3.19", when="@:2.11")
        depends_on("py-requests@2.21:2", when="@2.16:")
        depends_on("py-requests")
        depends_on("py-setuptools")
        depends_on("py-six@1.12:", when="@:2.3,2.7:")
        depends_on("py-six@1.15", when="@2.4:2.6")
        depends_on("py-termcolor@1.1:", when="@:2.3,2.7:")
        depends_on("py-termcolor@1.1", when="@2.4:2.6")
        depends_on("py-typing-extensions@3.6.6:", when="@2.7:2.12,2.14:")
        depends_on("py-typing-extensions@3.6.6:4.5", when="@2.13")
        depends_on("py-typing-extensions@3.7.4:3.7", when="@2.4:2.6")
        depends_on("py-wrapt@1.11:", when="@2.7:2.11,2.13,2.16:")
        depends_on("py-wrapt@1.11:1.14", when="@2.12,2.14:2.15")
        depends_on("py-wrapt@1.12.1:1.12", when="@2.4:2.6")
        depends_on("py-wrapt@1.11.1:", when="@:2.3")

        # TODO: add packages for these dependencies
        # depends_on('py-tensorflow-io-gcs-filesystem@0.23.1:', when='@2.8:')
        # depends_on('py-tensorflow-io-gcs-filesystem@0.21:', when='@2.7')

        if sys.byteorder == "little":
            # Only builds correctly on little-endian machines
            depends_on("py-grpcio@1.24.3:1", when="@2.7:")
            depends_on("py-grpcio@1.37.0:1", when="@2.6")
            depends_on("py-grpcio@1.34", when="@2.5")
            depends_on("py-grpcio@1.32", when="@2.4")
            depends_on("py-grpcio@1.8.6:", when="@:2.3")

        for minor_ver in range(2, 18):
            depends_on("py-tensorboard@2.{}".format(minor_ver), when="@2.{}".format(minor_ver))

        # TODO: support circular run-time dependencies
        # depends_on('py-tensorflow-estimator')
        # depends_on('py-keras')

        # Historical dependencies
        depends_on("py-jax@0.3.15:", when="@2.12")
        depends_on("py-keras-preprocessing@1.1.1:", when="@2.7:2.10")
        depends_on("py-keras-preprocessing@1.1.2:1.1", when="@2.4:2.6")
        depends_on("py-keras-preprocessing@1.1.1:1.1", when="@2.3")
        depends_on("py-keras-preprocessing@1.1:", when="@2.2")
        depends_on("py-scipy@1.4.1", when="@2.2.0,2.3.0")
        depends_on("py-wheel@0.32:0", when="@2.7")
        depends_on("py-wheel@0.35:0", when="@2.4:2.6")
        depends_on("py-wheel@0.26:", when="@:2.3")

    # TODO: add packages for some of these dependencies
    depends_on("mkl", when="+mkl")
    depends_on("curl", when="+gcp")
    # depends_on('computecpp', when='+opencl+computecpp')
    # depends_on('trisycl',    when='+opencl~computepp')
    with when("+cuda"):
        # https://www.tensorflow.org/install/source#gpu
        depends_on("cuda@12.3:", when="@2.16:")
        depends_on("cuda@12.2:", when="@2.15:")
        depends_on("cuda@11.8:", when="@2.12:")
        depends_on("cuda@11.2:", when="@2.5:")
        depends_on("cuda@11.0:", when="@2.4:")
        depends_on("cuda@10.1:", when="@2.1:")

        depends_on("cuda@:11.7.0", when="@:2.9")
        depends_on("cuda@:11.4", when="@2.4:2.7")
        depends_on("cuda@:10.2", when="@:2.3")

        depends_on("cudnn@8.9:8", when="@2.15:")
        depends_on("cudnn@8.7:8", when="@2.14:")
        depends_on("cudnn@8.6:8", when="@2.12:")
        depends_on("cudnn@8.1:8", when="@2.5:")
        depends_on("cudnn@8.0:8", when="@2.4:")
        depends_on("cudnn@7.6:8", when="@2.1:")

        depends_on("cudnn@:7", when="@:2.2")
    # depends_on('tensorrt', when='+tensorrt')
    depends_on("nccl", when="+nccl+cuda")
    depends_on("mpi", when="+mpi")
    # depends_on('android-ndk@10:18', when='+android')
    # depends_on('android-sdk', when='+android')

    with when("+rocm"):
        for pkg_dep in rocm_dependencies:
            depends_on(f"{pkg_dep}@6.0:", when="@2.14:")
            depends_on(pkg_dep)

    # Check configure and configure.py to see when these variants are supported
    conflicts("+mkl", when="platform=darwin", msg="Darwin is not yet supported")
    conflicts(
        "+jemalloc",
        when="platform=darwin",
        msg="Currently jemalloc is only support on Linux platform",
    )
    conflicts("+opencl", when="platform=windows")
    conflicts("+computecpp", when="~opencl")
    conflicts(
        "+cuda",
        when="+rocm",
        msg="CUDA / ROCm are mututally exclusive. At most 1 GPU platform can be configured",
    )
    conflicts("+cuda", when="platform=darwin", msg="There is no GPU support for macOS")
    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify CUDA compute capabilities of your GPU, see https://developer.nvidia.com/cuda-gpus",
    )
    conflicts("cuda_arch=20", msg="TensorFlow only supports compute capabilities >= 3.5")
    conflicts("cuda_arch=30", msg="TensorFlow only supports compute capabilities >= 3.5")
    conflicts("cuda_arch=32", msg="TensorFlow only supports compute capabilities >= 3.5")
    conflicts("+tensorrt", when="~cuda")
    conflicts(
        "+tensorrt",
        when="platform=darwin",
        msg="Currently TensorRT is only supported on Linux platform",
    )
    conflicts("+nccl", when="~cuda~rocm")
    conflicts(
        "+nccl", when="platform=darwin", msg="Currently NCCL is only supported on Linux platform"
    )
    conflicts("+mpi", when="platform=windows")
    conflicts("+ios", when="platform=linux", msg="iOS support only available on macOS")
    # https://github.com/tensorflow/tensorflow/pull/45404
    conflicts("platform=darwin target=aarch64:", when="@:2.4")
    # https://github.com/tensorflow/tensorflow/pull/39225
    conflicts("target=aarch64:", when="@:2.2")
    conflicts(
        "~rocm",
        when="@2.7.4-rocm-enhanced,2.11.0-rocm-enhanced,2.14-rocm-enhanced,2.16.1-rocm-enhanced",
    )
    conflicts("+rocm", when="@:2.7.4-a,2.7.4.0:2.11.0-a,2.11.0.0:2.14-a,2.14-z:2.16.1-a,2.16.1-z:")
    # wheel 0.40 upgrades vendored packaging, trips over tensorflow-io-gcs-filesystem identifier
    conflicts("^py-wheel@0.40:", when="@2.11:2.13")

    # https://www.tensorflow.org/install/source#tested_build_configurations
    # https://github.com/tensorflow/tensorflow/issues/70199
    # (-mavx512fp16 exists in gcc@12:)
    conflicts("%gcc@13:", when="@:2.14")
    conflicts("%gcc@:11", when="@2.17:")
    conflicts("%gcc@:9.3.0", when="@2.9:")
    conflicts("%gcc@:7.3.0")

    # zlib is vendored and downloaded directly from zlib.org (or mirrors), but
    # old downloads are removed from that site immediately after a new release.
    # If the tf mirrors don't work, make sure the fallback is to something existing.
    patch(
        "https://github.com/tensorflow/tensorflow/commit/76b9fa22857148a562f3d9b5af6843402a93c15b.patch?full_index=1",
        sha256="f9e26c544da729cfd376dbd3b096030e3777d3592459add1f3c78b1b9828d493",
        when="@2.9:2.10.0",
    )

    # Version 2.10 produces an error related to cuBLAS:
    # E tensorflow/stream_executor/cuda/cuda_blas.cc:2981] Unable to register
    # cuBLAS factory: Attempting to register factory for plugin cuBLAS when one
    # has already been registered
    # See https://github.com/tensorflow/tensorflow/issues/57663
    # This is fixed for 2.11 but 2.10 needs the following patch.
    patch(
        "https://github.com/tensorflow/tensorflow/pull/56691.patch?full_index=1",
        sha256="d635ea6d6c1571505871d0caba3e2cd939ea0f4aff972095d552913a8109def3",
        when="@2.10",
    )

    # needed for protobuf 3.16+
    patch("example_parsing.patch", when="@:2.7 ^protobuf@3.16:")

    # allow linker to be found in PATH
    # https://github.com/tensorflow/tensorflow/issues/39263
    patch("null_linker_bin_path.patch", when="@2.5:")

    # Reset import order to that of 2.4. Part of
    # https://bugs.gentoo.org/800824#c3 From the patch:
    # When tensorflow and python protobuf use the same instance of libprotobuf,
    # pywrap_tensorflow must be imported before anything else that would import
    # protobuf definitions.
    patch("0008-Fix-protobuf-errors-when-using-system-protobuf.patch", when="@2.5:2.6")

    # see https://github.com/tensorflow/tensorflow/issues/62490
    # and https://github.com/abseil/abseil-cpp/issues/1665
    patch("absl_neon.patch", when="@2.16.1: target=aarch64:")

    # reverting change otherwise the c467913 commit patch won't apply
    patch(
        "https://github.com/ROCm/tensorflow-upstream/commit/fd6b0a4356c66f5f30cedbc62b24f18d9e32806f.patch?full_index=1",
        sha256="43f1519dfc618b4fb568f760d559c063234248fa12c47a35c1cf3b7114756424",
        when="@2.16.1-rocm-enhanced +rocm",
        reverse=True,
    )
    patch(
        "https://github.com/ROCm/tensorflow-upstream/commit/c467913bf4411ce2681391f37a9adf6031d23c2c.patch?full_index=1",
        sha256="82554a84d19d99180a6bec274c6106dd217361e809b446e2e4bc4b6b979bdf7a",
        when="@2.16.1-rocm-enhanced +rocm",
    )
    patch(
        "https://github.com/ROCm/tensorflow-upstream/commit/f4f4e8698b90755b0b5ea2d9da1933b0b988b111.patch?full_index=1",
        sha256="a4c0fd62a0af3ba113c8933fa531dd17fa6667e507202a144715cd87fbdaf476",
        when="@2.16.1-rocm-enhanced: +rocm",
    )
    patch(
        "https://github.com/ROCm/tensorflow-upstream/commit/8b7fcccb2914078737689347540cb79ace579bbb.patch?full_index=1",
        sha256="75a61a79ce3aae51fda920f677f4dc045374b20e25628626eb37ca19c3a3b4c4",
        when="@2.16.1-rocm-enhanced +rocm",
    )
    phases = ["configure", "build", "install"]

    def flag_handler(self, name, flags):
        spec = self.spec
        # ubuntu gcc has this workaround turned on by default in aarch64
        # and it causes issues with symbol relocation during link
        # note, archspec doesn't currently ever report cortex_a53!
        if (
            name == "ldflags"
            and spec.target.family == "aarch64"
            and "ubuntu" in spec.os
            and spec.compiler.name == "gcc"
            and "cortex_a53" not in spec.target.name
        ):
            flags.append("-mno-fix-cortex-a53-843419")

        return (flags, None, None)

    # https://www.tensorflow.org/install/source
    def setup_build_environment(self, env):
        spec = self.spec

        # Please specify the location of python
        env.set("PYTHON_BIN_PATH", python.path)

        # Please input the desired Python library path to use
        env.set("PYTHON_LIB_PATH", python_platlib)
        env.set("TF_PYTHON_VERSION", spec["python"].version.up_to(2))

        # Ensure swig is in PATH or set SWIG_PATH
        env.set("SWIG_PATH", spec["swig"].prefix.bin.swig)

        # Do you wish to build TensorFlow with MKL support?
        if "+mkl" in spec:
            env.set("TF_NEED_MKL", "1")

            # Do you wish to download MKL LIB from the web?
            env.set("TF_DOWNLOAD_MKL", "0")

            # Please specify the location where MKL is installed
            env.set("MKL_INSTALL_PATH", spec["mkl"].prefix)
        else:
            env.set("TF_NEED_MKL", "0")

        # Do you wish to build TensorFlow with jemalloc as malloc support?
        if "+jemalloc" in spec:
            env.set("TF_NEED_JEMALLOC", "1")
        else:
            env.set("TF_NEED_JEMALLOC", "0")

        # Do you wish to build TensorFlow with Google Cloud Platform support?
        if "+gcp" in spec:
            env.set("TF_NEED_GCP", "1")
        else:
            env.set("TF_NEED_GCP", "0")

        # Do you wish to build TensorFlow with Hadoop File System support?
        if "+hdfs" in spec:
            env.set("TF_NEED_HDFS", "1")
        else:
            env.set("TF_NEED_HDFS", "0")

        # Do you wish to build TensorFlow with Amazon AWS Platform support?
        if "+aws" in spec:
            env.set("TF_NEED_AWS", "1")
            env.set("TF_NEED_S3", "1")
        else:
            env.set("TF_NEED_AWS", "0")
            env.set("TF_NEED_S3", "0")

        # Do you wish to build TensorFlow with XLA JIT support?
        if "+xla" in spec:
            env.set("TF_ENABLE_XLA", "1")
        else:
            env.set("TF_ENABLE_XLA", "0")

        # Do you wish to build TensorFlow with GDR support?
        if "+gdr" in spec:
            env.set("TF_NEED_GDR", "1")
        else:
            env.set("TF_NEED_GDR", "0")

        # Do you wish to build TensorFlow with VERBS support?
        if "+verbs" in spec:
            env.set("TF_NEED_VERBS", "1")
        else:
            env.set("TF_NEED_VERBS", "0")

        # Do you wish to build TensorFlow with nGraph support?
        if "+ngraph" in spec:
            env.set("TF_NEED_NGRAPH", "1")
        else:
            env.set("TF_NEED_NGRAPH", "0")

        # Do you wish to build TensorFlow with OpenCL SYCL support?
        if "+opencl" in spec:
            env.set("TF_NEED_OPENCL_SYCL", "1")
            env.set("TF_NEED_OPENCL", "1")

            # Please specify which C++ compiler should be used as the host
            # C++ compiler
            env.set("HOST_CXX_COMPILER", spack_cxx)

            # Please specify which C compiler should be used as the host
            # C compiler
            env.set("HOST_C_COMPILER", spack_cc)

            # Do you wish to build TensorFlow with ComputeCPP support?
            if "+computecpp" in spec:
                env.set("TF_NEED_COMPUTECPP", "1")

                # Please specify the location where ComputeCpp is installed
                env.set("COMPUTECPP_TOOLKIT_PATH", spec["computecpp"].prefix)
            else:
                env.set("TF_NEED_COMPUTECPP", "0")

                # Please specify the location of the triSYCL include directory
                env.set("TRISYCL_INCLUDE_DIR", spec["trisycl"].prefix.include)
        else:
            env.set("TF_NEED_OPENCL_SYCL", "0")
            env.set("TF_NEED_OPENCL", "0")

        # Do you wish to build TensorFlow with ROCm support?
        if "+rocm" in spec:
            env.set("TF_NEED_ROCM", "1")
            env.set("TF_HIPBLASLT", "0")
            env.set("MIOPEN_PATH", spec["miopen-hip"].prefix)
            env.set("ROCTRACER_PATH", spec["roctracer-dev"].prefix)
            env.set("LLVM_PATH", spec["llvm-amdgpu"].prefix)
            for pkg_dep in rocm_dependencies:
                pkg_dep_cap = pkg_dep.upper().replace("-", "_")
                env.set(f"{pkg_dep_cap}_PATH", spec[pkg_dep].prefix)
            env.set("TF_ROCM_AMDGPU_TARGETS", ",".join(self.spec.variants["amdgpu_target"].value))
        else:
            env.set("TF_NEED_ROCM", "0")

        # Do you wish to build TensorFlow with CUDA support?
        if "+cuda" in spec:
            env.set("TF_NEED_CUDA", "1")

            # Do you want to use clang as CUDA compiler?
            env.set("TF_CUDA_CLANG", "0")

            # Please specify which gcc nvcc should use as the host compiler
            env.set("GCC_HOST_COMPILER_PATH", spack_cc)

            cuda_paths = [spec["cuda"].prefix, spec["cudnn"].prefix]

            # Do you wish to build TensorFlow with TensorRT support?
            if "+tensorrt" in spec:
                env.set("TF_NEED_TENSORRT", "1")

                cuda_paths.append(spec["tensorrt"].prefix)

                # Please specify the TensorRT version you want to use
                env.set("TF_TENSORRT_VERSION", spec["tensorrt"].version.up_to(1))

                # Please specify the location where TensorRT is installed
                env.set("TENSORRT_INSTALL_PATH", spec["tensorrt"].prefix)
            else:
                env.set("TF_NEED_TENSORRT", "0")
                env.unset("TF_TENSORRT_VERSION")

            # Please specify the CUDA SDK version you want to use
            env.set("TF_CUDA_VERSION", spec["cuda"].version.up_to(2))

            # Please specify the cuDNN version you want to use
            env.set("TF_CUDNN_VERSION", spec["cudnn"].version.up_to(1))

            if "+nccl" in spec:
                cuda_paths.append(spec["nccl"].prefix)

                # Please specify the locally installed NCCL version to use
                env.set("TF_NCCL_VERSION", spec["nccl"].version.up_to(1))

                # Please specify the location where NCCL is installed
                env.set("NCCL_INSTALL_PATH", spec["nccl"].prefix)
                env.set("NCCL_HDR_PATH", spec["nccl"].prefix.include)
            else:
                env.unset("TF_NCCL_VERSION")

            # Please specify the comma-separated list of base paths to
            # look for CUDA libraries and headers
            env.set("TF_CUDA_PATHS", ",".join(cuda_paths))

            # Please specify the location where CUDA toolkit is installed
            env.set("CUDA_TOOLKIT_PATH", spec["cuda"].prefix)

            # Please specify the location where CUDNN library is installed
            env.set("CUDNN_INSTALL_PATH", spec["cudnn"].prefix)

            # Please specify a list of comma-separated CUDA compute
            # capabilities you want to build with. You can find the compute
            # capability of your device at:
            # https://developer.nvidia.com/cuda-gpus.
            # Please note that each additional compute capability significantly
            # increases your build time and binary size, and that TensorFlow
            # only supports compute capabilities >= 3.5
            capabilities = CudaPackage.compute_capabilities(spec.variants["cuda_arch"].value)
            env.set("TF_CUDA_COMPUTE_CAPABILITIES", ",".join(capabilities))
        else:
            env.set("TF_NEED_CUDA", "0")

        # Do you want to use Clang to build TensorFlow?
        if "%clang" in spec:
            env.set("TF_NEED_CLANG", "1")
        else:
            env.set("TF_NEED_CLANG", "0")

        # Do you wish to download a fresh release of clang? (Experimental)
        env.set("TF_DOWNLOAD_CLANG", "0")

        # Do you wish to build TensorFlow with MPI support?
        if "+mpi" in spec:
            env.set("TF_NEED_MPI", "1")

            # Please specify the MPI toolkit folder
            env.set("MPI_HOME", spec["mpi"].prefix)
        else:
            env.set("TF_NEED_MPI", "0")
            env.unset("MPI_HOME")

        # Please specify optimization flags to use during compilation when
        # bazel option '--config=opt' is specified
        env.set("CC_OPT_FLAGS", optimization_flags(self.compiler, spec.target))

        # Would you like to interactively configure ./WORKSPACE for
        # Android builds?
        if "+android" in spec:
            env.set("TF_SET_ANDROID_WORKSPACE", "1")

            # Please specify the home path of the Android NDK to use
            env.set("ANDROID_NDK_HOME", spec["android-ndk"].prefix)
            env.set("ANDROID_NDK_API_LEVEL", spec["android-ndk"].version)

            # Please specify the home path of the Android SDK to use
            env.set("ANDROID_SDK_HOME", spec["android-sdk"].prefix)
            env.set("ANDROID_SDK_API_LEVEL", spec["android-sdk"].version)

            # Please specify the Android SDK API level to use
            env.set("ANDROID_API_LEVEL", spec["android-sdk"].version)

            # Please specify an Android build tools version to use
            env.set("ANDROID_BUILD_TOOLS_VERSION", spec["android-sdk"].version)
        else:
            env.set("TF_SET_ANDROID_WORKSPACE", "0")

        # Do you wish to build TensorFlow with iOS support?
        if "+ios" in spec:
            env.set("TF_CONFIGURE_IOS", "1")
        else:
            env.set("TF_CONFIGURE_IOS", "0")

        # set tmpdir to a non-NFS filesystem
        # (because bazel uses ~/.cache/bazel)
        # TODO: This should be checked for non-nfsy filesystem, but the current
        #       best idea for it is to check
        #           subprocess.call([
        #               'stat', '--file-system', '--format=%T', tmp_path
        #       ])
        #       to not be nfs. This is only valid for Linux and we'd like to
        #       stay at least also OSX compatible
        tmp_path = tempfile.mkdtemp(prefix="spack")
        env.set("TEST_TMPDIR", tmp_path)

    def configure(self, spec, prefix):
        # NOTE: configure script is interactive. If you set the appropriate
        # environment variables, this interactivity is skipped. If you don't,
        # Spack hangs during the configure phase. Use `spack build-env` to
        # determine which environment variables must be set for a particular
        # version.
        configure()

    @run_after("configure")
    def post_configure_fixes(self):
        spec = self.spec

        if spec.satisfies("@2.17:"):
            filter_file(
                "patchelf",
                spec["patchelf"].prefix.bin.patchelf,
                "tensorflow/tools/pip_package/build_pip_package.py",
                string=True,
            )

        # make sure xla is actually turned off
        if spec.satisfies("~xla"):
            filter_file(
                r"--define with_xla_support=true",
                r"--define with_xla_support=false",
                ".tf_configure.bazelrc",
            )

        if spec.satisfies("~android"):
            # env variable is somehow ignored -> brute force
            # TODO: find a better solution
            filter_file(r"if workspace_has_any_android_rule\(\)", r"if True", "configure.py")

        if spec.satisfies("~gcp"):
            # google cloud support seems to be installed on default, leading
            # to boringssl error manually set the flag to false to avoid
            # installing gcp support
            # https://github.com/tensorflow/tensorflow/issues/20677#issuecomment-404634519
            filter_file(
                r"--define with_gcp_support=true",
                r"--define with_gcp_support=false",
                ".tf_configure.bazelrc",
            )

        if spec.satisfies("~opencl"):
            # 1.8.0 and 1.9.0 aborts with numpy import error during python_api
            # generation somehow the wrong PYTHONPATH is used...
            # set --distinct_host_configuration=false as a workaround
            # https://github.com/tensorflow/tensorflow/issues/22395#issuecomment-431229451
            with open(".tf_configure.bazelrc", mode="a") as f:
                f.write("build --distinct_host_configuration=false\n")
                f.write('build --action_env PYTHONPATH="{0}"\n'.format(env["PYTHONPATH"]))

        if spec.satisfies("+cuda"):
            libs = spec["cuda"].libs.directories
            libs.extend(spec["cudnn"].libs.directories)
            if "+nccl" in spec:
                libs.extend(spec["nccl"].libs.directories)

            if "+tensorrt" in spec:
                libs.extend(spec["tensorrt"].libs.directories)
            slibs = ":".join(libs)

            with open(".tf_configure.bazelrc", mode="a") as f:
                f.write('build --action_env LD_LIBRARY_PATH="' + slibs + '"')

        if spec.satisfies("@2.16.1-rocm-enhanced +rocm"):
            if os.path.exists(spec["llvm-amdgpu"].prefix.bin.clang):
                filter_file(
                    "/usr/lib/llvm-17/bin/clang", spec["llvm-amdgpu"].prefix.bin.clang, ".bazelrc"
                )
            else:
                filter_file(
                    "/usr/lib/llvm-17/bin/clang",
                    spec["llvm-amdgpu"].prefix.llvm.bin.clang,
                    ".bazelrc",
                )

        filter_file("build:opt --copt=-march=native", "", ".tf_configure.bazelrc")
        filter_file("build:opt --host_copt=-march=native", "", ".tf_configure.bazelrc")

    def build(self, spec, prefix):
        # Bazel needs the directory to exist on install
        mkdirp(python_platlib)
        tmp_path = env["TEST_TMPDIR"]

        # https://docs.bazel.build/versions/master/command-line-reference.html
        args = [
            # Don't allow user or system .bazelrc to override build settings
            "--nohome_rc",
            "--nosystem_rc",
            # Bazel does not work properly on NFS, switch to /tmp
            "--output_user_root=" + tmp_path,
            "build",
            # Spack logs don't handle colored output well
            "--color=no",
            "--jobs={0}".format(make_jobs),
            "--config=opt",
            # Enable verbose output for failures
            "--verbose_failures",
        ]

        if spec.satisfies("^bazel@:3.5"):
            # removed in bazel 3.6
            args.append("--incompatible_no_support_tools_in_action_inputs=false")

        # See .bazelrc for when each config flag is supported
        if "+mkl" in spec:
            args.append("--config=mkl")

        if "+monolithic" in spec:
            args.append("--config=monolithic")

        if "+gdr" in spec:
            args.append("--config=gdr")

        if "+verbs" in spec:
            args.append("--config=verbs")

        if "+ngraph" in spec:
            args.append("--config=ngraph")

        if "+dynamic_kernels" in spec:
            args.append("--config=dynamic_kernels")

        if "+cuda" in spec:
            args.append("--config=cuda")

        if "+rocm" in spec:
            args.append("--config=rocm")

        if "~aws" in spec:
            args.append("--config=noaws")

        if "~gcp" in spec:
            args.append("--config=nogcp")

        if "~hdfs" in spec:
            args.append("--config=nohdfs")

        if "~nccl" in spec:
            args.append("--config=nonccl")

        # https://github.com/tensorflow/tensorflow/issues/63080
        if self.spec.satisfies("@2.14:"):
            args.append(f"--define=with_numa_support={'+numa' in spec}")
        else:
            if "+numa" in spec:
                args.append("--config=numa")

        args.append("--config=v2")

        # https://github.com/tensorflow/tensorflow/issues/63298
        if self.spec.satisfies("@2.17:"):
            args.append("//tensorflow/tools/pip_package:wheel")
        else:
            args.append("//tensorflow/tools/pip_package:build_pip_package")

        bazel(*args)

        if self.spec.satisfies("@:2.16"):
            build_pip_package = Executable(
                "bazel-bin/tensorflow/tools/pip_package/build_pip_package"
            )
            buildpath = join_path(self.stage.source_path, "spack-build")
            build_pip_package("--src", buildpath)

    def install(self, spec, prefix):
        tmp_path = env["TEST_TMPDIR"]
        if self.spec.satisfies("@2.17:"):
            buildpath = join_path(
                self.stage.source_path, "bazel-bin/tensorflow/tools/pip_package/wheel_house/"
            )
            with working_dir(buildpath):
                wheel = glob.glob("*.whl")[0]
                args = std_pip_args + ["--prefix=" + prefix, wheel]
                pip(*args)
        else:
            buildpath = join_path(self.stage.source_path, "spack-build")
            with working_dir(buildpath):
                args = std_pip_args + ["--prefix=" + prefix, "."]
                pip(*args)

        remove_linked_tree(tmp_path)
