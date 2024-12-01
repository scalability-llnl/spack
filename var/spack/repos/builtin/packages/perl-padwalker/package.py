# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPadwalker(PerlPackage):
    """play with other peoples' lexical variables"""

    homepage = "https://metacpan.org/pod/PadWalker"
    url = "http://search.cpan.org/CPAN/authors/id/R/RO/ROBIN/PadWalker-2.2.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.5", sha256="07b26abb841146af32072a8d68cb90176ffb176fd9268e6f2f7d106f817a0cd0")
    version("2.2", sha256="fc1df2084522e29e892da393f3719d2c1be0da022fdd89cff4b814167aecfea3")
