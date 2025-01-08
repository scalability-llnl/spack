# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVcd(RPackage):
    """Visualizing Categorical Data.

    Visualization techniques, data sets, summary and inference procedures aimed
    particularly at categorical data. Special emphasis is given to highly
    extensible grid graphics. The package was package was originally inspired
    by the book "Visualizing Categorical Data" by Michael Friendly and is now
    the main support package for a new book, "Discrete Data Analysis with R" by
    Michael Friendly and David Meyer (2015)."""

    cran = "vcd"

    license("GPL-2.0-only")

    version("1.4-12", sha256="c931ef115529931cddb1d5caec4d4d3569ebf12aadde719b2f5019812c9ded88")
    version("1.4-11", sha256="7a54e855689e1429d46e0d4d7a956f96b0ad2fd0c7084fa023902c55849e0932")
    version("1.4-10", sha256="7188192afa289350cc1b89790f4f8f5a5114c1c88bee7715a0c8f5347aa0b35b")
    version("1.4-9", sha256="a5b420ad5ff1a27fa92f98099a8b43f2dded7e5f60297b3e4d947ad6f039568f")
    version("1.4-8", sha256="236fcb183152f6e9d131eeb3931d5a064a5ff79be91e4533df9148fd2ff41e0c")
    version("1.4-4", sha256="a561adf120b5ce41b66e0c0c321542fcddc772eb12b3d7020d86e9cd014ce9d2")
    version("1.4-3", sha256="17ce89927421d9cd01285b6093eeaaecb1e7252388007f66d3b9222e58cc5f15")
    version("1.4-1", sha256="af4c77522efef28271afab7d90679824826132c6bc61abe17df763ed1fc24994")

    depends_on("r@2.4.0:", type=("build", "run"))
    depends_on("r@2.10:", type=("build", "run"), when="@1.4-11:")
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-colorspace", type=("build", "run"))
    depends_on("r-lmtest", type=("build", "run"))
