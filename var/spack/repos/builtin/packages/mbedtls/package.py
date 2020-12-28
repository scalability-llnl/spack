# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mbedtls(CMakePackage):
    """mbed TLS (formerly known as PolarSSL) makes it trivially easy for
       developers to include cryptographic and SSL/TLS capabilities in
       their (embedded) products, facilitating this functionality with a
       minimal coding footprint.
    """

    homepage = "https://tls.mbed.org"
    url      = "https://github.com/ARMmbed/mbedtls/archive/mbedtls-2.2.1.tar.gz"
    maintainers = ['mwkrentel']

    version('2.16.9', sha256='b7ca99ee10551b5b13242b7effebefd2a5cc38c287e5f5be1267d51ee45effe3')
    version('2.16.7', sha256='4786b7d1676f5e4d248f3a7f2d28446876d64962634f060ff21b92c690cfbe86')
    version('2.16.1', sha256='daf0d40f3016c34eb42d1e4b3b52be047e976d566aba8668977723c829af72f3')
    version('2.7.10', sha256='42b19b30b86a798bdb69c5da2f8bbd7d72ffede9a35b888ab986a29480f9dc3e')
    version('2.3.0', sha256='1614ee70be99a18ca8298148308fb725aad4ad31c569438bb51655a4999b14f9')
    version('2.2.1', sha256='32819c62c20e8740a11b49daa5d09ac6f179edf120a87ac559cd63120b66b699')
    version('2.2.0', sha256='75494361e412444b38ebb9c908b7e17a5fb582eb9c3fadb2fe9b21e96f1bf8cb')
    version('2.1.4', sha256='a0ee4d3dd135baf67a3cf5ad9e70d67575561704325d6c93d8f087181f4db338')
    version('2.1.3', sha256='94da4618d5a518b99f7914a5e348be436e3571113d9a9978d130725a1fc7bfac')
    version('1.3.16', sha256='0c2666222b66cf09c4630fa60a715aafd7decb1a09933b75c0c540b0625ac5df')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release', 'Coverage', 'ASan', 'ASanDbg',
                    'MemSan', 'MemSanDbg', 'Check', 'CheckFull'))

    variant('pic', default=False,
            description='Compile with position independent code.')

    depends_on('cmake@3.1.0:', type='build', when='@2.8.0:')
    depends_on('cmake@2.6:', type='build', when='@:2.7.99')
    depends_on('perl', type='build')

    def flag_handler(self, name, flags):

        # Compile with PIC, if requested.
        if name == 'cflags' and '+pic' in self.spec:
            flags.append(self.compiler.cc_pic_flag)

        return (flags, None, None)
