# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class Mxnet(CMakePackage, CudaPackage, PythonExtension):
    """MXNet is a deep learning framework designed for both efficiency and flexibility."""

    homepage = "https://mxnet.apache.org"
    url = "https://archive.apache.org/dist/incubator/mxnet/1.7.0/apache-mxnet-src-1.7.0-incubating.tar.gz"
    list_url = "https://mxnet.apache.org/get_started/download"
    git = "https://github.com/apache/mxnet.git"

    license("Apache-2.0")

    version("master", branch="master", submodules=True)
    version("1.9.1", sha256="11ea61328174d8c29b96f341977e03deb0bf4b0c37ace658f93e38d9eb8c9322")
    version("1.9.0", sha256="a2a99cf604d57094269cacdfc4066492b2dc886593ee02b862e034f6180f712d")
    version("1.8.0", sha256="95aff985895aba409c08d5514510ae38b88490cfb6281ab3a5ff0f5826c8db54")
    version("1.7.0", sha256="1d20c9be7d16ccb4e830e9ee3406796efaf96b0d93414d676337b64bc59ced18")
    version("1.6.0", sha256="01eb06069c90f33469c7354946261b0a94824bbaf819fd5d5a7318e8ee596def")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "build_type",
        default="Distribution",
        description="CMake build type",
        values=("Distribution", "Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )
    variant("cuda", default=True, description="Enable CUDA support")
    variant("cudnn", default=True, description="Build with cudnn support")
    variant("nccl", default=False, description="Use NVidia NCCL with CUDA")
    variant("opencv", default=True, description="Enable OpenCV support")
    variant("openmp", default=False, description="Enable OpenMP support")
    variant("lapack", default=True, description="Build with lapack support")
    variant("mkldnn", default=False, description="Build with MKL-DNN support")
    variant("python", default=True, description="Install python bindings")

    generator("ninja")
    depends_on("cmake@3.13:", type="build")
    depends_on("pkgconfig", when="@1.6.0", type="build")
    depends_on("blas")
    depends_on("cuda", when="+cuda")
    depends_on("cudnn", when="+cudnn")
    depends_on("nccl", when="+nccl")
    depends_on("opencv+highgui+imgproc+imgcodecs", when="+opencv")
    depends_on("lapack", when="+lapack")
    depends_on("onednn", when="+mkldnn")

    # python/setup.py
    extends("python", when="+python")
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-wheel", when="+python", type="build")
    depends_on("py-setuptools", when="+python", type="build")
    depends_on("py-cython", when="+python", type="build")
    depends_on("py-numpy@1.17:", when="@2.0.0:+python", type=("build", "run"))
    depends_on("py-numpy@1.16.1:1", when="@1.6:1.8.0+python", type=("build", "run"))
    depends_on("py-requests@2.20.0:2", when="@1.6:+python", type=("build", "run"))
    depends_on("py-graphviz@0.8.1:0.8", when="+python", type=("build", "run"))

    conflicts("+cudnn", when="~cuda")
    conflicts("+nccl", when="~cuda")
    conflicts("platform=darwin target=aarch64:", when="@:1")

    patch("openblas-1.7.0.patch", when="@1.7.0:1")
    patch("openblas-1.6.0.patch", when="@1.6.0")
    patch("cmake_cuda_flags.patch", when="@1.6:1.7")
    patch("parallell_shuffle.patch", when="@1.6.0")

    # python/setup.py assumes libs can be found in build directory
    build_directory = "build"

    def setup_run_environment(self, env):
        env.set("MXNET_LIBRARY_PATH", self.spec["mxnet"].libs[0])

        if self.spec.satisfies("+nccl ^nccl@2.1:"):
            env.set("NCCL_LAUNCH_MODE", "PARALLEL")

    def cmake_args(self):
        # https://mxnet.apache.org/get_started/build_from_source
        args = [
            self.define_from_variant("USE_CUDA", "cuda"),
            self.define_from_variant("USE_CUDNN", "cudnn"),
            self.define_from_variant("USE_OPENCV", "opencv"),
            self.define_from_variant("USE_OPENMP", "openmp"),
            self.define_from_variant("USE_LAPACK", "lapack"),
            self.define("BLAS_LIBRARIES", self.spec["blas"].libs[0]),
        ]

        if self.spec.satisfies("@:1"):
            args.append(self.define_from_variant("USE_MKLDNN", "mkldnn"))
        elif self.spec.satisfies("@2:"):
            args.append(self.define_from_variant("USE_ONEDNN", "mkldnn"))
            args.append(self.define("USE_CUTENSOR", False))

        if "+cuda" in self.spec:
            if "cuda_arch=none" not in self.spec:
                cuda_arch = ";".join(
                    "{0:.1f}".format(float(i) / 10.0)
                    for i in self.spec.variants["cuda_arch"].value
                )
                args.append(self.define("MXNET_CUDA_ARCH", cuda_arch))

            args.extend(
                [
                    self.define_from_variant("USE_NCCL", "nccl"),
                    # Workaround for bug in GCC 8+ and CUDA 10 on PowerPC
                    self.define("CMAKE_CUDA_FLAGS", self.compiler.cxx11_flag),
                    # https://github.com/apache/mxnet/issues/21193
                    # https://github.com/spack/spack/issues/36922
                    self.define(
                        "CMAKE_CXX_FLAGS",
                        "-L" + join_path(self.spec["cuda"].libs.directories[0], "stubs"),
                    ),
                ]
            )

        return args

    @run_after("install")
    def install_python(self):
        if "+python" in self.spec:
            with working_dir("python"):
                pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")
