# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPlanetaryComputer(PythonPackage):
    """Python library for interacting with the Microsoft Planetary Computer."""

    homepage = "https://github.com/microsoft/PlanetaryComputer"
    pypi = "planetary-computer/planetary-computer-0.4.9.tar.gz"

    license("MIT")

    version("0.4.9", sha256="f25030aa5b1fc3e44bd0d48300325ffbdbbabbed4a837dfcea55764359249720")

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-click@7.1:", type=("build", "run"))
    depends_on("py-pydantic@1.7.3:+dotenv", type=("build", "run"))
    depends_on("py-pystac@1:", type=("build", "run"))
    depends_on("py-pystac-client@0.2:", type=("build", "run"))
    depends_on("py-requests@2.25.1:", type=("build", "run"))
