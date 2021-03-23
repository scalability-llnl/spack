# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path


class Nim(Package):
    """Nim is a statically typed compiled systems programming language.
    It combines successful concepts from mature languages like Python,
    Ada and Modula.
    """

    homepage = "https://nim-lang.org/"
    url = "https://nim-lang.org/download/nim-1.4.4.tar.xz"

    version('1.4.4', sha256='6d73729def143f72fc2491ca937a9cab86d2a8243bd845a5d1403169ad20660e')
    version('1.4.2', sha256='03a47583777dd81380a3407aa6a788c9aa8a67df4821025770c9ac4186291161')
    version('0.20.0', sha256='51f479b831e87b9539f7264082bb6a64641802b54d2691b3c6e68ac7e2699a90', deprecated=True)
    version('0.19.6', sha256='a09f0c58d29392434d4fd6d15d4059cf7e013ae948413cb9233b8233d67e3a29', deprecated=True)
    version('0.19.9', sha256='154c440cb8f27da20b3d6b1a8cc03f63305073fb995bbf26ec9bc6ad891ce276',
            url='https://github.com/nim-lang/nightlies/releases/download/2019-06-02-devel-1255b3c/nim-0.19.9-linux_x64.tar.xz',
            deprecated=True)

    depends_on('pcre')
    depends_on('openssl')

    def patch(self):
        install_sh_path = os.path.join(self.stage.source_path, 'install.sh')
        filter_file("1/nim", "1", install_sh_path)

    def install(self, spec, prefix):
        bash = which('bash')
        bash('./build.sh')

        nim = Executable(os.path.join('bin', 'nim'))
        nim('c', 'koch')

        koch = Executable('./koch')
        koch('boot', '-d:release')
        koch('tools')

        bash('./install.sh', prefix)
