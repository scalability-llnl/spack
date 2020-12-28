# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMachotools(PythonPackage):
    """Python package for editing Mach-O headers using macholib"""

    homepage = "https://pypi.python.org/pypi/machotools"
    url = "https://pypi.io/packages/source/m/machotools/machotools-0.2.0.tar.gz"

    version('0.2.0', sha256='e3950fa263169087d44a3d0521a3267d5128efd1b85252670c7171955939ab58')

    depends_on('py-setuptools', type='build')
    depends_on('py-macholib', type=('build', 'run'))
