# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpdep(RPackage):
    """Spatial Dependence: Weighting Schemes, Statistics.

    A collection of functions to create spatial weights matrix objects from
    polygon 'contiguities', from point patterns by distance and tessellations,
    for summarizing these objects, and for permitting their use in spatial data
    analysis, including regional aggregation by minimum spanning tree; a
    collection of tests for spatial 'autocorrelation', including global 'Morans
    I' and 'Gearys C' proposed by 'Cliff' and 'Ord' (1973, ISBN: 0850860369)
    and (1981, ISBN: 0850860814), 'Hubert/Mantel' general cross product
    statistic, Empirical Bayes estimates and 'Assuncao/Reis' (1999)
    <doi:10.1002/(SICI)1097-0258(19990830)18:16%3C2147::AID-SIM179%3E3.0.CO"""

    cran = "spdep"

    license("GPL-2.0-or-later")

    version("1.3-5", sha256="ba8efa06ddbc12408f4f6d4c85606d84922131d9c05953e0b23b81f03e56e626")
    version("1.2-8", sha256="8d9fb4cb10d1035526ad6d9f7a11972efb0e3137dcff176d73df6ebfe96c9190")
    version("1.2-7", sha256="9dac594825bf2d0aa31e845bfec05d8ce206327840fe455391741dbbdf9c9eea")
    version("1.2-4", sha256="a9f4d5af56efb1a2bcd3e85fe4d0e8a42896a2c30a790b2487e1ebadf398a677")
    version("1.2-2", sha256="94f46f98be3bedde1655f8768b7ef2a977c399b5ca8977c68007e9e3b7515e23")
    version("1.2-1", sha256="e8cc788d4e6fbb962f4e1fb45dff166cd9dd0935a9fd502699f9a95fdf4a43f9")
    version("1.1-5", sha256="47cb46cf5cf1f4386eb1b5e4d8541d577d7f2939e74addbdb884ecf2323f6d5d")
    version("1.1-2", sha256="ba0ca3a0ad6b9cc1dc46cadd9e79259949ad38c88f738e98e482d6c06640b31a")
    version("1.0-2", sha256="6f9efa4347d5c13b49922b75481ac403431c3c76a65a109af29954aa7bb138b2")
    version("0.6-13", sha256="ed345f4c7ea7ba064b187eb6b25f0ac46f17616f3b56ab89978935cdc67df1c4")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.3.0:", type=("build", "run"), when="@0.7-8:")
    depends_on("r-sp@1.0:", type=("build", "run"))
    depends_on("r-spdata@0.2.6.0:", type=("build", "run"), when="@1.0-2:")
    depends_on("r-spdata@2.3.1:", type=("build", "run"), when="@1.3-5:")
    depends_on("r-sf", type=("build", "run"), when="@1.0-2:")
    depends_on("r-deldir", type=("build", "run"))
    depends_on("r-boot@1.3-1:", type=("build", "run"))
    depends_on("r-units", type=("build", "run"), when="@1.2-1:")
    depends_on("r-s2", type=("build", "run"), when="@1.2-1:")
    depends_on("r-e1071", type=("build", "run"), when="@1.2-1:")

    depends_on("r-matrix", type=("build", "run"), when="@:1.1-5")
    depends_on("r-learnbayes", type=("build", "run"), when="@:1.1-5")
    depends_on("r-mass", type=("build", "run"), when="@:1.1-5")
    depends_on("r-coda", type=("build", "run"), when="@:1.1-5")
    depends_on("r-expm", type=("build", "run"), when="@:1.1-5")
    depends_on("r-gmodels", type=("build", "run"), when="@:1.1-5")
    depends_on("r-nlme", type=("build", "run"), when="@:1.1-5")
