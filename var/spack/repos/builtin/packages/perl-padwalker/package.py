# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPadwalker(PerlPackage):
    """play with other peoples' lexical variables"""

    homepage = "http://search.cpan.org/~robin/PadWalker-2.2/PadWalker.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RO/ROBIN/PadWalker-2.2.tar.gz"

    version('2.2', sha256='fc1df2084522e29e892da393f3719d2c1be0da022fdd89cff4b814167aecfea3')
