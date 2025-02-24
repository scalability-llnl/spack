# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSystemfonts(RPackage):
    """System Native Font Finding.

    Provides system native access to the font catalogue. As font handling
    varies between systems it is difficult to correctly locate installed fonts
    across different operating systems. The 'systemfonts' package provides
    bindings to the native libraries on Windows, macOS and Linux for finding
    font files that can then be used further by e.g. graphic devices. The main
    use is intended to be from compiled code but 'systemfonts' also provides
    access from R."""

    cran = "systemfonts"

    license("MIT")

    version("1.1.0", sha256="1941069bd20320284ec026a38c53cb736be60bda431303ceaf8fd27ae13fb644")
    version("1.0.4", sha256="ef766c75b942f147d382664a00d6a4930f1bfe0cce9d88943f571682a85a84c0")
    version("1.0.3", sha256="647c99d5ea6f90a49768ea7b10b39816af6be85168475273369fd973a20dbbba")
    version("1.0.1", sha256="401db4d9e78e3a5e00b7a0b4fbad7fbb1c584734469b65fe5b7ebe1851c7a797")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-cpp11@0.2.1:", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"), when="@1.1.0:")
    depends_on("fontconfig")
    depends_on("freetype")
