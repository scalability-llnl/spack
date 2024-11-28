# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Aria2(AutotoolsPackage):
    """An ultra fast download utility"""

    homepage = "https://aria2.github.io"
    url = "https://github.com/aria2/aria2/releases/download/release-1.36.0/aria2-1.36.0.tar.gz"

    license("GPL-2.0-or-later")

    version("1.37.0", sha256="8e7021c6d5e8f8240c9cc19482e0c8589540836747744724d86bf8af5a21f0e8")
    version("1.36.0", sha256="b593b2fd382489909c96c62c6e180054c3332b950be3d73e0cb0d21ea8afb3c5")
    version("1.35.0", sha256="fd85589416f8246cefc4e6ba2fa52da54fdf11fd5602a2db4b6749f7c33b5b2d")
    version("1.34.0", sha256="ec4866985760b506aa36dc9021dbdc69551c1a647823cae328c30a4f3affaa6c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libxml2")
    depends_on("libssh2")
    depends_on("libgcrypt")
    depends_on("zlib-api")
    depends_on("c-ares")
    depends_on("sqlite")
