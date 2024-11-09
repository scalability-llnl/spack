# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libhugetlbfs(AutotoolsPackage):
    """libhugetlbfs is a library which provides easy access
    to huge pages of memory."""

    homepage = "https://github.com/libhugetlbfs/libhugetlbfs"
    url = "https://github.com/libhugetlbfs/libhugetlbfs/releases/download/2.24/libhugetlbfs-2.24.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.24", sha256="d501dfa91c8ead1106967a3d3829f2ba738c3fac0a65cb358ed2ab3870ddc5ef")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    build_targets = ["-e", "libs", "tools"]
    install_targets = ["-e", "install"]
    parallel = False

    def setup_build_environment(self, env):
        env.set("BUILDTYPE", "NATIVEONLY")
        env.set("PREFIX", self.prefix)
        env.set("V", "1")
