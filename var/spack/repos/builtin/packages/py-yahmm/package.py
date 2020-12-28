# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYahmm(PythonPackage):
    """YAHMM is a HMM package for Python, implemented in Cython for speed."""

    homepage = "http://pypi.python.org/pypi/yahmm/"
    url      = "https://pypi.io/packages/source/y/yahmm/yahmm-1.1.3.zip"

    version('1.1.3', sha256='fe3614ef96da9410468976756fb93dc8235485242c05df01d8e5ed356a7dfb43')

    depends_on('py-cython@0.20.1:', type=('build', 'run'))
    depends_on('py-numpy@1.8.0:', type=('build', 'run'))
    depends_on('py-scipy@0.13.3:', type=('build', 'run'))
    depends_on('py-matplotlib@1.3.1:', type=('build', 'run'))
    depends_on('py-networkx@1.8.1:', type=('build', 'run'))
