# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCodepy(PythonPackage):
    """CodePy is a C metaprogramming toolkit for Python.

    It handles two aspects of metaprogramming:
    - Generating C source code.
    - Compiling this source code and dynamically loading it into the Python interpreter.
    """

    homepage = "https://documen.tician.de/codepy/"
    pypi = "codepy/codepy-2019.1.tar.gz"

    license("MIT")

    version("2019.1", sha256="384f22c37fe987c0ca71951690c3c2fd14dacdeddbeb0fde4fd01cd84859c94e")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-pytools@2015.1.2:", type=("build", "run"))
    depends_on("py-numpy@1.6:", type=("build", "run"))
    depends_on("py-appdirs@1.4.0:", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-cgen", type=("build", "run"))
