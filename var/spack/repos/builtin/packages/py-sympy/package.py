# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySympy(PythonPackage):
    """SymPy is a Python library for symbolic mathematics."""
    homepage = "https://pypi.python.org/pypi/sympy"
    url      = "https://pypi.io/packages/source/s/sympy/sympy-0.7.6.tar.gz"

    version('1.4', sha256='71a11e5686ae7ab6cb8feb5bd2651ef4482f8fd43a7c27e645a165e4353b23e1')
    version('1.3', sha256='e1319b556207a3758a0efebae14e5e52c648fc1db8975953b05fff12b6871b54')
    version('1.1.1', sha256='ac5b57691bc43919dcc21167660a57cc51797c28a4301a6144eff07b751216a4')
    version('1.0', sha256='3eacd210d839e4db911d216a9258a3ac6f936992f66db211e22767983297ffae')
    version('0.7.6', sha256='dfa3927e9befdfa7da7a18783ccbc2fe489ce4c46aa335a879e49e48fc03d7a7')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-mpmath@0.19:', when='@1.0:', type=('build', 'run'))
