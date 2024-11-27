# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Libid3tag(AutotoolsPackage):
    """library for id3 tagging"""

    homepage = "https://www.underbit.com/products/mad/"
    url = "ftp://ftp.mars.org/pub/mpeg/libid3tag-0.15.1b.tar.gz"

    maintainers("TheQueasle")

    license("GPL-2.0-or-later")

    version("0.15.1b", sha256="63da4f6e7997278f8a3fef4c6a372d342f705051d1eeb6a46a86b03610e26151")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")
    depends_on("gperf")

    # source: https://git.archlinux.org/svntogit/packages.git/tree/trunk/10_utf16.diff?h=packages/libid3tag
    patch("10_utf16.diff")
    # source: https://git.archlinux.org/svntogit/packages.git/tree/trunk/11_unknown_encoding.diff?h=packages/libid3tag
    patch("11_unknown_encoding.dif")
    # source: https://git.archlinux.org/svntogit/packages.git/tree/trunk/CVE-2008-2109.patch?h=packages/libid3tag
    patch("CVE-2008-2109.patch", level=0)
    # source: https://git.archlinux.org/svntogit/packages.git/tree/trunk/libid3tag-gperf.patch?h=packages/libid3tag
    patch("libid3tag-gperf.patch", when="^gperf@3.1:")

    @run_before("configure")
    def preclean(self):
        """
        Remove compat.c and frametype.c in order to regenerate from gperf
        sources
        """
        os.remove("compat.c")
        os.remove("frametype.c")
