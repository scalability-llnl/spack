# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFutures(PythonPackage):
    """Backport of the concurrent.futures package from Python 3.2"""

    homepage = "https://pypi.python.org/pypi/futures"
    url      = "https://pypi.io/packages/source/f/futures/futures-3.0.5.tar.gz"

    version('3.2.0', sha256='9ec02aa7d674acb8618afb127e27fde7fc68994c0437ad759fa094a574adb265')
    version('3.0.5', sha256='0542525145d5afc984c88f914a0c85c77527f65946617edb5274f72406f981df')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('python@2.6:2.8', type=('build', 'run'))
