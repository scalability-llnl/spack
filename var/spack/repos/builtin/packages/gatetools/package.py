# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gatetools(PythonPackage):
    """Python tools for GATE, see https://github.com/OpenGATE/Gate"""

    homepage = "https://github.com/OpenGATE/GateTools"
    pypi     = "gatetools/gatetools-0.9.14.tar.gz"

    maintainers = ['glennpj']

    version('0.9.14', sha256='78fe864bb52fd4c6aeeee90d8f6c1bc5406ce02ac6f48712379efac606b5c006')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-pydicom', type=('build', 'run'))
    depends_on('py-tqdm', type=('build', 'run'))
    depends_on('py-colored', type=('build', 'run'))
    depends_on('py-itk@5.1.0:', type=('build', 'run'))
    depends_on('py-uproot3', type=('build', 'run'))
    depends_on('py-wget', type=('build', 'run'))
    depends_on('gate+rtk', type='run')

    # The readme.md file is not in the distribution, so fake it.
    @run_before('build')
    def readme(self):
        touch('readme.md')
