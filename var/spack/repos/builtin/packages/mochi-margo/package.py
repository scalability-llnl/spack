# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class MochiMargo(AutotoolsPackage):
    """A library that provides Argobots bindings to the Mercury RPC
    implementation."""

    homepage = 'https://github.com/mochi-hpc/mochi-margo'
    git = 'https://github.com/mochi-hpc/mochi-margo.git'
    url = 'https://github.com/mochi-hpc/mochi-margo/archive/v0.9.tar.gz'

    maintainers = ['carns', 'mdorier', 'fbudin69500', 'chuckatkins']

    version('main', branch='main')
    version('0.9.4', sha256='4292e083c8375ab07bc6dd0b3b1ea2ce9c9dd864c27ac7f07c6913dcccecc746')
    version('0.9.3', sha256='1331423d4864349c3a9ec52b2114122659da310d5270fa1aea652e8ee48a0b3a')
    version('0.9.2', sha256='de88cd725c8ff3ec63412f3f5ed22ad1a56cb367c31b842c816ce40cba777f7c')
    version('0.9.1', sha256='3fe933f2d758ef23d582bc776e4f8cfae9bf9d0849b8b1f9d73ee024e218f2bc')
    version('0.9', sha256='a24376f66450cc8fd7a43043e189f8efce5a931585e53c1e2e41894a3e99b517')
    version('0.7', sha256='492d1afe2e7984fa638614a5d34486d2ff761f5599b5984efd5ae3f55cafde54')
    version('0.7.2', sha256='0ca796abdb82084813a5de033d92364910b5ad1a0df135534d6b1c36ef627859')
    version('0.7.1', sha256='eebbe02c47ed4c65ef1d4f23ffdc6a8aa2e2348ca6c51bfc3c4dfbf78fbfc30b')
    version('0.6', sha256='56feb718da2b155d7277a7b10b669516ebffaa034f811f3665ceed7ad0f19d1b')
    version('0.6.4', sha256='5ba1c72ee05aa9738d3dc4d6d01bd59790284c6c77b909c5d7756fe7049d6177')
    version('0.6.3', sha256='5f373cd554edd15cead58bd5d30093bd88d45039d06ff7738eb18b3674287c76')
    version('0.6.2', sha256='c6a6909439e1d3ba1a1693d8da66057eb7e4ec4b239c04bc7f19fc487c4c58da')
    version('0.6.1', sha256='80d8d15d0917b5522c31dc2d83136de2313d50ca05c71c5e5ad83c483a3214b7')
    version('0.5', sha256='d3b768b8300bc2cb87964e74c39b4e8eb9822d8a2e56fc93dc475ddcb1a868e3')
    version('0.5.2', sha256='73be3acaf012a85a91ac62824c93f5ee1ea0ffe4c25779ece19723f4baf9547d')
    version('0.5.1', sha256='6fdf58e189538e22341c8361ab069fc80fe5460a6869882359b295a890febad7')
    version('0.4.7', sha256='596d83b11fb2bd9950fd99c9ab12c14915ab2cda233084ae40ecae1e6c584333')
    version('0.4.6', sha256='b27447a2050ae61091bae3ff6b4d23a56153947f18847face9f98facbdb4e329')
    version('0.4.5', sha256='b0d02f73edf180f2393f54c5a980620b8d6dcd42b90efdea6866861824fa49cf')
    version('0.4.4', sha256='2e2e6e2a8a7d7385e2fe204c113cb149f30847f0b1f48ec8dd708a74280bd89e')
    version('0.4.3', sha256='61a634d6983bee2ffa06e1e2da4c541cb8f56ddd9dd9f8e04e8044fb38657475')
    version('0.4.2', sha256='91085e28f50e373b9616e1ae5c3c8d40a19a7d3776259592d8f361766890bcaa')

    depends_on('json-c', when='@0.9:')
    depends_on('autoconf@2.65:', type=("build"))
    depends_on('m4', type=('build'))
    depends_on('automake', type=("build"))
    depends_on('libtool', type=("build"))
    depends_on('pkgconfig', type=("build"))
    depends_on('argobots@1.0:')
    # "breadcrumb" support not available in mercury-1.0
    depends_on('mercury@1.0.0:', type=("build", "link", "run"), when='@:0.5.1')
    depends_on('mercury@2.0.0:', type=("build", "link", "run"), when='@0.5.2:')

    def autoreconf(self, spec, prefix):
        sh = which('sh')
        sh('./prepare.sh')
