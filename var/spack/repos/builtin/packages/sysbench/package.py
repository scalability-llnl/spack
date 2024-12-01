# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sysbench(AutotoolsPackage):
    """Scriptable database and system performance benchmark."""

    homepage = "https://github.com/akopytov/sysbench"
    url = "https://github.com/akopytov/sysbench/archive/1.0.20.tar.gz"

    license("GPL-2.0")

    version("1.0.20", sha256="e8ee79b1f399b2d167e6a90de52ccc90e52408f7ade1b9b7135727efe181347f")
    version("1.0.19", sha256="39cde56b58754d97b2fe6a1688ffc0e888d80c262cf66daee19acfb2997f9bdd")
    version("1.0.18", sha256="c679b285e633c819d637bdafaeacc1bec13f37da5b3357c7e17d97a71bf28cb1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("mysql-client")
