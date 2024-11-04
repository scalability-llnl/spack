# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Yajl(CMakePackage):
    """Yet Another JSON Library (YAJL)"""

    homepage = "https://lloyd.github.io/yajl/"
    url = "https://github.com/lloyd/yajl/archive/refs/tags/2.1.0.zip"
    git = "https://github.com/lloyd/yajl.git"

    license("MIT")

    version("develop", branch="master")
    version("2.1.0", sha256="7458c4ed10ebe52c54f57e741bbfde69c73495e76e0f6a45d6d1986cf24794bc")
