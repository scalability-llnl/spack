# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTibble(RPackage):
    """Simple Data Frames.

    Provides a 'tbl_df' class (the 'tibble') that provides stricter checking
    and better formatting than the traditional data frame."""

    cran = "tibble"

    license("MIT")

    version("3.2.1", sha256="65a72d0c557fd6e7c510d150c935ed6ced5db7d05fc20236b370f11428372131")
    version("3.1.8", sha256="acf30e075d18d2f61de53ca20a13c502bb32abb8083089b0bb9172a0cb5cedea")
    version("3.1.7", sha256="e1a50891f476803526960b4c4d736a72e7d9c3d366946744a02d6347f591c872")
    version("3.1.6", sha256="5b33d909f146ebad38e262f6a57cb91ab70bfe240c2af01004beec11b3898292")
    version("3.1.5", sha256="da6387ba683a67cd7fc2a111f6b62468e480a8078bc1867d433a40c5460edbe7")
    version("3.0.5", sha256="1cc92d7bf5ecf8291718682fb7fcb96f6f87751f1ed101a7441cad5120195190")
    version("2.1.3", sha256="9a8cea9e6b5d24a7e9bf5f67ab38c40b2b6489eddb0d0edb8a48a21ba3574e1a")
    version("2.0.1", sha256="7ab2cc295eecf00a5310993c99853cd6622ad468e7a60d004b8a73957a713d13")
    version("2.0.0", sha256="05ad2d62e949909548c4bb8ac596810321f11b330afa9717d0889dc35edd99ba")
    version("1.4.2", sha256="11670353ff7059a55066dd075d1534d6a27bc5c3583fb9bc291bf750a75c5b17")
    version("1.4.1", sha256="32267fae1ca86abdd37c4683f9d2b1a47b8b65e1977ea3900aa197066c57aa29")
    version("1.3.4", sha256="a7eef7018a68fc07c17c583fb7821a08d6bc381f5961258bffaa6ef6b137760b")
    version("1.2", sha256="ed8a8bd0591223f742be80fd1cd8c4a9618d0f04011ec95c272b61ea45193104")
    version("1.1", sha256="10ea18890e5514faa4c2c05fa231a6e2bbb7689f3800850cead214306414c88e")

    depends_on("c", type="build")  # generated

    depends_on("r@3.1.2:", type=("build", "run"))
    depends_on("r@3.1.0:", type=("build", "run"), when="@1.3.0:")
    depends_on("r@3.4.0:", type=("build", "run"), when="@3.2.1:")
    depends_on("r-fansi@0.4.0:", type=("build", "run"), when="@2.0.0:")
    depends_on("r-lifecycle@0.2.0:", type=("build", "run"), when="@3.0.5:")
    depends_on("r-lifecycle@1.0.0:", type=("build", "run"), when="@3.1.5:")
    depends_on("r-magrittr", type=("build", "run"), when="@3.0.5:")
    depends_on("r-pillar@1.3.1:", type=("build", "run"), when="@1.4.1:")
    depends_on("r-pillar@1.4.3:", type=("build", "run"), when="@3.0.5:")
    depends_on("r-pillar@1.6.0:", type=("build", "run"), when="@3.1.0:")
    depends_on("r-pillar@1.6.2:", type=("build", "run"), when="@3.1.4:")
    depends_on("r-pillar@1.7.0:", type=("build", "run"), when="@3.1.7:")
    depends_on("r-pillar@1.8.1:", type=("build", "run"), when="@3.2.1:")
    depends_on("r-pkgconfig", type=("build", "run"), when="@2.0.0:")
    depends_on("r-rlang@0.3.0:", type=("build", "run"), when="@1.3.1:")
    depends_on("r-rlang@0.4.3:", type=("build", "run"), when="@3.0.5:")
    depends_on("r-rlang@1.0.1:", type=("build", "run"), when="@3.1.7:")
    depends_on("r-rlang@1.0.2:", type=("build", "run"), when="@3.1.8:")
    depends_on("r-vctrs@0.3.2:", type=("build", "run"), when="@3.0.5:")
    depends_on("r-vctrs@0.3.8:", type=("build", "run"), when="@3.1.2:")
    depends_on("r-vctrs@0.4.2:", type=("build", "run"), when="@3.2.1:")

    depends_on("r-cli", type=("build", "run"), when="@1.4.2:3.0")
    depends_on("r-crayon@1.3.4:", type=("build", "run"), when="@1.4.1:3.0")
    depends_on("r-assertthat", type=("build", "run"), when="@:1.3.1")
    depends_on("r-lazyeval@0.1.10:", type=("build", "run"), when="@:1.3.0")
    depends_on("r-rcpp@0.12.3:", type=("build", "run"), when="@:1.3.4")
    depends_on("r-ellipsis@0.2.0:", type=("build", "run"), when="@3.0.5:3.1.7")
    depends_on("r-ellipsis@0.3.2:", type=("build", "run"), when="@3.1.2:3.1.7")
