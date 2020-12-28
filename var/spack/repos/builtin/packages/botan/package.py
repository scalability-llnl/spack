# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Botan(Package):
    """Crypto and TLS for Modern C++"""

    homepage = "https://botan.randombit.net/"
    url      = "https://botan.randombit.net/releases/Botan-2.13.0.tar.xz"

    maintainers = ['aumuell']

    version('2.17.2', sha256='ebe27dfe2b55d7e02bf520e926606c48b76b22facb483256b13ab38e018e1e6c')
    version('2.17.1', sha256='741358b3f1638ed7d9b2f59b4e344aa46f4966b15958b5434c0ac1580df0c0c1')
    version('2.17.0', sha256='b97044b312aa718349af7851331b064bc7bd5352400d5f80793bace427d01343')
    version('2.16.0', sha256='92ed6ebc918d86bd1b04221ca518af4cf29cc326c4760740bd2d22e61cea2628')
    version('2.15.0', sha256='d88af1307f1fefac79aa4f2f524699478d69ce15a857cf2d0a90ac6bf2a50009')
    version('2.14.0', sha256='0c10f12b424a40ee19bde00292098e201d7498535c062d8d5b586d07861a54b5')
    version('2.13.0', sha256='f57ae42a41e1091bca58f44f41addebd9a390b651603952c881ec89d50187e90')
    version('2.12.1', sha256='7e035f142a51fca1359705792627a282456d49749bf62a37a8e48375d41baaa9')
    version('2.12.0', sha256='1eaefd459d52f27de1805cff8c68792e0610919648ee98e101980e94edb90a63')
    version('2.11.0', sha256='f7874da2aeb8c018fd77df40b2137879bf90b66f5589490c991e83fb3e8094be')

    variant('doc', default=False, description='Build documentation')

    depends_on('python', type='build')
    depends_on('py-sphinx@1.2:', type='build', when='+doc')

    phases = ['configure', 'build', 'install']

    def configure(self, spec, prefix):
        configure = Executable('./configure.py')
        configure(*self.configure_args())

    def configure_args(self):
        spec = self.spec
        args = []
        args.append('--prefix=' + prefix)
        if '+doc' in spec:
            args.append('--with-documentation')
        else:
            args.append('--without-documentation')
        return args

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make('install')
