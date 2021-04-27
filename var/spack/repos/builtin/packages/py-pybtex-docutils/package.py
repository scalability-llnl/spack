# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyPybtexDocutils(PythonPackage):
    """A docutils backend for pybtex."""

    pypi = "pybtex-docutils/pybtex-docutils-0.2.1.tar.gz"

    version('0.2.2', sha256='ea90935da188a0f4de2fe6b32930e185c33a0e306154322ccc12e519ebb5fa7d')
    version('0.2.1', sha256='e4b075641c1d68a3e98a6d73ad3d029293fcf9e0773512315ef9c8482f251337')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-docutils@0.8:', type=('build', 'run'))
    depends_on('py-pybtex@0.16:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
