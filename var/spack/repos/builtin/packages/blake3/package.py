# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Blake3(CMakePackage):
    """BLAKE3 is a cryptographic hash function"""

    homepage = "https://github.com/BLAKE3-team/BLAKE3"
    url = "https://github.com/BLAKE3-team/BLAKE3/archive/refs/tags/1.5.1.tar.gz"

    root_cmakelists_dir = "c"

    maintainers("haampie")

    version("1.5.1", sha256="822cd37f70152e5985433d2c50c8f6b2ec83aaf11aa31be9fe71486a91744f37")

    depends_on("c", type="build")  # generated

    depends_on("cmake@3.9:", type="build")
