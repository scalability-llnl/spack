# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GitDelta(CargoPackage):
    """A syntax-highlighting pager for git"""

    homepage  = "https://github.com/dandavison/delta"
    crates_io = "git-delta"
    git       = "https://github.com/dandavison/delta.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.4.3', sha256='6fe5636682428510a29198a056cb032cdcec2b18ed0ceba8f1854ee097d65d8e')

    depends_on('llvm@6.0:', type='build', when='@0.0.18:')
    depends_on('oniguruma')

    # delta has a dependency on libclang - specify path to llvm-config
    def setup_build_environment(self, env):
        # onig-sys environment
        env.append_flags('RUSTONIG_DYNAMIC_LIBONIG', '1')
        env.append_flags(
            'LLVM_CONFIG_PATH',
            join_path(self.spec['llvm'].prefix.bin, 'llvm-config'))
