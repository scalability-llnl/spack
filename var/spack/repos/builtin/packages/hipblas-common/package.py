# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class HipblasCommon(CMakePackage):
    """Common files shared by hipBLAS and hipBLASLt"""

    homepage = "https://github.com/ROCm/hipBLAS-common"
    url = "https://github.com/ROCm/hipBLAS-common/archive/refs/tags/rocm-6.3.0.tar.gz"

    maintainers("srekolam", "renjithravindrankannath", "afzpatel")

    license("MIT")

    version("6.3.0", sha256="240bb1b0f2e6632447e34deae967df259af1eec085470e58a6d0aa040c8530b0")
