# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lxc(AutotoolsPackage):
    """LXC is the well-known and heavily tested low-level Linux container
    runtime. It is in active development since 2008 and has proven itself
    in critical production environments world-wide. Some of its core
    contributors are the same people that helped to implement various
    well-known containerization features inside the Linux kernel."""

    homepage = "https://linuxcontainers.org/lxc/"
    url = "https://github.com/lxc/lxc/archive/lxc-4.0.2.tar.gz"

    license("LGPL-2.1-or-later")

    version("4.0.2", sha256="89a9f1c6c9c0c43ffc4ec4d281381d60dcf698af1578effa491be97885ab282a")
    version("4.0.1", sha256="5b17c48db24d93f8a687bf4557358e252126c50a66f5756b3e0ea2cf04a60d05")
    version("4.0.0", sha256="8cd36f002f656bbcd01679e6b8892f81ed036d5589aed45b36358014b32277dd")
    version("3.2.1", sha256="59f46fad0a6d921c59a6768ba781295e0986989a96e2d216de2b4b3a14392e65")
    version("3.2.0", sha256="5dbf25a1c15aa96e184a4e9ef580d40f08bf06818ad21614d6c79fce5447c7eb")
    version("3.1.0", sha256="14c34bb3390c60331107a5fbd5c6520e4873c774de2293e9efcb3c0e860b807d")
    version("3.0.4", sha256="12a126e634a8df81507fd9d3a4984bacaacf22153c11f024e215810ea78fcc4f")
    version("3.0.3", sha256="e794f287755d2529cb49f01b72802abfec31f2a02259719b60a62897da6e8298")
    version("2.0.11", sha256="31334ffe0e2d8e38779d80ce670a523f4f5559c2a02c9e085c2f0cf43995d0b0")
    version("2.0.10", sha256="b748de0914467aafea18a568602735907fc95f4272609dba7b0f8c91d7dde776")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def configure_args(self):
        args = [
            "bashcompdir="
            + join_path(self.spec["lxc"].prefix, "share", "bash-completion", "completions")
        ]
        return args
