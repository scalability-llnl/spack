# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyTraits(PythonPackage):
    """Explicitly typed attributes for Python."""

    homepage = "https://docs.enthought.com/traits"
    url      = "https://pypi.io/packages/source/t/traits/traits-6.0.0.tar.gz"

    version('6.0.0', sha256='dbcd70166feca434130a1193284d5819ca72ffbc8dbce8deeecc0cebb41a3bfb')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
