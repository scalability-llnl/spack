# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CubeBlade(AutotoolsPackage):
    """Simple OTF2 trace explorer"""

    homepage = "https://www.scalasca.org/software/cube-4.x/download.html"
    url = "https://apps.fz-juelich.de/scalasca/releases/cube/4.8/dist/blade-v0.5.tar.gz"
    maintainers("swat-jsc")

    version("0.5", sha256="0770cd4c2e1b8f31bdb6dadf39232b709aee869835e12f9e1ac670d0b276a689")
    version("0.4", sha256="fae8214a76d98991d300a33384f7ffe2fbe6e0f7760bb62ae592ae5b215d389f")
    version("0.3", sha256="0320cb86d492c85c7cf74677bd467217def0422ef38f46b7108ee592db6f6deb")
    version(
        "0.2",
        sha256="ab3c5bbca79e2ec599166e75b3c96a8f6a18b3064414fc39e56f78aaae9c165c",
        deprecated=True,
    )

    depends_on("cube@4.8:+gui", when="@0.5:")
    depends_on("cube@4.7:+gui", when="@0.4:")
    depends_on("cube@4.6:+gui", when="@0.3:")
    depends_on("cubelib@4.8:")
    depends_on("qt@5.9.1:")
    depends_on("otf2@3.0:")

    # Without this patch, the Blade plugin crashes Cube on startup
    patch("return-bool.patch")
