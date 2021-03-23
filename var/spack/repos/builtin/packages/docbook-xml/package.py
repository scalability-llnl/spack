# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class DocbookXml(Package):
    """Docbook DTD XML files."""

    homepage = "https://www.oasis-open.org/docbook"
    url      = "https://www.oasis-open.org/docbook/xml/4.5/docbook-xml-4.5.zip"
    list_url = "https://www.oasis-open.org/docbook/xml/"
    list_depth = 1

    version('4.5', sha256='4e4e037a2b83c98c6c94818390d4bdd3f6e10f6ec62dd79188594e26190dc7b4')
    version('4.3', sha256='23068a94ea6fd484b004c5a73ec36a66aa47ea8f0d6b62cc1695931f5c143464')

    def install(self, spec, prefix):
        install_tree('.', prefix)

    @property
    def catalog(self):
        return os.path.join(self.prefix, 'catalog.xml')

    def setup_run_environment(self, env):
        catalog = self.catalog
        env.set('XML_CATALOG_FILES', catalog, separator=' ')

    def setup_dependent_build_environment(self, env, dependent_spec):
        catalog = self.catalog
        env.set("XML_CATALOG_FILES", catalog, separator=' ')
