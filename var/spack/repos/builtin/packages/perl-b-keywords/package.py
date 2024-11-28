# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlBKeywords(PerlPackage):
    """Lists of reserved barewords and symbol names"""

    homepage = "https://metacpan.org/pod/B::Keywords"
    url = "https://cpan.metacpan.org/authors/id/R/RU/RURBAN/B-Keywords-1.26.tar.gz"

    maintainers("EbiArnie")

    version("1.26", sha256="2daa155d2f267fb0dedd87f8a4c4fb5663879fc106517b1ee258353ef87aed34")
