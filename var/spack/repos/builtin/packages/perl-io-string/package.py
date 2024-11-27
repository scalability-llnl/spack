# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIoString(PerlPackage):
    """Emulate file interface for in-core strings"""

    homepage = "https://metacpan.org/pod/IO::String"
    url = "http://search.cpan.org/CPAN/authors/id/G/GA/GAAS/IO-String-1.08.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.08", sha256="2a3f4ad8442d9070780e58ef43722d19d1ee21a803bf7c8206877a10482de5a0")
