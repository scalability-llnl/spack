# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lzop(CMakePackage):
    """lzop is a file compressor which is very similar to gzip. lzop uses
    the LZO data compression library for compression services, and its main
    advantages over gzip are much higher compression and decompression speed
    (at the cost of some compression ratio)."""

    homepage = "https://www.lzop.org"
    url = "https://www.lzop.org/download/lzop-1.03.tar.gz"

    license("GPL-2.0-only")

    version("1.04", sha256="7e72b62a8a60aff5200a047eea0773a8fb205caf7acbe1774d95147f305a2f41")
    version("1.03", sha256="c1425b8c77d49f5a679d5a126c90ea6ad99585a55e335a613cae59e909dbb2c9")
    version("1.01", sha256="28acd94d933befbc3af986abcfe833173fb7563b66533fdb4ac592f38bb944c7")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("lzo")
