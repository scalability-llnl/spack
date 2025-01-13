# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFarver(RPackage):
    """High Performance Colour Space Manipulation.

    The encoding of colour can be handled in many different ways, using
    different colour spaces. As different colour spaces have different uses,
    efficient conversion between these representations are important. The
    'farver' package provides a set of functions that gives access to very fast
    colour space conversion and comparisons implemented in C++, and offers
    speed improvements over the 'convertColor' function in the 'grDevices'
    package."""

    cran = "farver"

    license("MIT")

    version("2.1.2", sha256="528823b95daab4566137711f1c842027a952bea1b2ae6ff098e2ca512b17fe25")
    version("2.1.1", sha256="0dcfda6ca743f465372790bcff1bcbc6a7145fdac1c682b021f654e8c6c996ce")
    version("2.1.0", sha256="e5c8630607049f682fb3002b99ca4f5e7c6b94f8b2a4342df594e7853b77cef4")
    version("2.0.3", sha256="0e1590df79ec6078f10426411b96216b70568a4eaf3ffd84ca723add0ed8e5cc")
    version("2.0.1", sha256="71473e21727357084c6aec4bb9bb258a6797a0f676b4b27504a03f16aa2f4e54")
