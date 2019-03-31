# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import inspect

from spack import *


class Fzf(MakefilePackage):
    """fzf is a general-purpose command-line fuzzy finder."""

    homepage = "https://github.com/junegunn/fzf"
    url      = "https://github.com/junegunn/fzf/archive/0.17.5.tar.gz"

    version('0.17.5',   sha256='de3b39758e01b19bbc04ee0d5107e14052d3a32ce8f40d4a63d0ed311394f7ee')
    version('0.17.4',   sha256='a4b009638266b116f422d159cd1e09df64112e6ae3490964db2cd46636981ff0')
    version('0.17.3',   sha256='e843904417adf926613431e4403fded24fade56269446e92aac6ff1db86af81e')
    version('0.17.1',   sha256='9c881e55780c0f56b5a30b87df756634d853bfd3938e7e53cb2df6ed63aa84a7')
    version('0.17.0-2', sha256='a084415231b452b92a6b8aa87a69c0c02ee59bfe95774bf0d4fcc9a6251ece20')
    version('0.17.0',   sha256='23569faf64cd6831c09aad7030c8b4bace0eb7a979c580b33cc4e4f9ff303e29')
    version('0.16.11',  sha256='e3067d4ad58d7be51eba9a35c06518cd7145c0cc297882796c7e40285f268a99')
    version('0.16.10',  sha256='a6b9d8abcba4239d30201cc7911e9c305a5cd750081ce5cd389f8e7425f4dc93')
    version('0.16.9',   sha256='dd9434576c68313481613a5bd52dbf623eee37a5c87f7bb66ca71ac8add5ff94')
    version('0.16.8',   sha256='daef99f67cff3dad261dbcf2aef995bb78b360bcc7098d7230cb11674e1ee1d4')

    depends_on('go@1.11:')

    variant('vim', default=False, description='Install vim plugins for fzf')

    patch("github_mirrors.patch")

    def edit(self, spec, prefix):
        # the ${HOME}/.glide directory must exist on some systems
        home = os.path.expanduser('~')
        directory = os.path.join(home, '.glide')
        if not os.path.isdir(directory):
            os.mkdir(directory)

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.install_targets)

        mkdir(prefix.bin)
        install('bin/fzf', prefix.bin)

        if '+vim' in spec:
            mkdir(prefix.plugin)
            install('plugin/fzf.vim', prefix.plugin)
