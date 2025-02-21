# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpades(RPackage):
    """Develop and Run Spatially Explicit Discrete Event Simulation Models.

    Metapackage for implementing a variety of event-based models, with a focus
    on spatially explicit models. These include raster-based, event-based, and
    agent-based models. The core simulation components (provided by
    'SpaDES.core') are built upon a discrete event simulation (DES; see Matloff
    (2011) ch 7.8.3 <https://nostarch.com/artofr.htm>) framework that
    facilitates modularity, and easily enables the user to include additional
    functionality by running user-built simulation modules (see also
    'SpaDES.tools'). Included are numerous tools to visualize rasters and other
    maps (via 'quickPlot'), and caching methods for reproducible simulations
    (via 'reproducible'). Tools for running simulation experiments are provided
    by 'SpaDES.experiment'. Additional functionality is provided by the
    'SpaDES.addins' and 'SpaDES.shiny' packages."""

    cran = "SpaDES"

    maintainers("dorton21")

    version("2.0.11", sha256="a88e202d1fe6fa700dfc176018a07cc5dd9ac9a8d0695eb6bc507ace52b68a32")
    version("2.0.9", sha256="f68080318bc922c6d8c495e6d963acdbb24dc90a3e8013e3e2f894b40a584c85")
    version("2.0.8", sha256="2230704f700d07bda25a23ab5c6630a093c9ed2fe3c47ab6294eebaf1d86f03f")
    version("2.0.7", sha256="5b62e9d701aa178be57f22369a5d043c9793a1bd3dcd4acac18c5a6b906ed8a0")
    version("2.0.6", sha256="0fa59d1737c67abeb04eae894939bc4700f92d6c2cc2ec3489b4650720ede5a3")

    depends_on("r@3.6:", type=("build", "run"))
    depends_on("r@4.0:", type=("build", "run"), when="@2.0.8:")
    depends_on("r@4.2:", type=("build", "run"), when="@2.0.10:")
    depends_on("r-quickplot", type=("build", "run"))
    depends_on("r-quickplot@1.0.2:", type=("build", "run"), when="@2.0.10:")
    depends_on("r-reproducible@1.2.1.9007:", type=("build", "run"))
    depends_on("r-reproducible@1.2.2:", type=("build", "run"), when="@2.0.9:")
    depends_on("r-reproducible@2.0.10:", type=("build", "run"), when="@2.0.10:")
    depends_on("r-spades-core@1.0.4:", type=("build", "run"))
    depends_on("r-spades-core@2.0.3:", type=("build", "run"), when="@2.0.10:")
    depends_on("r-spades-tools", type=("build", "run"))
    depends_on("r-spades-tools@2.0.5:", type=("build", "run"), when="@2.0.10:")

    depends_on("r-spades-addins", type=("build", "run"), when="@:2.0.6")
