# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RReadr(RPackage):
    """Read Rectangular Text Data.

    The goal of 'readr' is to provide a fast and friendly way to read
    rectangular data (like 'csv', 'tsv', and 'fwf'). It is designed to flexibly
    parse many types of data found in the wild, while still cleanly failing
    when data unexpectedly changes."""

    cran = "readr"

    license("MIT")

    version("2.1.5", sha256="0fa65a5fe0a46cffe221b7696b52adb82dd4d7a692a895484e438e439594e10a")
    version("2.1.4", sha256="98144fa48c4fa61ef8c73ede8f87a2d2c5c44e9502b7875b266eb79984fbeb0d")
    version("2.1.3", sha256="d70dd55e80e87cf1387811fcdc3da92987a892ee75dae02f77ff074142618263")
    version("2.1.2", sha256="94afd03a1fa4abcf2985ec903bbf5995d7c590e1a50512ed80d081ef4fe10c1b")
    version("2.1.1", sha256="03937918a547e3a1587295f5e5f8c7f6865a4d04047d2b20c8d0f0701f1cbc84")
    version("2.0.2", sha256="98b05ed751dda2bcf7a29d070ce3d3e8475e0138a3e3ec68941dc45218db7615")
    version("1.4.0", sha256="02b1188aab8b2bc3f3d2bba5b946bd299610e87f3f7660c88b60b444093c46b9")
    version("1.3.1", sha256="33f94de39bb7f2a342fbb2bd4e5afcfec08798eac39672ee18042ac0b349e4f3")
    version("1.1.1", sha256="1a29b99009a06f2cee18d08bc6201fd4985b6d45c76cefca65084dcc1a2f7cb3")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@3.1:", type=("build", "run"), when="@1.3.0:")
    depends_on("r@3.4:", type=("build", "run"), when="@2.1.3:")
    depends_on("r@3.5:", type=("build", "run"), when="@2.1.4:")
    depends_on("r@3.6:", type=("build", "run"), when="@2.1.5:")
    depends_on("r-cli", type=("build", "run"), when="@1.4.0:")
    depends_on("r-cli@3.0.0:", type=("build", "run"), when="@2.1.2:")
    depends_on("r-cli@3.2.0:", type=("build", "run"), when="@2.1.3:")
    depends_on("r-clipr", type=("build", "run"), when="@1.2.0:")
    depends_on("r-crayon", type=("build", "run"), when="@1.3.1:")
    depends_on("r-hms@0.4.1:", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"), when="@1.4.0:")
    depends_on("r-lifecycle@0.2.0:", type=("build", "run"), when="@2:")
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"), when="@1.4.0:")
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-vroom@1.5.2:", type=("build", "run"), when="@2.0.0")
    depends_on("r-vroom@1.5.4:", type=("build", "run"), when="@2.0.1:")
    depends_on("r-vroom@1.5.6:", type=("build", "run"), when="@2.1.1:")
    depends_on("r-vroom@1.6.0:", type=("build", "run"), when="@2.1.3:")
    depends_on("r-cpp11", type=("build", "run"), when="@1.4.0:")
    depends_on("r-tzdb@0.1.1:", type=("build", "run"), when="@2:")

    depends_on("r-bh", type=("build", "run"), when="@:1")
    depends_on("r-rcpp@0.12.0.5:", type=("build", "run"), when="@:1.3.1")
