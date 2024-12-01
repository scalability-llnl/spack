# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFuncy(PythonPackage):
    """A collection of fancy functional tools focused on practicality"""

    homepage = "https://funcy.readthedocs.io"
    pypi = "funcy/funcy-1.15.tar.gz"

    license("BSD-3-Clause")

    version("1.15", sha256="65b746fed572b392d886810a98d56939c6e0d545abb750527a717c21ced21008")
    version("1.14", sha256="75ee84c3b446f92e68a857c2267b15a1b49c631c9d5a87a5f063cd2d6761a5c4")

    depends_on("python@2.7.0:2.7,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
