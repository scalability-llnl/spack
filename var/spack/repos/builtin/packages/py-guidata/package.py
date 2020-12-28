# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGuidata(PythonPackage):
    """Automatic graphical user interfaces generation for easy dataset editing
    and display"""

    homepage = "https://github.com/PierreRaybaut/guidata"
    url      = "https://pypi.io/packages/source/g/guidata/guidata-1.7.5.zip"

    version('1.7.5', sha256='531d5e9ea784120c2e14212cfbd9c63f78fc7a77bcb9c5497be984584ee455c0')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyqt4', type=('build', 'run'))
    depends_on('py-spyder@2.0:2.9.9', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
