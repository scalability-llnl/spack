# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bgpdump(AutotoolsPackage):
    """Utility and C Library for parsing MRT files"""

    homepage = "https://github.com/RIPE-NCC/bgpdump/wiki"
    git = "https://github.com/RIPE-NCC/bgpdump.git"

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("bzip2")
