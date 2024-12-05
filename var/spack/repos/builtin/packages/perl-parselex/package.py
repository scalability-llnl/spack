# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParselex(PerlPackage):
    """Parse::Lex - Generator of lexical analyzers - moving pointer inside text."""

    homepage = "https://metacpan.org/pod/Parse::Lex"
    url = "https://cpan.metacpan.org/authors/id/P/PS/PSCUST/ParseLex-2.21.tar.gz"

    version("2.21", sha256="f55f0a7d1e2a6b806a47840c81c16d505c5c76765cb156e5f5fd703159a4492d")
