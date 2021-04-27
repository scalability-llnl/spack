# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyParticle(PythonPackage):
    """Particle provides a pythonic interface to the Particle Data Group (PDG)
    particle data tables and particle identification codes, with extended
    particle information and extra goodies."""

    git = "https://github.com/scikit-hep/particle.git"
    pypi = "particle/particle-0.11.0.tar.gz"
    homepage = "https://github.com/scikit-hep/particle"

    maintainers = ['vvolkl']

    tags = ['hep']

    version('master', branch='master')
    version('0.14.1', sha256='05b345f8fbfdb12a0aa744c788b6e1b22326b5a6ad95230596e0fc9ebad56621')
    version('0.11.0', sha256='e90dc36c8b7d7431bd14ee5a28486d28b6c0708555845d1d7bdf59a165405f12')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-attrs@19.2.0:', type=('build', 'run'))
    depends_on('py-hepunits@1.2.0:', type=('build', 'run'))
    depends_on('py-importlib-resources@1.0:', when='^python@:3.6', type=('build', 'run'))

    depends_on('py-enum34@1.1:', when='^python@:3.3', type=('build', 'run'))
    depends_on("py-typing@3.7:", when='^python@:3.4', type=('build', 'run'))
