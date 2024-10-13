# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

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
    """XLA library for Jax"""

    homepage = "https://github.com/google/jax"
    url = "https://github.com/google/jax/archive/refs/tags/jaxlib-v0.4.27.tar.gz"

    tmp_path = ""
    buildtmp = ""

    license("Apache-2.0")
    maintainers("adamjstewart", "jonas-eschle")

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

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("cuda", default=True, description="Build with CUDA enabled")
    variant("nccl", default=True, description="Build with NCCL enabled", when="+cuda")

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
        depends_on("python@3.10:3.12", when="@0.4.31:")
        depends_on("python@3.9:3.12", when="@0.4.17:0.4.30")
        depends_on("python@3.9:3.11", when="@0.4.14:0.4.16")
        depends_on("python@3.8:3.11", when="@0.4.6:0.4.13")

        # jaxlib/setup.py
        depends_on("py-scipy@1.10:", when="@0.4.31:")
        depends_on("py-scipy@1.9:", when="@0.4.19:")
        depends_on("py-scipy@1.7:", when="@0.4.7:")
        depends_on("py-scipy@1.5:")
        depends_on("py-numpy@1.24:", when="@0.4.31:")
        depends_on("py-numpy@1.22:", when="@0.4.14:")
        depends_on("py-numpy@1.21:", when="@0.4.7:")
        depends_on("py-numpy@1.20:", when="@0.3:")
        depends_on("py-ml-dtypes@0.2:", when="@0.4.14:")
        depends_on("py-ml-dtypes@0.1:", when="@0.4.9:")
        depends_on("py-ml-dtypes@0.0.3:", when="@0.4.7:")

        # Historical dependencies
        # https://github.com/google/jax/issues/19246
        depends_on("py-numpy@:1", when="@:0.4.25")
        depends_on("py-ml-dtypes@0.4:", when="@0.4.29")

    patch(
        "https://github.com/google/jax/pull/20101.patch?full_index=1",
        sha256="4dfb9f32d4eeb0a0fb3a6f4124c4170e3fe49511f1b768cd634c78d489962275",
        when="@:0.4.25",
    )

    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )

    # https://github.com/google/jax/issues/19992
    conflicts("@0.4.4:", when="target=ppc64le:")

    def patch(self):
        self.tmp_path = tempfile.mkdtemp(prefix="spack")
        self.buildtmp = tempfile.mkdtemp(prefix="spack")
        filter_file(
            "build --spawn_strategy=standalone",
            f"""
# Limit CPU workers to spack jobs instead of using all HOST_CPUS.
build --spawn_strategy=standalone
build --local_cpu_resources={make_jobs}
""".strip(),
            ".bazelrc",
            string=True,
        )
        filter_file(
            'f"--output_path={output_path}",',
            'f"--output_path={output_path}",'
            f' "--sources_path={self.tmp_path}",'
            ' "--nohome_rc",'
            ' "--nosystem_rc",'
            f' "--jobs={make_jobs}",',
            "build/build.py",
            string=True,
        )
        build_wheel = join_path("build", "build_wheel.py")
        if self.spec.satisfies("@0.4.14:"):
            build_wheel = join_path("jaxlib", "tools", "build_wheel.py")
        filter_file(
            "args = parser.parse_args()",
            "args, junk = parser.parse_known_args()",
            build_wheel,
            string=True,
        )

    def install(self, spec, prefix):
        args = []
        args.append("build/build.py")
        if "+cuda" in spec:
            args.append("--enable_cuda")
            args.append("--cuda_path={0}".format(self.spec["cuda"].prefix))
            args.append("--cudnn_path={0}".format(self.spec["cudnn"].prefix))
            capabilities = CudaPackage.compute_capabilities(spec.variants["cuda_arch"].value)
            args.append("--cuda_compute_capabilities={0}".format(",".join(capabilities)))
        args.append(
            "--bazel_startup_options="
            "--output_user_root={0}".format(self.wrapped_package_object.buildtmp)
        )
        if "+rocm" in spec:
            args.append("--enable_rocm")
            args.append("--rocm_path={0}".format(self.spec["hip"].prefix))

        python(*args)
        with working_dir(self.wrapped_package_object.tmp_path):
            args = std_pip_args + ["--prefix=" + self.prefix, "."]
            pip(*args)
        remove_linked_tree(self.wrapped_package_object.tmp_path)
        remove_linked_tree(self.wrapped_package_object.buildtmp)
