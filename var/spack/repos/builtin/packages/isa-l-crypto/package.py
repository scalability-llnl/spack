# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class IsaLCrypto(AutotoolsPackage):
    """ISA-L_crypto is a collection of optimized low-level functions
    targeting storage applications. ISA-L_crypto includes:

    - Multi-buffer hashes - run multiple hash jobs together on one
      core for much better throughput than single-buffer versions.
      + SHA1, SHA256, SHA512, MD5
    - Multi-hash - Get the performance of multi-buffer hashing with
      a single-buffer interface.
    - Multi-hash + murmur - run both together.
    - AES - block ciphers
      + XTS, GCM, CBC
    - Rolling hash - Hash input in a window which moves through the input
    """

    homepage = "https://github.com/intel/isa-l_crypto"
    url = "https://github.com/intel/isa-l_crypto/archive/v2.22.0.tar.gz"
    git = "https://github.com/intel/isa-l_crypto.git"
    maintainers("hyoklee")

    license("BSD-3-Clause")

    version("master", branch="master")

    # Current
    version("2.24.0", sha256="1b2d5623f75c94562222a00187c7a9de010266ab7f76e86b553b68bb654d39be")
    version("2.23.0", sha256="4827bc3e281d19a434deaa17a172f22f38c113ffc65f5df4348062165cb89eb8")
    version("2.22.0", sha256="c6503b455bdf0efcad74fdae4e9b30465e0e208cff2b0b34fd8f471553455527")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("yasm@1.2.0:", type="build")
    depends_on("nasm@2.13:", type="build")

    def configure_args(self):
        config_args = ["--enable-shared"]

        return config_args
