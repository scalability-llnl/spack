# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Conmon(MakefilePackage):
    """An OCI container runtime monitor"""

    homepage = "https://github.com/containers/conmon"
    url = "https://github.com/containers/conmon/archive/v2.0.30.tar.gz"
    maintainers("bernhardkaindl")

    license("Apache-2.0")

    version("2.1.12", sha256="842f0b5614281f7e35eec2a4e35f9f7b9834819aa58ecdad8d0ff6a84f6796a6")
    version("2.1.7", sha256="7d0f9a2f7cb8a76c51990128ac837aaf0cc89950b6ef9972e94417aa9cf901fe")
    version("2.1.5", sha256="ee3179ee2b9a9107acec00eb546062cf7deb847f135a3b81503d22b0d226b3ed")
    version("2.0.30", sha256="4b0a98fbe8a63c42f60edac25c19aa6606caa7b1e4fe7846fc7f7de0b566ba25")

    depends_on("c", type="build")  # generated

    depends_on("go", type="build")
    depends_on("go-md2man", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("libseccomp")
    depends_on("glib")

    def install(self, spec, prefix):
        make("install", "PREFIX=" + prefix)
