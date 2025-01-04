# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStringr(RPackage):
    """Simple, Consistent Wrappers for Common String Operations.

    A consistent, simple and easy to use set of wrappers around the fantastic
    'stringi' package. All function and argument names (and positions) are
    consistent, all functions deal with "NA"'s and zero length vectors in the
    same way, and the output from one function is easy to feed into the input
    of another."""

    cran = "stringr"

    license("MIT")

    version("1.5.1", sha256="a4adec51bb3f04214b1d8ef40d3a58949f21b1497cbeaf2ba552e0891eef45de")
    version("1.5.0", sha256="52b159d7700a139111b4caf939e7c9c6ab3e01185181400d70a74c552826633a")
    version("1.4.1", sha256="ec0d8e90caa3e107f18c188ed313dea8bfd12a738011b0be09ef5362360ddcb1")
    version("1.4.0", sha256="87604d2d3a9ad8fd68444ce0865b59e2ffbdb548a38d6634796bbd83eeb931dd")
    version("1.3.1", sha256="7a8b8ea038e45978bd797419b16793f44f10c5355ad4c64b74d15276fef20343")
    version("1.2.0", sha256="61d0b30768bbfd7c0bb89310e2de5b7b457ac504538acbcca50374b46b16129a")
    version("1.1.0", sha256="ccb1f0e0f3e9524786f6cbae705c42eedf3874d0e641564e5e00517d892c5a33")
    version("1.0.0", sha256="f8267db85b83c0fc8904009719c93296934775b0d6890c996ec779ec5336df4a")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.3:", type=("build", "run"), when="@1.5.0:")
    depends_on("r@3.6:", type=("build", "run"), when="@1.5.1:")
    depends_on("r-lifecycle@1.0.3:", type=("build", "run"), when="@1.5.0:")
    depends_on("r-cli", type=("build", "run"), when="@1.5.0:")
    depends_on("r-stringi@1.1.7:", type=("build", "run"))
    depends_on("r-stringi@1.5.3:", type=("build", "run"), when="@1.5.0:")
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-vctrs", type=("build", "run"), when="@1.5.0:")
    depends_on("r-vctrs@0.4.0:", type=("build", "run"), when="@1.5.1:")
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@1.5.0:")
    depends_on("r-glue@1.2.0:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-glue@1.6.1:", type=("build", "run"), when="@1.5.0:")
