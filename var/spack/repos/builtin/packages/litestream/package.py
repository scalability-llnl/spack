# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Litestream(GoPackage):
    """Streaming replication for SQLite."""

    homepage = "https://github.com/benbjohnson/litestream"
    url = "https://github.com/benbjohnson/litestream/archive/refs/tags/v0.3.13.tar.gz"

    maintainers("alecbcs")

    license("Apache-2.0", checked_by="cmelone")

    version("0.3.13", sha256="92cb22323b8168f6efdfcad270772fea9e78c709a7149b1bf35d81fcb88bdaf9")

    depends_on("go@1.21:", type="build", when="@0.3.12:")

    build_directory = "cmd/litestream"
