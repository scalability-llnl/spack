# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAccelerate(PythonPackage):
    """A simple way to train and use PyTorch models with multi-GPU, TPU, mixed-precision."""

    homepage = "https://github.com/huggingface/accelerate"
    pypi = "accelerate/accelerate-0.16.0.tar.gz"

    maintainers("meyersbs")

    license("Apache-2.0")

    version("0.21.0", sha256="e2959a0bf74d97c0b3c0e036ed96065142a060242281d27970d4c4e34f11ca59")
    version("0.16.0", sha256="d13e30f3e6debfb46cada7b931af85560619b6a6a839d0cafeeab6ed7c6a498d")

    depends_on("python@3.8.0:", when="@0.21.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.17:", type=("build", "run"))
    depends_on("py-packaging@20:", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-torch@1.10.0:", when="@0.21.0:", type=("build", "run"))
    depends_on("py-torch@1.4:", type=("build", "run"))
