# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Argon2(MakefilePackage):
    """Argon2 is a password-hashing function that summarizes the state
    of the art in the design of memory-hard functions and can be used
    to hash passwords for credential storage, key derivation, or other
    applications."""

    homepage = "https://password-hashing.net/"
    url      = "https://github.com/P-H-C/phc-winner-argon2/archive/20190702.tar.gz"

    version('20190702', sha256='daf972a89577f8772602bf2eb38b6a3dd3d922bf5724d45e7f9589b5e830442c')
    version('20171227', sha256='eaea0172c1f4ee4550d1b6c9ce01aab8d1ab66b4207776aa67991eb5872fdcd8')
    version('20161029', sha256='fe0049728b946b58b94cc6db89b34e2d050c62325d16316a534d2bedd78cd5e7')

    # Unlike the distro choice in spack we prefer to have bin/lib
    # Validated on CentOS7
    def setup_build_environment(self, env):
        env.set('LIBRARY_REL', 'lib')

    def install(self, spec, prefix):
        make('PREFIX={0}'.format(prefix), 'install')
