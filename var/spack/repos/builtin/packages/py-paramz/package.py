# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParamz(PythonPackage):
    """The Parameterization Framework."""

    homepage = "https://github.com/sods/paramz"
    pypi = "paramz/paramz-0.9.5.tar.gz"

    license("BSD-3-Clause")

    version("0.9.5", sha256="0917211c0f083f344e7f1bc997e0d713dbc147b6380bc19f606119394f820b9a")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-decorator@4.0.10:", type=("build", "run"))
