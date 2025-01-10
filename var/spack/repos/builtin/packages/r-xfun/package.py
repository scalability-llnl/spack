# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXfun(RPackage):
    """Supporting Functions for Packages Maintained by 'Yihui Xie'.

    Miscellaneous functions commonly used in other packages maintained by
    'Yihui Xie'."""

    cran = "xfun"

    license("MIT")

    version("0.47", sha256="999874fdbf4df2e686a3cb134bfef782c0d3eb0141006191ca1eda94ce232c4b")
    version("0.39", sha256="d0ecaabb243dd3496da6029932fcdd4772914843de7ffd0b78a172efde1356c9")
    version("0.34", sha256="50e76c1febb988c044e44fb78e1abc1ba681173c9ff3c336f4c0ad71e6a2853d")
    version("0.33", sha256="45fbc2d252867b69bbde64d4a4e3d2e049ad1d3a84984e9cfb242d8d1f41ee6c")
    version("0.31", sha256="d169f3e682dab0c3f2ca381f2dba9b7014a5e2ca3d6863dbae3d1bca699ef235")
    version("0.29", sha256="bf85bb7b4653d03e0730682ffe1d6d3544ac0b36989f9196b2054d356c224ef4")
    version("0.24", sha256="e3e39a95202f6db4f6de3a8b9a344074a4944a3a8a522d44971390c905e2b583")
    version("0.20", sha256="284239d12a3d5ea7d1ef8b1382fb0a7a4661af54c85510501279681871da7c10")
    version("0.8", sha256="c2f8ecf8b57ddec02f9be7f417d9e22fc1ae2c7db8d70aa703fc62bf4a5c5416")

    depends_on("r@3.2.0:", when="@0.47:", type=("build", "run"))
