# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libtermkey(MakefilePackage):
    """Easy keyboard entry processing for terminal programs"""

    homepage = "http://www.leonerd.org.uk/code/libtermkey/"
    url = "http://www.leonerd.org.uk/code/libtermkey/libtermkey-0.18.tar.gz"

    license("MIT")

    version("0.22", sha256="6945bd3c4aaa83da83d80a045c5563da4edd7d0374c62c0d35aec09eb3014600")
    version("0.18", sha256="239746de41c845af52bb3c14055558f743292dd6c24ac26c2d6567a5a6093926")
    version("0.17", sha256="68949364ed5eaad857b3dea10071cde74b00b9f236dfbb702169f246c3cef389")
    version("0.16", sha256="6c8136efa5d0b3277014a5d4519ea81190079c82656b7db1655a1bd147326a70")
    version("0.15b", sha256="6825422c6297e4f81b2c48962b4512585ca8a50bf31f24b3234a1be71a9d7a6e")
    version("0.14", sha256="3d114d4509499b80a583ea39cd35f18268aacf4a7bbf56c142cd032632005c79")

    depends_on("c", type="build")  # generated

    depends_on("gzip", type="build")
    depends_on("libtool", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("unibilium")

    def setup_build_environment(self, env):
        env.set("LIBTOOL", self.spec["libtool"].prefix.bin.join("libtool"))

    def build(self, spec, prefix):
        make("PREFIX=" + prefix)

    def install(self, spec, prefix):
        make("install", "PREFIX=" + prefix)
