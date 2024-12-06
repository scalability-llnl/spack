# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RInteractivedisplaybase(RPackage):
    """Base package for enabling powerful shiny web displays of Bioconductor
    objects.

    The interactiveDisplayBase package contains the the basic methods needed
    to generate interactive Shiny based display methods for Bioconductor
    objects."""

    bioc = "interactiveDisplayBase"

    version("1.38.0", commit="3b3a3fdc4bafca767ae66c5f8869e2d93a9a4cb3")
    version("1.36.0", commit="79a0552bd467367866ceda2efc2b60a04a81f5fb")
    version("1.34.0", commit="fafbb13a42bb7549f17aa08cdb0e51728c5e825e")
    version("1.32.0", commit="0f88b2ac3689d51abb6ac0045b3207ca77963a5a")
    version("1.28.0", commit="a74c02c971c4f9c7086e14abd23f1a4190da4599")
    version("1.22.0", commit="4ce3cde1dabc01375c153ad614d77a5e28b96916")
    version("1.20.0", commit="f40912c8af7afbaaf68c003a6e148d81cbe84df6")
    version("1.18.0", commit="d07ea72a595877f27bf054f664f23e8f0304def8")
    version("1.16.0", commit="a86aa586b589497f5449d36c2ce67a6b6055026d")
    version("1.14.0", commit="e2ccc7eefdd904e3b1032dc6b3f4a28d08c1cd40")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-shiny", type=("build", "run"))
    depends_on("r-dt", type=("build", "run"), when="@1.28.0:")
