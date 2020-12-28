# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyClick(PythonPackage):
    """A simple wrapper around optparse for powerful command line utilities."""

    homepage = "http://github.com/mitsuhiko/click"
    url = "https://pypi.io/packages/source/c/click/click-7.1.2.tar.gz"

    version('7.1.2', sha256='d2b5255c7c6349bc1bd1e59e08cd12acbbd63ce649f2588755783aa94dfb6b1a')
    version('7.0', sha256='5b94b49521f6456670fdb30cd82a4eca9412788a93fa6dd6df72c94d5a8ff2d7',
            url='https://pypi.io/packages/source/c/click/Click-7.0.tar.gz')
    version('6.6', sha256='cc6a19da8ebff6e7074f731447ef7e112bd23adf3de5c597cf9989f2fd8defe9')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
