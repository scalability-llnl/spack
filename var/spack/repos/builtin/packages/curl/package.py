# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class Curl(AutotoolsPackage):
    """cURL is an open source command line tool and library for
    transferring data with URL syntax"""

    homepage = "https://curl.se/"
    # URL must remain http:// so Spack can bootstrap curl
    url      = "http://curl.haxx.se/download/curl-7.74.0.tar.bz2"

    version('7.76.1', sha256='7a8e184d7d31312c4ebf6a8cb59cd757e61b2b2833a9ed4f9bf708066e7695e9')
    version('7.76.0', sha256='e29bfe3633701590d75b0071bbb649ee5ca4ca73f00649268bd389639531c49a')
    version('7.75.0', sha256='50552d4501c178e4cc68baaecc487f466a3d6d19bbf4e50a01869effb316d026')
    version('7.74.0', sha256='0f4d63e6681636539dc88fa8e929f934cd3a840c46e0bf28c73be11e521b77a5')
    version('7.73.0', sha256='cf34fe0b07b800f1c01a499a6e8b2af548f6d0e044dca4a29d88a4bee146d131')
    version('7.72.0', sha256='ad91970864102a59765e20ce16216efc9d6ad381471f7accceceab7d905703ef')
    version('7.71.0', sha256='600f00ac2481a89548a4141ddf983fd9386165e1960bac91d0a1c81dca5dd341')
    version('7.68.0', sha256='207f54917dd6a2dc733065ccf18d61bb5bebeaceb5df49cd9445483e8623eeb9')
    version('7.64.0', sha256='d573ba1c2d1cf9d8533fadcce480d778417964e8d04ccddcc76e591d544cf2eb')
    version('7.63.0', sha256='9bab7ed4ecff77020a312d84cc5fb7eb02d58419d218f267477a724a17fd8dd8')
    version('7.60.0', sha256='897dfb2204bd99be328279f88f55b7c61592216b0542fcbe995c60aa92871e9b')
    version('7.59.0', sha256='b5920ffd6a8c95585fb95070e0ced38322790cb335c39d0dab852d12e157b5a0')
    version('7.56.0', sha256='de60a4725a3d461c70aa571d7d69c788f1816d9d1a8a2ef05f864ce8f01279df')
    version('7.54.0', sha256='f50ebaf43c507fa7cc32be4b8108fa8bbd0f5022e90794388f3c7694a302ff06')
    version('7.53.1', sha256='1c7207c06d75e9136a944a2e0528337ce76f15b9ec9ae4bb30d703b59bf530e8')
    version('7.52.1', sha256='d16185a767cb2c1ba3d5b9096ec54e5ec198b213f45864a38b3bda4bbf87389b')
    version('7.50.3', sha256='7b7347d976661d02c84a1f4d6daf40dee377efdc45b9e2c77dedb8acf140d8ec')
    version('7.50.2', sha256='0c72105df4e9575d68bcf43aea1751056c1d29b1040df6194a49c5ac08f8e233')
    version('7.50.1', sha256='3c12c5f54ccaa1d40abc65d672107dcc75d3e1fcb38c267484334280096e5156')
    version('7.49.1', sha256='eb63cec4bef692eab9db459033f409533e6d10e20942f4b060b32819e81885f1')
    version('7.47.1', sha256='ddc643ab9382e24bbe4747d43df189a0a6ce38fcb33df041b9cb0b3cd47ae98f')
    version('7.46.0', sha256='b7d726cdd8ed4b6db0fa1b474a3c59ebbbe4dcd4c61ac5e7ade0e0270d3195ad')
    version('7.45.0', sha256='65154e66b9f8a442b57c436904639507b4ac37ec13d6f8a48248f1b4012b98ea')
    version('7.44.0', sha256='1e2541bae6582bb697c0fbae49e1d3e6fad5d05d5aa80dbd6f072e0a44341814')
    version('7.43.0', sha256='baa654a1122530483ccc1c58cc112fec3724a82c11c6a389f1e6a37dc8858df9')
    version('7.42.1', sha256='e2905973391ec2dfd7743a8034ad10eeb58dab8b3a297e7892a41a7999cac887')

    variant('nghttp2',    default=False, description='build nghttp2 library (requires C++11)')
    variant('libssh2',    default=False, description='enable libssh2 support')
    variant('libssh',     default=False, description='enable libssh support')  # , when='7.58:')
    variant('darwinssl',  default=sys.platform == 'darwin', description="use Apple's SSL/TLS implementation")
    variant('gssapi',     default=False, description='enable Kerberos support')

    conflicts('+libssh', when='@:7.57.99')
    # on OSX and --with-ssh the configure steps fails with
    # one or more libs available at link-time are not available run-time
    # unless the libssh are installed externally (e.g. via homebrew), even
    # though spack isn't supposed to know about such a libssh installation.
    # C.f. https://github.com/spack/spack/issues/7777
    conflicts('platform=darwin', when='+libssh2')
    conflicts('platform=darwin', when='+libssh')
    conflicts('platform=linux', when='+darwinssl')

    depends_on('openssl', when='~darwinssl')
    depends_on('libidn2')
    depends_on('zlib')
    depends_on('nghttp2', when='+nghttp2')
    depends_on('libssh2', when='+libssh2')
    depends_on('libssh', when='+libssh')
    depends_on('krb5', when='+gssapi')

    def configure_args(self):
        spec = self.spec

        args = ['--with-zlib={0}'.format(spec['zlib'].prefix)]
        args.append('--with-libidn2={0}'.format(spec['libidn2'].prefix))

        if spec.satisfies('+darwinssl'):
            args.append('--with-darwinssl')
        else:
            args.append('--with-ssl={0}'.format(spec['openssl'].prefix))

        if spec.satisfies('+gssapi'):
            args.append('--with-gssapi={0}'.format(spec['krb5'].prefix))

        args += self.with_or_without('nghttp2')
        args += self.with_or_without('libssh2')
        args += self.with_or_without('libssh')
        return args
