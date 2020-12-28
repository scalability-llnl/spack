# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libssh(CMakePackage):
    """libssh: the SSH library"""

    homepage = "https://www.libssh.org"
    url      = "https://www.libssh.org/files/0.8/libssh-0.8.5.tar.xz"

    version('0.8.5', sha256='07d2c431240fc88f6b06bcb36ae267f9afeedce2e32f6c42f8844b205ab5a335')
    version('0.7.5', sha256='54e86dd5dc20e5367e58f3caab337ce37675f863f80df85b6b1614966a337095')

    variant("gssapi", default=True, description="Build with gssapi support")
    depends_on('openssl@:1.0', when='@:0.7')
    depends_on('openssl')
    depends_on('zlib')
    depends_on('krb5', when='+gssapi')

    def url_for_version(self, version):
        url = "https://www.libssh.org/files/{0}/libssh-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def cmake_args(self):
        args = ['-DWITH_GSSAPI=%s' %
                ('ON' if '+gssapi' in self.spec else 'OFF')]
        return args
