# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Distcc(AutotoolsPackage):
    """distcc is a program to distribute compilation of C or C++
    code across several machines on a network."""

    homepage = "https://github.com/distcc/distcc"
    url      = "https://github.com/distcc/distcc/archive/v3.3.3.tar.gz"

    version('3.3.3', sha256='b7f37d314704fbaf006d747514ff6e4d0d722102ef7d2aea132f97cf170f5169')

    depends_on('popt')
    depends_on('libiberty')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix.sbin)
