# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import subprocess
import sys

from spack.package import *


class NodeJs(Package):
    """Node.js is a JavaScript runtime built on Chrome's V8 JavaScript
    engine."""

    homepage = "https://nodejs.org/"
    url      = "https://nodejs.org/dist/v13.5.0/node-v13.5.0.tar.gz"
    list_url = "https://nodejs.org/dist/"
    list_depth = 1

    # Current (latest features)
    version('15.3.0',  sha256='cadfa384a5f14591b84ce07a1afe529f28deb0d43366fb0ae4e78afba96bfaf2')
    version('14.13.0', sha256='8538b2e76aa06ee0e6eb1c118426c3c5ca53b2e49d66591738eacf76e89edd61')
    version('14.10.0', sha256='7e0d7a1aa23697415e3588a1ca4f1c47496e6c88b9cf37c66be90353d3e4ac3e')
    version('13.8.0',  sha256='815b5e1b18114f35da89e4d98febeaba97555d51ef593bd5175db2b05f2e8be6')
    version('13.5.0',  sha256='4b8078d896a7550d7ed399c1b4ac9043e9f883be404d9b337185c8d8479f2db8')

    # LTS (recommended for most users)
    version('14.15.1', sha256='a1120472bf55aea745287693a6651e16973e1008c9d6107df350126adf9716fe', preferred=True)
    version('12.18.4', sha256='a802d87e579e46fc52771ed6f2667048320caca867be3276f4c4f1bbb41389c3')
    version('12.18.3', sha256='6ea85f80e01b007cc9b566b8836513bc5102667d833bad4c1092be60fa60c2d4')
    version('12.16.0', sha256='ae2dfe74485d821d4fef7cf1802acd2322cd994c853a2327c4306952f4453441')
    version('12.14.0', sha256='5c1939867228f3845c808ef84a89c8ee93cc35f857bf7587ecee1b5a6d9da67b')
    version('11.1.0',  sha256='3f53b5ac25b2d36ad538267083c0e603d9236867a936c22a9116d95fa10c60d5')
    version('10.13.0', sha256='aa06825fff375ece7c0d881ae0de5d402a857e8cabff9b4a50f2f0b7b44906be')
    version('8.11.4',  sha256='459144e361d64ca7362c37cc9717c044ef909d348cb5aa3f2b62538560a6085a')
    version('8.9.1',   sha256='32491b7fcc4696b2cdead45c47e52ad16bbed8f78885d32e873952fee0f971e1')
    version('7.1.0',   sha256='595e7e2a37d1e0573044a90077bb12c0f750e5d8851899ffa74038238da9a983')
    version('6.3.0',   sha256='4ed7a99985f8afee337cc22d5fef61b495ab4238dfff3750ac9019e87fc6aae6')
    version('6.2.2',   sha256='b6baee57a0ede496c7c7765001f7495ad74c8dfe8c34f1a6fb2cd5d8d526ffce')

    variant('debug', default=False, description='Include debugger support')
    variant('doc', default=False, description='Compile with documentation')
    variant('icu4c', default=False, description='Build with support for all locales instead of just English')
    variant('openssl', default=True,  description='Build with Spacks OpenSSL instead of the bundled version')
    variant('zlib', default=True,  description='Build with Spacks zlib instead of the bundled version')

    # https://github.com/nodejs/node/blob/master/BUILDING.md#unix-and-macos
    depends_on('gmake@3.81:', type='build')
    depends_on('libtool', type='build', when=sys.platform != 'darwin')
    depends_on('pkgconfig', type='build')
    depends_on('python@2.7:2.8,3.5:', when='@12:', type='build')
    depends_on('python@2.7:2.8', when='@:11', type='build')
    # depends_on('bash-completion', when="+bash-completion")
    depends_on('icu4c', when='+icu4c')
    depends_on('openssl@1.0.2d:1.0.99', when='@:9+openssl')
    depends_on('openssl@1.1:', when='@10:+openssl')
    depends_on('zlib', when='+zlib')

    phases = ['configure', 'build', 'install']

    # https://github.com/spack/spack/issues/19310
    conflicts('%gcc@:4.8',
              msg="fails to build with gcc 4.8 "
                  "(see https://github.com/spack/spack/issues/19310")

    def setup_build_environment(self, env):
        # Force use of experimental Python 3 support
        env.set('PYTHON', self.spec['python'].command.path)
        env.set('NODE_GYP_FORCE_PYTHON', self.spec['python'].command.path)

    def configure_args(self):
        # On OSX, the system libtool must be used
        # So, we ensure that this is the case by...
        if sys.platform == 'darwin':
            process_pipe = subprocess.Popen(["which", "libtool"],
                                            stdout=subprocess.PIPE)
            result_which = process_pipe.communicate()[0]
            process_pipe = subprocess.Popen(["whereis", "libtool"],
                                            stdout=subprocess.PIPE)
            result_whereis = process_pipe.communicate()[0]
            assert result_which == result_whereis, (
                'On OSX the system libtool must be used. Please'
                '(temporarily) remove \n %s or its link to libtool from'
                'path')

        args = [
            '--prefix={0}'.format(self.prefix),
            # Note: npm is updated more regularly than node.js, so we build
            # the package instead of using the bundled version
            '--without-npm'
        ]

        if '+debug' in self.spec:
            args.append('--debug')

        if '+openssl' in self.spec:
            args.extend([
                '--shared-openssl',
                '--shared-openssl-includes={0}'.format(
                    self.spec['openssl'].prefix.include),
                '--shared-openssl-libpath={0}'.format(
                    self.spec['openssl'].prefix.lib),
            ])

        if '+zlib' in self.spec:
            args.extend([
                '--shared-zlib',
                '--shared-zlib-includes={0}'.format(
                    self.spec['zlib'].prefix.include),
                '--shared-zlib-libpath={0}'.format(
                    self.spec['zlib'].prefix.lib),
            ])

        if '+icu4c' in self.spec:
            args.append('--with-intl=full-icu')

        return args

    def configure(self, spec, prefix):
        if self.version >= Version('10.11.0'):
            python('configure.py', *self.configure_args())
        else:
            python('configure', *self.configure_args())

    def build(self, spec, prefix):
        make()
        if '+doc' in spec:
            make('doc')

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def build_test(self):
        make('test')
        make('test-addons')

    def install(self, spec, prefix):
        make('install')
