# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Banner(AutotoolsPackage):
    """banner is a classic-style banner program similar to the one found
    in Solaris or AIX in the late 1990s.

    The banner program prints a short string to the console in very large letters."""

    homepage = "https://github.com/pronovic/banner"
    url = "https://github.com/pronovic/banner/archive/refs/tags/BANNER_V1.3.5.tar.gz"

    maintainers("cessenat")

    license("GPL-2.0-only")

    version("1.3.5", sha256="fb21c42620a0a668334b5732a6216b23b3990ca5d87cf3b15f0689dc617e7fdc")

    depends_on("c", type="build")  # generated

    def url_for_version(self, version):
        return "https://github.com/pronovic/banner/archive/refs/tags/BANNER_V{0}.tar.gz".format(
            version
        )
