# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class DocbookXsl(Package):
    """DocBook XSLT 1.0 Stylesheets."""

    homepage = "https://github.com/docbook/xslt10-stylesheets"
    url      = "https://github.com/docbook/xslt10-stylesheets/releases/download/release%2F1.79.2/docbook-xsl-1.79.2.tar.bz2"

    version('1.79.2', sha256='316524ea444e53208a2fb90eeb676af755da96e1417835ba5f5eb719c81fa371')
    version('1.78.1', sha256='c98f7296ab5c8ccd2e0bc07634976a37f50847df2d8a59bdb1e157664700b467', url='https://sourceforge.net/projects/docbook/files/docbook-xsl/1.78.1/docbook-xsl-1.78.1.tar.bz2')

    depends_on('docbook-xml')

    patch('docbook-xsl-1.79.2-stack_fix-1.patch', when='@1.79.2')

    def install(self, spec, prefix):
        install_tree('.', prefix)

    @property
    def catalog(self):
        return os.path.join(self.prefix, 'catalog.xml')

    def setup_run_environment(self, env):
        catalog = self.catalog
        env.prepend_path('XML_CATALOG_FILES', catalog, separator=' ')

    def setup_dependent_build_environment(self, env, dependent_spec):
        catalog = self.catalog
        env.prepend_path("XML_CATALOG_FILES", catalog, separator=' ')
