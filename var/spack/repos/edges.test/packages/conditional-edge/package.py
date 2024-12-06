# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class ConditionalEdge(Package):
    """This package has a variant that triggers a condition only if a required dependency is
    providing a virtual.
    """

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant("foo", default=False, description="Just a regular foo")

    # zlib is a real package, providing zlib-api
    depends_on("zlib")
    depends_on("zlib-api", when="+foo")
    depends_on("zlib@1.0", when="^[virtuals=zlib-api] zlib")
