# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Smartmontools(AutotoolsPackage):
    """S.M.A.R.T. utility toolset."""

    homepage = "https://smartmontools.sourceforge.net"
    url = "https://nchc.dl.sourceforge.net/project/smartmontools/smartmontools/6.6/smartmontools-6.6.tar.gz"

    license("GPL-2.0-or-later")

    version("6.6", sha256="51f43d0fb064fccaf823bbe68cf0d317d0895ff895aa353b3339a3b316a53054")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.usr.lib)
