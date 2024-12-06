# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RDeoptim(RPackage):
    """Global Optimization by Differential Evolution.

    Implements the differential evolution algorithm for global optimization of
    a real-valued function of a real-valued parameter vector."""

    cran = "DEoptim"

    version("2.2-8", sha256="631eabdcf26ec25a759651f699db1971beca3ae193c7fbd1c63a78248fdbf54c")
    version("2.2-7", sha256="40ac7e15246f86c6d659ae90c91579a9d96e49558862c70ea43bc3c898ad9478")
    version("2.2-6", sha256="8c63397d83a067212d003ef3e639fd81f5f00bf61e3c271b4e4999031a69e2e1")
    version("2.2-5", sha256="ae12dedcd4a43994e811e7285f8c12bfdb688e7c99d65515cf7e8cb6db13955a")
    version("2.2-4", sha256="0a547784090d1e9b93efc53768110621f35bed3692864f6ce5c0dda2ebd6d482")
    version("2.2-3", sha256="af2120feea3a736ee7a5a93c6767d464abc0d45ce75568074b233405e73c9a5d")

    depends_on("c", type="build")  # generated

    depends_on("r-parallelly", type=("build", "run"), when="@2.2-7:2.2-7")
