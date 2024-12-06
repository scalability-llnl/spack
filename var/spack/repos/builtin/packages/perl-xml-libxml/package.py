# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlLibxml(PerlPackage):
    """This module is an interface to libxml2, providing XML and HTML parsers
    with DOM, SAX and XMLReader interfaces, a large subset of DOM Layer 3
    interface and a XML::XPath-like interface to XPath API of libxml2. The
    module is split into several packages which are not described in this
    section; unless stated otherwise, you only need to use XML::LibXML; in your
    programs."""

    homepage = "https://metacpan.org/pod/XML::LibXML"
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/XML-LibXML-2.0201.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.0210", sha256="a29bf3f00ab9c9ee04218154e0afc8f799bf23674eb99c1a9ed4de1f4059a48d")
    version("2.0209", sha256="b4a5abbcd689aa2fbbc8b7b45339e961c4984e48108494eb6c282b4748222425")
    version("2.0201", sha256="e008700732502b3f1f0890696ec6e2dc70abf526cd710efd9ab7675cae199bc2")

    depends_on("c", type="build")  # generated

    depends_on("libxml2")
    depends_on("perl-xml-namespacesupport", type=("build", "run"))
    depends_on("perl-xml-sax", type=("build", "run"))
    depends_on("perl-xml-sax-base", type=("build", "run"))
    depends_on("perl-alien-libxml2", type="build")

    conflicts("%gcc@14:", when="@:2.0209")
