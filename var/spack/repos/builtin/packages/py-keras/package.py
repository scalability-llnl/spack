# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.package import *


class PyKeras(PythonPackage):
    """Multi-backend Keras.

    Keras 3 is a new multi-backend implementation of the Keras API,
    with support for TensorFlow, JAX, and PyTorch.
    """

    homepage = "https://keras.io"
    git = "https://github.com/keras-team/keras.git"
    pypi = "keras/keras-3.0.0.tar.gz"

    maintainers("adamjstewart")
    license("Apache-2.0")

    version("3.6.0", sha256="405727525a3522ed8f9ec0b46e0667e4c65fcf714a067322c16a00d902ded41d")
    version("3.5.0", sha256="53ae4f9472ec9d9c6941c82a3fda86969724ace3b7630a94ba0a1f17ba1065c3")
    version("3.4.1", sha256="34cd9aeaa008914715149234c215657ca758e1b473bd2aab2e211ac967d1f8fe")
    version("3.4.0", sha256="c4b05b150b1c4df27b4a17efd137b2d5e20f385f146fd48636791d675e75059d")
    version("3.3.3", sha256="f2fdffc8434fd77045cf8fb21816dbaa2308d5f76974ca924b2f60b40433b1a0")
    version("3.3.2", sha256="e7e2ccba2dfe2cf10b82e3c75ea971b82a4c62560dc562c43b33f7790127c92f")
    version("3.3.1", sha256="03531beb01b108b867683762ceaacd0f28efc40cb92eee3c8c988b80cf718bbe")
    version("3.3.0", sha256="46763bd84696aa5e326734ee0ccfde12bef73b27f1e5e241bbf539cb6411e78d")
    version("3.2.1", sha256="966abbf0dfc1f9725f6293fb2a04ec83f56cd2a800990b38d1a03041255214a7")
    version("3.2.0", sha256="e3ff572c872ebb24d2ae62d4e12c3579ccd0019d0f0adaf3cb7dc610e77e84c1")
    version("3.1.1", sha256="55558ea228dc38e7667874fd2e83eaf7faeb026e2e8615b36a8616830f7e303b")
    version("3.1.0", sha256="cac46e053f0493da313e7c9b16379a532b1a38f9f19c7a5fe4578759f4c6aa4d")
    version("3.0.5", sha256="df3d3795e12c3f6035e811c43c13f1eb41e37241796a0fea120ede4ebe1c4496")
    version("3.0.4", sha256="ff2204792582e3889c51c77722cc6e8258dbb1ece7db192f5a9bcd1887cf3385")
    version("3.0.3", sha256="1e455a82be63b7fb4f699e26bd1e04b7dbcbf66fa3a799117afca9ab067b5d61")
    version("3.0.2", sha256="526b6c053cdd880a33467c5bfd5c460a5bdc0c58869c2683171c2dec2ad3c2d0")
    version("3.0.1", sha256="d993721510fa654582132192193f69b1b3165418a6e00a73c3edce615b3cc672")
    version("3.0.0", sha256="82a9fa4b32a049b38151d11188ed15d74f21f853f163e78da0950dce1f244ccc")
    version("2.15.0", sha256="b281ce09226576e0593b8dab0d9e5d42c334e053ce6f4f154dc6cd745ab93d2f")
    version("2.14.0", sha256="a845d446b6ae626f61dde5ab2fa952530b6c17b4f9ed03e9362bd20172d00cca")
    version("2.13.1", sha256="b3591493cce75a69adef7b192cec6be222e76e2386d132cd4e34aa190b0ecbd5")
    version("2.12.0", sha256="6336cebb6b2b0a91f7efd3ff3a9db3a94f2abccf07a40323138afb80826aec62")
    version("2.11.0", sha256="e7a7c4199ac76ea750d145c1d84ae1b932e68b9bca34e83596bd66b2fc2ad79e")
    version("2.10.0", sha256="b1d8d9358700f4a585455854a142d88cc987419c1638ef935b440842d593ad04")
    version("2.9.0", sha256="90226eaa0337573304f3e5ab44d4d9e3a65fe002776c5cbd0f65b738152c1084")
    version("2.8.0", sha256="5e777b0101d8385d3a90fc9056f1b2f6313f2c830d2e8181828b300c9229ec0c")
    version("2.7.0", sha256="7502746467ab15184e2e267f13fbb2c3f33ba24f8e02a097d229ba376dabaa04")
    version("2.6.0", sha256="15586a3f3e1ed9182e6e0d4c0dbd052dfb7250e779ceb7e24f8839db5c63fcae")
    version("2.4.3", sha256="fedd729b52572fb108a98e3d97e1bac10a81d3917d2103cc20ab2a5f03beb973")
    version("2.4.2", sha256="e26bc51b7b8fb7add452cdf6fba77d6509e6c78b9d9ef5fd32fe132c6d9182d2")
    version("2.4.1", sha256="e282cc9c5c996043b21d045765c0c5bf541c1879232a97a574c51af0ce132cb1")
    version("2.4.0", sha256="e31c6d2910767ab72f630309286fb7bf5476810dd64fde3e254054478442e9b0")
    version("2.3.1", sha256="321d43772006a25a1d58eea17401ef2a34d388b588c9f7646c34796151ebc8cc")
    version("2.3.0", sha256="a0d6ecf1d71cd0b85ea1da27ea7314a9d4723f5b468b7cedd87dcad0a491b354")
    version("2.2.5", sha256="0fb448b95643a708d25d2394183a2f3a84eefb55fb64917152a46826990113ea")
    version("2.2.4", sha256="90b610a3dbbf6d257b20a079eba3fdf2eed2158f64066a7c6f7227023fd60bc9")
    version("2.2.3", sha256="694aee60a6f8e0d3d6d3e4967e063b4623e3ca90032f023fd6d16bb5f81d18de")
    version("2.2.2", sha256="468d98da104ec5c3dbb10c2ef6bb345ab154f6ca2d722d4c250ef4d6105de17a")
    version("2.2.1", sha256="0d3cb14260a3fa2f4a5c4c9efa72226ffac3b4c50135ba6edaf2b3d1d23b11ee")
    version("2.2.0", sha256="5b8499d157af217f1a5ee33589e774127ebc3e266c833c22cb5afbb0ed1734bf")

    variant(
        "backend",
        default="tensorflow",
        description="backend library",
        values=["tensorflow", "jax", "torch"],
        multi=False,
        when="@3:",
    )

    with default_args(type="build"):
        depends_on("py-setuptools")

    with default_args(type=("build", "run")):
        # setup.py
        depends_on("python@3.9:", when="@3:")
        depends_on("python@3.8:", when="@2.12:")
        depends_on("py-absl-py", when="@2.6:")
        depends_on("py-numpy")
        depends_on("py-rich", when="@3:")
        depends_on("py-namex@0.0.8:", when="@3.3.3:")
        depends_on("py-namex", when="@3:")
        depends_on("py-h5py")
        depends_on("py-optree", when="@3.1:")
        depends_on("py-ml-dtypes", when="@3.0.5:")
        depends_on("py-packaging", when="@3.4:")

        # requirements-common.txt
        depends_on("py-scipy")
        depends_on("py-pandas")
        depends_on("py-requests", when="@3:")
        depends_on("py-protobuf", when="@3:")

        # requirements-tensorflow-cuda.txt
        with when("backend=tensorflow"):
            depends_on("py-tensorflow@2.17", when="@3.5:")
            depends_on("py-tensorflow@2.16.1:2.16", when="@3.0:3.4")

        # requirements-jax-cuda.txt
        with when("backend=jax"):
            depends_on("py-jax@0.4.28", when="@3.6:")
            depends_on("py-jax@0.4.23", when="@3.0.5:3.5")
            depends_on("py-jax", when="@3:")

        # requirements-torch-cuda.txt
        with when("backend=torch"):
            depends_on("py-torch@2.4.1", when="@3.6:")
            depends_on("py-torch@2.4.0", when="@3.5")
            depends_on("py-torch@2.2.1", when="@3.1:3.4")
            depends_on("py-torch@2.1.2", when="@3.0.3:3.0.5")
            depends_on("py-torch@2.1.1", when="@3.0.1:3.0.2")
            depends_on("py-torch@2.1.0", when="@3.0.0")
            depends_on("py-torchvision@0.19.1", when="@3.6:")
            depends_on("py-torchvision@0.19.0", when="@3.5")
            depends_on("py-torchvision@0.17.1", when="@3.1:3.4")
            depends_on("py-torchvision@0.16.2", when="@3.0.3:3.0.5")
            depends_on("py-torchvision@0.16.1", when="@3.0.1:3.0.2")
            depends_on("py-torchvision@0.16.0", when="@3.0.0")

    # Historical dependencies
    with default_args(type="build"):
        depends_on("bazel", when="@2.5:2")
        depends_on("protobuf", when="@2.5:2")

    with default_args(type=("build", "run")):
        depends_on("pil", when="@:2")
        depends_on("py-dm-tree", when="@3.0")
        # https://github.com/keras-team/keras/issues/19691
        depends_on("py-numpy@:1", when="@:3.4")
        depends_on("py-portpicker", when="@2.10:2")
        depends_on("py-pydot", when="@:2")
        depends_on("py-pyyaml", when="@:2")
        depends_on("py-six", when="@:2")

        for minor_ver in range(6, 16):
            depends_on("py-tensorflow@2.{}".format(minor_ver), when="@2.{}".format(minor_ver))
            depends_on("py-tensorboard@2.{}".format(minor_ver), when="@2.{}".format(minor_ver))

    def url_for_version(self, version):
        if version >= Version("3"):
            url = "https://files.pythonhosted.org/packages/source/k/keras/keras-{}.tar.gz"
        elif version >= Version("2.6"):
            url = "https://github.com/keras-team/keras/archive/refs/tags/v{}.tar.gz"
        else:
            url = "https://files.pythonhosted.org/packages/source/k/keras/Keras-{}.tar.gz"
        return url.format(version)

    def setup_run_environment(self, env):
        if self.spec.satisfies("@3:"):
            env.set("KERAS_BACKEND", self.spec.variants["backend"].value)

    @when("@2.5:2")
    def patch(self):
        infile = join_path(self.package_dir, "protobuf_build.patch")
        with open(infile, "r") as source_file:
            text = source_file.read()
        with open("keras/keras.bzl", mode="a") as f:
            f.write(text)

        filter_file(
            'load("@com_google_protobuf//:protobuf.bzl", "py_proto_library")',
            'load("@org_keras//keras:keras.bzl", "py_proto_library")',
            "keras/protobuf/BUILD",
            string=True,
        )

    @when("@2.5:2")
    def install(self, spec, prefix):
        self.tmp_path = tempfile.mkdtemp(prefix="spack")
        env["HOME"] = self.tmp_path

        args = [
            # Don't allow user or system .bazelrc to override build settings
            "--nohome_rc",
            "--nosystem_rc",
            # Bazel does not work properly on NFS, switch to /tmp
            "--output_user_root=" + self.tmp_path,
            "build",
            # Spack logs don't handle colored output well
            "--color=no",
            "--jobs={0}".format(make_jobs),
            # Enable verbose output for failures
            "--verbose_failures",
            "--spawn_strategy=local",
            # bazel uses system PYTHONPATH instead of spack paths
            "--action_env",
            "PYTHONPATH={0}".format(env["PYTHONPATH"]),
            "//keras/tools/pip_package:build_pip_package",
        ]

        bazel(*args)

        build_pip_package = Executable("bazel-bin/keras/tools/pip_package/build_pip_package")
        buildpath = join_path(self.stage.source_path, "spack-build")
        build_pip_package("--src", buildpath)

        with working_dir(buildpath):
            args = std_pip_args + ["--prefix=" + prefix, "."]
            pip(*args)
        remove_linked_tree(self.tmp_path)
