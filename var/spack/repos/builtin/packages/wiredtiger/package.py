# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Wiredtiger(AutotoolsPackage):
    """WiredTiger is an high performance, scalable, production quality,
    NoSQL, Open Source extensible platform for data management."""

    homepage = "https://source.wiredtiger.com/"
    url = "https://github.com/wiredtiger/wiredtiger/releases/download/10.0.0/wiredtiger-10.0.0.tar.bz2"

    version("10.0.0", sha256="4830107ac744c0459ef99697652aa3e655c2122005a469a49d221e692fb834a5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@3:", type=("build", "run"), when="+python")
    depends_on("swig", type=("build", "run"), when="+python")
    depends_on("lz4", when="+lz4")
    depends_on("snappy", when="+snappy")
    depends_on("zlib-api", when="+zlib")
    depends_on("zstd", when="+zstd")
    depends_on("rsync", type="build")

    variant("python", default=False, description="Compile Python API")
    variant("lz4", default=False, description="Build the lz4 compressor extension")
    variant("snappy", default=False, description="Build the snappy compressor extension")
    variant("zlib", default=False, description="Build the zlib compressor extension")
    variant("zstd", default=False, description="Build the zstd compressor extension")

    def configure_args(self):
        args = []
        args += self.enable_or_disable("python")
        args += self.enable_or_disable("lz4")
        args += self.enable_or_disable("snappy")
        args += self.enable_or_disable("zlib")
        args += self.enable_or_disable("zstd")
        return args
