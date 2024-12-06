# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestXml(PerlPackage):
    """Compare XML in perl tests"""

    homepage = "https://metacpan.org/pod/Test::XML"
    url = "https://cpan.metacpan.org/authors/id/S/SE/SEMANTICO/Test-XML-0.08.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.08", sha256="eb54cc23cdec860d3ad8ac8a697cbf038d0dec95229912d975c301890ca83ee2")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-xml-parser@2.34:", type=("build", "run", "test"))
    depends_on("perl-xml-semanticdiff@0.95:", type=("build", "run", "test"))
