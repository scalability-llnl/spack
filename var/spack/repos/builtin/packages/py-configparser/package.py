# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConfigparser(PythonPackage):
    """This library brings the updated configparser from Python 3.5 to
    Python 2.6-3.5."""

    homepage = "https://docs.python.org/3/library/configparser.html"
    url      = "https://pypi.io/packages/source/c/configparser/configparser-3.5.0.tar.gz"

    version('3.5.1', sha256='f41e19cb29bebfccb1a78627b3f328ec198cc8f39510c7c55e7dfc0ab58c8c62')
    version('3.5.0', sha256='5308b47021bc2340965c371f0f058cc6971a04502638d4244225c49d80db273a')

    depends_on('py-setuptools', type='build')
    depends_on('py-ordereddict', when='^python@:2.6', type=('build', 'run'))
