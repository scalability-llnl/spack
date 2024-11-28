# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CubeBlade(AutotoolsPackage):
    """Simple OTF2 trace explorer"""

    homepage = "https://www.scalasca.org/software/cube-4.x/download.html"
    url = "https://apps.fz-juelich.de/scalasca/releases/cube/4.5/dist/blade-0.2.tar.gz"

    license("BSD-3-Clause")

    version("0.2", sha256="ab3c5bbca79e2ec599166e75b3c96a8f6a18b3064414fc39e56f78aaae9c165c")

    depends_on("cxx", type="build")  # generated

    depends_on("cube@4.5:")
    depends_on("cubelib@4.5:")
    depends_on("qt@5.9.1:")
    depends_on("otf2@2.1.1:")

    # Without this patch, the Blade plugin crashes Cube on startup
    patch("return-bool.patch")
