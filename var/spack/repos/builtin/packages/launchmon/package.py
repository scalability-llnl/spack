# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Launchmon(AutotoolsPackage):
    """Software infrastructure that enables HPC run-time tools to
       co-locate tool daemons with a parallel job."""
    homepage = "https://github.com/LLNL/LaunchMON"
    url = "https://github.com/LLNL/LaunchMON/releases/download/v1.0.2/launchmon-v1.0.2.tar.gz"
    git      = "https://github.com/llnl/launchmon.git"
    maintainers = ['lee218llnl']

    version('master', branch='master')
    version('1.0.2', sha256='1d301ccccfe0873efcd66da87ed5e4d7bafc560b00aee396d8a9365f53b3a33a')

    depends_on('autoconf', type='build', when='@master')
    depends_on('automake', type='build', when='@master')
    depends_on('libtool', type='build', when='@master')
    depends_on('pkgconfig', type='build')
    depends_on('libgcrypt')
    depends_on('libgpg-error')
    depends_on("elf", type='link')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("spectrum-mpi", when='arch=ppc64le')

    patch('launchmon-char-conv.patch', when='@1.0.2')
    patch('for_aarch64.patch', when='@:1.0.2 target=aarch64:')

    def setup_build_environment(self, env):
        if self.spec.satisfies('@master'):
            # automake for launchmon requires the AM_PATH_LIBGCRYPT macro
            # which is defined in libgcrypt.m4
            env.prepend_path('ACLOCAL_PATH',
                             self.spec['libgcrypt'].prefix.share.aclocal)
