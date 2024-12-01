# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Consul(MakefilePackage):
    """Consul is a distributed, highly available,
    and data center aware solution to connect and configure applications
    across dynamic, distributed infrastructure."""

    homepage = "https://www.consul.io"
    url = "https://github.com/hashicorp/consul/archive/v1.8.1.tar.gz"

    license("MPL-2.0")

    version("1.15.3", sha256="5137e9831b4bc094c8ce5be64c661dc0d9a96ee9509d756030d60d4bcca42503")
    version("1.8.1", sha256="c173e9866e6181b3679a942233adade118976414f6ca2da8deaea0fa2bba9b06")
    version("1.8.0", sha256="a87925bde6aecddf532dfd050e907b6a0a6447cdd5dc4f49b46d97c9f73b58f9")
    version("1.7.6", sha256="893abad7563c1f085303705f72d8789b338236972123f0ab6d2be24dbb58c2ac")

    depends_on("go@1.14:")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
