# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cronie(AutotoolsPackage):
    """Cronie contains the standard UNIX daemon crond that runs specified
    programs at scheduled times and related tools."""

    homepage = "https://github.com/cronie-crond/cronie"
    url      = "https://github.com/cronie-crond/cronie/archive/cronie-1.5.5.tar.gz"

    version('1.5.5', sha256='22c2a2b22577c0f776c1268d0e0f305c5c041e10155022a345b43b665da0ffe9')

    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix.sbin)
