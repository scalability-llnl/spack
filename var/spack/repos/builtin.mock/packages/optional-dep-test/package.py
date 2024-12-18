# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OptionalDepTest(Package):
    """Description"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/optional_dep_test-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")
    version("1.1", md5="0123456789abcdef0123456789abcdef")

    variant("a", default=False)
    variant("f", default=False)
    variant("mpi", default=False)

    depends_on("pkg-a", when="+a")
    depends_on("pkg-b", when="@1.1")
    depends_on("pkg-c", when="%intel")
    depends_on("pkg-d", when="%intel@64.1")
    depends_on("pkg-e", when="%clang@34:40")

    depends_on("pkg-f", when="+f")
    depends_on("pkg-g", when="^pkg-f")
    depends_on("mpi", when="^pkg-g")

    depends_on("mpi", when="+mpi")
