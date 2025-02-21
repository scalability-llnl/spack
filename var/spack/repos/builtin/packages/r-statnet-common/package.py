# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStatnetCommon(RPackage):
    """Common R Scripts and Utilities Used by the Statnet Project Software.

    Non-statistical utilities used by the software developed by the Statnet
    Project. They may also be of use to others."""

    cran = "statnet.common"

    version("4.9.0", sha256="a485dc6e363a993d87336fbd1027adb1cd7b9103447fd63904cae4dc3bfc2dd7")
    version("4.8.0", sha256="def999130673fbcb315fecf3620a2559864f51961a828625aa5cd5fded7946f0")
    version("4.7.0", sha256="b69731a606b56b729b1917375efafb572b960ce5000a0fc2ec5222fd7d80a1b3")
    version("4.6.0", sha256="ddad51128b50d465e1d1aca3a53b452810b9ba578e96b08b8f50f5850d7bb21d")
    version("4.5.0", sha256="3cdb23db86f3080462f15e29bcf3e941590bc17ea719993b301199b22d6f882f")
    version("4.4.1", sha256="4ecf2b84718d7fb60f196215b4cf6f52cd6b26cc9148a6da6981b26e885509fd")
    version("4.3.0", sha256="834a3359eac967df0420eee416ae4983e3b502a3de56bb24f494a7ca4104e959")
    version("4.2.0", sha256="1176c3303436ebe858d02979cf0a0c33e4e2d1f3637516b4761d573ccd132461")
    version("3.3.0", sha256="d714c4e7b0cbf71b7a628af443f5be530e74ad1e21f6b04f1b1087f6d7e40fa4")

    depends_on("r@3.5:", type=("build", "run"), when="@4.2.0:")
    depends_on("r-coda", type=("build", "run"), when="@4.1.2:")

    depends_on("r-rle", type=("build", "run"), when="@4.4.1")
