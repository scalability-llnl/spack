# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlDom(PerlPackage):
    """This module extends the XML::Parser module by Clark Cooper. The
    XML::Parser module is built on top of XML::Parser::Expat, which is a lower
    level interface to James Clark's expat library."""

    homepage = "https://metacpan.org/pod/XML::DOM"
    url = "https://cpan.metacpan.org/authors/id/T/TJ/TJMATHER/XML-DOM-1.46.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.46", sha256="8ba24b0b459b01d6c5e5b0408829c7d5dfe47ff79b3548c813759048099b175e")

    depends_on("perl-xml-parser", type=("build", "run"))
    depends_on("perl-xml-regexp", type=("build", "run"))
    depends_on("perl-libwww-perl", type=("build", "run"))
    depends_on("perl-libxml-perl", type=("build", "run"))
