# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cscope(AutotoolsPackage):
    """Cscope is a developer's tool for browsing source code."""

    homepage = "https://cscope.sourceforge.net/"
    url = "https://sourceforge.net/projects/cscope/files/cscope/v15.9/cscope-15.9.tar.gz"

    license("BSD-3-Clause")

    version("15.9", sha256="c5505ae075a871a9cd8d9801859b0ff1c09782075df281c72c23e72115d9f159")
    version("15.8b", sha256="4889d091f05aa0845384b1e4965aa31d2b20911fb2c001b2cdcffbcb7212d3af")

    depends_on("c", type="build")  # generated

    depends_on("ncurses")

    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("pkgconfig", type="build")

    build_targets = ["CURSES_LIBS=-lncursesw -ltinfow"]

    def url_for_version(self, version):
        url = "https://sourceforge.net/projects/cscope/files/cscope/{0}{1}/cscope-{1}.tar.gz"
        if version >= Version("15.9"):
            return url.format("v", version)
        else:
            return url.format("", version)
