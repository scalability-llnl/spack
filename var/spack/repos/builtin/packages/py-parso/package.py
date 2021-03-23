# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyParso(PythonPackage):
    """Parso is a Python parser that supports error recovery and round-trip parsing
       for different Python versions (in multiple Python versions).
       Parso is also able to list multiple syntax errors
       in your python file."""

    pypi = "parso/parso-0.6.1.tar.gz"

    version('0.8.1', sha256='8519430ad07087d4c997fda3a7918f7cfa27cb58972a8c89c2a0295a1c940e9e')
    version('0.7.1', sha256='caba44724b994a8a5e086460bb212abc5a8bc46951bf4a9a1210745953622eb9')
    version('0.6.1', sha256='56b2105a80e9c4df49de85e125feb6be69f49920e121406f15e7acde6c9dfc57')
    version('0.4.0', sha256='2e9574cb12e7112a87253e14e2c380ce312060269d04bd018478a3c92ea9a376')

    depends_on('python@3.6:', type=('build', 'run'), when='@0.8.1:')
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'), when='@0.6.1:')
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'), when='@0.4.0:')
    depends_on('py-setuptools',    type='build')
