# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxRemovedIn(PythonPackage):
    """This is a Sphinx extension which recognizes the
    .. versionremoved:: and .. removed-in directives.
    These are missing from Sphinx'es core markup.
    """

    homepage = "https://github.com/MrSenko/sphinx-removed-in"
    url      = "https://pypi.io/packages/source/s/sphinx-removed-in/sphinx-removed-in-0.2.0.tar.gz"

    version('0.2.0', sha256='bdba7f212c1abd99a9e9c2144c75a41edca02e71dfbb77653be39abe2cb19087')

    depends_on('py-setuptools', type='build')
    depends_on('py-sphinx', type=('build', 'run'))
