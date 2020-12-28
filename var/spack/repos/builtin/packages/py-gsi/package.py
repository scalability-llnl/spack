# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGsi(PythonPackage):
    """Python interface for GSI authentication"""

    homepage = "https://github.com/DIRACGrid/pyGSI"
    url      = "https://pypi.io/packages/source/g/gsi/GSI-0.6.5.tar.gz"

    version('0.6.5', sha256='8291dd2fab2be12626272629f7f9661487c4e29f1f9ab8c61614c54b06cb0643')

    depends_on('python@2.7:2.7.99', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('openssl', type='link')
