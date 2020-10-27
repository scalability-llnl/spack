# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bat(CargoPackage):
    """A cat(1) clone with wings."""

    homepage = "https://github.com/sharkdp/bat"
    crates_io = "bat"
    git = "https://github.com/sharkdp/bat.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.15.4', sha256='91f17c2d9e1cee447a788a15fa6819c0cb488fb2935e3e8c4e7120e1678b7aa8')

    depends_on('pkgconfig', type='build')
    depends_on('libgit2')
    depends_on('oniguruma')

    # Tell onig-sys to prefer spack-installed oniguruma
    def setup_build_environment(self, env):
        # onig-sys environment
        env.append_flags('RUSTONIG_DYNAMIC_LIBONIG', '1')

        # git-sys environment
        env.append_flags('LIBGIT2_SYS_USE_PKG_CONFIG', '1')
