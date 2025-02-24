# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cnmem(CMakePackage):
    """CNMem mempool for CUDA devices"""

    homepage = "https://github.com/NVIDIA/cnmem"
    git = "https://github.com/NVIDIA/cnmem.git"

    license("BSD-3-Clause")

    version("git", branch="master")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8.8:", type="build")
