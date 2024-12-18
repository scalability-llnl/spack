# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Whip(CMakePackage, CudaPackage, ROCmPackage):
    """whip is a small C++ abstraction layer for CUDA and HIP."""

    homepage = "https://github.com/eth-cscs/whip/"
    url = "https://github.com/eth-cscs/whip/archive/0.0.0.tar.gz"
    git = "https://github.com/eth-cscs/whip.git"
    maintainers("msimberg", "rasolca")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("0.3.0", sha256="0c803e9453bc9c0cc8fbead507635b5c30465b6c2d46328f2a6a1140b4a8ff48")
    version("0.2.0", sha256="d8fec662526accbd1624922fdf01a077d6f312cf253382660e4a2f65e28e8686")
    version("0.1.0", sha256="5d557794f4afc8332fc660948a342f69e22bc9e5d575ffb3e3944cf526db5ec9")

    depends_on("cxx", type="build")

    depends_on("cmake@3.22:", type="build")

    # Exactly one of +cuda and +rocm need to be set
    conflicts("~cuda ~rocm")
    conflicts("+cuda +rocm")

    def cmake_args(self):
        if self.spec.satisfies("+cuda"):
            return [self.define("WHIP_BACKEND", "CUDA")]
        else:
            return [self.define("WHIP_BACKEND", "HIP")]
