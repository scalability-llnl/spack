# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyomo(PythonPackage):
    """Pyomo is a Python-based open-source software package that supports a
       diverse set of optimization capabilities for formulating and analyzing
       optimization models."""

    homepage = "https://github.com/Pyomo/pyomo"
    url      = "https://github.com/Pyomo/pyomo/archive/5.6.6.tar.gz"

    version('5.6.6', sha256='9330956b9fb244351ce76aaaf88688b5bdd03eebb122020cbee7b46e198a4110')

    depends_on('python@2.7:2.9,3.4:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')
    depends_on('py-cython', type='build')

    depends_on('py-appdirs', type=('build', 'run'))
    depends_on('py-pyutilib@5.7.1:', type=('build', 'run'))
    depends_on('py-ply', type=('build', 'run'))
    depends_on('py-six@1.4:', type=('build', 'run'))
