# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDevelSymdump(PerlPackage):
    """Devel::Symdump - dump symbol names or the symbol table"""

    homepage = "https://metacpan.org/pod/Devel::Symdump"
    url = "https://cpan.metacpan.org/authors/id/A/AN/ANDK/Devel-Symdump-2.0604.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.0604", sha256="1f9eaa557733f775ccaa852e846566274c017e6fee380aeb8d08e425cfa86d3e")
