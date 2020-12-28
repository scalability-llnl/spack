# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAtomicwrites(PythonPackage):
    """Atomic file writes."""

    homepage = "https://github.com/untitaker/python-atomicwrites"
    url      = "https://pypi.io/packages/source/a/atomicwrites/atomicwrites-1.3.0.tar.gz"

    version('1.3.0', sha256='75a9445bac02d8d058d5e1fe689654ba5a6556a1dfd8ce6ec55a0ed79866cfa6')
    version('1.1.5', sha256='240831ea22da9ab882b551b31d4225591e5e447a68c5e188db5b89ca1d487585')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
