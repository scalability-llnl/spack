# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmacaroons(AutotoolsPackage):
    """ "This library provides an implementation of macaroons[1], which
    are flexible authorization tokens that work great in distributed
    systems."""

    homepage = "https://github.com/rescrv/libmacaroons/"
    url = "https://github.com/rescrv/libmacaroons/archive/releases/0.3.0.tar.gz"

    license("BSD-3-Clause")

    version("0.3.0", sha256="e1db403c01b0407a276a84b2aaf54515faebe1a5c1a31ec10857a1917161d109")
    version("0.2.0", sha256="fa2146d89a4e844703896ece778f0c42b2b0ee3d09dea350ff34fd6873e72018")
    version("0.1.0", sha256="0aa413d8a793f004874695466f93eed9c8e721524765704fe410694583928007")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("libsodium")
