# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.build_systems.python import PythonPipBuilder
from spack.package import *

rocm_dependencies = [
    "hsa-rocr-dev",
    "hip",
    "rccl",
    "rocprim",
    "hipcub",
    "rocthrust",
    "roctracer-dev",
    "rocrand",
    "hipsparse",
    "hipfft",
    "rocfft",
    "rocblas",
    "miopen-hip",
    "rocminfo",
]


class PyJaxlib(PythonPackage, CudaPackage, ROCmPackage):
    """XLA library for Jax.

    jaxlib is the support library for JAX. While JAX itself is a pure Python package,
    jaxlib contains the binary (C/C++) parts of the library, including Python bindings,
    the XLA compiler, the PJRT runtime, and a handful of handwritten kernels.
    """

    homepage = "https://github.com/jax-ml/jax"
    url = "https://github.com/jax-ml/jax/archive/refs/tags/jax-v0.4.34.tar.gz"

    license("Apache-2.0")
    maintainers("adamjstewart", "jonas-eschle")

    # version("0.5.0", sha256="04cc2eeb2e7ce1916674cea03a7d75a59d583ddb779d5104e103a2798a283ce9")
    # version("0.4.38", sha256="ca1e63c488d505b9c92e81499e8b06cc1977319c50d64a0e58adbd2dae1a625c")
    # version("0.4.37", sha256="17a8444a931f26edda8ccbc921ab71c6bf46857287b1db186deebd357e526870")
    # version("0.4.36", sha256="442bfdf491b509995aa160361e23a9db488d5b97c87e6648cc733501b06eda77")
    # version("0.4.35", sha256="65e086708ae56670676b7b2340ad82b901d8c9993d1241a839c8990bdb8d6212")
    # version("0.4.34", sha256="d3a75ad667772309ade81350fa70c4a78028a920028800282e46d8383c0ee6bb")
    # version("0.4.33", sha256="122a806e80fc1cd7d8ffaf9620701f2cb8e4fe22271c2cec53a9c60b30bd4c31")
    # version("0.4.32", sha256="3fe36d596e4d640443c0a5c533845c74fbc4341e024d9bb1cd75cb49f5f419c2")
    version("0.4.31", sha256="022ea1347f9b21cbea31410b3d650d976ea4452a48ea7317a5f91c238031bf94")
    version("0.4.30", sha256="0ef9635c734d9bbb44fcc87df4f1c3ccce1cfcfd243572c80d36fcdf826fe1e6")
    version("0.4.29", sha256="3a8005f4f62d35a5aad7e3dbd596890b47c81cc6e34fcfe3dcb93b3ca7cb1246")
    version("0.4.28", sha256="4dd11577d4ba5a095fbc35258ddd4e4c020829ed6e6afd498c9e38ccbcdfe20b")
    version("0.4.27", sha256="c2c82cd9ad3b395d5cbc0affa26a2938e52677a69ca8f0b9ef9922a52cac4f0c")
    version("0.4.26", sha256="ddc14da1eaa34f23430d40ad9b9585088575cac439a2fa1c6833a247e1b221fd")
    version("0.4.25", sha256="fc1197c401924942eb14185a61688d0c476e3e81ff71f9dc95e620b57c06eec8")
    version("0.4.24", sha256="c4e6963c2c36f634a9a1765e476a1ed4e6c4a7954465ebf72e29f344c28ddc28")
    version("0.4.23", sha256="e4c06d62ba54becffd91abc862627b8b11b79c5a77366af8843b819665b6d568")
    version("0.4.21", sha256="8d57f66d00b9c0b824b1eff84adda5b765a412b3f316ef7c773632d1edbf9477")
    version("0.4.20", sha256="058410d2bc12f7562c7b01e0c8cd587cb68059c12f78bc945055e5ddc445f5fd")
    version("0.4.19", sha256="51242b217a1f82474e42d24f09ed5dedff951eeb4579c6e49e706d1adfd6949d")
    version("0.4.16", sha256="85c8bc050abe0a2cf62e8cfc7edb4904dd3807924b5714ec6277f291c576b5ca")
    version("0.4.14", sha256="9f309476a8f6337717b059b8d10b5859b4134c30cf8f1220bb70379b5e2744a4")
    version("0.4.11", sha256="bdfc45f33970beba5caf28d061668a4863f05994deea26791db50ea605fc2e36")
    version("0.4.7", sha256="0578d5dd5035b5225cadb6a62ca5f93dd76b70292268502fc01a0fd9ca7001d0")
    version("0.4.6", sha256="2c9bf8962815bc54ef524e33dc8eda9d165d379fe87e0df210f316adead27787")
    version("0.4.4", sha256="881f402c7983b56b185e182d5315dd64c9f5320be96213d0415996ece1826806")
    version("0.4.3", sha256="2104735dc22be2b105e5517bd5bc6ae97f40e8e9e54928cac1585c6112a3d910")

    variant("cuda", default=True, description="Build with CUDA enabled")
    variant("nccl", default=True, description="Build with NCCL enabled", when="+cuda")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # docs/installation.md (Compatible with)
    with when("+cuda"):
        depends_on("cuda@12.1:", when="@0.4.26:")
        depends_on("cuda@11.8:", when="@0.4.11:")
        depends_on("cuda@11.4:", when="@0.4.0:0.4.7")
        depends_on("cudnn@9.1:9", when="@0.4.31:")
        depends_on("cudnn@9", when="@0.4.29:0.4.30")
        depends_on("cudnn@8.9:8", when="@0.4.26:0.4.28")
        depends_on("cudnn@8.8:8", when="@0.4.11:0.4.25")
        depends_on("cudnn@8.2:8", when="@0.4:0.4.7")

    with when("+nccl"):
        depends_on("nccl@2.18:", when="@0.4.26:")
        depends_on("nccl@2.16:", when="@0.4.18:")
        depends_on("nccl")

    with when("+rocm"):
        for pkg_dep in rocm_dependencies:
            depends_on(f"{pkg_dep}@6:", when="@0.4.28:")
            depends_on(pkg_dep)
        depends_on("py-nanobind")

    with default_args(type="build"):
        # .bazelversion
        depends_on("bazel@6.5.0", when="@0.4.28:")
        depends_on("bazel@6.1.2", when="@0.4.11:0.4.27")
        depends_on("bazel@5.1.1", when="@0.3.7:0.4.10")

        # jaxlib/setup.py
        depends_on("py-setuptools")

        # build/build.py
        depends_on("py-build", when="@0.4.14:")

    with default_args(type=("build", "run")):
        # Based on PyPI wheels
        depends_on("python@3.10:", when="@0.4.31:")
        depends_on("python@3.9:", when="@0.4.14:")
        depends_on("python@3.8:", when="@0.4.6:")
        depends_on("python@:3.13")
        depends_on("python@:3.12", when="@:0.4.33")
        depends_on("python@:3.11", when="@:0.4.16")

        # jaxlib/setup.py
        depends_on("py-scipy@1.11.1:", when="@0.5:")
        depends_on("py-scipy@1.10:", when="@0.4.31:")
        depends_on("py-scipy@1.9:", when="@0.4.19:")
        depends_on("py-scipy@1.7:", when="@0.4.7:")
        depends_on("py-scipy@1.5:")
        depends_on("py-numpy@1.25:", when="@0.5:")
        depends_on("py-numpy@1.24:", when="@0.4.31:")
        depends_on("py-numpy@1.22:", when="@0.4.14:")
        depends_on("py-numpy@1.21:", when="@0.4.7:")
        depends_on("py-numpy@1.20:", when="@0.3:")
        # https://github.com/google/jax/issues/19246
        depends_on("py-numpy@:1", when="@:0.4.25")
        depends_on("py-ml-dtypes@0.4:", when="@0.4.29")
        depends_on("py-ml-dtypes@0.2:", when="@0.4.14:")
        depends_on("py-ml-dtypes@0.1:", when="@0.4.9:")
        depends_on("py-ml-dtypes@0.0.3:", when="@0.4.7:")

    patch(
        "https://github.com/jax-ml/jax/commit/f62af6457a6cc575a7b1ada08d541f0dd0eb5765.patch?full_index=1",
        sha256="d3b7ea2cfeba927e40a11f07e4cbf80939f7fe69448c9eb55231a93bd64e5c02",
        when="@0.4.36:0.4.38",
    )
    patch(
        "https://github.com/jax-ml/jax/pull/25473.patch?full_index=1",
        sha256="9d6977bc32046600bf8b15863251283fe7546896340367a7f14e3dccf418b4fe",
        when="@0.4.36:0.4.37",
    )
    patch(
        "https://github.com/google/jax/pull/20101.patch?full_index=1",
        sha256="4dfb9f32d4eeb0a0fb3a6f4124c4170e3fe49511f1b768cd634c78d489962275",
        when="@:0.4.25",
    )

    # Might be able to be applied to earlier versions
    # backports https://github.com/abseil/abseil-cpp/pull/1732
    patch("jaxxlatsl.patch", when="@0.4.28:0.4.32 target=aarch64:")

    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )

    # https://github.com/google/jax/issues/19992
    conflicts("@0.4.4:", when="target=ppc64le:")

    # Fails to build with freshly released CUDA (#48708).
    conflicts("^cuda@12.8:", when="@:0.4.31")

    def url_for_version(self, version):
        url = "https://github.com/jax-ml/jax/archive/refs/tags/{}-v{}.tar.gz"
        if version >= Version("0.4.33"):
            name = "jax"
        else:
            name = "jaxlib"
        return url.format(name, version)

    def install(self, spec, prefix):
        # https://jax.readthedocs.io/en/latest/developer.html
        args = ["build/build.py"]

        if spec.satisfies("@0.4.36:"):
            args.append("build")

            if spec.satisfies("+cuda"):
                args.append("--wheels=jaxlib,jax-cuda-plugin,jax-cuda-pjrt")
            elif spec.satisfies("+rocm"):
                args.append("--wheels=jaxlib,jax-rocm-plugin,jax-rocm-pjrt")
            else:
                args.append("--wheels=jaxlib")

        if spec.satisfies("@0.4.32:"):
            if spec.satisfies("%clang"):
                args.append("--use_clang=true")
            else:
                args.append("--use_clang=false")

        if "+cuda" in spec:
            capabilities = CudaPackage.compute_capabilities(spec.variants["cuda_arch"].value)
            args.append(f"--cuda_compute_capabilities={','.join(capabilities)}")
            if spec.satisfies("@:0.4.35"):
                args.append("--enable_cuda")
            if spec.satisfies("@0.4.32:"):
                args.extend(
                    [
                        f"--bazel_options=--repo_env=LOCAL_CUDA_PATH={spec['cuda'].prefix}",
                        f"--bazel_options=--repo_env=LOCAL_CUDNN_PATH={spec['cudnn'].prefix}",
                    ]
                )
            else:
                args.extend(
                    [f"--cuda_path={spec['cuda'].prefix}", f"--cudnn_path={spec['cudnn'].prefix}"]
                )

        if "+nccl" in spec and spec.satisfies("@0.4.32:"):
            args.append(f"--bazel_options=--repo_env=LOCAL_NCCL_PATH={spec['nccl'].prefix}")

        if "+rocm" in spec:
            args.extend(["--enable_rocm", f"--rocm_path={self.spec['hip'].prefix}"])

        args.extend(
            [
                f"--bazel_options=--jobs={make_jobs}",
                "--bazel_startup_options=--nohome_rc",
                "--bazel_startup_options=--nosystem_rc",
            ]
        )

        python(*args)
        whl = glob.glob(join_path("dist", "*.whl"))[0]
        pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", whl)
