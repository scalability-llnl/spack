# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRversions(RPackage):
    """Query 'R' Versions, Including 'r-release' and 'r-oldrel'.

    Query the main 'R' 'SVN' repository to find the versions 'r-release' and
    'r-oldrel' refer to, and also all previous 'R' versions and their release
    dates."""

    cran = "rversions"

    license("MIT")

    version("2.1.2", sha256="de5818233e8271132fe8ea70145618950b35786e0d2f270e39bf3338f3b8b160")
    version("2.1.1", sha256="79aaacf5a1258d91ac0ddedf3c8c16a2d10d39010993dcc7b0a2638afee27cb1")
    version("2.0.2", sha256="3523f4b7393365341d429500b01ba3a224056e89d134635b81dfb4918ba2173e")
    version("2.0.1", sha256="51ec1f64e7d628e88d716a020d5d521eba71d472e3c9ae7b694428ef6dd786c5")
    version("2.0.0", sha256="b50c321d9e973284ae6b1d0c89bd46a40f5174de51fb28e3c77cd12ef34f6f56")
    version("1.1.0", sha256="14a5a2f06b74e332fd9cbd4d715baa6165f5269c9ba2c0b9f1d0c6540dde9c3c")
    version("1.0.3", sha256="21d0809f46505de89a2be7be9449e39c39cff5bc77e584dec976ee6c0b884f44")
    version("1.0.2", sha256="c8ec8e24524cc42893e445e01e1a65d15889d28959877cd6b3c5e5f08221b176")
    version("1.0.1", sha256="9099d37d2f6cc1cab0cd0fdddfb9657c7bd3651226810b496e2808f458c80ae3")
    version("1.0.0", sha256="ce1e5368ff1d15665ca2db700521a96cf44f0e78daaab68aabbdaf7ed7393b4d")

    depends_on("r-curl", type=("build", "run"))
    depends_on("r-xml2@1.0.0:", type=("build", "run"))
