# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNumpyStl(PythonPackage):
    """Library to make reading, writing and modifying both binary and ascii STL files easy"""

    homepage = "https://github.com/WoLpH/numpy-stl/"
    pypi = "numpy-stl/numpy-stl-2.10.1.tar.gz"

    license("BSD-3-Clause")

    version("3.0.0", sha256="578b78eacb0529ac9aba2f17dcc363d58c7c3c5708710c18f8c1e9965f2e81ac")
    version("2.10.1", sha256="f6b529b8a8112dfe456d4f7697c7aee0aca62be5a873879306afe4b26fca963c")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-python-utils@1.6.2:", when="@2.10.1", type=("build", "run"))
    depends_on("py-python-utils@3.4.5:", when="@3:", type=("build", "run"))
