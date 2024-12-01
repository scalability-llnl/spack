# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SquashfsMount(MakefilePackage):
    """Allows non-root users to mount squashfs files without the overhead of
    squashfuse."""

    homepage = "https://github.com/eth-cscs/squashfs-mount"
    url = "https://github.com/eth-cscs/squashfs-mount/archive/refs/tags/v0.1.0.tar.gz"

    maintainers("haampie")

    license("BSD-3-Clause")

    version("0.4.0", sha256="0b17c797b4befdab172fc58a74f3b647bbdf127ff5bdaf7c21d907b7a9714339")
    version("0.1.0", sha256="37841ede7a7486d437fd06ae13e432560f81806f69addc72cfc8e564c8727bc6")

    depends_on("c", type="build")  # generated

    variant("suid", default=False, description="Make squashfs-mount a suid executable")

    depends_on("util-linux", type="link")

    def install(self, spec, prefix):
        tgt = "install" if "~suid" in spec else "install-suid"
        make(tgt, "prefix=" + prefix)
