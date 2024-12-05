# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ignite(Package):
    """
    Apache Ignite is a memory-centric distributed database, caching, and
    processing platform for transactional, analytical, and streaming
    workloads delivering in-memory speeds at petabyte scale.
    """

    homepage = "https://ignite.apache.org/"
    url = "https://archive.apache.org/dist/ignite/2.6.0/apache-ignite-hadoop-2.6.0-bin.zip"

    license("CC0-1.0")

    version("2.6.0", sha256="be40350f301a308a0ab09413a130d421730bf253d200e054b82a7d0c275c69f2")
    version("2.5.0", sha256="00bd35b6c50754325b966d50c7eee7067e0558f3d52b3dee27aff981b6da38be")
    version("2.4.0", sha256="3d4f44fbb1c46731cf6ad4acce26da72960b292b307221cec55057b4f305abd9")
    version("2.3.0", sha256="aae162c3df243592f7baa0d63b9bf60a7bdb00c7198f43e75b0a777a6fe5b639")
    version("2.2.0", sha256="e4c150f59b11e14fdf4f663cf6f2c433dd55c17720221c89f3c67b9868177bd3")

    depends_on("java", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)
