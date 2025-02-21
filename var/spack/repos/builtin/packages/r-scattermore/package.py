# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScattermore(RPackage):
    """Scatterplots with More Points.

    C-based conversion of large scatterplot data to rasters. Speeds up plotting
    of data with millions of points."""

    cran = "scattermore"

    license("GPL-3.0-or-later")

    version("1.2", sha256="5534a87b0bdd1375f0fbffc1a5c980ad64e33a108435a67469b8324b580602d1")
    version("0.8", sha256="dbdd73d8261cb063464bb29d5c17733b7e87bc50a19948bc80439e19f2a9f8e5")
    version("0.7", sha256="f36280197b8476314d6ce81a51c4ae737180b180204043d2937bc25bf3a5dfa2")

    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
