# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgvis(RPackage):
    """Interactive Grammar of Graphics.

    An implementation of an interactive grammar of graphics, taking the best
    parts of 'ggplot2', combining them with the reactive framework from 'shiny'
    and web graphics from 'vega'."""

    cran = "ggvis"

    license("GPL-2.0-only OR custom")

    version("0.4.9", sha256="69b9d184789c90aedd2f336d43033a8b710a16b052580bf9e7ce229ac25ba12f")
    version("0.4.8", sha256="3d5480a0b97a57c26b595785f826b13d7695dab1f1dd8fcf5d7964fa8546a26a")
    version("0.4.7", sha256="9e6b067e11d497c796d42156570e2481afb554c5db265f42afbb74d2ae0865e3")
    version("0.4.4", sha256="1332ea122b768688c8a407a483be80febc4576de0ec8929077738421b27cafaf")
    version("0.4.3", sha256="34d517783016aaa1c4bef8972f4c06df5cd9ca0568035b647e60a8369043ecdc")
    version("0.4.2", sha256="2fcc2b6ca4fbdc69fe75a2c58c12cb43096ab418160c98367e5ac0fd19fc591d")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r-assertthat", type=("build", "run"))
    depends_on("r-jsonlite@0.9.11:", type=("build", "run"))
    depends_on("r-shiny@0.11.1:", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-dplyr@0.4.0:", type=("build", "run"))
    depends_on("r-dplyr@0.5.0:", type=("build", "run"), when="@0.4.7:")
    depends_on("r-rlang", type=("build", "run"), when="@0.4.7:")
    depends_on("r-htmltools@0.2.4:", type=("build", "run"))

    depends_on("r-lazyeval", type=("build", "run"), when="@:0.4.4")
