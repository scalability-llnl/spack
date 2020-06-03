# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyProtobuf(PythonPackage):
    """Protocol buffers are Google's language-neutral, platform-neutral,
    extensible mechanism for serializing structured data - think XML, but
    smaller, faster, and simpler. You define how you want your data to be
    structured once, then you can use special generated source code to easily
    write and read your structured data to and from a variety of data streams
    and using a variety of languages."""

    homepage = 'https://developers.google.com/protocol-buffers/'
    url      = 'https://pypi.io/packages/source/p/protobuf/protobuf-3.11.0.tar.gz'

    variant('cpp', default=False,
            description='Enable the cpp implementation')

    version('3.11.2',         sha256='3d7a7d8d20b4e7a8f63f62de2d192cfd8b7a53c56caba7ece95367ca2b80c574')
    version('3.11.1',         sha256='aecdf12ef6dc7fd91713a6da93a86c2f2a8fe54840a3b1670853a2b7402e77c9')
    version('3.11.0',         sha256='97b08853b9bb71512ed52381f05cf2d4179f4234825b505d8f8d2bb9d9429939')
    version('3.10.0',         sha256='db83b5c12c0cd30150bb568e6feb2435c49ce4e68fe2d7b903113f0e221e58fe')
    version('3.9.2',          sha256='843f498e98ad1469ad54ecb4a7ccf48605a1c5d2bd26ae799c7a2cddab4a37ec')
    version('3.9.1',          sha256='d831b047bd69becaf64019a47179eb22118a50dd008340655266a906c69c6417')
    version('3.9.0',          sha256='b3452bbda12b1cbe2187d416779de07b2ab4c497d83a050e43c344778763721d')
    version('3.8.0',          sha256='8c61cc8a76e9d381c665aecc5105fa0f1878cf7db8b5cd17202603bcb386d0fc')
    version('3.7.1',          sha256='21e395d7959551e759d604940a115c51c6347d90a475c9baf471a1a86b5604a9')
    version('3.7.0',          sha256='ad385fbb9754023d17be14dd5aa67efff07f43c5df7f93118aef3c20e635ea19')
    version('3.6.1',          sha256='1489b376b0f364bcc6f89519718c057eb191d7ad6f1b395ffd93d1aa45587811')
    version('3.6.0',          sha256='a37836aa47d1b81c2db1a6b7a5e79926062b5d76bd962115a0e615551be2b48d')
    version('3.5.2.post1',    sha256='3b60685732bd0cbdc802dfcb6071efbcf5d927ce3127c13c33ea1a8efae3aa76')
    version('3.5.2',          sha256='09879a295fd7234e523b62066223b128c5a8a88f682e3aff62fb115e4a0d8be0')
    version('3.5.1',          sha256='95b78959572de7d7fafa3acb718ed71f482932ddddddbd29ba8319c10639d863')
    version('3.5.0.post1',    sha256='f656bf5fdfcf0fbc8ba1bd23cab0f2a78fad08741f536c3ffdc9e463621a16ed')
    version('3.4.0',          sha256='ef02609ef445987976a3a26bff77119c518e0915c96661c3a3b17856d0ef6374')
    version('3.3.0',          sha256='1cbcee2c45773f57cb6de7ee0eceb97f92b9b69c0178305509b162c0160c1f04')
    version('3.2.0',          sha256='a48475035c42d13284fd7bf3a2ffa193f8c472ad1e8539c8444ea7e2d25823a1')
    version('3.1.0.post1',    sha256='1a2e989ff8820ef2eaf56b07cd40ad764ec505a0f0b52b69f7fa9e0d5afbddb7')
    version('3.1.0',          sha256='0bc10bfd00a9614fae58c86c21fbcf339790e48accf6d45f098034de985f5405',
            url='https://github.com/protocolbuffers/protobuf/releases/download/v3.1.0/protobuf-python-3.1.0.tar.gz')
    version('3.0.0b4',        sha256='f3b2d4572d62c8bcbb464b5f5d44697c8c8bc904de0acd0b8a9cadc790ddfba3')
    version('3.0.0b3',        sha256='b4f0a326f1776f874152243bea10ba924278bf76b7b9e10991c7f8d17eb71525')
    version('3.0.0b2.post2',  sha256='37127b74dd673f3815e24f8c1c62df25879da508e22537d5603603658f99b229')
    version('3.0.0b2.post1',  sha256='f48d7376806056bed44f18c93daa9d1a6ef804a98876ab7e802a45dfcd771f7e')
    version('3.0.0b2',        sha256='d5b560bbc4b7d97cc2455c05cad9299d9db02d7bd11193b05684e3a86303c229')
    version('3.0.0b1.post2',  sha256='15768af52b42c2114c0ddb2011c70c53e72db0eab0bd39d7debb1d10ee91009b')
    version('3.0.0a3',        sha256='b61622de5048415bfd3f2d812ad64606438ac9e25009ae84191405fe58e522c1')
    version('3.0.0a2',        sha256='288bd1393bc0ed839f7e1e09822451495e5bfe7561c1440c9cdd20166e9509d9')
    version('3.0.0',          sha256='ecc40bc30f1183b418fe0ec0c90bc3b53fa1707c4205ee278c6b90479e5b6ff5')
    version('2.6.1',          sha256='8faca1fb462ee1be58d00f5efb4ca4f64bde92187fe61fde32615bbee7b3e745')
    version('2.6.0',          sha256='b1556c5e9cca9069143b41312fd45d0d4785ca0cab682b2624195a6bc4ec296f')
    version('2.5.0',          sha256='58292c459598c9297258bf57acc055f701c727f0154a86af8c0947dde37d8172')
    version('2.4.1',          sha256='df30b98acb6ef892da8b4776175510cff2131908fd0526b6bad960c55a830a1b')
    version('2.3.0',          sha256='374bb047874a506507912c3717d0ce62affbaa9a22bcb494d63d60326a0867b5')
    version('2.0.3',          sha256='5e17f2b3b9e459fc25c718c18ae4bf1b8eba3a9d5b5c18c178369d58a469c6d1')
    version('2.0.0beta',      sha256='cf04f05851eb7aac66a29fa6e6ba7072a4808389848c01cbfd82fb5e68cf2b73')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-six@1.9:', when='@3:', type=('build', 'run'))
    depends_on('py-ordereddict', when='@3: ^python@:2', type=('build', 'run'))
    depends_on('py-unittest2', when='@3: ^python@:2', type=('build', 'run'))

    same_version_as("protobuf", when="+cpp",
                    pkg_to_dep_version=lambda v: v.up_to(3))

    @property
    def build_directory(self):
        if self.spec.satisfies('@3.1.0'):
            return 'python'
        else:
            return '.'

    @when('+cpp')
    def build_args(self, spec, prefix):
        return ['--cpp_implementation']

    @when('+cpp')
    def install_args(self, spec, prefix):
        args = super(PyProtobuf, self).install_args(spec, prefix)
        return args + ['--cpp_implementation']

    @run_after('install')
    def fix_import_error(self):
        if str(self.spec['python'].version.up_to(1)) == '2':
            touch = which('touch')
            touch(self.prefix + '/' +
                  self.spec['python'].package.site_packages_dir +
                  '/google/__init__.py')
