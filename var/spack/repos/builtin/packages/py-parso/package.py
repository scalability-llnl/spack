# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParso(PythonPackage):
    """Parso is a Python parser that supports error recovery and round-trip parsing
       for different Python versions (in multiple Python versions).
       Parso is also able to list multiple syntax errors
       in your python file."""

    homepage = "https://pypi.org/project/parso/"
    url      = "https://pypi.io/packages/source/p/parso/parso-0.6.1.tar.gz"

    version('0.6.1', sha256='56b2105a80e9c4df49de85e125feb6be69f49920e121406f15e7acde6c9dfc57')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools',    type='build')
