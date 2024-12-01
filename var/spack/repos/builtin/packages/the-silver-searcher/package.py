# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TheSilverSearcher(AutotoolsPackage):
    """Fast recursive grep alternative"""

    homepage = "https://geoff.greer.fm/ag/"
    url = "https://geoff.greer.fm/ag/releases/the_silver_searcher-0.32.0.tar.gz"

    license("Apache-2.0")

    version("2.2.0", sha256="d9621a878542f3733b5c6e71c849b9d1a830ed77cb1a1f6c2ea441d4b0643170")
    version("2.1.0", sha256="d4652bd91c3a05e87a15809c5f3f14ad2e5e1f80185af510e3fa4ad2038c15d4")
    version("0.32.0", sha256="944ca77e498f344b2bfbd8df6d5d8df7bbc1c7e080b50c0bab3d1a9a55151b60")
    version("0.30.0", sha256="b4bf9e50bf48bc5fde27fc386f7bcad8644ef15a174c862a10813e81bd127e69")

    depends_on("c", type="build")  # generated

    depends_on("pcre")
    depends_on("xz")
    depends_on("zlib-api")
    depends_on("pkgconfig", type="build")
