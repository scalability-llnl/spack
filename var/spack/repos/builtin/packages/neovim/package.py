# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Neovim(CMakePackage):
    """Neovim: Vim-fork focused on extensibility and usability"""

    homepage = "https://neovim.io"
    git = "https://github.com/neovim/neovim.git"
    url = "https://github.com/neovim/neovim/archive/v0.4.3.tar.gz"

    version('master', branch='master')
    version('stable', tag='stable')
    version('0.4.4', sha256='2f76aac59363677f37592e853ab2c06151cca8830d4b3fe4675b4a52d41fc42c')
    version('0.4.3', sha256='91a0b5d32204a821bf414690e6b48cf69224d1961d37158c2b383f6a6cf854d2')
    version('0.3.4', sha256='a641108bdebfaf319844ed46b1bf35d6f7c30ef5aeadeb29ba06e19c3274bc0e')
    version('0.3.1', sha256='bc5e392d4c076407906ccecbc283e1a44b7832c2f486cad81aa04cc29973ad22')
    version('0.3.0', sha256='f7acb61b16d3f521907d99c486b7a9f1e505e8b2a18c9ef69a6d7f18f29f74b8')
    version('0.2.2', sha256='a838ee07cc9a2ef8ade1b31a2a4f2d5e9339e244ade68e64556c1f4b40ccc5ed')
    version('0.2.1', sha256='9e2c068a8994c9023a5f84cde9eb7188d3c85996a7e42e611e3cd0996e345dd3')
    version('0.2.0', sha256='72e263f9d23fe60403d53a52d4c95026b0be428c1b9c02b80ab55166ea3f62b5')

    depends_on('cmake@3.0:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('gettext', type=('build', 'link'))
    depends_on('lua@5.1.0:5.1.9', type=('build', 'link'))
    depends_on('lua-lpeg', type='link')
    depends_on('lua-mpack', type='link')
    depends_on('lua-bitlib', type='link')
    depends_on('libuv', type='link')
    depends_on('libuv@1.28:', type='link', when='@0.4:,stable')
    depends_on('jemalloc', type='link')
    depends_on('libtermkey', type='link')
    depends_on('libtermkey@0.18:', type='link', when='@0.3.4:,stable')
    depends_on('libvterm@0.0.0', type='link', when='@0.2.0:0.3')
    depends_on('libvterm@0.1:', type='link', when='@0.4:,stable')
    depends_on('unibilium', type='link')
    depends_on('unibilium@:1.2.0', type='link', when='@0.2.0')
    depends_on('unibilium@2.0:', type='link', when='@0.4:,stable')
    depends_on('msgpack-c', type='link')
    depends_on('msgpack-c@1.0.0:', type='link', when='@0.4:,stable')
    depends_on('gperf', type='link')
    depends_on('libluv@1.30.0:', type='link', when='@0.4:,stable')

    def cmake_args(self):
        return ['-DPREFER_LUA=ON']
