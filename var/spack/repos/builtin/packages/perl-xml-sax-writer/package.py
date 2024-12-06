# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlSaxWriter(PerlPackage):
    """A new XML Writer was needed to match the SAX2 effort because quite
    naturally no existing writer understood SAX2. My first intention had been
    to start patching XML::Handler::YAWriter as it had previously been my
    favourite writer in the SAX1 world."""

    homepage = "https://metacpan.org/pod/XML::SAX::Writer"
    url = "https://cpan.metacpan.org/authors/id/P/PE/PERIGRIN/XML-SAX-Writer-0.57.tar.gz"

    license("Artistic-1.0")

    version("0.57", sha256="3d61d07ef43b0126f5b4de4f415a256fa859fa88dc4fdabaad70b7be7c682cf0")

    depends_on("perl-xml-filter-buffertext", type=("build", "run"))
    depends_on("perl-xml-namespacesupport", type=("build", "run"))
    depends_on("perl-xml-sax-base", type=("build", "run"))
