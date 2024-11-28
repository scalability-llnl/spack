# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTensorstore(PythonPackage):
    """Read and write large, multi-dimensional arrays."""

    homepage = "https://github.com/google/tensorstore"
    pypi = "tensorstore/tensorstore-0.1.54.tar.gz"

    license("Apache-2.0")

    version("0.1.54", sha256="e1a9dcb0be7c828f752375409537d4b39c658dd6c6a0873fe21a24a556ec0e2a")

    depends_on("cxx", type="build")  # generated

    # .bazelversion
    depends_on("bazel@6.4.0", type="build")

    with default_args(type="build"):
        depends_on("py-setuptools@30.3:")
        depends_on("py-setuptools-scm")

    with default_args(type=("build", "run")):
        depends_on("python@3.9:")
        depends_on("py-numpy@1.16:")
        depends_on("py-ml-dtypes@0.3.1:")

    def patch(self):
        # Trick bazelisk into using the Spack-installed copy of bazel
        symlink(bazel.path, join_path("tools", "bazel"))
