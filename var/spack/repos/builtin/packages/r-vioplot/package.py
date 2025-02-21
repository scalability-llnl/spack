# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVioplot(RPackage):
    """Violin Plot.

    A violin plot is a combination of a box plot and a kernel density plot.
    This package allows extensive customisation of violin plots."""

    cran = "vioplot"

    license("BSD-3-Clause")

    version("0.5.0", sha256="b04e91ccb810573d13a2ac1136bc6e4747c4c663fa53ff1ce7327c1a13530965")
    version("0.4.0", sha256="5729b483e3a4f7c81d2cc22c8bc5211b64e289734e9da5b5696c4974067867b5")
    version("0.3.7", sha256="06475d9a47644245ec91598e9aaef7db1c393802d9fc314420ac5139ae56adb6")
    version("0.3.5", sha256="1b64833c1bd6851036cf1c400c7d0036a047e71def94a399c897263b4b303e2a")
    version("0.3.2", sha256="7b51d0876903a3c315744cb051ac61920eeaa1f0694814959edfae43ce956e8e")

    depends_on("r+X", type=("build", "run"))
    depends_on("r-sm", type=("build", "run"))
    depends_on("r-zoo", type=("build", "run"))
