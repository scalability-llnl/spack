# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Conserver(AutotoolsPackage):
    """Conserver is an application that allows multiple users to
    watch a serial console at the same time."""

    homepage = "https://www.conserver.com/"
    url = "https://github.com/bstansell/conserver/releases/download/v8.2.5/conserver-8.2.5.tar.gz"

    license("BSD-3-Clause")

    version("8.2.7", sha256="0607f2147a4d384f1e677fbe4e6c68b66a3f015136b21bcf83ef9575985273d8")
    version("8.2.5", sha256="7db192f304126d7e5c15421c4c83cd5c08039f2f2b3c61b2998e71881ae47eea")
    version("8.2.4", sha256="a591eabb4abb632322d2f3058a2f0bd6502754069a99a153efe2d6d05bd97f6f")
    version("8.2.3", sha256="764443b2798047f7429747510eeb3207240260590551700d13dbbad8a5bdee08")
    version("8.2.2", sha256="05ea1693bf92b42ad2f0a9389c60352ccd35c2ea93c8fc8e618d0153362a7d81")
    version("8.2.1", sha256="251ae01997e8f3ee75106a5b84ec6f2a8eb5ff2f8092438eba34384a615153d0")

    depends_on("c", type="build")  # generated

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
