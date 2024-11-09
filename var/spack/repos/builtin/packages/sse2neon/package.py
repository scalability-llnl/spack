# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sse2neon(Package):
    """A C/C++ header file that converts Intel SSE intrinsics to Arm/Aarch64
    NEON intrinsics."""

    homepage = "https://github.com/DLTcollab/sse2neon"
    git = "https://github.com/DLTcollab/sse2neon.git"
    url = "https://github.com/DLTcollab/sse2neon/archive/refs/tags/v1.6.0.tar.gz"

    license("MIT")

    version("master", branch="master")
    version("1.7.0", sha256="cee6d54922dbc9d4fa57749e3e4b46161b7f435a22e592db9da008051806812a")
    version("1.6.0", sha256="06f4693219deccb91b457135d836fc514a1c0a57e9fa66b143982901d2d19677")
    version("1.5.1", sha256="4001e2dfb14fcf3831211581ed83bcc83cf6a3a69f638dcbaa899044a351bb2a")
    version("1.5.0", sha256="92ab852aac6c8726a615f77438f2aa340f168f9f6e70c72033d678613e97b65a")

    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install("*.h", prefix.include)
