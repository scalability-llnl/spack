# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SqliteJdbc(MavenPackage):
    """SQLite JDBC, developed by Taro L. Saito, is a library for accessing
    and creating SQLite database files in Java."""

    homepage = "https://github.com/xerial/sqlite-jdbc"
    url = "https://github.com/xerial/sqlite-jdbc/archive/3.32.3.2.tar.gz"

    license("Apache-2.0")

    version("3.32.3.2", sha256="9168ad02cb8b01449271eabd8a2a81461954c2c3fa854d3828a37dc07a1fefec")
    version("3.32.3.1", sha256="455e2a009101ede40f9510cf2c34e76f30d411f290957bfd9296da12d6e06591")
    version("3.32.3", sha256="19725caa4742960d385472a6094b8164bb8f29e816f04b830fa65c56517b4564")

    depends_on("c", type="build")  # generated
