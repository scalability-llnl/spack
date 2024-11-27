# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLinkifyItPy(PythonPackage):
    """Links recognition library with FULL unicode support."""

    homepage = "https://github.com/tsutsu3/linkify-it-py"
    pypi = "linkify-it-py/linkify-it-py-2.0.2.tar.gz"

    license("MIT")

    version("2.0.2", sha256="19f3060727842c254c808e99d465c80c49d2c7306788140987a1a7a29b0d6ad2")
    version("1.0.3", sha256="2b3f168d5ce75e3a425e34b341a6b73e116b5d9ed8dbbbf5dc7456843b7ce2ee")

    depends_on("python@3.6:", when="@1.0.3", type=("build", "run"))
    depends_on("python@3.7:", when="@2.0.2:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-uc-micro-py", type=("build", "run"))
