# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDismo(RPackage):
    """Species Distribution Modeling.

    Methods for species distribution modeling, that is, predicting the
    environmental similarity of any site to that of the locations of known
    occurrences of a species."""

    cran = "dismo"

    license("GPL-3.0-or-later")

    version("1.3-14", sha256="67a0f2e95562dd2aa612d52dfffab86985b52591a5ed7891b58b26667b394cd7")
    version("1.3-9", sha256="3924521db67716b004a4c870985c65d037edfe926b14222740fd6c2b2093beee")
    version("1.3-5", sha256="812e1932d42c0f40acf2ab5c5b2d068f93128caf648626e1d11baf1a09340ee7")
    version("1.3-3", sha256="fd65331ac18a4287ba0856b90508ddd0e2738c653eecc5f3eb2b14e1d06949ca")
    version("1.1-4", sha256="f2110f716cd9e4cca5fd2b22130c6954658aaf61361d2fe688ba22bbfdfa97c8")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.3-5:")
    depends_on("r@3.6.3:", type=("build", "run"), when="@1.3-9:")
    depends_on("r-raster@2.5-2:", type=("build", "run"))
    depends_on("r-raster@3.5-2:", type=("build", "run"), when="@1.3-5:")
    depends_on("r-raster@3.5-21:", type=("build", "run"), when="@1.3-9:")
    depends_on("r-sp@1.2-0:", type=("build", "run"))
    depends_on("r-sp@1.4-5:", type=("build", "run"), when="@1.3-5:")
    depends_on("r-terra@1.5-34:", type=("build", "run"), when="@1.3-9:")
    depends_on("r-rcpp", type=("build", "run"), when="@1.3-9:")
    depends_on("java@8:", when="@1.3-3:")
