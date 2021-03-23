# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Nix(AutotoolsPackage):
    """Nix, the purely functional package manager"""

    homepage = "http://nixos.org/nix"
    url      = "https://github.com/NixOS/nix/archive/2.2.1.zip"

    version('2.2.1', sha256='b591664dd1b04a8f197407d445799ece41140a3117bcbdf8e3c5e94cd3f59854')
    version('2.1.3', sha256='80d0834f3e34b3e91bd20969733d8010b3e253517ea64bf12258c5f450f86425')
    version('2.0.4', sha256='49c78122b20e3ad894f546dd2a2f01c32ec528de790314820b1f1335276e3c22')

    patch('fix-doc-build.patch')

    variant('storedir', values=str, default='none',
            description='path of the Nix store (defaults to /nix)')
    variant('statedir', values=str, default='none',
            description='path to the locale state (defaults to /nix/var)')
    variant('doc', default=True,
            description='Build and install documentation')
    variant('sandboxing', default=True,
            description='Enable build isolation')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('bison@2.6.0:', type='build')
    depends_on('flex@2.5.35:', type='build')
    depends_on('libtool', type='build')
    depends_on('libxslt', when='+doc', type='build')

    depends_on('boost@1.66.0:+coroutine+context cxxstd=14', when='@2.2.0:')
    depends_on('boost@1.61.0:+coroutine+context cxxstd=14', when='@2.0.0:')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when='@2.0.0:')
    depends_on('brotli')
    depends_on('editline')
    depends_on('m4', type='build')

    depends_on('bzip2')
    depends_on('curl')
    depends_on('libseccomp', when='+sandboxing')
    depends_on('openssl')
    depends_on('sqlite@3.6.19:')
    depends_on('xz')

    # gcc 4.9+ and higher supported with c++14
    conflicts('%gcc@:4.8.99')

    def configure_args(self):
        args = []
        if '+sandboxing' not in self.spec:
            args.append('--disable-seccomp-sandboxing')
        if '+doc' not in self.spec:
            args.append('--disable-doc-gen')
        storedir = self.spec.variants['storedir'].value
        if storedir != 'none':
            args.append('--with-store-dir=' + storedir)
        statedir = self.spec.variants['statedir'].value
        if statedir != 'none':
            args.append('--localstatedir=' + statedir)
        return args
