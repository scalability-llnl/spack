# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPympler(PythonPackage):
    """Development tool to measure, monitor and analyze the memory behavior
    of Python objects in a running Python application.
    """

    homepage = "https://github.com/pympler/pympler"
    pypi = "Pympler/Pympler-0.4.3.tar.gz"

    license("Apache-2.0")

    version("1.0.1", sha256="993f1a3599ca3f4fcd7160c7545ad06310c9e12f70174ae7ae8d4e25f6c5d3fa")

    depends_on("python@3.6:3.10", type=("build", "run"))
    depends_on("py-setuptools", type="build")
