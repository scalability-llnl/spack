# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUrllib3(PythonPackage):
    """HTTP library with thread-safe connection pooling, file post, and
    more."""

    homepage = "https://urllib3.readthedocs.io/"
    url = "https://pypi.io/packages/source/u/urllib3/urllib3-1.25.6.tar.gz"

    version('1.25.6', sha256='9a107b99a5393caf59c7aa3c1249c16e6879447533d0887f4336dde834c7be86')
    version('1.25.3', sha256='dbe59173209418ae49d485b87d1681aefa36252ee85884c31346debd19463232')
    version('1.21.1', sha256='b14486978518ca0901a76ba973d7821047409d7f726f22156b24e83fd71382a5')
    version('1.20',   sha256='97ef2b6e2878d84c0126b9f4e608e37a951ca7848e4855a7f7f4437d5c34a72f')
    version('1.14',   sha256='dd4fb13a4ce50b18338c7e4d665b21fd38632c5d4b1d9f1a1379276bd3c08d37')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    variant('secure', default=False, description='Add SSL/TLS support')
    depends_on('py-pyopenssl@0.14:', when='+secure')
    depends_on('py-cryptography@1.3.4:', when='+secure')
    depends_on('py-idna@2:', when='+secure')
    depends_on('py-certifi', when='+secure')
    depends_on('py-ipaddress', when='+secure ^python@2.7:2.8')

    variant('socks', default=False, description='SOCKS and HTTP proxy support')
    depends_on('py-pysocks@1.5.6,1.5.8:1.999', when='+socks')
