# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlEncodeLocale(PerlPackage):
    """Determine the locale encoding"""

    homepage = "http://search.cpan.org/~gaas/Encode-Locale-1.05/lib/Encode/Locale.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/Encode-Locale-1.05.tar.gz"

    version('1.05', sha256='176fa02771f542a4efb1dbc2a4c928e8f4391bf4078473bd6040d8f11adb0ec1')
