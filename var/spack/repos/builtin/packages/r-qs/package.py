# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQs(RPackage):
    """Quick Serialization of R Objects.

    Provides functions for quickly writing and reading any R object to and from
    disk."""

    cran = "qs"

    maintainers("dorton21")

    license("GPL-3.0-only")

    version("0.26.3", sha256="8801a41f6e5161a55193dc9a75fcee8da1b0e02eebd7653ec05326d594321ee3")
    version("0.25.5", sha256="3f87388708a0fdfb0e68caade75ed771fd395cb4f649973459bc97f41d42064c")
    version("0.25.4", sha256="92c49206a9c1c66dbd95f12efc3a57acb728e1f8387b549c437519fb2b98a533")
    version("0.25.3", sha256="51adf6a112c19f78ceeefa55acf800c7e6bf2664e7d9cea9d932abb24f22be6b")
    version("0.25.2", sha256="fe428ae5dc46f88fdf454ca74c4a073f5ac288d6d039080a3c0d66c4ebbd5cbf")
    version("0.23.6", sha256="c6e958e9741ee981bf2388c91b8f181718ffb0f32283cd7ebcd2d054817280e4")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r@3.0.2:", type=("build", "run"), when="@0.25.2:")
    depends_on("r-bh", type=("build", "run"), when="@0.26.0:")
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-rapiserialize", type=("build", "run"))
    depends_on("r-rapiserialize@0.1.1:", type=("build", "run"), when="@0.25.4:")
    depends_on("r-stringfish@0.14.1:", type=("build", "run"))
    depends_on("r-stringfish@0.15.1:", type=("build", "run"), when="@0.25.2:")
    depends_on("zstd")
