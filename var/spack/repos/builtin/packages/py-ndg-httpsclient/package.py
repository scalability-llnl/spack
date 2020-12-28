# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyNdgHttpsclient(PythonPackage):
    """Provides enhanced HTTPS support for httplib and urllib2 using
    PyOpenSSL."""

    homepage = "https://github.com/cedadev/ndg_httpsclient/"
    url      = "https://pypi.io/packages/source/n/ndg_httpsclient/ndg_httpsclient-0.5.1.tar.gz"

    version('0.5.1', sha256='d72faed0376ab039736c2ba12e30695e2788c4aa569c9c3e3d72131de2592210')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pyopenssl', type=('build', 'run'))
    depends_on('py-pyasn1@0.1.1:', type=('build', 'run'))
