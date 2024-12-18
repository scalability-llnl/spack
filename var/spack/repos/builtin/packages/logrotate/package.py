# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Logrotate(AutotoolsPackage):
    """The logrotate utility is designed to simplify the administration of
    log files on a system which generates a lot of log files."""

    homepage = "https://github.com/logrotate/logrotate"
    url = "https://github.com/logrotate/logrotate/archive/3.17.0.tar.gz"

    license("GPL-2.0-or-later")

    version("3.21.0", sha256="7f58d6ab7e4eab3403528a88d3747a91b03e83e866a8fb966551016e0df527bb")
    version("3.17.0", sha256="c25ea219018b024988b791e91e9f6070c34d2056efa6ffed878067866c0ed765")
    version("3.16.0", sha256="bc6acfd09925045d48b5ff553c24c567cfd5f59d513c4ac34bfb51fa6b79dc8a")
    version("3.15.1", sha256="a7b20f5184c9598c36546f9200d3bd616d561478a0423ab8074e97a1cd7b1c25")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("popt")
    depends_on("acl")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
