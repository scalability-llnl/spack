# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LksctpTools(AutotoolsPackage):
    """A Linux SCTP helper library"""

    homepage = "https://github.com/sctp/lksctp-tools"
    url = "https://github.com/sctp/lksctp-tools/archive/v1.0.18.tar.gz"

    license("GPL-2.0-or-later AND LGPL-2.1-or-later")

    version("1.0.21", sha256="8738bf17ecffbbe2440a6e2ffaf1cbcebb633fc99d63d88761af35c02a571893")
    version("1.0.18", sha256="3e9ab5b3844a8b65fc8152633aafe85f406e6da463e53921583dfc4a443ff03a")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
