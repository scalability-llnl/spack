# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class PyTensorflowEstimator(Package):
    """TensorFlow Estimator is a high-level API that encapsulates
    model training, evaluation, prediction, and exporting.
    """

    homepage = "https://github.com/tensorflow/estimator"
    url = "https://github.com/tensorflow/estimator/archive/v2.2.0.tar.gz"

    maintainers("aweits")

    license("Apache-2.0")

    version("2.14.0", sha256="622797bf5311f239c2b123364fa360868ae97d16b678413e5e0633241f7d7d5c")
    version("2.13.0", sha256="4175e9276a1eb8b5e4e876d228e4605871832e7bd8517965d6a47f1481af2c3e")
    version("2.12.0", sha256="86c75e830c6ba762d0e3cf04c160096930fb12a992e69b3f24674b9f58902063")
    version("2.11.0", sha256="922f9187de79e8e7f7d7a5b2d6d3aabc81bbbd6ba5f12a4f52967dd302214a43")
    version("2.10", sha256="60df309377cf4e584ca20198f9639beb685d50616395f50770fc0999092d6d85")
    version("2.9.0", sha256="62d7b5a574d9c995542f6cb485ff1c18ad115afd9ec6d63437b2aab227c35ef6")
    version("2.8.0", sha256="58a2c3562ca6491c257e9a4d9bd8825667883257edcdb452181efa691c586b17")
    version("2.7.0", sha256="e5164e802638d3cf110ecc17912be9d514a9d3354ec48e77200b9403dcc15965")
    version("2.6.0", sha256="947705c60c50da0b4a8ceec1bc058aaf6bf567a7efdcd50d5173ebf6bafcf30f")
    version("2.4.0", sha256="e6ea12014c3d8c89a81ace95f8f8b7c39ffcd3e4e4626709e4aee0010eefd962")
    version("2.3.0", sha256="75403e7de7e8ec30ec0781ede56ed84cbe5e90daad64a9c242cd489c8fe63a17")
    version("2.2.0", sha256="2d68cb6e6442e7dcbfa2e092aa25bdcb0eda420536a829b85d732854a4c85d46")

    extends("python")

    with default_args(type="build"):
        depends_on("bazel@0.19.0:")
        depends_on("py-pip")
        depends_on("py-wheel")

    # See expect_*_installed in tensorflow_estimator/python/estimator/BUILD
    with default_args(type=("build", "run")):
        depends_on("py-absl-py")
        depends_on("py-h5py")
        depends_on("py-numpy")
        depends_on("py-pandas")
        depends_on("py-six")
        for ver in [
            "2.14",
            "2.13",
            "2.12",
            "2.11",
            "2.10",
            "2.9",
            "2.8",
            "2.7",
            "2.6",
            "2.4",
            "2.3",
            "2.2",
        ]:
            depends_on(f"py-tensorboard@{ver}", when=f"@{ver}")
            depends_on(f"py-tensorflow@{ver}", when=f"@{ver}")
            depends_on(f"py-keras@{ver}", when=f"@{ver}")

    def install(self, spec, prefix):
        self.tmp_path = tempfile.mkdtemp(prefix="spack")
        env["TEST_TMPDIR"] = self.tmp_path
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
            "//tensorflow_estimator/tools/pip_package:build_pip_package",
        ]

        bazel(*args)

        build_pip_package = Executable(
            join_path("bazel-bin/tensorflow_estimator/tools", "pip_package/build_pip_package")
        )
        buildpath = join_path(self.stage.source_path, "spack-build")
        build_pip_package("--src", buildpath)
        with working_dir(buildpath):
            pip(*PythonPipBuilder.std_args(self), f"--prefix={self.prefix}", ".")
        remove_linked_tree(self.tmp_path)
