# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class F2c(MakefilePackage):
    """F2c converts Fortran 77 source code to C or C++ source files."""

    homepage = "https://www.netlib.org/f2c/"
    url = "https://www.netlib.org/f2c/src.tgz"

    version("master", sha256="d4847456aa91c74e5e61e2097780ca6ac3b20869fae8864bfa8dcc66f6721d35")

    depends_on("c", type="build")  # generated

    def url_for_version(self, version):
        url = "https://www.netlib.org/f2c/src.tgz"
        return url

    def edit(self, spec, prefix):
        copy("makefile.u", "makefile")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("f2c", prefix.bin)
        install("xsum", prefix.bin)
