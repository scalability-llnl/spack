# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRstan(RPackage):
    """R Interface to Stan.

    User-facing R functions are provided to parse, compile, test, estimate, and
    analyze Stan models by accessing the header-only Stan library provided by
    the 'StanHeaders' package. The Stan project develops a probabilistic
    programming language that implements full Bayesian statistical inference
    via Markov Chain Monte Carlo, rough Bayesian inference via variational
    approximation, and (optionally penalized) maximum likelihood estimation via
    optimization. In all three cases, automatic differentiation is used to
    quickly and accurately evaluate gradients without burdening the user with
    the need to derive the partial derivatives."""

    cran = "rstan"

    license("GPL-3.0-or-later")

    version("2.32.6", sha256="3390d00191bbd3b0739dd19fe437b99a041a6b04be208877b48419d1348a1a70")
    version("2.21.8", sha256="b2d4edc315419037970c9fa2e8740b934966d88d40548152811f3d4a28475075")
    version("2.21.7", sha256="4495221310d390925b665c32e05ffabd3ae8857225bda65131a7ed2be41d6d45")
    version("2.21.5", sha256="86e4fe562d8ddcd0b02336f35a420fa8786dd21de7ca2bebb4ed6e9c252bb9ea")
    version("2.21.3", sha256="76bcbf1cb246a202e5680ea6e91bb4142ce19156e8960a9850f6ea0e206f92b1")
    version("2.21.2", sha256="e30e04d38a612e2cb3ac69b53eaa19f7ede8b3548bf82f7892a2e9991d46054a")
    version("2.19.2", sha256="31e4ceb9c327cd62873225097ffa538c2ac4cb0547c52271e52e4c7652d508da")
    version("2.18.2", sha256="4d75dad95610d5a1d1c89a4ddbaf4326462e4ffe0ad28aed2129f2d9292e70ff")
    version("2.17.2", sha256="a7b197e6e42f8f0c302da9205afc19a0261eaf6af1425854303d2ce6cbd36729")
    version("2.10.1", sha256="4d2040742607f8675633c6b8c0a2e810f2fe3077f9242b1edfd42642613a8294")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@2.18.1:")
    depends_on("r-stanheaders@2.18.1:", type=("build", "run"))
    depends_on("r-stanheaders@2.21.0:", type=("build", "run"), when="@2.21.2:")
    depends_on("r-stanheaders@2.32.0:", type=("build", "run"), when="@2.26.23:")
    depends_on("r-ggplot2@2.0.0:", type=("build", "run"))
    depends_on("r-ggplot2@3.0.0:", type=("build", "run"), when="@2.21.2:")
    depends_on("r-ggplot2@3.3.5:", type=("build", "run"), when="@2.26.23:")
    depends_on("r-inline", type=("build", "run"))
    depends_on("r-inline@0.3.19:", type=("build", "run"), when="@2.26.23:")
    depends_on("r-gridextra@2.0.0:", type=("build", "run"))
    depends_on("r-gridextra@2.3:", type=("build", "run"), when="@2.26.23:")
    depends_on("r-rcpp@0.12.0:", type=("build", "run"))
    depends_on("r-rcpp@1.0.7:", type=("build", "run"), when="@2.26.23:")
    depends_on("r-rcppparallel@5.0.1:", type=("build", "run"), when="@2.21.2:")
    depends_on("r-rcppparallel@5.1.4:", type=("build", "run"), when="@2.26.23:")
    depends_on("r-loo@2.0.0:", type=("build", "run"), when="@2.18:")
    depends_on("r-loo@2.3.0:", type=("build", "run"), when="@2.21.2:")
    depends_on("r-loo@2.4.1:", type=("build", "run"), when="@2.26.23:")
    depends_on("r-pkgbuild", type=("build", "run"), when="@2.18:")
    depends_on("r-pkgbuild@1.2.0:", type=("build", "run"), when="@2.26.23:")
    depends_on("r-quickjsr", type=("build", "run"), when="@2.26.23:")
    depends_on("r-rcppeigen@0.3.3.3.0:", type=("build", "run"))
    depends_on("r-rcppeigen@0.3.4.0.0:", type=("build", "run"), when="@2.26.23:")
    depends_on("r-bh@1.69.0:", type=("build", "run"))
    depends_on("r-bh@1.72.0-2:", type=("build", "run"), when="@2.21.2:")
    depends_on("r-bh@1.75.0-0:", type=("build", "run"), when="@2.26.23:")
    depends_on("gmake", type="build")
    depends_on("pandoc", type="build")

    depends_on("r-withr", type=("build", "run"), when="@2.21.2")
    depends_on("r-v8", type=("build", "run"), when="@2.21.2")

    conflicts("%gcc@:4.9", when="@2.18:")
