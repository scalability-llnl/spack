# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fpart(AutotoolsPackage):
    """Fpart is a filesystem partitioner. It helps you sort file trees and pack them
    into bags (called "partitions"). Fpsync wraps fpart and rsync, tar, or cpio
    to launch several synchronization jobs in parallel."""

    homepage = "https://www.fpart.org"
    url = "https://github.com/martymac/fpart/archive/refs/tags/fpart-1.5.1.tar.gz"
    git = "https://github.com/martymac/fpart.git"

    maintainers("drkrynstrng")

    license("BSD-2-Clause", checked_by="drkrynstrng")

    version("master", branch="master")
    version("1.6.0", sha256="ed1fac2853fc421071b72e4c5d8455a231bc30e50034db14af8b0485ece6e097")
    version("1.5.1", sha256="c353a28f48e4c08f597304cb4ebb88b382f66b7fabfc8d0328ccbb0ceae9220c")

    variant("embfts", default=False, description="Build with embedded fts functions")
    variant("static", default=False, description="Build static binary")
    variant("debug", default=False, description="Build with debugging support")
    # fpsync has the following run dependencies, at least one is required
    variant(
        "fpsynctools",
        default="rsync",
        values=("rsync", "tar", "cpio"),
        multi=True,
        description="Tools used by fpsync to copy files",
    )

    depends_on("c", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("rsync", when="fpsynctools=rsync", type="run")
    depends_on("tar", when="fpsynctools=tar", type="run")
    depends_on("cpio", when="fpsynctools=cpio", type="run")

    def configure_args(self):
        config_args = []
        config_args.extend(self.enable_or_disable("embfts"))
        config_args.extend(self.enable_or_disable("static"))
        config_args.extend(self.enable_or_disable("debug"))
        return config_args
