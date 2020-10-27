# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Oniguruma(AutotoolsPackage):
    """Regular expression library."""

    homepage = "https://github.com/kkos/oniguruma"
    url      = "https://github.com/kkos/oniguruma/releases/download/v6.9.4/onig-6.9.4.tar.gz"

    version('6.9.5', sha256='2f25cc3165e6da4b12dcabdb6b77c48f436d835e127ec2e3cad7abae9ea8e9a6')
    version('6.9.4', sha256='4669d22ff7e0992a7e93e116161cac9c0949cd8960d1c562982026726f0e6d53')
    version('6.1.3', sha256='480c850cd7c7f2fcaad0942b4a488e2af01fbb8e65375d34908f558b432725cf')

    @property
    def libs(self):
        return find_libraries('libonig', root=self.prefix, recursive=True)

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def configuration_check(self):
        onig_config = Executable(join_path(self.prefix.bin, 'onig-config'))

        assert onig_config('--cflags',      output=str).rstrip() == \
            self.spec['oniguruma'].headers.include_flags
        assert onig_config('--libs',        output=str).rstrip() == \
            self.spec['oniguruma'].libs.ld_flags
        assert onig_config('--prefix',      output=str).rstrip() == \
            self.prefix
        assert onig_config('--exec-prefix', output=str).rstrip() == \
            self.prefix
