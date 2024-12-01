# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVisnetwork(RPackage):
    """Network Visualization using 'vis.js' Library.

    Provides an R interface to the 'vis.js' JavaScript charting library. It
    allows an interactive visualization of networks."""

    cran = "visNetwork"

    version("2.1.2", sha256="47c99d42fc89e6ae929257b2648d998c5ffed60dff97ad7e47613f5a0c1ddc84")
    version("2.1.0", sha256="a2b91e7fbbd9d08a9929a5b2c891d9c0bca5977ad772fa37510d96656af1152f")
    version("2.0.9", sha256="5e0b3dc3a91e66e0a359433f03cc856d04b981b0f9ad228d8fa9c96b7fcaa420")
    version("2.0.7", sha256="15ad01636a3a19e1901be6743052805a5b6a9ac1240fb3dab765252b1e865128")
    version("2.0.6", sha256="ec2478e6a2af446569ef2d5210a2bc6b2600bcb7fd9908cef8f8c80b01e9c8aa")
    version("1.0.1", sha256="13aacf58d3bf9e78c7fb3af180062762bf22aec1777c829715c5b00396639a70")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r-htmlwidgets", type=("build", "run"))
    depends_on("r-htmltools", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
