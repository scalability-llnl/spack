# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack import *


class Fzf(MakefilePackage):
    """fzf is a general-purpose command-line fuzzy finder."""

    homepage = "https://github.com/junegunn/fzf"
    url      = "https://github.com/junegunn/fzf/archive/0.17.5.tar.gz"

    version('0.19.0',   sha256='4d7ee0b621287e64ed450d187e5022d906aa378c5390d8c7c1f843417d2f3422')
    version('0.18.0',   sha256='5406d181785ea17b007544082b972ae004b62fb19cdb41f25e265ea3cc8c2d9d')

    depends_on('go@1.11:')
    import_resources('resources-0.19.0.json')
    import_resources('resources-0.18.0.json')

    variant('vim', default=False, description='Install vim plugins for fzf')

    # ensure that things run in module mode (belt&suspenders)
    def setup_build_environment(self, env):
        # forcibly enable module mode
        env.set('GO111MODULE', 'on')
        # forcibly enable vendoring, prevent network access
        env.set('GOFLAGS', '-mod=vendor')

    # use the default build()

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        fzf = glob.glob('target/fzf*')[0]
        install(fzf, prefix.bin.fzf)
        # also install the tmux helper
        install('bin/fzf-tmux', prefix.bin)

        if '+vim' in spec:
            mkdir(prefix.plugin)
            install('plugin/fzf.vim', prefix.plugin)
