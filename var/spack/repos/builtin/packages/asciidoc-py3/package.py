# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AsciidocPy3(AutotoolsPackage):
    """Python 3 port of Asciidoc Python.
    AsciiDoc is a text document format for writing notes,
    documentation, articles, books, ebooks, slideshows,
    web pages, man pages and blogs. AsciiDoc files can
    be translated to many formats including HTML, PDF,
    EPUB, man page."""

    homepage = "https://github.com/asciidoc/asciidoc-py3"
    url      = "https://github.com/asciidoc/asciidoc-py3/releases/download/9.0.2/asciidoc-9.0.2.tar.gz"

    version('9.0.3', sha256='d99c8be8e8a9232742253c2d87c547b2efd4bbd3f0c1e23ef14898ad0fff77c4')
    version('9.0.2', sha256='185fd68e47034c4dd892e1d4ae64c81152bc049e9bdc7d1ad63f927d35810a3b')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('libxml2',     type=('build', 'run'))
    depends_on('libxslt',     type=('build', 'run'))
    depends_on('docbook-xml', type=('build', 'run'))
    depends_on('docbook-xsl', type=('build', 'run'))
