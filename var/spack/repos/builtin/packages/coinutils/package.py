# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Coinutils(AutotoolsPackage):
    """CoinUtils is an open-source collection of classes and helper
    functions that are generally useful to multiple COIN-OR
    projects."""

    homepage = "https://projects.coin-or.org/Coinutils"
    url = "https://github.com/coin-or/CoinUtils/archive/releases/2.11.4.tar.gz"

    license("EPL-2.0")

    version("2.11.10", sha256="80c7c215262df8d6bd2ba171617c5df844445871e9891ec6372df12ccbe5bcfd")
    version("2.11.9", sha256="15d572ace4cd3b7c8ce117081b65a2bd5b5a4ebaba54fadc99c7a244160f88b8")
    version("2.11.6", sha256="6ea31d5214f7eb27fa3ffb2bdad7ec96499dd2aaaeb4a7d0abd90ef852fc79ca")
    version("2.11.4", sha256="d4effff4452e73356eed9f889efd9c44fe9cd68bd37b608a5ebb2c58bd45ef81")

    depends_on("cxx", type="build")  # generated

    build_directory = "spack-build"
