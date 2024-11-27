# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXlconnectjars(RPackage):
    """JAR Dependencies for the XLConnect Package.

    Provides external JAR dependencies for the XLConnect package."""

    cran = "XLConnectJars"

    version("0.2-15", sha256="bd6f48a72c3a02b7a5e9373bcfc671614bc793f41d7bb8f4f34115a89ff4f8c6")
    version("0.2-14", sha256="c675f0ccff0c3e56b2b1cc00d4d28bf8fdfa508266ac0ffab5c0641151dd7332")
    version("0.2-12", sha256="676bf430ec118355142b3ebe8ecdadcd0019f6e9ac17c7b79b770668eace6df2")
    version("0.2-9", sha256="e31dd189f24afad84abb8bd865c2353b0eccee60ac74ce9030b846789248474b")

    depends_on("r-rjava", type=("build", "run"))
    depends_on("java@6:")
