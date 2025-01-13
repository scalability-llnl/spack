# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGlobals(RPackage):
    """Identify Global Objects in R Expressions.

    Identifies global ("unknown" or "free") objects in R expressions by code
    inspection using various strategies, e.g. conservative or liberal. The
    objective of this package is to make it as simple as possible to identify
    global objects for the purpose of exporting them in distributed compute
    environments."""

    cran = "globals"

    license("LGPL-2.1-or-later")

    version("0.16.3", sha256="d73ced94248d8b81d29d774bdfc41496274d7da683a5d84440aed6a501a18c5b")
    version("0.16.2", sha256="682c26a95fa6c4e76a3a875be1a3192fc5b88e036c80dfa3b256add0336d770a")
    version("0.16.1", sha256="f7f63a575a3dd518c6afeabb4116bd26692a2a250df113059bc1a5b4711a1e95")
    version("0.15.0", sha256="f83689a420590b0d62b049c40a944c1c8c7202b3f1cc12102712c63104e99496")
    version("0.14.0", sha256="203dbccb829ca9cc6aedb6f5e79cb126ea31f8dd379dff9111ec66e3628c32f3")
    version("0.12.4", sha256="7985356ad75afa1f795f8267a20dee847020c0207252dc075c614cef55d8fe6b")

    depends_on("r@3.1.2:", type=("build", "run"))
    depends_on("r-codetools", type=("build", "run"))
