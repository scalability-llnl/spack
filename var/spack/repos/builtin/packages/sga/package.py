# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sga(AutotoolsPackage):
    """SGA is a de novo genome assembler based on the concept of string graphs.
    The major goal of SGA is to be very memory efficient, which is achieved
    by using a compressed representation of DNA sequence reads."""

    homepage = "https://www.msi.umn.edu/sw/sga"
    url = "https://github.com/jts/sga/archive/v0.10.15.tar.gz"

    version("0.10.15", sha256="1b18996e6ec47985bc4889a8cbc3cd4dd3a8c7d385ae9f450bd474e36342558b")
    version("0.10.14", sha256="763c011b302e1085048c93d917f081ea9348a8470e222dfd369064548e8b3994")
    version("0.10.13", sha256="77859ab233980594941aa4c4cb5c2cbe1f5c43f2519f329c3a88a97865dee599")
    version("0.10.12", sha256="f27f13ce1e7c1a3f35f9f4eed6c1896f3b92471bc4acc7f2364a12ce098e9779")
    version("0.10.11", sha256="4704ad74705931311ed66a0886453e57616798147d149e16e13ac5acd9b5b87c")
    version("0.10.10", sha256="5a75a81d405d22d51f3b7388c42d5baced4388110d39e5d77249bf3eac76a83a")
    version("0.10.9", sha256="34573cb7423affd5e15c1175d9af69f7495b094b60ddfcbafd910fd703c25006")
    version("0.10.8", sha256="55c5e0e425e14902e83d68cfb8cee4c86ee186459e54113a484b2a1b06d223c8")
    version("0.10.3", sha256="c000823a58428d9db2979b30a571ad89aec78a8cb1af60bae1ce252dd4e8adac")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")
    depends_on("sparsehash")
    depends_on("jemalloc")
    depends_on("bamtools")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    configure_directory = "src"

    def configure_args(self):
        return [
            "--with-sparsehash={0}".format(self.spec["sparsehash"].prefix),
            "--with-bamtools={0}".format(self.spec["bamtools"].prefix),
            "--with-jemalloc={0}".format(self.spec["jemalloc"].prefix),
        ]
