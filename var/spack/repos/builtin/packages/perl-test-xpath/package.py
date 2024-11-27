# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestXpath(PerlPackage):
    """Test XML and HTML content and structure with XPath expressions"""

    homepage = "https://metacpan.org/pod/Test::XPath"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MANWAR/Test-XPath-0.20.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.20", sha256="dfaa611e7146ad9c9769b5bcf688949976b8372df7e787a40b933a148d892039")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-xml-libxml@1.70:", type=("build", "run", "test"))
