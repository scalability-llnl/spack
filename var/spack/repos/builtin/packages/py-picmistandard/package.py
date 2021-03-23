# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPicmistandard(PythonPackage):
    """Standard input format for Particle-In-Cell codes"""

    homepage = "https://picmi-standard.github.io"
    git      = "https://github.com/picmi-standard/picmi.git"

    maintainers = ['ax3l', 'dpgrote', 'RemiLehe']

    version('develop', branch='master')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    build_directory = 'PICMI_Python'
