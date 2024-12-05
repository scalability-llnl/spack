# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyupgrade(PythonPackage):
    """A tool to automatically upgrade syntax for newer versions."""

    homepage = "https://github.com/asottile/pyupgrade"
    pypi = "pyupgrade/pyupgrade-2.31.1.tar.gz"

    license("MIT")

    version("3.3.1", sha256="f88bce38b0ba92c2a9a5063c8629e456e8d919b67d2d42c7ecab82ff196f9813")
    version("2.31.1", sha256="22e0ad6dd39c4381805cb059f1e691b6315c62c0ebcec98a5f29d22cd186a72a")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-tokenize-rt@3.2:", type=("build", "run"))
