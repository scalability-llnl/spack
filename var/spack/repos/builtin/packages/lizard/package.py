# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lizard(MakefilePackage):
    """Lizard (formerly LZ5) is an efficient compressor with very
    fast decompression. It achieves compression ratio that is
    comparable to zip/zlib and zstd/brotli (at low and medium
    compression levels) at decompression speed of 1000 MB/s and
    faster."""

    homepage = "https://github.com/inikep/lizard"
    url = "https://github.com/inikep/lizard/archive/v1.0.tar.gz"
    git = "https://github.com/inikep/lizard.git"

    version("develop", branch="lizard")
    version("2.0", sha256="85456b7274c9f0e477ff8e3f06dbc2f8ee8619d737a73c730c8a1adacb45f6da")
    version("1.0", sha256="6f666ed699fc15dc7fdaabfaa55787b40ac251681b50c0d8df017c671a9457e6")

    depends_on("c", type="build")  # generated

    patch("fix-install-decompress.patch", when="@1.0")

    def install(self, spec, prefix):
        make(f"PREFIX={prefix}", "install")
