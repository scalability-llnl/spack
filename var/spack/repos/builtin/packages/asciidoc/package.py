# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Asciidoc(AutotoolsPackage):
    """A presentable text document format for writing articles, UNIX man
    pages and other small to medium sized documents."""

    homepage = "http://asciidoc.org"
    url      = "http://downloads.sourceforge.net/project/asciidoc/asciidoc/8.6.9/asciidoc-8.6.9.tar.gz"

    version('8.6.9', sha256='78db9d0567c8ab6570a6eff7ffdf84eadd91f2dfc0a92a2d0105d323cab4e1f0')

    depends_on('libxml2')
    depends_on('libxslt')
    depends_on('docbook-xml')
    depends_on('docbook-xsl')
