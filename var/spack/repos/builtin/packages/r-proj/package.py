# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProj(RPackage):
    """Generic Coordinate System Transformations Using 'PROJ'.

    A wrapper around the generic coordinate transformation software 'PROJ'
    that transforms coordinates from one coordinate reference system ('CRS')
    to another. This includes cartographic projections as well as geodetic
    transformations.  The intention is for this package to be used by
    user-packages such as 'reproj', and that the older 'PROJ.4' and version 5
    pathways be provided by the 'proj4' package."""

    cran = "PROJ"

    version("0.5.0", sha256="fa6316693289a65d53a764b422f15072c34f440375264b822f2ddd2c6ec88c9b")
    version("0.4.0", sha256="dde90cfeca83864e61a7422e1573d2d55bb0377c32b9a8f550f47b8631121ce7")
    version("0.1.0", sha256="5186f221335e8092bbcd4d82bd323ee7e752c7c9cf83d3f94e4567e0b407aa6f")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@3.0.2:", type=("build", "run"), when="@0.4.0:")

    depends_on("r-lifecycle", type=("build", "run"), when="@0.5.0:")
    depends_on("r-wk", type=("build", "run"), when="@0.5.0:")

    depends_on("proj@6.3.1:", type=("build", "run"), when="@0.4.5:")
    # pkgconfig for proj requires libtiff-4 and libcurl
    depends_on("libtiff@4", type=("build", "run"))
    depends_on("curl", type=("build", "run"))

    def setup_build_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.spec["proj"].prefix.lib)
