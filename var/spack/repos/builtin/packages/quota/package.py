# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Quota(AutotoolsPackage):
    """Linux Diskquota system as part of the Linux kernel."""

    homepage = "https://sourceforge.net/projects/linuxquota/"
    url = (
        "https://udomain.dl.sourceforge.net/project/linuxquota/quota-tools/4.05/quota-4.05.tar.gz"
    )

    version("4.05", sha256="ef3b5b5d1014ed1344b46c1826145e20cbef8db967b522403c9a060761cf7ab9")

    depends_on("c", type="build")  # generated

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
