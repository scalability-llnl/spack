# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zookeeper(Package):
    """
    Apache ZooKeeper is an effort to develop and maintain an open-source
    server which enables highly reliable distributed coordination.
    """

    homepage = "https://archive.apache.org"
    urls = [
        "https://archive.apache.org/dist/zookeeper/zookeeper-3.8.4/apache-zookeeper-3.8.4-bin.tar.gz",
        "https://archive.apache.org/dist/zookeeper/zookeeper-3.4.11/zookeeper-3.4.11.tar.gz",
    ]

    license("Apache-2.0")

    version("3.8.4", sha256="284cb4675adb64794c63d95bf202d265cebddc0cda86ac86fb0ede8049de9187")
    with default_args(deprecated=True):
        # 3.6 is EoL since 30th of December, 2022
        # 3.5 is EoL since 1st of June, 2022
        version(
            "3.4.11", sha256="f6bd68a1c8f7c13ea4c2c99f13082d0d71ac464ffaf3bf7a365879ab6ad10e84"
        )

    depends_on("java")

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        env.set("ZOOBINDIR", self.prefix.bin)
        env.set("ZOOCFGDIR", ".")
        env.set("ZOO_LOG_DIR", ".")
