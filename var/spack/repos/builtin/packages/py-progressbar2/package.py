# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyProgressbar2(PythonPackage):
    """A progress bar for Python 2 and Python 3"""

    homepage = "https://github.com/WoLpH/python-progressbar"
    url      = "https://pypi.io/packages/source/p/progressbar2/progressbar2-3.50.1.tar.gz"

    version('3.50.1', sha256='2c21c14482016162852c8265da03886c2b4dea6f84e5a817ad9b39f6bd82a772')
    version('3.39.3', sha256='8e5b5419e04193bb7c3fea71579937bbbcd64c26472b929718c2fe7ec420fe39')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-python-utils@2.3.0:', type=('build', 'run'))
