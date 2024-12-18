# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Unqlite(CMakePackage):
    """UnQLite is a in-process software library which implements a self-contained,
    serverless, zero-configuration, transactional NoSQL database engine."""

    homepage = "https://unqlite.org/"
    url = "https://github.com/symisc/unqlite/archive/v1.1.9.tar.gz"
    git = "https://github.com/symisc/unqlite.git"

    license("JSON")

    version("master", branch="master")
    version("1.1.9", sha256="33d5b5e7b2ca223942e77d31112d2e20512bc507808414451c8a98a7be5e15c0")

    depends_on("c", type="build")  # generated

    # This patch corresponds to https://github.com/symisc/unqlite/pull/99
    patch("0001-Removed-the-STATIC-key-word-to-enable-building-a-sha.patch", when="@1.1.9")

    def cmake_args(self):
        args = ["-DBUILD_SHARED_LIBS:BOOL=ON"]
        return args
