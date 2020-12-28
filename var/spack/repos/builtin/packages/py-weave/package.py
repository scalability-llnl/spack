# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWeave(PythonPackage):
    """Weave provides tools for including C/C++ code within Python code.

    Weave is the stand-alone version of the now-removed SciPy submodule
    ``scipy.weave``. It is Python 2.x only, and is provided for users that
    need new versions of SciPy but have existing code that still depends on
    ``scipy.weave``. For new code, users are recommended to use Cython."""

    homepage = "https://www.github.com/scipy/weave"
    url      = "https://pypi.io/packages/source/w/weave/weave-0.17.0.tar.gz"

    version('0.17.0', sha256='2703f3ae6d23ad47b5f09b6bcb7affd0fb587120a0c973e7be40ef24de709998')

    depends_on('python@2.6:2.8', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
