# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libestr(AutotoolsPackage):
    """C library for string handling (and a bit more)."""

    homepage = "https://libestr.adiscon.com/"
    url = "https://github.com/rsyslog/libestr/archive/v0.1.11.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.1.11", sha256="46b53b80f875fd82981d927a45f0c9df9d17ee1d0e29efab76aaa9cd54a46bb4")
    version("0.1.10", sha256="e8756b071540314abef25c044f893d6b5d249e46709329a4b3e7361403c29a1e")
    version("0.1.9", sha256="efa0b90b5fe22844bac26042f988de6e8b2770e28dbd84bf49b9982d9c3e34f8")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
