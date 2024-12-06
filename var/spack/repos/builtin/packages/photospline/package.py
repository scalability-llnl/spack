# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Photospline(CMakePackage):
    """Library for interpolating multi-dimensional detector response histograms."""

    homepage = "https://github.com/icecube/photospline"
    url = "https://github.com/icecube/photospline/archive/refs/tags/v2.2.1.tar.gz"

    license("BSD-2-Clause")

    version("2.2.1", sha256="2b455daf8736d24bf57cae9eb67d48463a6c4bd6a66c3ffacf52296454bb82ad")
    version("2.2.0", sha256="81f79b42fd63e12c13cc369fb5c6ef356389f7c7aaa10a584aae2e22dba79ccf")
    version("2.1.1", sha256="0a0dae8e1b994a35be23896982bd572fa97c617ad55a99b3da34782ad9435de8")
    version("2.1.0", sha256="bd6c58df8893917909b79ef2510a2043f909fbb7020bdace328d4d36e0222b60")
    version("2.0.7", sha256="59a3607c4aa036c55bcd233e8a0ec11575bd74173f3b4095cc6a77aa50baebcd")
    version("2.0.6", sha256="2f87c377e548f5fb44f8090c7559b2895f463a395b40a3276a04db44f39b1a4d")
    version("2.0.5", sha256="7e2679fac733fb4d881ff9d16fc99348a62b421811f256641f2449b98a6fb041")
    version("2.0.4", sha256="0a675ffe27e1d99fe482cdd7692320d6852c11c9a63de7e710ba075989e0bfb5")
    version("2.0.3", sha256="7045a631c41489085037b05fac98fd9cad73dc4262b7eead143d09e5f8265dec")
    version("2.0.2", sha256="0a3368205a7971a6919483ad5b5f0fbebb74614ec1891c95bb6a4fc9d3b950d4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cfitsio")
