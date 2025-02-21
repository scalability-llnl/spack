# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBrio(RPackage):
    """Basic R Input Output.

    Functions to handle basic input output, these functions always read and
    write UTF-8 (8-bit Unicode Transformation Format) files and provide more
    explicit control over line endings."""

    cran = "brio"

    license("MIT")

    version("1.1.5", sha256="a9f22335ea39039de25bb27bccd5ff1ffb2b743579b31d150b6b91c9ea81d0b8")
    version("1.1.3", sha256="eaa89041856189bee545bf1c42c7920a0bb0f1f70bb477487c467ee3e8fedcc6")
    version("1.1.0", sha256="6bb3a3b47bea13f1a1e3dcdc8b9f688502643e4b40a481a34aa04a261aabea38")

    depends_on("r@3.6:", when="@1.1.4:", type=("build", "run"))
