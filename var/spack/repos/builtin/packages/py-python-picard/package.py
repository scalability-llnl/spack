# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonPicard(PythonPackage):
    """Preconditoned ICA for Real Data."""

    homepage = "https://pierreablin.github.io/picard/"
    pypi = "python-picard/python-picard-0.6.tar.gz"

    license("BSD-3-Clause")

    version("0.6", sha256="dad377c9a50f9850f85841eba0ffb58ad557885ca93364bb73153f33210b52e2")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.8:", type=("build", "run"))
    depends_on("py-matplotlib@1.3:", type=("build", "run"))
    depends_on("py-scipy@0.16:", type=("build", "run"))
    depends_on("py-numexpr@2.0:", type=("build", "run"))
    depends_on("py-scikit-learn@0.23:", type=("build", "run"))
