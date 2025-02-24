# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RWithr(RPackage):
    """Run Code 'With' Temporarily Modified Global State.

    A set of functions to run code 'with' safely and temporarily modified
    global state. Many of these functions were originally a part of the
    'devtools' package, this provides a simple package with limited
    dependencies to provide access to these functions."""

    cran = "withr"

    license("MIT")

    version("3.0.1", sha256="d573f1ac2f733c7dd89669feb495d68f1f15d7a9774473c2e46a9848945a3841")
    version("2.5.0", sha256="37317b3ed790a08407072993a05ab255f6305f95a12a16e0e28aa6aa80fc8bc0")
    version("2.4.3", sha256="9bdac7459ccc6c2d599ecfd132a7f0aa68d958942d9fe7dbb0442c9eda129d4c")
    version("2.4.2", sha256="48f96a4cb780cf6fd5fbbea1f1eb04ea3102d7a4a644cae1ed1e91139dcbbac8")
    version("2.4.0", sha256="ede4cdc7e4d17e0ad24afc9fb940cba46fac4421d3a39281e9918377d73714f8")
    version("2.2.0", sha256="4c21e51cf48f8c281ddd5f5ec358ac446df3c982104fd00bfe62d9259d73b582")
    version("2.1.2", sha256="41366f777d8adb83d0bdbac1392a1ab118b36217ca648d3bb9db763aa7ff4686")
    version("1.0.2", sha256="2391545020adc4256ee7c2e31c30ff6f688f0b6032e355e1ce8f468cab455f10")
    version("1.0.1", sha256="7e245fdd17d290ff9e7c237159804dd06e1c6a3efe7855ed641eb0765a1e727d")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r@3.2.0:", type=("build", "run"), when="@2.2:")
    depends_on("r@3.6.0:", type=("build", "run"), when="@3.0.1:")
