# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGraphlayouts(RPackage):
    """Additional Layout Algorithms for Network Visualizations.

    Several new layout algorithms to visualize networks are provided which are
    not part of 'igraph'. Most are based on the concept of stress majorization
    by Gansner et al. (2004) <doi:10.1007/978-3-540-31843-9_25>. Some more
    specific algorithms allow to emphasize hidden group structures in networks
    or focus on specific nodes."""

    cran = "graphlayouts"

    license("MIT")

    version("1.1.1", sha256="7bc2459a02b1339ac01184a76687a3e50de5680f4699b5966a3f2e6a882f3801")
    version("0.8.4", sha256="778d8f7e190b05d0dbbaa7e6dbdfc0b8fef3c83b71333a6fa89926e6c04690fd")
    version("0.8.3", sha256="f9e4e5d794b4d1c6eba962490b3220d09b73e10893f5fa3be210240bfc654421")
    version("0.8.2", sha256="0fa2777a2c159f3ef1209cd96838d2651d144c9c971abfef1d22bc6376f47bec")
    version("0.8.0", sha256="d724266778e4d97ca7a762253c293ffa3d09e2627cb1c3c7a654c690819defd0")
    version("0.7.1", sha256="380f8ccb0b08735694e83f661fd56a0d592a78448ae91b89c290ba8582d66717")
    version("0.5.0", sha256="83f61ce07580c5a64c7044c12b20d98ccf138c7e78ff12855cdfc206e1fab10d")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-igraph", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-rcpparmadillo", type=("build", "run"))
