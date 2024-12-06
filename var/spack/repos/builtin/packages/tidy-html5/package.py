# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TidyHtml5(CMakePackage):
    """Tidy is a console application for Mac OS X, Linux, Windows, UNIX, and more.
    It corrects and cleans up HTML and XML documents by fixing markup errors and
    upgrading legacy code to modern standards."""

    homepage = "https://www.html-tidy.org/"
    url = "https://github.com/htacg/tidy-html5/archive/5.6.0.tar.gz"

    version("5.7.28", sha256="5caa2c769204f506e24ea4986a45abe23f71d14f0fe968314f20065f342ffdba")
    version("5.6.0", sha256="08a63bba3d9e7618d1570b4ecd6a7daa83c8e18a41c82455b6308bc11fe34958")

    depends_on("cmake@2.8.12:", type="build")
