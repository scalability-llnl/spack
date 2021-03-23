# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

from spack import *
import spack.architecture

import os
import re


class Openssl(Package):   # Uses Fake Autotools, should subclass Package
    """OpenSSL is an open source project that provides a robust,
       commercial-grade, and full-featured toolkit for the Transport
       Layer Security (TLS) and Secure Sockets Layer (SSL) protocols.
       It is also a general-purpose cryptography library."""
    homepage = "http://www.openssl.org"

    # URL must remain http:// so Spack can bootstrap curl
    url = "http://www.openssl.org/source/openssl-1.1.1d.tar.gz"
    list_url = "http://www.openssl.org/source/old/"
    list_depth = 1

    executables = ['openssl']

    # The latest stable version is the 1.1.1 series. This is also our Long Term
    # Support (LTS) version, supported until 11th September 2023.
    version('1.1.1j', sha256='aaf2fcb575cdf6491b98ab4829abf78a3dec8402b8b81efc8f23c00d443981bf')
    version('1.1.1i', sha256='e8be6a35fe41d10603c3cc635e93289ed00bf34b79671a3a4de64fcee00d5242')
    version('1.1.1h', sha256='5c9ca8774bd7b03e5784f26ae9e9e6d749c9da2438545077e6b3d755a06595d9')
    version('1.1.1g', sha256='ddb04774f1e32f0c49751e21b67216ac87852ceb056b75209af2443400636d46')
    version('1.1.1f', sha256='186c6bfe6ecfba7a5b48c47f8a1673d0f3b0e5ba2e25602dd23b629975da3f35')
    version('1.1.1e', sha256='694f61ac11cb51c9bf73f54e771ff6022b0327a43bbdfa1b2f19de1662a6dcbe')
    version('1.1.1d', sha256='1e3a91bc1f9dfce01af26026f856e064eab4c8ee0a8f457b5ae30b40b8b711f2')
    version('1.1.1c', sha256='f6fb3079ad15076154eda9413fed42877d668e7069d9b87396d0804fdb3f4c90')
    version('1.1.1b', sha256='5c557b023230413dfb0756f3137a13e6d726838ccd1430888ad15bfb2b43ea4b')
    version('1.1.1a', sha256='fc20130f8b7cbd2fb918b2f14e2f429e109c31ddd0fb38fc5d71d9ffed3f9f41')
    version('1.1.1',  sha256='2836875a0f89c03d0fdf483941512613a50cfb421d6fd94b9f41d7279d586a3d')

    # The 1.1.0 series is out of support and should not be used.
    version('1.1.0l', sha256='74a2f756c64fd7386a29184dc0344f4831192d61dc2481a93a4c5dd727f41148', deprecated=True)
    version('1.1.0k', sha256='efa4965f4f773574d6cbda1cf874dbbe455ab1c0d4f906115f867d30444470b1', deprecated=True)
    version('1.1.0j', sha256='31bec6c203ce1a8e93d5994f4ed304c63ccf07676118b6634edded12ad1b3246', deprecated=True)
    version('1.1.0i', sha256='ebbfc844a8c8cc0ea5dc10b86c9ce97f401837f3fa08c17b2cdadc118253cf99', deprecated=True)
    version('1.1.0g', sha256='de4d501267da39310905cb6dc8c6121f7a2cad45a7707f76df828fe1b85073af', deprecated=True)
    version('1.1.0e', sha256='57be8618979d80c910728cfc99369bf97b2a1abd8f366ab6ebdee8975ad3874c', deprecated=True)
    version('1.1.0d', sha256='7d5ebb9e89756545c156ff9c13cf2aa6214193b010a468a3bc789c3c28fe60df', deprecated=True)
    version('1.1.0c', sha256='fc436441a2e05752d31b4e46115eb89709a28aef96d4fe786abe92409b2fd6f5', deprecated=True)

    # The 1.0.2 series is out of support and should not be used.
    version('1.0.2u', sha256='ecd0c6ffb493dd06707d38b14bb4d8c2288bb7033735606569d8f90f89669d16', deprecated=True)
    version('1.0.2t', sha256='14cb464efe7ac6b54799b34456bd69558a749a4931ecfd9cf9f71d7881cac7bc', deprecated=True)
    version('1.0.2s', sha256='cabd5c9492825ce5bd23f3c3aeed6a97f8142f606d893df216411f07d1abab96', deprecated=True)
    version('1.0.2r', sha256='ae51d08bba8a83958e894946f15303ff894d75c2b8bbd44a852b64e3fe11d0d6', deprecated=True)
    version('1.0.2p', sha256='50a98e07b1a89eb8f6a99477f262df71c6fa7bef77df4dc83025a2845c827d00', deprecated=True)
    version('1.0.2o', sha256='ec3f5c9714ba0fd45cb4e087301eb1336c317e0d20b575a125050470e8089e4d', deprecated=True)
    version('1.0.2n', sha256='370babb75f278c39e0c50e8c4e7493bc0f18db6867478341a832a982fd15a8fe', deprecated=True)
    version('1.0.2m', sha256='8c6ff15ec6b319b50788f42c7abc2890c08ba5a1cdcd3810eb9092deada37b0f', deprecated=True)
    version('1.0.2k', sha256='6b3977c61f2aedf0f96367dcfb5c6e578cf37e7b8d913b4ecb6643c3cb88d8c0', deprecated=True)
    version('1.0.2j', sha256='e7aff292be21c259c6af26469c7a9b3ba26e9abaaffd325e3dccc9785256c431', deprecated=True)
    version('1.0.2i', sha256='9287487d11c9545b6efb287cdb70535d4e9b284dd10d51441d9b9963d000de6f', deprecated=True)
    version('1.0.2h', sha256='1d4007e53aad94a5b2002fe045ee7bb0b3d98f1a47f8b2bc851dcd1c74332919', deprecated=True)
    version('1.0.2g', sha256='b784b1b3907ce39abf4098702dade6365522a253ad1552e267a9a0e89594aa33', deprecated=True)
    version('1.0.2f', sha256='932b4ee4def2b434f85435d9e3e19ca8ba99ce9a065a61524b429a9d5e9b2e9c', deprecated=True)
    version('1.0.2e', sha256='e23ccafdb75cfcde782da0151731aa2185195ac745eea3846133f2e05c0e0bff', deprecated=True)
    version('1.0.2d', sha256='671c36487785628a703374c652ad2cebea45fa920ae5681515df25d9f2c9a8c8', deprecated=True)

    # The 1.0.1 version is out of support and should not be used.
    version('1.0.1u', sha256='4312b4ca1215b6f2c97007503d80db80d5157f76f8f7d3febbe6b4c56ff26739', deprecated=True)
    version('1.0.1t', sha256='4a6ee491a2fdb22e519c76fdc2a628bb3cec12762cd456861d207996c8a07088', deprecated=True)
    version('1.0.1r', sha256='784bd8d355ed01ce98b812f873f8b2313da61df7c7b5677fcf2e57b0863a3346', deprecated=True)
    version('1.0.1h', sha256='9d1c8a9836aa63e2c6adb684186cbd4371c9e9dcc01d6e3bb447abf2d4d3d093', deprecated=True)
    version('1.0.1e', sha256='f74f15e8c8ff11aa3d5bb5f276d202ec18d7246e95f961db76054199c69c1ae3', deprecated=True)

    variant('systemcerts', default=True, description='Use system certificates')
    variant('docs', default=False, description='Install docs and manpages')

    depends_on('zlib')

    depends_on('perl@5.14.0:', type=('build', 'test'))

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('version', output=str, error=str)
        match = re.search(r'OpenSSL.(\S+)*', output)
        return match.group(1) if match else None

    @property
    def libs(self):
        return find_libraries(
            ['libssl', 'libcrypto'], root=self.prefix, recursive=True)

    def handle_fetch_error(self, error):
        tty.warn("Fetching OpenSSL failed. This may indicate that OpenSSL has "
                 "been updated, and the version in your instance of Spack is "
                 "insecure. Consider updating to the latest OpenSSL version.")

    def install(self, spec, prefix):
        # OpenSSL uses a variable APPS in its Makefile. If it happens to be set
        # in the environment, then this will override what is set in the
        # Makefile, leading to build errors.
        env.pop('APPS', None)

        if str(spec.target.family) in ('x86_64', 'ppc64'):
            # This needs to be done for all 64-bit architectures (except Linux,
            # where it happens automatically?)
            env['KERNEL_BITS'] = '64'

        options = ['zlib', 'shared']
        if spec.satisfies('@1.0'):
            options.append('no-krb5')
        # clang does not support the .arch directive in assembly files.
        if 'clang' in self.compiler.cc and \
           'aarch64' in spack.architecture.sys_type():
            options.append('no-asm')

        # The default glibc provided by CentOS 7 does not provide proper
        # atomic support when using the NVIDIA compilers
        if self.spec.satisfies('%nvhpc os=centos7'):
            options.append('-D__STDC_NO_ATOMICS__')

        config = Executable('./config')
        config('--prefix=%s' % prefix,
               '--openssldir=%s' % join_path(prefix, 'etc', 'openssl'),
               '-I{0}'.format(self.spec['zlib'].prefix.include),
               '-L{0}'.format(self.spec['zlib'].prefix.lib),
               *options)

        # Remove non-standard compiler options if present. These options are
        # present e.g. on Darwin. They are non-standard, i.e. most compilers
        # (e.g. gcc) will not accept them.
        filter_file(r'-arch x86_64', '', 'Makefile')

        make()
        if self.run_tests:
            make('test', parallel=False)  # 'VERBOSE=1'

        install_tgt = 'install' if self.spec.satisfies('+docs') else 'install_sw'

        # See https://github.com/openssl/openssl/issues/7466#issuecomment-432148137
        make(install_tgt, parallel=False)

    @run_after('install')
    def link_system_certs(self):
        if '+systemcerts' not in self.spec:
            return

        system_dirs = [
            # CentOS, Fedora, RHEL
            '/etc/pki/tls',
            # Ubuntu
            '/usr/lib/ssl',
            # OpenSUSE
            '/etc/ssl'
        ]

        pkg_dir = join_path(self.prefix, 'etc', 'openssl')

        mkdirp(pkg_dir)

        for directory in system_dirs:
            sys_cert = join_path(directory, 'cert.pem')
            pkg_cert = join_path(pkg_dir, 'cert.pem')
            # If a bundle exists, use it. This is the preferred way on Fedora,
            # where the certs directory does not work.
            if os.path.exists(sys_cert) and not os.path.exists(pkg_cert):
                os.symlink(sys_cert, pkg_cert)

            sys_certs = join_path(directory, 'certs')
            pkg_certs = join_path(pkg_dir, 'certs')
            # If the certs directory exists, symlink it into the package.
            # We symlink the whole directory instead of all files because
            # the directory contents might change without Spack noticing.
            if os.path.isdir(sys_certs) and not os.path.islink(pkg_certs):
                if os.path.isdir(pkg_certs):
                    os.rmdir(pkg_certs)
                os.symlink(sys_certs, pkg_certs)

    def patch(self):
        if self.spec.satisfies('%nvhpc'):
            # Remove incompatible preprocessor flags
            filter_file('-MF ', '',
                        'Configurations/unix-Makefile.tmpl', string=True)
            filter_file(r'-MT \$\@ ', '',
                        'Configurations/unix-Makefile.tmpl', string=True)

    def setup_build_environment(self, env):
        env.set('PERL', self.spec['perl'].prefix.bin.perl)
