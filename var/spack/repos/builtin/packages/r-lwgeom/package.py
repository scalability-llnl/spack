# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLwgeom(RPackage):
    """Bindings to Selected 'liblwgeom' Functions for Simple Features.

    Access to selected functions found in 'liblwgeom'
    <https://github.com/postgis/postgis/tree/master/liblwgeom>, the
    light-weight geometry library used by 'PostGIS' <https://postgis.net/>."""

    cran = "lwgeom"

    license("GPL-2.0-only")

    version("0.2-14", sha256="26db6cf7dbc8cf43a70e5e2a34941a1c4b65e182f86f58d64ff9f614b3be929c")
    version("0.2-11", sha256="7fd73cf58981f9566d946bf63ed6575ea0c70634abeaf4e60ef9615040d63419")
    version("0.2-9", sha256="69b2a2efdafb0b32c801932eee7cd2c4b8402cede6487f4dfea4e14873091aa8")
    version("0.2-8", sha256="f48a92de222da0590b37a30d5cbf2364555044a842795f6b488afecc650b8b34")
    version("0.2-5", sha256="4a1d93f96c10c2aac173d8186cf7d7bef7febcb3cf066a7f45da32251496d02f")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-units", type=("build", "run"))
    depends_on("r-sf@0.6-0:", type=("build", "run"), when="@0.1-3:")
    depends_on("r-sf@0.9-0:", type=("build", "run"), when="@0.2-2:")
    depends_on("r-sf@0.9-3:", type=("build", "run"), when="@0.2-4:")
    depends_on("r-sf@1.0-15:", type=("build", "run"), when="@0.2-14:")
    depends_on("geos@3.5.0:")
    depends_on("proj@4.8.0:6.999")
    depends_on("sqlite", when="@0.2-8:")
