# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLazyarray(PythonPackage):
    """a Python package that provides a lazily-evaluated numerical array class,
    larray, based on and compatible with NumPy arrays."""

    homepage = "http://bitbucket.org/apdavison/lazyarray/"
    url      = "https://pypi.io/packages/source/l/lazyarray/lazyarray-0.2.8.tar.gz"

    version('0.2.10', sha256='7a53f81b5f3a098c04003d2ad179fc197451fd96bc921510f8534c6af8cc8e19')
    version('0.2.8',  sha256='aaee4e18117cc512de7a4e64522f37bc6f4bf125ecffdbdbf4e4e390fbdd9ba2')

    depends_on('py-numpy@1.3:', type=('build', 'run'))
    depends_on('py-numpy@1.5:', type=('build', 'run'), when='^python@3:')
