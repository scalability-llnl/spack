# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libwebsockets(CMakePackage):
    """C library for lightweight websocket clients and servers."""

    homepage = "https://github.com/warmcat/libwebsockets"
    url = "https://github.com/warmcat/libwebsockets/archive/v2.1.0.tar.gz"
    maintainers("ax3l")

    license("MIT")

    version("4.3.3", sha256="6fd33527b410a37ebc91bb64ca51bdabab12b076bc99d153d7c5dd405e4bdf90")
    version("2.2.1", sha256="e7f9eaef258e003c9ada0803a9a5636757a5bc0a58927858834fb38a87d18ad2")
    version("2.1.1", sha256="96183cbdfcd6e6a3d9465e854a924b7bfde6c8c6d3384d6159ad797c2e823b4d")
    version("2.1.0", sha256="bcc96aaa609daae4d3f7ab1ee480126709ef4f6a8bf9c85de40aae48e38cce66")
    version("2.0.3", sha256="cf0e91b564c879ab98844385c98e7c9e298cbb969dbc251a3f18a47feb94342c")
    version("1.7.9", sha256="86a5105881ea2cb206f8795483d294e9509055decf60436bcc1e746262416438")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")
    depends_on("openssl")

    def cmake_args(self):
        return ["-DLWS_WITHOUT_TESTAPPS=ON"]
