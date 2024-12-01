# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sqlitebrowser(CMakePackage):
    """DB Browser for SQLite (DB4S) is a high quality, visual,
    open source tool to create, design, and edit database files
    compatible with SQLite."""

    homepage = "https://sqlitebrowser.org"
    url = "https://github.com/sqlitebrowser/sqlitebrowser/archive/v3.10.1.tar.gz"

    license("GPL-3.0-only")

    version("3.12.2", sha256="645f98d38e5d128a449e93cebf03c8070f9eacd2d16b10e433a781d54a9d478a")
    version("3.10.1", sha256="36eb53bc75192c687dce298c79f1532c410ce4ecbeeacfb07b9d02a307f16bef")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    msg = "sqlitebrowser requires C++11 support"
    conflicts("%gcc@:4.8.0", msg=msg)
    conflicts("%apple-clang@:3.9", msg=msg)
    conflicts("%clang@:3.2", msg=msg)
    conflicts("%intel@:12", msg=msg)
    conflicts("%xl@:13.0", msg=msg)
    conflicts("%xl_r@:13.0", msg=msg)

    depends_on("sqlite@3:+functions")
    depends_on("qt@5.5:")
