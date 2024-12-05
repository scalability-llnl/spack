# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParsetemplate(PerlPackage):
    """Parse::Template - Processor for templates containing Perl expressions."""

    homepage = "https://metacpan.org/pod/Parse::Template"
    url = "https://cpan.metacpan.org/authors/id/P/PS/PSCUST/ParseTemplate-3.08.tar.gz"

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("3.08", sha256="3c7734f53999de8351a77cb09631d7a4a0482b6f54bca63d69d5a4eec8686d51")
