# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cmark(CMakePackage):
    """cmark is the C reference implementation of CommonMark,
    a rationalized version of Markdown syntax with a spec."""

    homepage = "https://commonmark.org/"
    url = "https://github.com/commonmark/cmark/archive/0.29.0.tar.gz"

    license("BSD-2-Clause")

    version("0.31.0", sha256="bbcb8f8c03b5af33fcfcf11a74e9499f20a9043200b8552f78a6e8ba76e04d11")
    version("0.29.0", sha256="2558ace3cbeff85610de3bda32858f722b359acdadf0c4691851865bb84924a6")
    version("0.28.3", sha256="acc98685d3c1b515ff787ac7c994188dadaf28a2d700c10c1221da4199bae1fc")
    version("0.28.2", sha256="fe4b04fcccb2dc72641096de02a8eefb53059e85f9dd904f0386dc86326cc414")
    version("0.28.1", sha256="dda7b8b5974815b7cbc8f12f509ad419250571f258ee697db2efe3deae01aaf8")
    version("0.28.0", sha256="68cf191f4a78494a43b7e1663506635e370f0ba4c67c9ee9518e295685bbfe0e")
    version("0.27.1", sha256="669b4c19355e8cb90139fdd03b02283b97130e92ea99a104552a2976751446b5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
