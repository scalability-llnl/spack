# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RA4reporting(RPackage):
    """Automated Affymetrix Array Analysis Reporting Package.

    Utility functions to facilitate the reporting of the Automated Affymetrix
    Array Analysis Reporting set of packages."""

    bioc = "a4Reporting"

    version("1.48.0", commit="de8c4b76f6b7ef502d77d55289df0d64fe70447c")
    version("1.46.0", commit="00b82d25bef4d518ae92f615d3a6f7931c0618dc")
    version("1.44.0", commit="bfe83507daf53e2e327474ea3012f0dc920efac1")
    version("1.42.0", commit="b0d715b9cdac80bc412f0a9a6b33941c4a7582bb")
    version("1.38.0", commit="cd3cf244e7a299b2485684ed15519cbbda1c590f")
    version("1.32.0", commit="8d781899c625892080eb50f322694dd640d5f792")
    version("1.30.0", commit="ae9b9ade45cfac2636d0445a7e0a029dfe3b9390")
    version("1.28.0", commit="0fe72f48374353c39479a45e5516d0709f8c9ef7")
    version("1.26.0", commit="cce201502e2d3b28fd2823b66d9f81b034dc7eaa")
    version("1.24.0", commit="bf22c4d50daf40fc9eaf8c476385bf4a24a5b5ce")

    depends_on("r-xtable", type=("build", "run"))

    depends_on("r-annaffy", type=("build", "run"), when="@:1.32.0")
