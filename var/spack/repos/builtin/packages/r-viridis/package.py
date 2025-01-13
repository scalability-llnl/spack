# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RViridis(RPackage):
    """Colorblind-Friendly Color Maps for R.

    Color maps designed to improve graph readability for readers with common
    forms of color blindness and/or color vision deficiency. The color maps are
    also perceptually-uniform, both in regular form and also when converted to
    black-and-white for printing. This package also contains 'ggplot2' bindings
    for discrete and continuous color and fill scales. A lean version of the
    package called 'viridisLite' that does not include the 'ggplot2' bindings
    can be found at <https://cran.r-project.org/package=viridisLite>."""

    cran = "viridis"

    license("MIT")

    version("0.6.5", sha256="862b5cb6be115deea0207cdd3c8bb33de28552cfdc29900777512fd488d0005c")
    version("0.6.2", sha256="69b58cd1d992710a08b0b227fd0a9590430eea3ed4858099412f910617e41311")
    version("0.5.1", sha256="ddf267515838c6eb092938133035cee62ab6a78760413bfc28b8256165701918")
    version("0.5.0", sha256="fea477172c1e11be40554545260b36d6ddff3fe6bc3bbed87813ffb77c5546cd")
    version("0.4.0", sha256="93d2ded68ed7cec5633c260dbc47051416147aae074f29ebe135cc329250b00e")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-viridislite@0.3.0:", type=("build", "run"))
    depends_on("r-viridislite@0.4.0:", type=("build", "run"), when="@0.6.2:")
    depends_on("r-ggplot2@1.0.1:", type=("build", "run"))
    depends_on("r-gridextra", type=("build", "run"))
