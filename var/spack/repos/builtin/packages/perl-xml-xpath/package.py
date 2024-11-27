# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlXpath(PerlPackage):
    """Parse and evaluate XPath statements."""

    homepage = "https://metacpan.org/pod/XML::XPath"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MANWAR/XML-XPath-1.48.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-2.0")

    version("1.48", sha256="7bc75be36b239e5b2e700a9570d2b53b43093d467f2abe6a743f9ff9093790cd")

    depends_on("perl@5.10.1:", type=("build", "link", "run", "test"))
    depends_on("perl-path-tiny@0.076:", type=("build", "link"))
    depends_on("perl-xml-parser@2.23:", type=("build", "run", "test"))
