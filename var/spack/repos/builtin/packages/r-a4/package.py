# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RA4(RPackage):
    """Automated Affymetrix Array Analysis Umbrella Package.

    Umbrella package is available for the entire Automated Affymetrix Array
    Analysis suite of package."""

    bioc = "a4"

    version("1.48.0", commit="89ef9f4afdde5270acecc7c65be3752b71237eba")
    version("1.46.0", commit="1b8f1300025fb0940e7f24cff7ffec9fca02d0e4")
    version("1.44.0", commit="5b0fc5a9971d8f3688ad1f88a4f5ee1498e91633")
    version("1.42.0", commit="fc26809e2bce7cd50d99d6f6dd5f85c38342fdea")
    version("1.38.0", commit="5b7a9087bab10c55e24707e96e48046995236c94")
    version("1.32.0", commit="03770d4e53be4eed1bd0ab8f8cddba66854b4712")
    version("1.30.0", commit="771e01ae3aaac1c4db12f781c41d90fa7191b64d")
    version("1.28.0", commit="e81a8c15e1062ed9433e2d4d333f0484bc0e8bfb")
    version("1.26.0", commit="e6af2cba5b684f81cc6e44dbc432916f75a2f774")
    version("1.24.0", commit="79b5143652176787c85a0d587b3bbfad6b4a19f4")

    depends_on("r-a4base", type=("build", "run"))
    depends_on("r-a4preproc", type=("build", "run"))
    depends_on("r-a4classif", type=("build", "run"))
    depends_on("r-a4core", type=("build", "run"))
    depends_on("r-a4reporting", type=("build", "run"))
