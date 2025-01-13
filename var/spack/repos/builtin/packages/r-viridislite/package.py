# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RViridislite(RPackage):
    """Colorblind-Friendly Color Maps (Lite Version).

    Color maps designed to improve graph readability for readers with common
    forms of color blindness and/or color vision deficiency. The color maps are
    also perceptually-uniform, both in regular form and also when converted to
    black-and-white for printing. This is the 'lite' version of the 'viridis'
    package that also contains 'ggplot2' bindings for discrete and continuous
    color and fill scales and can be found at
    <https://cran.r-project.org/package=viridis>."""

    cran = "viridisLite"

    version("0.4.2", sha256="893f111d31deccd2cc959bc9db7ba2ce9020a2dd1b9c1c009587e449c4cce1a1")
    version("0.4.1", sha256="a896db1ccae5fc1a8b3764d02f24cef74ef7a8341cf9f3401c4efe799870ea97")
    version("0.4.0", sha256="849955dc8ad9bc52bdc50ed4867fd92a510696fc8294e6971efa018437c83c6a")
    version("0.3.0", sha256="780ea12e7c4024d5ba9029f3a107321c74b8d6d9165262f6e64b79e00aa0c2af")
    version("0.2.0", sha256="2d4d909f21c51e720bd685f05041ba158294e0a4064e0946d0bd916709818694")

    depends_on("r@2.10:", type=("build", "run"))
