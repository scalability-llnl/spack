# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RReticulate(RPackage):
    """Interface to 'Python'.

    Interface to 'Python' modules, classes, and functions. When calling into
    'Python', R data types are automatically converted to their equivalent
    'Python' types. When values are returned from 'Python' to R they are
    converted back to R types. Compatible with all versions of 'Python' >=
    2.7."""

    cran = "reticulate"

    license("Apache-2.0")

    version("1.38.0", sha256="cb2f313e2351a3cde03be55561b592318ec5376fba3b10e371eeff1986deca8d")
    version("1.28", sha256="58a299ed18faaa3ff14936752fcc2b86e64ae18fc9f36befdfd492ccb251516f")
    version("1.26", sha256="3fd74823bde1b0e094db7c2bf6b40ee2501f8d724b4c35b53da95c3c588c74c5")
    version("1.25", sha256="2125af9e75939c3b7c0dc74f28f42606e816d63aa1143baf631c318ff5ff3a2c")
    version("1.24", sha256="b918c5204916601f757ad0fc629b2ae1eabab7cdf7f6aa2e219d26e506d916cc")
    version("1.23", sha256="fea04a3ff33c71f1910d65000a93c6882180ca03f8657ee118ea9e79786c36d6")
    version("1.18", sha256="b33f855a58f446eefbe38df8a1a4865390f5d4ebd64b2c72266baaee64628513")
    version("1.15", sha256="47db3e9c9424263ade15287da8e74f6ba261a936b644b197dba6772853b7b50d")
    version("1.13", sha256="adbe41d556b667c4419d563680f8608a56b0f792b8bc427b3bf4c584ff819de3")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@1.30.0:")
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-rcpp@0.12.7:", type=("build", "run", "link"))
    depends_on("r-rcpp@1.0.7:", type=("build", "run"), when="@1.29.0:")
    depends_on("r-rcpptoml", type=("build", "run", "link"), when="@1.23:")
    depends_on("r-rlang", type=("build", "run"), when="@1.29.0:")
    depends_on("r-here", type=("build", "run", "link"), when="@1.23:")
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-png", type=("build", "run", "link"), when="@1.23:")
    depends_on("r-rappdirs", type=("build", "run"), when="@1.15:")
    depends_on("r-withr", type=("build", "run", "link"), when="@1.23:")
    depends_on("python@2.7.0:", type=("build", "run"))
