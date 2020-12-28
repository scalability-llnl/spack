# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGuiqwt(PythonPackage):
    """guiqwt is a set of tools for curve and image plotting
    (extension to PythonQwt)"""

    homepage = "https://github.com/PierreRaybaut/guiqwt"
    url      = "https://pypi.io/packages/source/g/guiqwt/guiqwt-3.0.2.zip"

    version('3.0.2', sha256='387c0b9430624ecc87931e33ff963785194968c9f848337eb050eca48c6cd858')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.3:',       type=('build', 'run'))
    depends_on('py-scipy@0.7:',       type=('build', 'run'))
    depends_on('py-guidata@1.7.0:',   type=('build', 'run'))
    depends_on('py-pythonqwt@0.5.0:', type=('build', 'run'))
    depends_on('pil',                 type=('build', 'run'))
