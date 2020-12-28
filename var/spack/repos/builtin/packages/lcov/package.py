# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Lcov(MakefilePackage):
    """LCOV is a graphical front-end for GCC's coverage testing tool gcov.
    It collects gcov data for multiple source files and creates HTML pages
    containing the source code annotated with coverage information. It also
    adds overview pages for easy navigation within the file structure. LCOV
    supports statement, function and branch coverage measurement."""

    homepage = "http://ltp.sourceforge.net/coverage/lcov.php"
    url      = "https://github.com/linux-test-project/lcov/releases/download/v1.14/lcov-1.14.tar.gz"

    version('1.15', sha256='c1cda2fa33bec9aa2c2c73c87226cfe97de0831887176b45ee523c5e30f8053a')
    version('1.14', sha256='14995699187440e0ae4da57fe3a64adc0a3c5cf14feab971f8db38fb7d8f071a')

    def install(self, spec, prefix):
        make("DESTDIR=", "PREFIX=%s" % prefix, "install")
