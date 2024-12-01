# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Drill(Package):
    """
    Apache Drill is a distributed MPP query layer that supports SQL and
    alternative query languages against NoSQL and Hadoop data storage
    systems.
    """

    homepage = "https://drill.apache.org/"
    url = "https://dist.apache.org/repos/dist/release/drill/1.17.0/apache-drill-1.17.0.tar.gz"
    git = "https://github.com/apache/drill.git"

    license("Apache-2.0", checked_by="wdconinc")

    version("1.21.2", sha256="77e2e7438f1b4605409828eaa86690f1e84b038465778a04585bd8fb21d68e3b")
    version("1.20.3", sha256="1520cd2524cf8e0ce45fcf02e8e5e3e044465c6dacad853f9fadf9c918863cad")
    with default_args(deprecated=True):
        # Log4Shell vulnerability (CVE-2021-44228) affects all versions before 1.20.0
        version(
            "1.17.0", sha256="a3d2d544bcc32b915fb53fced0f982670bd6fe2abd764423e566a5f6b54debf1"
        )
        version(
            "1.16.0", sha256="fd195d2b38f393459b37d8f13ac1f36cdbe38495eabb08252da38e3544e87839"
        )
        version(
            "1.15.0", sha256="188c1d0df28e50f0265f4bc3c5871b4e7abc9450a4e5a7dbe7f0b23146bec76b"
        )
        version(
            "1.14.0", sha256="1145bdbb723119f271d32daf4cdd77cdeebe88ddcb7d04facd585b715bb5723b"
        )
        version(
            "1.13.0", sha256="8da6d56f75ae01e0bee6176095d32760e7183dd0200f10ee68b8cd3f882def6a"
        )

    # pom.xml, requireJavaVersion
    depends_on("java@7:", type="run")
    depends_on("java@8:", type="run", when="@1.14:")

    def install(self, spec, prefix):
        install_tree(".", prefix)
