# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Orc(CMakePackage):
    """The smallest, fastest columnar storage for Hadoop workloads."""

    homepage = "https://orc.apache.org/"
    url = "https://github.com/apache/orc/archive/rel/release-1.6.5.tar.gz"

    license("BSD-2-Clause")

    version("1.6.5", sha256="df5885db8fa2e4435db8d486c6c7fc4e2c565d6197eee27729cf9cbdf36353c0")

    depends_on("cxx", type="build")  # generated

    depends_on("maven")
    depends_on("openssl")
    depends_on("zlib-api")
    depends_on("zlib@1.2.11:", when="^[virtuals=zlib-api] zlib")
    depends_on("pcre")
    depends_on("protobuf@3.5.1:")
    depends_on("zstd@1.4.5:")
    depends_on("googletest@1.8.0:")
    depends_on("snappy@1.1.7:")
    depends_on("lz4@1.7.5:")

    patch("thirdparty.patch")

    def cmake_args(self):
        args = []
        args.append("-DCMAKE_CXX_FLAGS=" + self.compiler.cxx_pic_flag)
        args.append("-DCMAKE_C_FLAGS=" + self.compiler.cc_pic_flag)
        args.append("-DINSTALL_VENDORED_LIBS:BOOL=OFF")
        args.append("-DBUILD_LIBHDFSPP:BOOL=OFF")
        args.append("-DBUILD_TOOLS:BOOL=OFF")
        args.append("-DBUILD_CPP_TESTS:BOOL=OFF")

        for x in ("snappy", "zstd", "lz4", "protobuf"):
            args.append("-D{0}_HOME={1}".format(x.upper(), self.spec[x].prefix))

        args.append(self.define("ZLIB_HOME", self.spec["zlib-api"].prefix))

        return args
