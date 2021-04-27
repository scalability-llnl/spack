# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyPathspec(PythonPackage):
    """pathspec extends the test loading and running features of unittest,
    making it easier to write, find and run tests."""

    pypi = "pathspec/pathspec-0.8.1.tar.gz"

    version('0.8.1', sha256='86379d6b86d75816baba717e64b1a3a3469deb93bb76d613c9ce79edc5cb68fd')
    version('0.3.4', sha256='7605ca5c26f554766afe1d177164a2275a85bb803b76eba3428f422972f66728')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
