# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zfs(AutotoolsPackage):
    """OpenZFS is an advanced file system and volume manager which was
    originally developed for Solaris and is now maintained by the OpenZFS
    community. This repository contains the code for running OpenZFS on
    Linux and FreeBSD."""

    homepage = "https://zfsonlinux.org/"
    url = "https://github.com/openzfs/zfs/releases/download/zfs-0.8.3/zfs-0.8.3.tar.gz"

    license("CDDL-1.0")

    version("0.8.3", sha256="545a4897ce30c2d2dd9010a0fdb600a0d3d45805e2387093c473efc03aa9d7fd")
    version("0.8.2", sha256="47608e257c8ecebb918014ef1da6172c3a45d990885891af18e80f5cc28beab8")
    version("0.8.1", sha256="0af79fde44b7b8ecb94d5166ce2e4fff7409c20ed874c2d759db92909e6c2799")
    version("0.8.0", sha256="0fd92e87f4b9df9686f18e2ac707c16b2eeaf00f682d41c20ea519f3a0fe4705")

    depends_on("c", type="build")  # generated

    depends_on("uuid")
    depends_on("libtirpc")
    depends_on("util-linux")

    def setup_build_environment(self, env):
        env.prepend_path("CPATH", self.spec["util-linux"].prefix.include)
