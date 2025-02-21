# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RFda(RPackage):
    """Functional Data Analysis.

    These functions were developed to support functional data
    analysis as described in Ramsay, J. O. and Silverman, B. W. (2005)
    Functional Data Analysis. New York: Springer and in Ramsay, J. O.,
    Hooker, Giles, and Graves, Spencer (2009)."""

    cran = "fda"

    license("GPL-2.0-or-later")

    version("6.1.8", sha256="ef8d858a2879491aa2c441d171ba14462bf27852d16e8420fa49aab83f42c407")
    version("6.0.5", sha256="14445776fc65284cd6cae98e5b4dd14c2626d96db5f78c0fcc6aabce5419b8f1")
    version("6.0.3", sha256="205814b9812664e8201221f99e0e8391aa49dba2ae287dc404c57c0c492477d3")
    version("5.5.1", sha256="dcaa2f6ae226d35855bc79c6967f60d45404b984c0afaec215b139c4b8dea23a")

    depends_on("r@3.5:", type=("build", "run"))
    depends_on("r-fds", type=("build", "run"))
    depends_on("r-desolve", type=("build", "run"))

    depends_on("r-matrix", type=("build", "run"), when="@5.5.1")
