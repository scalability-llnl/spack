# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GtkorvoEnet(AutotoolsPackage):
    """ENet reliable UDP networking library.
    This is a downstream branch of lsalzman's ENet.
    This version has expanded the client ID to handle more clients.
    The original is at https://github.com/lsalzman/enet.
    """

    homepage = "https://www.github.com/GTkorvo/enet"
    url = "https://github.com/GTkorvo/enet/archive/v1.3.13.tar.gz"

    license("MIT")

    version("1.3.14", sha256="d1fda051bdee46ad8cce7c3bb36fb6b7a7a443945f27a280ac104753c29465b0")
    version("1.3.13", sha256="ede6e4f03e4cb0c3d93044ace9e8c1818ef4d3ced4aaa70384155769b3c436dc")

    depends_on("c", type="build")  # generated
