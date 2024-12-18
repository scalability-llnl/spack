# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jpegoptim(AutotoolsPackage):
    """jpegoptim - utility to optimize/compress JPEG files"""

    homepage = "https://www.iki.fi/tjko/projects.html"
    url = "https://github.com/tjko/jpegoptim/archive/RELEASE.1.4.6.tar.gz"

    license("GPL-2.0-or-later")

    version("1.4.6", sha256="c44dcfac0a113c3bec13d0fc60faf57a0f9a31f88473ccad33ecdf210b4c0c52")
    version("1.4.5", sha256="53207f479f96c4f792b3187f31abf3534d69c88fe23720d0c23f5310c5d2b2f5")
    version("1.4.4", sha256="bc6b018ae8c3eb12d07596693d54243e214780a2a2303a6578747d3671f45da3")

    depends_on("c", type="build")  # generated

    depends_on("libjpeg")
