# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGamlssData(RPackage):
    """GAMLSS Data.

    Data used as examples in the current two books on Generalised Additive
    Models for Location Scale and Shape introduced by Rigby and Stasinopoulos
    (2005), <doi:10.1111/j.1467-9876.2005.00510.x>."""

    cran = "gamlss.data"

    version("6.0-6", sha256="bae0db19d95500b3f49f855d4ebd3ddb071c5e2d9104b27e0a73865f4909ab22")
    version("6.0-2", sha256="dbb3b6f855540928ccdbda497f8d552144895e34565799e8b595e704096db71e")
    version("5.1-4", sha256="0d3777d8c3cd76cef273aa6bde40a91688719be401195ed9bfd1e85bd7d5eeb5")
    version("5.1-3", sha256="4941180e7eebe97678ba02ca24c2a797bcb69d92cd34600215a94110e2a70470")
    version("5.1-0", sha256="0aad438ea1aa6395677e52cd2cb496f9f4c9ba2d39edc92c8cb42e7fc91fe6c1")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@6.0-2:")
