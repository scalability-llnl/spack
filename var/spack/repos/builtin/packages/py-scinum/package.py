# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScinum(PythonPackage):
    """Scientific numbers with multiple uncertainties and
    correlation-aware, gaussian propagation and numpy"""

    homepage = "https://github.com/riga/scinum"
    pypi = "scinum/scinum-1.2.0.tar.gz"

    license("BSD-3-Clause")

    version("1.4.3", sha256="c8144b6a2ed5cb58b2c26a8151752b6f5f5ea460678a9e092015b91da926c443")
    version("1.2.0", sha256="31802d9b580f3a89c0876f34432851bc4def9cb2844d6f3c8e044480f2dd2f91")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("python@2.7:2,3.6:3", when="@1.4.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
