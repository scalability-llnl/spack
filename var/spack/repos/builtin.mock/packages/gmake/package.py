# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


def check(condition, msg):
    """Raise an install error if condition is False."""
    if not condition:
        raise InstallError(msg)


class Gmake(Package):
    """A dumy package for the gmake."""
    homepage = "https://www.gnu.org/software/make/"
    url       = 'http://ftp.gnu.org/gnu/make/make-4.2.1.tar.gz'

    version('4.2.1', sha256='e40b8f018c1da64edd1cc9a6fce5fa63b2e707e404e20cad91fbae337c98a5b7',
            url='http://ftp.gnu.org/gnu/make/make-4.2.1.tar.gz')

    def setup_environment(self, spack_env, run_env):
        spack_cc    # Ensure spack module-scope variable is avaiable
        spack_env.set('for_install', 'for_install')

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_cc    # Ensure spack module-scope variable is avaiable
        spack_env.set('from_gmake', 'from_gmake')

    def setup_dependent_package(self, module, dspec):
        spack_cc    # Ensure spack module-scope variable is avaiable

        self.spec.from_gmake = "from_gmake"
        module.from_gmake = "from_gmake"

        self.spec.link_arg = "test link arg"

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        check(os.environ['for_install'] == 'for_install',
              "Couldn't read env var set in compile envieonmnt")

        gmake_exe = join_path(prefix.bin, 'make')
        touch(gmake_exe)
        set_executable(gmake_exe)
