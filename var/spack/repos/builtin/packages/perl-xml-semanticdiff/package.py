# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlSemanticdiff(PerlPackage):
    """Perl extension for comparing XML documents."""

    homepage = "https://metacpan.org/pod/XML::SemanticDiff"
    url = "https://cpan.metacpan.org/authors/id/P/PE/PERIGRIN/XML-SemanticDiff-1.0007.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.0007", sha256="05fdefefbbc3f6b62fc7c9b5fabafb6b695ed68f0a3d958577251d1f0402a0f5")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
    depends_on("perl-xml-parser", type=("build", "run", "test"))
