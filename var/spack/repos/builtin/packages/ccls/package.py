# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ccls(CMakePackage):
    """C/C++ language server"""

    homepage = "https://github.com/MaskRay/ccls"
    git = "https://github.com/MaskRay/ccls.git"
    url = "https://github.com/MaskRay/ccls/archive/0.20201025.tar.gz"

    maintainers("jacobmerson")

    license("Apache-2.0")

    version(
        "0.20240202", sha256="355ff7f5eb5f24d278dda05cccd9157e89583272d0559d6b382630171f142d86"
    )
    version(
        "0.20230717", sha256="118e84cc17172b1deef0f9c50767b7a2015198fd44adac7966614eb399867af8"
    )
    version(
        "0.20220729", sha256="af19be36597c2a38b526ce7138c72a64c7fb63827830c4cff92256151fc7a6f4"
    )
    version(
        "0.20210330", sha256="28c228f49dfc0f23cb5d581b7de35792648f32c39f4ca35f68ff8c9cb5ce56c2"
    )
    version(
        "0.20201025", sha256="1470797b2c1a466e2d8a069efd807aac6fefdef8a556e1edf2d44f370c949221"
    )

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.8:", type="build")
    depends_on("llvm@7:")
    depends_on("rapidjson")
