# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Faketime(MakefilePackage):
    """libfaketime modifies the system time for a single application."""

    homepage = "https://github.com/wolfcw/libfaketime"
    url = "https://github.com/wolfcw/libfaketime/archive/refs/tags/v0.9.10.tar.gz"

    maintainers("wdconinc")

    license("GPL-2.0-only", checked_by="wdconinc")

    version("0.9.10", sha256="729ad33b9c750a50d9c68e97b90499680a74afd1568d859c574c0fe56fe7947f")

    depends_on("c", type="build")

    def edit(self, spec, prefix):
        for makefile in ["Makefile", "man/Makefile", "src/Makefile"]:
            FileFilter(makefile).filter("PREFIX .=.*", f"PREFIX = {prefix}")
