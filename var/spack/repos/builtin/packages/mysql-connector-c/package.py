# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MysqlConnectorC(CMakePackage):
    """MySQL Connector/C, the C interface for communicating with MySQL servers.

    Connector/C is a client library that implements the C API for client/server
    communication. It is a standalone replacement for the MySQL client library
    shipped with MySQL Server distributions."""

    homepage = "https://dev.mysql.com/downloads/connector/c/"
    url = "https://dev.mysql.com/get/Downloads/Connector-C/mysql-connector-c-6.1.11-src.tar.gz"

    depends_on("cmake")

    patch("fix-cmake.patch", when="@6.1.11")

    license("GPL-2.0-or-later")

    version("6.1.11", sha256="c8664851487200162b38b6f3c8db69850bd4f0e4c5ff5a6d161dbfb5cb76b6c4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
