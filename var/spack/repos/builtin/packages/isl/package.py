# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Isl(AutotoolsPackage):
    """isl (Integer Set Library) is a thread-safe C library for manipulating
    sets and relations of integer points bounded by affine constraints."""

    homepage = "https://libisl.sourceforge.io/"
    url = "https://libisl.sourceforge.io/isl-0.21.tar.bz2"

    license("MIT")

    version("0.26", sha256="5eac8664e9d67be6bd0bee5085d6840b8baf738c06814df47eaf4166d9776436")
    version("0.25", sha256="4305c54d4eebc4bf3ce365af85f04984ef5aa97a52e01128445e26da5b1f467a")
    version("0.24", sha256="fcf78dd9656c10eb8cf9fbd5f59a0b6b01386205fe1934b3b287a0a1898145c0")
    version("0.21", sha256="d18ca11f8ad1a39ab6d03d3dcb3365ab416720fcb65b42d69f34f51bf0a0e859")
    version("0.20", sha256="b587e083eb65a8b394e833dea1744f21af3f0e413a448c17536b5549ae42a4c2")
    version("0.19", sha256="d59726f34f7852a081fbd3defd1ab2136f174110fc2e0c8d10bb122173fa9ed8")
    version("0.18", sha256="6b8b0fd7f81d0a957beb3679c81bbb34ccc7568d5682844d8924424a0dadcb1b")
    version("0.15", sha256="8ceebbf4d9a81afa2b4449113cee4b7cb14a687d7a549a963deb5e2a41458b6b")
    version("0.14", sha256="7e3c02ff52f8540f6a85534f54158968417fd676001651c8289c705bd0228f36")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("gmp")

    def configure_args(self):
        return [f"--with-gmp-prefix={self.spec['gmp'].prefix}"]
