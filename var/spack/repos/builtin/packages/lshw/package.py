# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lshw(MakefilePackage):
    """
    lshw is a small tool to provide detailed information on the
    hardware configuration of the machine. It can report exact memory
    configuration, firmware version, mainboard configuration, CPU version
    and speed, cache configuration, bus speed, etc. on DMI-capable x86 or
    EFI (IA-64) systems and on some ARM and PowerPC machines.
    """

    homepage = "https://github.com/lyonel/lshw"
    url = "https://github.com/lyonel/lshw/archive/B.02.18.tar.gz"
    list_url = "https://github.com/lyonel/lshw/tags"

    license("GPL-2.0-only", checked_by="wdconinc")

    version("02.20", sha256="6b8346a89fb0f0f1798e66f6a707a881d38b9b3a67256b30fc4628dac09f291a")
    version("02.18", sha256="aa8cb2eebf36e9e46dfc227f24784aa8c87181ec96e57ee6c455da8a0ce4fa77")
    version("02.17", sha256="0bb76c7df7733dc9b80d5d35f9d9752409ddb506e190453a2cc960461de5ddeb")
    version("02.16", sha256="58a7731d204791dd33db5eb3fde9808d1235283e069e6c33a193637ccec27b3e")
    version("02.15", sha256="33c51ba0554d4bcd8ff9a67e5971a63b9ddd58213e2901a09000815376bc61b9")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    def setup_build_environment(self, env):
        env.set("PREFIX", self.prefix)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
