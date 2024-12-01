# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHydraCore(PythonPackage):
    """A framework for elegantly configuring complex applications."""

    homepage = "https://github.com/facebookresearch/hydra"
    pypi = "hydra-core/hydra-core-1.3.1.tar.gz"

    license("MIT")

    version("1.3.1", sha256="8dd42d551befc43dfca0c612cbd58c4f3e273dbd97a87214c1a030ba557d238b")

    depends_on("py-setuptools", type="build")
    depends_on("py-omegaconf@2.2:2.3", type=("build", "run"))
    depends_on("py-antlr4-python3-runtime@4.9", type=("build", "run"))
    depends_on("py-importlib-resources", when="^python@:3.8", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("java", type="build")
