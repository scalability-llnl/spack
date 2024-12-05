# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hivex(AutotoolsPackage):
    """Windows Registry "hive" extraction library."""

    homepage = "https://libguestfs.org"
    url = "https://libguestfs.org/download/hivex/hivex-1.3.17.tar.gz"

    license("LGPL-2.1")

    version("1.3.23", sha256="40cf5484f15c94672259fb3b99a90bef6f390e63f37a52a1c06808a2016a6bbd")
    version("1.3.19", sha256="5102cc5149767229dbfb436ae7b47dd85b90e0215445e42c2809cbe32e54f762")
    version("1.3.18", sha256="8a1e788fd9ea9b6e8a99705ebd0ff8a65b1bdee28e319c89c4a965430d0a7445")
    version("1.3.17", sha256="13cb4b87ab72d74d9e83e56ae0f77152312f33ee772dc84fdd86b2cb9e8c52db")

    depends_on("c", type="build")  # generated

    depends_on("perl")
