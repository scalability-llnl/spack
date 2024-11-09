# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class W(Package):
    version("3.1")
    version("3.0")

    variant("moveflaglater", default=False)

    depends_on("x +activatemultiflag")
    depends_on('y cflags="-d0"', when="~moveflaglater")
    depends_on('y cflags="-d3"', when="+moveflaglater")

    depends_on("c", type="build")
