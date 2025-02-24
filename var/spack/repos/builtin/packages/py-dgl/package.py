# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class PyDgl(CMakePackage, PythonExtension, CudaPackage):
    """Deep Graph Library (DGL).

    DGL is an easy-to-use, high performance and scalable Python package for
    deep learning on graphs. DGL is framework agnostic, meaning if a deep graph
    model is a component of an end-to-end application, the rest of the logics
    can be implemented in any major frameworks, such as PyTorch, Apache MXNet
    or TensorFlow."""

    homepage = "https://www.dgl.ai/"
    git = "https://github.com/dmlc/dgl.git"

    maintainers("adamjstewart", "meyersbs")

    license("Apache-2.0")

    version("master", branch="master", submodules=True)
    version(
        "1.0.1", tag="1.0.1", commit="cc2e9933f309f585fae90965ab61ad11ac1eecd5", submodules=True
    )
    version(
        "0.4.3", tag="0.4.3", commit="e1d90f9b5eeee7359a6b4f5edca7473a497984ba", submodules=True
    )
    version(
        "0.4.2", tag="0.4.2", commit="55e056fbae8f25f3da4aab0a0d864d72c2a445ff", submodules=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("cuda", default=True, description="Build with CUDA")
    variant("openmp", default=True, description="Build with OpenMP")
    variant(
        "backend",
        default="pytorch",
        description="Default backend",
        values=["pytorch", "mxnet", "tensorflow"],
        multi=False,
    )

    depends_on("cmake@3.5:", type="build")
    depends_on("llvm-openmp", when="%apple-clang +openmp")

    # Python dependencies
    # See python/setup.py
    extends("python")
    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-numpy@1.14.0:", type=("build", "run"))
    depends_on("py-scipy@1.1.0:", type=("build", "run"))
    depends_on("py-networkx@2.1:", type=("build", "run"))
    depends_on("py-requests@2.19.0:", when="@0.4.3:", type=("build", "run"))
    depends_on("py-tqdm", when="@1.0.1:", type=("build", "run"))
    depends_on("py-psutil@5.8.0:", when="@1.0.1:", type=("build", "run"))

    # Backends
    # See https://docs.dgl.ai/install/index.html#working-with-different-backends
    depends_on("py-torch@1.12.0:", when="@1.0.1: backend=pytorch", type="run")
    depends_on("py-torch@1.2.0:", when="@0.4.3: backend=pytorch", type="run")
    depends_on("py-torch@0.4.1:", when="backend=pytorch", type="run")
    depends_on("mxnet@1.6.0:", when="@1.0.1: backend=mxnet", type="run")
    depends_on("mxnet@1.5.1:", when="@0.4.3: backend=mxnet", type="run")
    depends_on("mxnet@1.5.0:", when="backend=mxnet", type="run")
    depends_on("py-tensorflow@2.3:", when="@1.0.1: backend=tensorflow", type="run")
    depends_on("py-tensorflow@2.1:", when="@0.4.3: backend=tensorflow", type="run")
    depends_on("py-tensorflow@2.0:", when="backend=tensorflow", type="run")

    # Cuda
    # See https://github.com/dmlc/dgl/issues/3083
    depends_on("cuda@:10", when="@:0.4 +cuda", type=("build", "run"))
    # From error: "Your installed Caffe2 version uses cuDNN but I cannot find the
    # cuDNN libraries.  Please set the proper cuDNN prefixes and / or install cuDNN."
    depends_on("cudnn", when="+cuda", type=("build", "run"))

    patch(
        "https://patch-diff.githubusercontent.com/raw/dmlc/dgl/pull/5434.patch?full_index=1",
        sha256="8c5f14784637a9bb3dd55e6104715d4a35b4e6594c99884aa19e67bc0544e91a",
        when="@1.0.1",
    )

    build_directory = "build"

    # https://docs.dgl.ai/install/index.html#install-from-source
    def cmake_args(self):
        args = []

        if "+cuda" in self.spec:
            args.append("-DUSE_CUDA=ON")
            # Prevent defaulting to old compute_ and sm_ despite defining cuda_arch
            args.append("-DCUDA_ARCH_NAME=Manual")
            cuda_arch_list = " ".join(list(self.spec.variants["cuda_arch"].value))
            args.append("-DCUDA_ARCH_BIN={0}".format(cuda_arch_list))
            args.append("_DCUDA_ARCH_PTX={0}".format(cuda_arch_list))
        else:
            args.append("-DUSE_CUDA=OFF")

        if "+openmp" in self.spec:
            args.append("-DUSE_OPENMP=ON")

            if self.spec.satisfies("%apple-clang"):
                args.extend(
                    [
                        "-DOpenMP_CXX_FLAGS=" + self.spec["llvm-openmp"].headers.include_flags,
                        "-DOpenMP_CXX_LIB_NAMES=" + self.spec["llvm-openmp"].libs.names[0],
                        "-DOpenMP_C_FLAGS=" + self.spec["llvm-openmp"].headers.include_flags,
                        "-DOpenMP_C_LIB_NAMES=" + self.spec["llvm-openmp"].libs.names[0],
                        "-DOpenMP_omp_LIBRARY=" + self.spec["llvm-openmp"].libs[0],
                    ]
                )
        else:
            args.append("-DUSE_OPENMP=OFF")

        if self.run_tests:
            args.append("-DBUILD_CPP_TEST=ON")
        else:
            args.append("-DBUILD_CPP_TEST=OFF")

        return args

    def install(self, spec, prefix):
        with working_dir("python"):
            pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")

        # Older versions do not install correctly
        if self.spec.satisfies("@:0.4.3"):
            # Work around installation bug: https://github.com/dmlc/dgl/issues/1379
            install_tree(prefix.dgl, prefix.lib)

    def setup_run_environment(self, env):
        # https://docs.dgl.ai/install/backend.html
        backend = self.spec.variants["backend"].value
        env.set("DGLBACKEND", backend)

    @property
    def import_modules(self):
        modules = [
            "dgl",
            "dgl.nn",
            "dgl.runtime",
            "dgl.backend",
            "dgl.function",
            "dgl.contrib",
            "dgl._ffi",
            "dgl.data",
            "dgl.runtime.ir",
            "dgl.backend.numpy",
            "dgl.contrib.sampling",
            "dgl._ffi._cy2",
            "dgl._ffi._cy3",
            "dgl._ffi._ctypes",
        ]

        if "backend=pytorch" in self.spec:
            modules.extend(["dgl.nn.pytorch", "dgl.nn.pytorch.conv", "dgl.backend.pytorch"])
        elif "backend=mxnet" in self.spec:
            modules.extend(["dgl.nn.mxnet", "dgl.nn.mxnet.conv", "dgl.backend.mxnet"])
        elif "backend=tensorflow" in self.spec:
            modules.extend(
                ["dgl.nn.tensorflow", "dgl.nn.tensorflow.conv", "dgl.backend.tensorflow"]
            )

        return modules
