# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpentuner(PythonPackage):
    """An extensible framework for program autotuning."""

    homepage = "http://opentuner.org/"
    git      = "https://github.com/jansel/opentuner.git"

    maintainers = ['matthiasdiener']

    version('0.8.2', commit='8e720a2')
    version('0.8.0', commit='4cb9135')

    depends_on('python@3:', type=('build', 'run'), when='@0.8.1:')
    depends_on('python@2.7:2.8', type=('build', 'run'), when='@:0.8.0')

    depends_on('py-argparse@1.2.1:', type=('build', 'run'))
    depends_on('py-fn-py@0.2.12:', type=('build', 'run'))
    depends_on('py-future', type=('build', 'run'))
    depends_on('py-numpy@1.8.0:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-sqlalchemy@0.8.2:', type=('build', 'run'))
