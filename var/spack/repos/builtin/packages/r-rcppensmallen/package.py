# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcppensmallen(RPackage):
    """Rcpp integration for the Ensmallen templated C++ mathematical    optimization library."""

    cran = "RcppEnsmallen"

    version(
        "0.2.21.1.1", sha256="87396e259666c8797a00c4255d912da58c7880313a8c4e7d48c6384eb6161956"
    )
    version(
        "0.2.19.0.1", sha256="b4a9bde4dde309a52a47b56790389ecab14fe64066098d2a38b1b588ba3d8631"
    )

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@0.2.20.0.1:")
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-rcpparmadillo@0.9.800.0.0:", type=("build", "run"))
