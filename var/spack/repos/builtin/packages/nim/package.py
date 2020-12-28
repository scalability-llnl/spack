# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Nim(Package):
    """Nim is a statically typed compiled systems programming language.
    It combines successful concepts from mature languages like Python,
    Ada and Modula."""

    homepage = "https://nim-lang.org/"
    url = "https://nim-lang.org/download/nim-0.20.0.tar.xz"

    version('0.20.0', sha256='4be00d7dd47220da508b30ce3b4deade4ba39800ea4a1e574018b3c733359780')
    version('0.19.6', sha256='a09f0c58d29392434d4fd6d15d4059cf7e013ae948413cb9233b8233d67e3a29')
    version('0.19.9', sha256='154c440cb8f27da20b3d6b1a8cc03f63305073fb995bbf26ec9bc6ad891ce276',
            url='https://github.com/nim-lang/nightlies/releases/download/2019-06-02-devel-1255b3c/nim-0.19.9-linux_x64.tar.xz')

    depends_on('pcre', type='build')
    depends_on('openssl', type='build')

    def install(self, spec, prefix):
        bash = which('bash')
        bash('./build.sh')

        nim = Executable(join_path('.', 'bin/nim'))
        nim('c', 'koch')

        koch = Executable(join_path('.', 'koch'))
        koch('tools')

        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('compiler', prefix.compiler)
        install_tree('config', prefix.config)
        install_tree('doc', prefix.doc)
        install('compiler.nimble', prefix)
