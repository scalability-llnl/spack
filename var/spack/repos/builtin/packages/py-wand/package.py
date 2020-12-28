# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWand(PythonPackage):
    """Wand is a ctypes-based simple ImageMagick binding for Python.
    """

    homepage = "http://docs.wand-py.org"
    url      = "https://pypi.io/packages/source/W/Wand/Wand-0.5.6.tar.gz"

    version('0.5.6', sha256='d06b59f36454024ce952488956319eb542d5dc65f1e1b00fead71df94dbfcf88')
    version('0.4.2', sha256='a0ded99a9824ddd82617a4b449164e2c5c93853aaff96f9e0bab8b405d62ca7c')

    variant('docs', default=False, description='Build docs')

    depends_on('py-setuptools', type='build')
    # provides libmagickwand
    depends_on('imagemagick')
    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))

    depends_on('py-sphinx@1:', type='build', when='+docs')
