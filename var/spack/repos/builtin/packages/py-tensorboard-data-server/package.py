# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class PyTensorboardDataServer(PythonPackage):
    """Fast data loading for TensorBoard"""

    homepage = "https://github.com/tensorflow/tensorboard/tree/master/tensorboard/data/server"
    git = "https://github.com/tensorflow/tensorboard"

    license("Apache-2.0")

    version("0.7.0", commit="f1cb31c86d871e0258250248ab9488575410e784")
    version("0.6.1", commit="6acf0be88b5727e546dd64a8b9b12d790601d561")

    depends_on("py-setuptools", type="build")
    depends_on("rust+dev", type="build")

    # https://github.com/tensorflow/tensorboard/issues/5713
    patch(
        "https://github.com/tensorflow/tensorboard/pull/5715.patch?full_index=1",
        sha256="878bbd60fd9c38216a372792f02a65c1b422b6c546050fdf335b264ab263cd8a",
        when="@0.6.1",
    )
    patch(
        "https://github.com/tensorflow/tensorboard/pull/6101.patch?full_index=1",
        sha256="4b3bcc2ed656699e9faad7937d013b65fa65fed58fbe58d2ae38e0e7b8006ad8",
        when="@0.6.1",
    )

    def setup_build_environment(self, env):
        env.set("CARGO_HOME", self.stage.source_path)

    def install(self, spec, prefix):
        with working_dir(join_path("tensorboard", "data", "server")):
            cargo = which("cargo")
            cargo("build", "--release")

        with working_dir(join_path("tensorboard", "data", "server", "pip_package")):
            python(
                "build.py",
                "--out-dir={0}".format(self.stage.source_path),
                "--server-binary={0}".format(
                    join_path(
                        self.stage.source_path,
                        "tensorboard",
                        "data",
                        "server",
                        "target",
                        "release",
                        "rustboard",
                    )
                ),
            )

        wheel = glob.glob("*.whl")[0]
        pip(*PythonPipBuilder.std_args(self), f"--prefix={prefix}", wheel)
