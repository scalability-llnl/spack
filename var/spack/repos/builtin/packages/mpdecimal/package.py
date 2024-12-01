# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mpdecimal(AutotoolsPackage):
    """mpdecimal is a package for correctly-rounded arbitrary precision
    decimal floating point arithmetic."""

    homepage = "https://www.bytereef.org/mpdecimal/"
    url = "https://www.bytereef.org/software/mpdecimal/releases/mpdecimal-2.4.2.tar.gz"
    list_url = "https://www.bytereef.org/mpdecimal/download.html"

    license("BSD-2-Clause")

    version("2.5.1", sha256="9f9cd4c041f99b5c49ffb7b59d9f12d95b683d88585608aa56a6307667b2b21f")
    version("2.4.2", sha256="83c628b90f009470981cf084c5418329c88b19835d8af3691b930afccb7d79c7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("gmake", type="build")

    @property
    def libs(self):
        # Suffix is .so, even on macOS
        return LibraryList(find(self.prefix.lib, "libmpdec.so"))
