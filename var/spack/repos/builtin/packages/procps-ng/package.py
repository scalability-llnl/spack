# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ProcpsNg(AutotoolsPackage):
    """Utilities that provide system information."""

    homepage = "https://sourceforge.net/projects/procps-ng/"
    url = "https://udomain.dl.sourceforge.net/project/procps-ng/Production/procps-ng-3.3.16.tar.xz"

    license("GPL-2.0-or-later AND LGPL-2.1-or-later", checked_by="tgamblin")

    version("3.3.16", sha256="925eacd65dedcf9c98eb94e8978bbfb63f5de37294cc1047d81462ed477a20af")

    depends_on("c", type="build")  # generated

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
