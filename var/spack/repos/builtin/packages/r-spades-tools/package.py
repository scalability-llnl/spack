# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpadesTools(RPackage):
    """Tools for Spatially Explicit Discrete Event Simulation (SpaDES) Models.

    Provides GIS and map utilities, plus additional modeling tools for
    developing cellular automata, dynamic raster models, and agent based models
    in 'SpaDES'.  Included are various methods for spatial spreading, spatial
    agents, GIS operations, random map generation, and others. See
    '?SpaDES.tools' for an categorized overview of these additional tools."""

    cran = "SpaDES.tools"

    maintainers("dorton21")

    version("2.0.7", sha256="f1c62cc76ff75119ae54e35be81d5819a282c547f77292e4f392599465e7b2cf")
    version("1.0.1", sha256="6b0d69c8737ff06e2cf312ff94b298b81f4c50af2efd498a124b99ed66a2be9a")
    version("1.0.0", sha256="1172b96ada7052fcaa3a113ed31eeb1b67dba70f40fa74cbb378c6e75e9235dc")
    version("0.3.10", sha256="ba4c075b534caaca413e2e97711b5475c2679d9546c8fee4a07fb2bb94d52c94")
    version("0.3.9", sha256="84dc47f55ded58746dcb943fde97fa4a4b852e1d2f45949ab1914cf8454e00f3")
    version("0.3.6", sha256="661f8ee792874e7447be78103775b63f18ec69e773a7b275dd977adb406dd3e5")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r@3.6:", type=("build", "run"), when="@0.3.9:")
    depends_on("r@4.0:", type=("build", "run"), when="@0.3.10:")
    depends_on("r@4.2:", type=("build", "run"), when="@2.0.6:")
    depends_on("r-backports", type=("build", "run"))
    depends_on("r-checkmate@1.8.2:", type=("build", "run"))
    depends_on("r-data-table@1.10.4:", type=("build", "run"))
    depends_on("r-fpcompare@0.2.1:", type=("build", "run"))
    depends_on("r-rcpp@0.12.12:", type=("build", "run"))
    depends_on("r-reproducible@2.0.2:", type=("build", "run"), when="@2.0.0:")
    depends_on("r-reproducible@2.0.5:", type=("build", "run"), when="@2.0.1:")
    depends_on("r-reproducible@2.0.9:", type=("build", "run"), when="@2.0.5:")
    depends_on("r-terra", type=("build", "run"), when="@2.0.0:")

    depends_on("r-circstats@0.2-4:", type=("build", "run"), when="@:1.0.1")
    depends_on("r-fastmatch@1.1-0:", type=("build", "run"), when="@:1.0.1")
    depends_on("r-magrittr", type=("build", "run"), when="@:1.0.1")
    depends_on("r-quickplot", type=("build", "run"), when="@:1.0.1")
    depends_on("r-raster@2.5-8:", type=("build", "run"), when="@:1.0.1")
    depends_on("r-reproducible@0.2.0:", type=("build", "run"), when="@:0.3.6")
    depends_on("r-reproducible@1.2.7:", type=("build", "run"), when="@0.3.9")
    depends_on("r-require", type=("build", "run"), when="@0.3.10:1.0.1")
    depends_on("r-rgeos", type=("build", "run"), when="@:1.0.1")
    depends_on("r-sp@1.2-4:", type=("build", "run"), when="@:1.0.1")
