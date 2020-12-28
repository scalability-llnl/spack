# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ProcpsNg(AutotoolsPackage):
    """Utilities that provide system information."""

    homepage = "https://sourceforge.net/projects/procps-ng"
    url      = "https://udomain.dl.sourceforge.net/project/procps-ng/Production/procps-ng-3.3.16.tar.xz"

    version('3.3.16', sha256='925eacd65dedcf9c98eb94e8978bbfb63f5de37294cc1047d81462ed477a20af')

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix.sbin)
