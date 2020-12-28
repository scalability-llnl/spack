# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIoString(PerlPackage):
    """Emulate file interface for in-core strings"""

    homepage = "http://search.cpan.org/~gaas/IO-String-1.08/String.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/IO-String-1.08.tar.gz"

    version('1.08', sha256='2a3f4ad8442d9070780e58ef43722d19d1ee21a803bf7c8206877a10482de5a0')
