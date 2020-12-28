# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWcwidth(PythonPackage):
    """Measures number of Terminal column cells of wide-character codes"""

    homepage = "https://pypi.python.org/pypi/wcwidth"
    url      = "https://pypi.io/packages/source/w/wcwidth/wcwidth-0.1.7.tar.gz"

    version('0.1.7', sha256='3df37372226d6e63e1b1e1eda15c594bca98a22d33a23832a90998faa96bc65e')

    depends_on('py-setuptools', type='build')
