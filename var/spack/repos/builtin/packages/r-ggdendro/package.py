# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgdendro(RPackage):
    """Create Dendrograms and Tree Diagrams Using 'ggplot2'.

    This is a set of tools for dendrograms and tree plots using 'ggplot2'. The
    'ggplot2' philosophy is to clearly separate data from the presentation.
    Unfortunately the plot method for dendrograms plots directly to a plot
    device without exposing the data. The 'ggdendro' package resolves this by
    making available functions that extract the dendrogram plot data.  The
    package provides implementations for tree, rpart, as well as diana and
    agnes cluster diagrams."""

    cran = "ggdendro"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("0.2.0", sha256="1940c34ddb30083a4c3bc3be98b6b466dcc78e03ac22a32088744db8bff7aa69")
    version("0.1.23", sha256="3a33e988c4fe12eec540876ad8ba09bda998773b2d2a90e043ebae4a69fa8eb8")
    version("0.1.22", sha256="f0a65f3498c1abc3076df0fb56364b63bdf5d212d8931f85bcc6997510916b6a")
    version("0.1-20", sha256="125cae904fa5d426cccaf32ebe9c6297e9ef0c6fd3f19f61513834d03a0cf8ff")

    depends_on("r@3.5:", type=("build", "run"), when="@0.2.0:")
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-ggplot2@0.9.2:", type=("build", "run"))
