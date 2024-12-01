# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Slf4j(MavenPackage):
    """The Simple Logging Facade for Java (SLF4J) serves as a simple facade
    or abstraction for various logging frameworks (e.g. java.util.logging,
    logback,log4j) allowing the end user to plug in the desired logging
    framework at deployment time."""

    homepage = "http://www.slf4j.org/"
    url = "https://github.com/qos-ch/slf4j/archive/v_1.7.30.tar.gz"

    license("MIT")

    version("1.7.30", sha256="217519588d0dd1f85cee2357ca31afdd7c0a1a8a6963953b3bf455cf5174633e")
    version("1.7.29", sha256="e584f1f380d8c64ed8a45944cec3c2fb4d6b850783fd5bc166a9246bc8b6ac56")
    version("1.7.28", sha256="14063bfcbc942bda03e07759e64307163c1646d70a42c632f066812a8630eec7")
    version("1.7.27", sha256="238883cab9808a5cd58cf5245f9f13ac645c9fca878b60d959e00fc4ac588231")
    version("1.7.26", sha256="dc422820f92e581241c4cfe796d01531d12bad3dc04225bdb315761871156942")

    depends_on("java@8", type=("build", "run"))
