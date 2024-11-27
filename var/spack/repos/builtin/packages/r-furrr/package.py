# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFurrr(RPackage):
    """Apply Mapping Functions in Parallel using Futures

    Implementations of the family of map() functions from 'purrr' that can be
    resolved using any 'future'-supported backend, e.g. parallel on the local
    machine or distributed on a compute cluster."""

    homepage = "https://furrr.futureverse.org"
    cran = "furrr"

    maintainers("jgaeb")

    license("MIT")

    version("0.3.1", sha256="0d91735e2e9be759b1ab148d115c2c7429b79740514778828e5dab631dc0e48b")
    version("0.3.0", sha256="3fe91cc1614f9404c708ea3a15b6a40289fa57f40f3ece54452093408d91fd84")
    version("0.2.3", sha256="0a213422dc0a2e84173f2d3e6c7900dcb677f980c255d6b6ccf666fba1173700")
    version("0.2.2", sha256="e5c10353dc47416eda870d16cf810c576f11bdc9e4c7277f7755581f3824cd4d")
    version("0.2.1", sha256="07b3c98324aeb6a7e77a3d48c54fb90696a6e14efeee391cfc5e05f8dcd3469b")
    version("0.2.0", sha256="9d6483656fdb5b90e998e2c2f1494c721185079a1412316c6d391e1eade89e1b")
    version("0.1.0", sha256="dd2937f7cad1bc69e7a512b2a777f82d6cb7e40fe99afa2049ca360f9352a9d1")

    depends_on("r@3.2.0:", type=("build", "run"), when="@0.1.0:")
    depends_on("r@3.4.0:", type=("build", "run"), when="@0.3.0:")
    depends_on("r-future@1.6.2:1.19.1", type=("build", "run"), when="@0.1.0")
    depends_on("r-future@1.19.1:1.22.1", type=("build", "run"), when="@0.2.0:0.2.3")
    depends_on("r-future@1.25.0:", type=("build", "run"), when="@0.3.0:")
    depends_on("r-globals@0.10.3:", type=("build", "run"), when="@0.1.0:")
    depends_on("r-globals@0.13.1:", type=("build", "run"), when="@0.2.0:")
    depends_on("r-globals@0.14.0:", type=("build", "run"), when="@0.3.0:")
    depends_on("r-rlang@0.2.0:", type=("build", "run"), when="@0.1.0:")
    depends_on("r-rlang@0.3.0:", type=("build", "run"), when="@0.2.0:")
    depends_on("r-rlang@1.0.2:", type=("build", "run"), when="@0.3.0:")
    depends_on("r-purrr@0.2.4:", type=("build", "run"), when="@0.1.0:")
    depends_on("r-purrr@0.3.0:", type=("build", "run"), when="@0.2.0:")
    depends_on("r-purrr@0.3.4:", type=("build", "run"), when="@0.3.0:")
    depends_on("r-ellipsis", type=("build", "run"), when="@0.2.0:0.3.0")
    depends_on("r-lifecycle@0.2.0:", type=("build", "run"), when="@0.2.0:")
    depends_on("r-lifecycle@1.0.0:", type=("build", "run"), when="@0.2.3:")
    depends_on("r-lifecycle@1.0.1:", type=("build", "run"), when="@0.3.0:")
    depends_on("r-vctrs@0.3.2:", type=("build", "run"), when="@0.2.0:")
    depends_on("r-vctrs@0.4.1:", type=("build", "run"), when="@0.3.0:")
