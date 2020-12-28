# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytools(PythonPackage):
    """A collection of tools for Python"""

    homepage = "https://pypi.org/project/pytools/"
    url      = "https://pypi.io/packages/source/p/pytools/pytools-2019.1.1.tar.gz"

    version('2019.1.1', sha256='ce2d702ae4ef10a70197b00b93141461140d00578f2a862fa946ca1446a300db')
    version('2016.2.6', sha256='6dd49932b8f81a8b622685cff3dd515e351a9290aef0fd5d020e4df00c06aa95')

    depends_on('py-setuptools', type='build')
    depends_on('py-decorator@3.2.0:', type=('build', 'run'))
    depends_on('py-appdirs@1.4.0:', type=('build', 'run'))
    depends_on('py-six@1.8.0:', type=('build', 'run'))
    depends_on('py-numpy@1.6.0:', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.4:', type=('build', 'run'))
