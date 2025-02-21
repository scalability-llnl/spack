# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQuantreg(RPackage):
    """Quantile Regression.

    Estimation and inference methods for models of conditional quantiles:
    Linear and nonlinear parametric and non-parametric (total variation
    penalized) models  for conditional quantiles of a univariate response and
    several methods for handling censored survival data.  Portfolio selection
    methods based on expected shortfall risk are also now included. See Koenker
    (2006) <doi:10.1017/CBO9780511754098> and Koenker et al. (2017)
    <doi:10.1201/9781315120256>."""

    cran = "quantreg"

    license("GPL-2.0-or-later")

    version("5.98", sha256="a98cb259d8cf563f66a25ae8858794e574dd40de6206816ad61b1ffeb9686a61")
    version("5.95", sha256="4b05a81eceebbd927372cefdc4912dfa70b6dfcd96528489f78e125eb32a96cc")
    version("5.94", sha256="52d585ccb972ed7726b7d083f5635d3e42915847398e00fd6e0f69a5fe1b17c1")
    version("5.93", sha256="d4a94984a500bf4c92dec21013441f001a4aa0541c4c651384e257a4b4e9e539")
    version("5.88", sha256="1940e553711ed50655b2692ba29432d1083ed83c2db06e31a031ce8f82823a3f")
    version("5.87", sha256="9ad7ef09e5f53b89ef09dea3a1aa25cfda9f3f2528994f874ec1cd9ca7fda38e")
    version("5.86", sha256="71d1c829af7574ca00575cc0375376ac3ecd54b3d6d36e8eecd71ed8acb9d605")
    version("5.82", sha256="eac34e1e34d00a24ed7cb6981af258a3afc561843c00501de3206b4540548c07")
    version("5.51", sha256="df1330d245f66ee6d924b209bd4c15d44ff8cce52667959ec0d299975428bdb1")
    version("5.42.1", sha256="4cc2b0883c52694e58fcfde83e30e4a54be9f4d9cbcf6138f6498cc8e0b3ccab")
    version("5.40", sha256="86e310a235009ab85635dfb8803c175f80a35892e237db2525c4ef37a98936eb")
    version("5.29", sha256="bb4638e8f295579afa5c40c4de7266a6ea9221436ba4ca802f94cdb43bf20f25")
    version("5.26", sha256="9d7403f7c5ee219ec155838648401a1c4915a46a74f5774a0f6876c537ef2c87")

    depends_on("r@2.6:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@5.93:")
    depends_on("r-sparsem", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-matrixmodels", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"), when="@5.93:")
    depends_on("r-mass", type=("build", "run"), when="@5.93:")

    depends_on("r-conquer", type=("build", "run"), when="@5.82:5.86")
