# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParseYapp(PerlPackage):
    """Parse::Yapp - Perl extension for generating and using LALR parsers."""

    homepage = "https://metacpan.org/pod/Parse::Yapp"
    url = "https://cpan.metacpan.org/authors/id/W/WB/WBRASWELL/Parse-Yapp-1.21.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.21", sha256="3810e998308fba2e0f4f26043035032b027ce51ce5c8a52a8b8e340ca65f13e5")

    depends_on("perl-extutils-makemaker", type="build")
