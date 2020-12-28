# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenpmdValidator(PythonPackage):
    """Validator and Example Scripts for the openPMD markup.

    openPMD is an open standard for particle-mesh data files."""

    homepage = "http://www.openPMD.org"
    url      = "https://github.com/openPMD/openPMD-validator/archive/1.0.0.2.tar.gz"
    maintainers = ['ax3l']

    version('1.0.0.2', sha256='1b97452991feb0f0ac1ffb3c92b7f9743a86b0b5390dbbfb21160e04f0a35a95')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.6.1:', type=('build', 'run'))
    depends_on('py-python-dateutil@2.3.0:', type=('build', 'run'))
    depends_on('py-h5py@2.0.0:', type=('build', 'run'))
