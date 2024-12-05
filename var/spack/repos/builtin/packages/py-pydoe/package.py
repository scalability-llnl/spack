# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydoe(PythonPackage):
    """The pyDOE package is designed to help the scientist, engineer,
    statistician, etc., to construct appropriate experimental designs"""

    homepage = "https://github.com/tisimst/pyDOE"
    pypi = "pyDOE/pyDOE-0.3.8.zip"

    version("0.3.8", sha256="cbd6f14ae26d3c9f736013205f53ea1191add4567033c3ee77b7dd356566c4b6")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
