# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LibpressioSperr(CMakePackage):
    """A LibPressio plugin for Sperr"""

    homepage = "https://github.com/robertu94/libpressio-sperr"
    url = "https://github.com/robertu94/libpressio-sperr/archive/refs/tags/0.0.4.tar.gz"
    git = homepage

    maintainers("robertu94")

    license("GPL-3.0-only")

    version("master", branch="master")
    version("0.0.5", sha256="8fda62ad923b4229b9a434d5f9197010e396e972ffb9e29c2e7783ec14fdc324")
    version("0.0.4", sha256="97f2879460b1a28ed8ebf0c300c1cf7ceeb2c7aa7b8a1307ed19bf8cce0b7941")
    version("0.0.3", sha256="e0d1fd083419aaaa243cbf780b7de17aeb96533000071088aa21ec238d358ecc")
    version("0.0.2", sha256="61995d687f9e7e798e17ec7238d19d917890dc0ff5dec18293b840c4d6f8c115")
    version("0.0.1", sha256="e2c164822708624b97654046b42abff704594cba6537d6d0646d485bdf2d03ca")

    depends_on("cxx", type="build")  # generated

    depends_on("libpressio@0.99.4:", when="@0.0.5:")
    depends_on("libpressio@0.88.0:", when="@0.0.3:0.0.4")
    depends_on("libpressio@:0.88.0", when="@:0.0.2")
    depends_on("sperr@:0.6.2", when="@:0.0.3")
    depends_on("sperr@0.7.1:", when="@0.0.4:")
    depends_on("pkgconfig", type="build")
