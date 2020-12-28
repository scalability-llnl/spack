# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    url      = "https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/XML-LibXML-2.0201.tar.gz"

    version('2.0201', sha256='e008700732502b3f1f0890696ec6e2dc70abf526cd710efd9ab7675cae199bc2')

    depends_on('libxml2')
    depends_on('perl-xml-namespacesupport', type=('build', 'run'))
    depends_on('perl-xml-sax', type=('build', 'run'))
    depends_on('perl-xml-sax-base', type=('build', 'run'))
    depends_on('perl-alien-libxml2', type='build')
