# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Activemq(Package):
    """
    Apache ActiveMQ is a high performance Apache 2.0 licensed Message Broker
    and JMS 1.1 implementation.
    """

    homepage = "https://archive.apache.org/dist/activemq"
    url = "https://archive.apache.org/dist/activemq/5.14.0/apache-activemq-5.14.0-bin.tar.gz"

    license("Apache-2.0")

    version("6.1.3", sha256="cad14e816e990f1312709ebfc228f42895d8c54c652d3cd56f0b5145635dc794")
    version("5.18.6", sha256="b1363696e4e014423f6ab22f1ece4bf14ee32b80bfa5bdbae7dd4026a47ff03a")

    # https://nvd.nist.gov/vuln/detail/CVE-2023-46604
    version(
        "5.17.3",
        sha256="a4cc4c3a2f136707c2c696f3bb3ee2a86dbeff1b9eb5e237b14edc0c5e5a328f",
        deprecated=True,
    )
    # https://nvd.nist.gov/vuln/detail/CVE-2018-11775
    version(
        "5.14.0",
        sha256="81c623465af277dd50a141a8d9308d6ec8e1b78d9019b845873dc12d117aa9a6",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated

    depends_on("java")
    depends_on("java@8:", when="@5.15:")
    depends_on("java@11:", when="@5.17:")
    depends_on("java@17:", when="@6:")

    def install(self, spec, prefix):
        install_tree(".", prefix)
