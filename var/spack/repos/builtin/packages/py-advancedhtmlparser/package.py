# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAdvancedhtmlparser(PythonPackage):
    """Fast Indexed python HTML parser which builds a DOM node tree,
    providing common getElementsBy* functions for scraping, testing,
    modification, and formatting"""

    homepage = "https://github.com/kata198/AdvancedHTMLParser"
    url      = "https://pypi.io/packages/source/a/advancedhtmlparser/AdvancedHTMLParser-8.1.4.tar.gz"

    version('8.1.4', sha256='21a73137026c8ec3248c654a24cc40064196029256cdf71681149f6835e9ed39')

    depends_on('py-setuptools', type='build')
    depends_on('py-queryablelist', type=('build', 'run'))
