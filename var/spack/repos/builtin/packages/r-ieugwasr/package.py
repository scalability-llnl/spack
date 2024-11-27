# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIeugwasr(RPackage):
    """R Interface to the OpenGWAS Database API.

    R interface to the OpenGWAS database API. Includes a wrapper
    to make generic calls to the API, plus convenience functions for
    specific queries."""

    homepage = "https://github.com/MRCIEU/ieugwasr"
    url = "https://github.com/MRCIEU/ieugwasr/archive/refs/tags/0.1.5.tar.gz"

    license("MIT")

    version("0.1.5", sha256="8d900d5a780f23836c80191f9635fbf48a0ca94f828452948c0f445e3217f422")

    depends_on("r@3.6.0:", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-googleauthr", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-httr", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
