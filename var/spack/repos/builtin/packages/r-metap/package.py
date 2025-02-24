# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMetap(RPackage):
    """Meta-Analysis of Significance Values.

    The canonical way to perform meta-analysis involves using effect sizes.
    When they are not available this package provides a number of methods for
    meta-analysis of significance values including the methods of Edgington,
    Fisher, Lancaster, Stouffer, Tippett, and Wilkinson; a number of data-sets
    to replicate published results; and a routine for graphical display."""

    cran = "metap"

    license("GPL-2.0-only")

    version("1.11", sha256="34e8c9fc3ccaae23f57389001987de02339416f843084869f92ff635052093b7")
    version("1.8", sha256="ee9501a8de8a4c47af1632e6053e42ef53fc4b8bdf0f2759edc4d3eefaf5552b")
    version("1.7", sha256="d9b511607d0e37de4428549061c5577a4e812b0f55bb7ed887d1b24711f58c42")
    version("1.4", sha256="5fac23d823d0ad4eebc3f97620364e25f7b41f8d0c3579f6c09ec059940b85a5")
    version("1.1", sha256="20120428672d39dc15829c7e66850fc4350a34df290d48cef0b1cc78d13f7b82")

    depends_on("r@3.5.0:", type=("build", "run"), when="@1.7:")
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-rdpack", type=("build", "run"))
    depends_on("r-rdpack@0.7:", type=("build", "run"), when="@1.4:")
    depends_on("r-tfisher", type=("build", "run"), when="@1.4:")
    depends_on("r-mutoss", type=("build", "run"), when="@1.4:")
    depends_on("r-mathjaxr@0.8-3:", type=("build", "run"), when="@1.4:")
    depends_on("r-qqconf", type=("build", "run"), when="@1.8:")
