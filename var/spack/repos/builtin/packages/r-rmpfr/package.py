# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRmpfr(RPackage):
    """R MPFR - Multiple Precision Floating-Point Reliable.

    Arithmetic (via S4 classes and methods) for arbitrary precision floating
    point numbers, including transcendental ("special") functions. To this end,
    Rmpfr interfaces to the LGPL'ed MPFR (Multiple Precision Floating-Point
    Reliable) Library which itself is based on the GMP (GNU Multiple Precision)
    Library."""

    cran = "Rmpfr"

    version("0.9-5", sha256="bce9a2729efcd329a13910e2ecb4675b4626dd3322cd01b01cb835d516a5f31b")
    version("0.9-2", sha256="ed63da32f3b970900c87cdb728eb16ed9fb0c79114cdecdc09e573f50ff7175e")
    version("0.8-9", sha256="cfee5ab47d49c6433c372a267f7d849c8f7c61a84e00d08afb047eaafcdbbc8a")
    version("0.8-7", sha256="93c2db785ff705dcfc6fa7f0373c2426cdc2ef72ceb5b294edeb2952775f57d2")
    version("0.8-2", sha256="74f6af1738b2cd21e7f2564b4cc2c84d5473a3745ba88ec76355d07fdd61f700")
    version("0.7-2", sha256="ec1da6ec5292ea6ac95495c6a299591d367e520ae324719817fb884c865603ff")
    version("0.7-1", sha256="9b3021617a22b0710b0f1acc279290762317ff123fd9e8fd03f1449f4bbfe204")
    version("0.6-1", sha256="bf50991055e9336cd6a110d711ae8a91a0551b96f9eaab5fef8c05f578006e1c")

    depends_on("r@3.0.1:", type=("build", "run"))
    depends_on("r@3.1.0:", type=("build", "run"), when="@0.7-0")
    depends_on("r@3.3.0:", type=("build", "run"), when="@0.7-1:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.8-2:")
    depends_on("r@3.6.0:", type=("build", "run"), when="@0.9-2:")
    depends_on("r-gmp@0.5-8:", type=("build", "run"))
    depends_on("r-gmp@0.6-1:", type=("build", "run"), when="@0.8-2:")
    depends_on("gmp@4.2.3:")
    depends_on("mpfr@3.0.0:")
    depends_on("texlive@2019:", type="build")
