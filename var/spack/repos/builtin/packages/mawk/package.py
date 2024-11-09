# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mawk(AutotoolsPackage):
    """mawk is an interpreter for the AWK Programming Language."""

    homepage = "https://invisible-island.net/mawk/mawk.html"
    url = "https://invisible-mirror.net/archives/mawk/mawk-1.3.4.tgz"

    license("GPL-2.0-only")

    version(
        "1.3.4-20240123", sha256="a8e319a83744b1f1fb6988dfa189d61887f866e9140cc9a49eb003b2b0655e88"
    )
    version(
        "1.3.4-20171017", sha256="db17115d1ed18ed1607c8b93291db9ccd4fe5e0f30d2928c3c5d127b23ec9e5b"
    )
    version("1.3.4", sha256="2f2ab8831c441a5793ad333193c888c9ba29c900f009aa23c9fffc100c405925")

    depends_on("c", type="build")  # generated

    provides("awk")
