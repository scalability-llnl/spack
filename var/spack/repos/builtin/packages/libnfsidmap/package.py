# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libnfsidmap(AutotoolsPackage):
    """Library to help mapping id's, mainly for NFSv4."""

    homepage = "https://github.com/Distrotech/libnfsidmap/"
    url = "https://github.com/Distrotech/libnfsidmap/archive/libnfsidmap-0-27-rc2.tar.gz"

    version("0-26", sha256="8c6d62285b528d673fcb8908fbe230ae82287b292d90925d014c6f367e8425ef")
    version("0-25", sha256="dbf844a2aa820d7275eca55c2e392d12453ab4020d37d532ea6beac47efc4725")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
