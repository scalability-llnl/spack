# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMatlab(RPackage):
    """MATLAB emulation package.

    Emulate MATLAB code using R."""

    cran = "matlab"

    license("Artistic-2.0")

    version("1.0.4.1", sha256="fc3fba560b73a9bf0a4f317340856c91af2c9dcc80f5df291f3f7e6d6ac4fd50")
    version("1.0.4", sha256="1988a2220703444a575f2bad4eb090a0da71478599eb53081dd7237b7ec216ea")
    version("1.0.2", sha256="a23dec736c51ae1864c1a53caac556a2f98e8020138a3b121badb0f5b7984154")

    depends_on("r@2.15:", type=("build", "run"))
