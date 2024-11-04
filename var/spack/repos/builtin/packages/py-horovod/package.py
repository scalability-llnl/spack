# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyHorovod(PythonPackage, CudaPackage):
    """Horovod is a distributed deep learning training framework for
    TensorFlow, Keras, PyTorch, and Apache MXNet."""

    homepage = "https://github.com/horovod"
    git = "https://github.com/horovod/horovod.git"
    submodules = True

    license("Apache-2.0")
    maintainers("adamjstewart", "aweits", "tgaddair", "thomas-bouvier")

    version("master", branch="master")
    version("0.28.1", tag="v0.28.1", commit="1d217b59949986d025f6db93c49943fb6b6cc78f")
    version("0.28.0", tag="v0.28.0", commit="587d72004736209a93ebda8cec0acdb7870db583")
    version("0.27.0", tag="v0.27.0", commit="bfaca90d5cf66780a97d8799d4e1573855b64560")
    version("0.26.1", tag="v0.26.1", commit="34604870eabd9dc670c222deb1da9acc6b9d7c03")
    version("0.26.0", tag="v0.26.0", commit="c638dcec972750d4a75b229bc208cff9dc76b00a")
    version("0.25.0", tag="v0.25.0", commit="48e0affcba962831668cd1222866af2d632920c2")
    version("0.24.3", tag="v0.24.3", commit="a2d9e280c1210a8e364a7dc83ca6c2182fefa99d")
    version("0.24.2", tag="v0.24.2", commit="b4c191c8d05086842517b3836285a85c6f96ab22")
    version("0.24.1", tag="v0.24.1", commit="ebd135098571722469bb6290a6d098a9e1c96574")
    version("0.24.0", tag="v0.24.0", commit="b089df66a29d3ba6672073eef3d42714d9d3626b")
    version("0.23.0", tag="v0.23.0", commit="66ad6d5a3586decdac356e8ec95c204990bbc3d6")
    version("0.22.1", tag="v0.22.1", commit="93a2f2583ed63391a904aaeb03b602729be90f15")
    version("0.22.0", tag="v0.22.0", commit="3ff94801fbb4dbf6bc47c23888c93cad4887435f")
    version("0.21.3", tag="v0.21.3", commit="6916985c9df111f36864724e2611827f64de8e11")
    version("0.21.2", tag="v0.21.2", commit="c64b1d60c6bad7834f3315f12707f8ebf11c9c3d")
    version("0.21.1", tag="v0.21.1", commit="a9dea74abc1f0b8e81cd2b6dd9fe81e2c4244e39")
    version("0.21.0", tag="v0.21.0", commit="7d71874258fc8625ad8952defad0ea5b24531248")
    version("0.20.3", tag="v0.20.3", commit="b3c4d81327590c9064d544622b6250d9a19ce2c2")
    version("0.20.2", tag="v0.20.2", commit="cef4393eb980d4137bb91256da4dd847b7f44d1c")
    version("0.20.1", tag="v0.20.1", commit="4099c2b7f34f709f0db1c09f06b2594d7b4b9615")
    version("0.20.0", tag="v0.20.0", commit="396c1319876039ad8f5a56c007a020605ccb8277")
    version("0.19.5", tag="v0.19.5", commit="b52e4b3e6ce5b1b494b77052878a0aad05c2e3ce")
    version("0.19.4", tag="v0.19.4", commit="31f1f700b8fa6d3b6df284e291e302593fbb4fa3")
    version("0.19.3", tag="v0.19.3", commit="ad63bbe9da8b41d0940260a2dd6935fa0486505f")
    version("0.19.2", tag="v0.19.2", commit="f8fb21e0ceebbdc6ccc069c43239731223d2961d")
    version("0.19.1", tag="v0.19.1", commit="9ad69e78e83c34568743e8e97b1504c6c7af34c3")
    version("0.19.0", tag="v0.19.0", commit="1a805d9b20224069b294f361e47f5d9b55f426ff")
    version("0.18.2", tag="v0.18.2", commit="bb2134b427e0e0c5a83624d02fafa4f14de623d9")
    version("0.18.1", tag="v0.18.1", commit="0008191b3e61b5dfccddabe0129bbed7cd544c56")
    version("0.18.0", tag="v0.18.0", commit="a639de51e9a38d5c1f99f458c045aeaebe70351e")
    version("0.17.1", tag="v0.17.1", commit="399e70adc0f74184b5848d9a46b9b6ad67b5fe6d")
    version("0.17.0", tag="v0.17.0", commit="2fed0410774b480ad19057320be9027be06b309e")
    version("0.16.4", tag="v0.16.4", commit="2aac48c95c035bee7d68f9aff30e59319f46c21e")
    version("0.16.3", tag="v0.16.3", commit="30a2148784478415dc31d65a6aa08d237f364b42")
    version("0.16.2", tag="v0.16.2", commit="217774652eeccfcd60aa6e268dfd6b766d71b768")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    # https://github.com/horovod/horovod/blob/master/docs/install.rst
    variant(
        "frameworks",
        default="pytorch",
        description="Deep learning frameworks to build support for",
        values=("tensorflow", "keras", "pytorch", "mxnet", "spark", "ray"),
        multi=True,
    )
    variant(
        "controllers",
        default="mpi",
        description="Controllers to coordinate work between processes",
        values=("mpi", "gloo"),
        multi=True,
    )
    variant(
        "tensor_ops",
        default="nccl",
        description="Framework to use for GPU/CPU operations",
        values=("nccl", "mpi", "gloo", "ccl"),
        multi=False,
    )
    variant("cuda", default=True, description="Build with CUDA")
    variant("rocm", default=False, description="Build with ROCm")

    # Build dependencies
    depends_on("cmake@3.13:", type="build", when="@0.24:")
    depends_on("cmake@2.8.12:", type="build", when="@0.20:")
    depends_on("pkgconfig", type="build")

    # Required dependencies
    depends_on("python@3.6:", type=("build", "run"), when="@0.20:")
    depends_on("py-setuptools", type="build")
    depends_on("py-cloudpickle", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-six", type=("build", "run"), when="@:0.19")
    depends_on("py-packaging", type=("build", "run"), when="@0.26:")

    # Framework dependencies
    depends_on("py-tensorflow@1.1.0:", type=("build", "link", "run"), when="frameworks=tensorflow")
    depends_on(
        "py-tensorflow@1.15:", type=("build", "link", "run"), when="frameworks=tensorflow @0.20:"
    )
    depends_on("py-tensorflow-estimator", type=("build", "run"), when="frameworks=tensorflow")
    depends_on("py-keras@2.0.8,2.1.2:", type=("build", "run"), when="frameworks=keras")
    depends_on("py-torch@0.4.0:", type=("build", "link", "run"), when="frameworks=pytorch")
    depends_on("py-torch@1.2:", type=("build", "link", "run"), when="frameworks=pytorch @0.20:")
    depends_on("py-torch@1.5:", type=("build", "link", "run"), when="frameworks=pytorch @0.25:")
    depends_on("py-torchvision", type=("build", "run"), when="frameworks=pytorch @:0.19.1")
    depends_on("py-cffi@1.4.0:", type=("build", "run"), when="frameworks=pytorch")
    depends_on("py-pytorch-lightning", type=("build", "run"), when="frameworks=pytorch @0.22:0.23")
    depends_on(
        "py-pytorch-lightning@1.3.8", type=("build", "run"), when="frameworks=pytorch @0.24"
    )
    depends_on(
        "py-pytorch-lightning@1.3.8:1.5.9", type=("build", "run"), when="frameworks=pytorch @0.25:"
    )
    depends_on("mxnet@1.4.1:+python", type=("build", "link", "run"), when="frameworks=mxnet")
    depends_on("py-h5py@:2", type=("build", "run"), when="frameworks=spark @:0.23")
    depends_on("py-numpy", type=("build", "run"), when="frameworks=spark")
    depends_on("py-petastorm@0.8.2", type=("build", "run"), when="frameworks=spark @:0.19.1")
    depends_on(
        "py-petastorm@0.9.0:", type=("build", "run"), when="frameworks=spark @0.19.2:0.21.0"
    )
    depends_on("py-petastorm@0.9.8:", type=("build", "run"), when="frameworks=spark @0.21.1:")
    depends_on("py-petastorm@0.11:", type=("build", "run"), when="frameworks=spark @0.22:")
    depends_on("py-petastorm@0.12:", type=("build", "run"), when="frameworks=spark @0.26:")
    depends_on("py-pyarrow@0.15.0:10", type=("build", "run"), when="frameworks=spark")
    depends_on("py-pyspark@2.3.2:", type=("build", "run"), when="frameworks=spark ^python@:3.7")
    depends_on("py-pyspark@3.0.0:", type=("build", "run"), when="frameworks=spark ^python@3.8:")
    depends_on("py-fsspec", type=("build", "run"), when="frameworks=spark @0.22.1:0.24.1")
    depends_on("py-fsspec@2021.07:", type=("build", "run"), when="frameworks=spark @0.24.2:")
    depends_on("py-ray", type=("build", "run"), when="frameworks=ray")
    depends_on("py-aioredis@:1", type=("build", "run"), when="frameworks=ray @0.23:")
    depends_on("py-google-api-core@:2.8", type=("build", "run"), when="frameworks=ray @0.26:")

    # Controller dependencies
    depends_on("mpi", when="controllers=mpi")
    depends_on("cmake", type="build", when="controllers=gloo")
    depends_on("libuv@1.26:", when="controllers=gloo platform=darwin")

    # Tensor Operations dependencies
    depends_on("nccl@2:", when="tensor_ops=nccl")
    depends_on("mpi", when="tensor_ops=mpi")
    depends_on("cmake", type="build", when="tensor_ops=gloo")
    depends_on("libuv@1.26:", when="tensor_ops=gloo platform=darwin")
    depends_on("intel-oneapi-ccl", when="tensor_ops=ccl")

    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )
    conflicts(
        "tensor_ops=nccl", when="~cuda~rocm", msg="NCCL requires either CUDA or ROCm support"
    )
    conflicts("frameworks=ray", when="@:0.19", msg="Ray integration was added in 0.20.X")
    conflicts(
        "controllers=gloo", when="@:0.20.0 platform=darwin", msg="Gloo cannot be compiled on MacOS"
    )
    # https://github.com/horovod/horovod/issues/3996
    patch(
        "https://github.com/horovod/horovod/pull/3998.patch?full_index=1",
        sha256="9ecd4e8e315764afab20f2086e24baccf8178779a3c663196b24dc55a23a6aca",
        when="@0.25:0.28.1",
    )
    conflicts("^py-torch@2.1:", when="@:0.24")

    # https://github.com/horovod/horovod/pull/3957
    patch(
        "https://github.com/horovod/horovod/pull/3957.patch?full_index=1",
        sha256="9e22e312c0cbf224b4135ba70bd4fd2e4170d8316c996643e360112abaac8f93",
        when="@0.21:0.28.1",
    )
    conflicts("%gcc@13:", when="@:0.20")

    # https://github.com/horovod/horovod/pull/1835
    patch("fma.patch", when="@0.19.0:0.19.1")

    # Patch vendored copy of eigen to fix build on aarch64
    # https://github.com/horovod/horovod/issues/3605
    # https://gitlab.com/libeigen/eigen/-/commit/fd1dcb6b45a2c797ad4c4d6cc7678ee70763b4ed
    patch("eigen.patch", when="@0.21:0.25 target=aarch64:")

    @property
    def import_modules(self):
        modules = [
            "horovod",
            "horovod.runner",
            "horovod.runner.util",
            "horovod.runner.elastic",
            "horovod.runner.driver",
            "horovod.runner.common",
            "horovod.runner.common.util",
            "horovod.runner.common.service",
            "horovod.runner.http",
            "horovod.runner.task",
            "horovod.common",
        ]

        if "frameworks=tensorflow" in self.spec:
            modules.append("horovod.tensorflow")

        if "frameworks=pytorch" in self.spec:
            modules.extend(["horovod.torch", "horovod.torch.elastic"])

        if "frameworks=mxnet" in self.spec:
            modules.append("horovod.mxnet")

        if "frameworks=keras" in self.spec:
            modules.extend(["horovod.keras", "horovod._keras"])

        if "frameworks=spark" in self.spec:
            modules.extend(
                [
                    "horovod.spark",
                    "horovod.spark.driver",
                    "horovod.spark.common",
                    "horovod.spark.task",
                ]
            )

        if "frameworks=ray" in self.spec:
            modules.append("horovod.ray")

        if "frameworks=tensorflow,keras" in self.spec:
            modules.append("horovod.tensorflow.keras")

        if "frameworks=spark,pytorch" in self.spec:
            modules.append("horovod.spark.torch")

        if "frameworks=spark,keras" in self.spec:
            modules.append("horovod.spark.keras")

        return modules

    def setup_build_environment(self, env):
        # https://github.com/horovod/horovod/blob/master/docs/install.rst#environment-variables

        # Build system
        env.set("PKG_CONFIG_EXECUTABLE", self.spec["pkgconfig"].prefix.bin.join("pkg-config"))
        if "cmake" in self.spec:
            env.set("HOROVOD_CMAKE", self.spec["cmake"].command.path)
        env.set("MAKEFLAGS", "-j{0}".format(make_jobs))

        # Frameworks
        if "frameworks=tensorflow" in self.spec:
            env.set("HOROVOD_WITH_TENSORFLOW", 1)
        else:
            env.set("HOROVOD_WITHOUT_TENSORFLOW", 1)
        if "frameworks=pytorch" in self.spec:
            env.set("HOROVOD_WITH_PYTORCH", 1)
        else:
            env.set("HOROVOD_WITHOUT_PYTORCH", 1)
        if "frameworks=mxnet" in self.spec:
            env.set("HOROVOD_WITH_MXNET", 1)
            env.set("MXNET_INCLUDE_PATH", self.spec["mxnet"].prefix.include)
            env.set("MXNET_LIBRARY_PATH", join_path(self.spec["mxnet"].libs[0]))
        else:
            env.set("HOROVOD_WITHOUT_MXNET", 1)

        # Controllers
        if "controllers=mpi" in self.spec or "tensor_ops=mpi" in self.spec:
            env.set("HOROVOD_WITH_MPI", 1)
        else:
            env.set("HOROVOD_WITHOUT_MPI", 1)
        if "controllers=gloo" in self.spec or "tensor_ops=gloo" in self.spec:
            env.set("HOROVOD_WITH_GLOO", 1)
        else:
            env.set("HOROVOD_WITHOUT_GLOO", 1)

        # Tensor Operations
        if "tensor_ops=nccl" in self.spec:
            env.set("HOROVOD_GPU_ALLREDUCE", "NCCL")
            env.set("HOROVOD_GPU_ALLGATHER", "NCCL")
            env.set("HOROVOD_GPU_BROADCAST", "NCCL")

            env.set("HOROVOD_NCCL_HOME", self.spec["nccl"].prefix)
            env.set("HOROVOD_NCCL_INCLUDE", self.spec["nccl"].headers.directories[0])
            env.set("HOROVOD_NCCL_LIB", self.spec["nccl"].libs.directories[0])

            if "+cuda" in self.spec:
                env.set("HOROVOD_GPU", "CUDA")

                env.set("HOROVOD_CUDA_HOME", self.spec["cuda"].prefix)
                cuda_cc_list = ",".join(self.spec.variants["cuda_arch"].value)
                env.set("HOROVOD_BUILD_CUDA_CC_LIST", cuda_cc_list)
                env.set("HOROVOD_CUDA_INCLUDE", self.spec["cuda"].headers.directories[0])
                env.set("HOROVOD_CUDA_LIB", self.spec["cuda"].libs.directories[0])
            elif "+rocm" in self.spec:
                env.set("HOROVOD_GPU", "ROCM")
                # env.set('HOROVOD_ROCM_HOME', self.spec['rocm'].prefix)
        else:
            env.set("HOROVOD_CPU_OPERATIONS", self.spec.variants["tensor_ops"].value.upper())

    def test_check_build(self):
        """run horovodrun --check-build"""
        horovodrun = which(self.prefix.bin.horovodrun)
        horovodrun("--check-build")
