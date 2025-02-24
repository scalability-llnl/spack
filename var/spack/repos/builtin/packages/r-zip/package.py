# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RZip(RPackage):
    """Cross-Platform 'zip' Compression.

    Cross-Platform 'zip' Compression Library. A replacement for the 'zip'
    function, that does not require any additional external tools on any
    platform."""

    cran = "zip"

    license("MIT")

    version("2.3.1", sha256="83754408781c525917f36535865d28214893de0778b5f337e050cb543cacc28f")
    version("2.3.0", sha256="33eba844922af9981732ee6ec1582d46cf04c562344f09a0f0f14a22c6f74543")
    version("2.2.2", sha256="e16cde23bb283efbe9b6bce19575c716c371d09033b42514471ccb444c0a8ea4")
    version("2.2.1", sha256="14873d0874813139411c120d8b209af71e4e087871eeb963f235411eb1061422")
    version("2.2.0", sha256="9f95987c964039834f770ecda2d5f7e3d3a9de553c89db2a5926c4219bf4b9d8")
    version("2.1.1", sha256="11dd417932296d3a25c53aa8d3b908973c4945a496cc473dd321825dfaaa7c2c")
    version("2.0.3", sha256="4a8cb8e41eb630bbf448a0fd56bcaeb752b8484fef98c6419334edf46401317e")
