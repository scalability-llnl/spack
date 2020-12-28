# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKiwisolver(PythonPackage):
    """A fast implementation of the Cassowary constraint solver"""

    homepage = "https://github.com/nucleic/kiwi"
    url      = "https://pypi.io/packages/source/k/kiwisolver/kiwisolver-1.1.0.tar.gz"

    version('1.1.0', sha256='53eaed412477c836e1b9522c19858a8557d6e595077830146182225613b11a75')
    version('1.0.1', sha256='ce3be5d520b4d2c3e5eeb4cd2ef62b9b9ab8ac6b6fedbaa0e39cdb6f50644278')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
