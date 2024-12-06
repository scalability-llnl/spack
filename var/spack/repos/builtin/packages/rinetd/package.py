# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rinetd(AutotoolsPackage):
    """This program is used to efficiently redirect connections
    from one IP address/port combination to another."""

    homepage = "https://github.com/samhocevar/rinetd"
    url = "https://github.com/samhocevar/rinetd/archive/v0.70.tar.gz"

    license("GPL-2.0-only")

    version("0.73", sha256="62d3e5800299bb3940aea847ffd7662722deb5d4b85625fcfe8f7ebbc0424c80")
    version("0.70", sha256="e69538e9d1fdc1ba5cc24733a52c571568e9cad0876c09144aa1eaa71e13fba5")
    version("0.63", sha256="1f0e8cda524b8f4811a876e69e16d11f12c33a63d00b55c66e2129f87444000c")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./bootstrap")
