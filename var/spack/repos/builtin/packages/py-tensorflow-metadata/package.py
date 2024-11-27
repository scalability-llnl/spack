# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.package import *


class PyTensorflowMetadata(PythonPackage):
    """Library and standards for schema and statistics.

    TensorFlow Metadata provides standard representations for metadata that are
    useful when training machine learning models with TensorFlow."""

    homepage = "https://pypi.org/project/tensorflow-metadata/"

    # Only available as a wheel on PyPI
    url = "https://github.com/tensorflow/metadata/archive/refs/tags/v1.5.0.tar.gz"

    license("Apache-2.0")

    version("1.10.0", sha256="e7aa81aa01433e2a75c11425affd55125b64f384baf96b71eeb3a88dca8cf2ae")
    version("1.5.0", sha256="f0ec8aaf62fd772ef908efe4ee5ea3bc0d67dcbf10ae118415b7b206a1d61745")

    # Fix non-existing zlib URL
    patch(
        "https://github.com/tensorflow/metadata/commit/8df679e782f5bf2d163d63e550d8752c3812d566.patch?full_index=1",
        sha256="a6b294d5e6099979192fcdb4d5b7b0388dc30b48671944d22e51a9e6bd5e1490",
        when="@1.10.0",
    )

    depends_on("bazel@0.24.1:", type="build")
    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-absl-py@0.9:1", when="@1.6:", type=("build", "run"))
    depends_on("py-absl-py@0.9:0.12", when="@:1.5", type=("build", "run"))
    depends_on("py-googleapis-common-protos@1.52:1", type=("build", "run"))
    depends_on("py-protobuf@3.13:3", type=("build", "run"))

    def patch(self):
        filter_file(
            "self._additional_build_options = ['--copt=-DWIN32_LEAN_AND_MEAN']",
            "self._additional_build_options = ['--copt=-DWIN32_LEAN_AND_MEAN',"
            f" '--jobs={make_jobs}']",
            "setup.py",
            string=True,
        )
        filter_file(
            "self._additional_build_options = []",
            f"self._additional_build_options = ['--jobs={make_jobs}']",
            "setup.py",
            string=True,
        )

    def setup_build_environment(self, env):
        tmp_path = tempfile.mkdtemp(prefix="spack")
        env.set("TEST_TMPDIR", tmp_path)
