# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Authd(MakefilePackage):
    """authd is a small and fast RFC 1413 ident protocol daemon with
    both xinetd server and interactive modes that supports IPv6 and
    IPv4 as well as the more popular features of pidentd."""

    homepage = "https://github.com/InfrastructureServices/authd"
    url = "https://github.com/InfrastructureServices/authd/releases/download/v1.4.4/authd-1.4.4.tar.gz"

    license("GPL-2.0-only")

    version("1.4.4", sha256="71ee3d1c3e107c93e082148f75ee460c949b203c861dd20d48f7c5cfdc272bf8")

    depends_on("c", type="build")  # generated

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)

    def install(self, spec, prefix):
        make(f"prefix={prefix}", "install")
