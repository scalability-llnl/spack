# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Quartz(MavenPackage):
    """Quartz is a richly featured, open source job scheduling
    library that can be integrated within virtually any Java
    application - from the smallest stand-alone application
    to the largest e-commerce system."""

    homepage = "https://www.quartz-scheduler.org/"
    url = "https://github.com/quartz-scheduler/quartz/archive/v2.3.2.tar.gz"

    version("2.3.2", sha256="058c64777956aeaad3e79e2307f0f512c66d29acf026ea8373ad359050f6856c")
    version("2.3.1", sha256="3b92fc4d562bb428ebc4c1fc7cbb5b764830d8317c20a011fbcee42601b72415")

    depends_on("java@8", type=("build", "run"))
