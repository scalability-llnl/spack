# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sbt(Package):
    """Scala Build Tool"""

    homepage = "https://www.scala-sbt.org"
    url = "https://github.com/sbt/sbt/releases/download/v1.1.4/sbt-1.1.4.tgz"

    license("Apache-2.0")

    version("1.10.0", sha256="154b7de6c19207c73d0a304f901c8c4b6ead9a9c3a99a98a9d72ac19419d2640")
    version("1.8.3", sha256="21f4210786fd68fd15dca3f4c8ee9cae0db249c54e1b0ef6e829e9fa4936423a")
    version("1.1.6", sha256="f545b530884e3abbca026df08df33d5a15892e6d98da5b8c2297413d1c7b68c1")
    version("1.1.5", sha256="8303d7496bc70eb441e8136bd29ffc295c629dadecefa4e7a475176ab4d282d5")
    version("1.1.4", sha256="2fbd592b1cfd7bc3612154a32925d5843b602490e8c8977a53fa86b35e308341")
    version("0.13.17", sha256="25f782ccb2ad6d54e13ce6cec0afa3d2328874c508d68ee34e2f742e99f2c847")

    depends_on("java")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("conf", prefix.conf)
