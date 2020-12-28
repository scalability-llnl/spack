# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack.package import *


class PyCryptography(PythonPackage):
    """cryptography is a package which provides cryptographic recipes
       and primitives to Python developers"""

    homepage = "https://github.com/pyca/cryptography"
    url      = "https://pypi.io/packages/source/c/cryptography/cryptography-1.8.1.tar.gz"

    version('2.7',   sha256='e6347742ac8f35ded4a46ff835c60e68c22a536a8ae5c4422966d06946b6d4c6')
    version('2.3.1', sha256='8d10113ca826a4c29d5b85b2c4e045ffa8bad74fb525ee0eceb1d38d4c70dfd6')
    version('1.8.1', sha256='323524312bb467565ebca7e50c8ae5e9674e544951d28a2904a50012a8828190')

    variant('idna', default=False, description='Deprecated U-label support')
    conflicts('+idna', when='@:2.4')

    # dependencies taken from https://github.com/pyca/cryptography/blob/master/setup.py
    depends_on('python@2.6:2.8,3.4:',                 type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@2.3.1:', type=('build', 'run'))

    depends_on('py-setuptools@20.5:',   type='build')

    depends_on('py-cffi@1.4.1:',             type=('build', 'run'))
    depends_on('py-cffi@1.8:1.11.2,1.11.4:', type=('build', 'run'), when='@2.7:')

    depends_on('py-asn1crypto@0.21.0:', type=('build', 'run'))
    depends_on('py-six@1.4.1:',         type=('build', 'run'))
    depends_on('py-idna@2.1:',          type=('build', 'run'), when='@:2.4')  # deprecated
    depends_on('py-idna@2.1:',          type=('build', 'run'), when='@2.5: +idna')  # deprecated
    depends_on('py-enum34',             type=('build', 'run'), when='^python@:3.4')
    depends_on('py-ipaddress',          type=('build', 'run'), when='^python@:3.3')
    depends_on('openssl@:1.0', when='@:1.8.1')
    depends_on('openssl')
