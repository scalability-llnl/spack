# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zopfli(CMakePackage):
    """Zopfli Compression Algorithm is a compression library programmed
    in C to perform very good, but slow, deflate or zlib compression."""

    homepage = "https://github.com/google/zopfli"
    url = "https://github.com/google/zopfli/archive/refs/tags/zopfli-1.0.3.tar.gz"

    variant("shared", default=False, description="Build shared libraries")

    license("Apache-2.0")

    version("1.0.3", sha256="e955a7739f71af37ef3349c4fa141c648e8775bceb2195be07e86f8e638814bd")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def cmake_args(self):
        args = [self.define_from_variant("ZOPFLI_BUILD_SHARED", "shared")]

        return args
