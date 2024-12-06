# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Powertop(AutotoolsPackage):
    """Powertop is a Linux tool to diagnose issues with power consumption
    and power management"""

    homepage = "https://01.org/powertop/"
    url = "https://01.org/sites/default/files/downloads/powertop/powertop-v2.9.tar.gz"

    license("GPL-2.0-only")

    version("2.9", sha256="aa7fb7d8e9a00f05e7d8a7a2866d85929741e0d03a5bf40cab22d2021c959250")

    depends_on("libnl")
    depends_on("ncurses", type="link")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
