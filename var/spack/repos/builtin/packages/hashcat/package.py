# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hashcat(MakefilePackage):
    """hashcat is the world's fastest and most advanced password recovery
    utility, supporting five unique modes of attack for over 300 highly
    optimized hashing algorithms. hashcat currently supports CPUs, GPUs,
    and other hardware accelerators on Linux, Windows, and macOS,and has
    facilities to help enable distributed password cracking."""

    homepage = "https://hashcat.net/hashcat/"
    url = "https://github.com/hashcat/hashcat/archive/v6.1.1.tar.gz"

    license("MIT")

    version("6.2.6", sha256="b25e1077bcf34908cc8f18c1a69a2ec98b047b2cbcf0f51144dcf3ba1e0b7b2a")
    version("6.1.1", sha256="39c140bbb3c0bdb1564bfa9b9a1cff49115a42f4c9c19e9b066b617aea309f80")
    version("6.1.0", sha256="916f92434e3b36a126be1d1247a95cd3b32b4d814604960a2ca325d4cc0542d1")
    version("6.0.0", sha256="e8e70f2a5a608a4e224ccf847ad2b8e4d68286900296afe00eb514d8c9ec1285")
    version("5.1.0", sha256="283beaa68e1eab41de080a58bb92349c8e47a2bb1b93d10f36ea30f418f1e338")
    version("5.0.0", sha256="7092d98cf0d8b29bd6efe2cf94802442dd8d7283982e9439eafbdef62b0db08f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        make("SHARED=1", "PREFIX={0}".format(prefix), "install")
