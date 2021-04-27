# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWheel(PythonPackage):
    """A built-package format for Python."""

    homepage = "https://github.com/pypa/wheel"
    pypi = "wheel/wheel-0.34.2.tar.gz"

    version('0.36.2', sha256='e11eefd162658ea59a60a0f6c7d493a7190ea4b9a85e335b33489d9f17e0245e')
    version('0.35.1', sha256='99a22d87add3f634ff917310a3d87e499f19e663413a52eb9232c447aa646c9f')
    version('0.34.2', sha256='8788e9155fe14f54164c1b9eb0a319d98ef02c160725587ad60f14ddc57b6f96')
    version('0.33.4', sha256='62fcfa03d45b5b722539ccbc07b190e4bfff4bb9e3a4d470dd9f6a0981002565')
    version('0.33.1', sha256='66a8fd76f28977bb664b098372daef2b27f60dc4d1688cfab7b37a09448f0e9d')
    version('0.32.3', sha256='029703bf514e16c8271c3821806a1c171220cc5bdd325cbf4e7da1e056a01db6')
    version('0.29.0', sha256='1ebb8ad7e26b448e9caa4773d2357849bf80ff9e313964bcaf79cbf0201a1648')
    version('0.26.0', sha256='eaad353805c180a47545a256e6508835b65a8e830ba1093ed8162f19a50a530c')

    depends_on('python@2.7:2.8,3.5:', when='@0.34:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@0.30:', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.2:', type=('build', 'run'))
    depends_on('py-setuptools@40.9.0:', when='@0.34.1:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm@3.4:', when='@0.34.0', type='build')
