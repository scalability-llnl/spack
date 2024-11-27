# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLmodule(PythonPackage):
    """Lmodule is a Python API for Lmod module system. It's primary purpose is
    to help automate module testing. Lmodule uses Lmod spider tool to query
    all modules in-order to automate module testing. Lmodule can be used with
    environment-modules to interact with module using the Module class."""

    homepage = "https://lmodule.readthedocs.io/en/latest/"
    pypi = "lmodule/lmodule-0.1.0.tar.gz"
    git = "https://github.com/buildtesters/lmodule"

    maintainers("shahzebsiddiqui")

    license("MIT")

    version("0.1.0", sha256="cac8f3dad2df27b10e051b2c56ccbde1fcdd7044af594d13fd2e4144d3d46a29")

    depends_on("python@3.6.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("lmod@7.0:", type="run")
