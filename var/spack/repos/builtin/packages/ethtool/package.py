# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ethtool(AutotoolsPackage):
    """Ethtool is a small utility for examining and tuning your ethernet-based
    network interface."""

    homepage = "https://github.com/Distrotech/ethtool"
    url = "https://github.com/Distrotech/ethtool/archive/v4.8.tar.gz"

    license("GPL-2.0-only")

    version("4.8", sha256="e4443c612b01b6c4891e21f55a59aa2d6da1c9915edcf067bb66a0855590e143")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--verbose", "--force")
