# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStarsessions(PythonPackage):
    """Advanced sessions for Starlette and FastAPI frameworks."""

    homepage = "https://github.com/alex-oleshkevich/starsessions"
    pypi = "starsessions/starsessions-2.1.1.tar.gz"

    license("MIT")

    version("2.1.1", sha256="cb250de84ebc6159ad187cab69e6fe60eab11684b40349457e74dcfb7656c805")
    version("1.3.0", sha256="8d3b509d4e6d235655f7dd495fcf0afc1bd86da84de3a8d434e6f82137ebcde8")

    depends_on("python@3.8:3", when="@2:", type=("build", "run"))
    depends_on("py-poetry-core@1:", type="build")
    depends_on("py-starlette@0", type=("build", "run"))
    depends_on("py-itsdangerous@2.0.1:2", type=("build", "run"))
