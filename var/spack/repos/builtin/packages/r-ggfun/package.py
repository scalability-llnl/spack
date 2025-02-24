# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgfun(RPackage):
    """Miscellaneous Functions for 'ggplot2'.

    Useful functions to edit 'ggplot' object (e.g., setting fonts for theme and
    layers, adding rounded rectangle as background for each of the legends)."""

    cran = "ggfun"

    license("Artistic-2.0")

    version("0.1.5", sha256="fe6c01fd68c17497f23f76dfd4e5a6edd79a6e86850b8c5054748f31527b16d3")
    version("0.0.9", sha256="5c740e9d1e73b77658f41ed65e21492f4e71b12c7c9ff4b9e52ebf5f8f197612")
    version("0.0.8", sha256="9471a12fc7af203a419767b845e6b6c1e63c080370cb8f2dac80187194122273")
    version("0.0.7", sha256="a83b5fb95f61e366f96d6d8e6b04dafff8e885e7c80c913614876b50ebb8e174")
    version("0.0.6", sha256="59989ed260fcc71cd95487cf3493113a2d8a47d273d9a2f3e5e842609620511b")
    version("0.0.5", sha256="b1e340a8932d2cffbbbf6070ce96c9356599e9955a2b6534fcb17e599c575783")
    version("0.0.4", sha256="5926365f9a90baf47320baf48c40f515ef570f9c767484adea5f04219964d21e")

    depends_on("r@4.1.0:", type=("build", "run"), when="@0.1.2:")
    depends_on("r-cli", type=("build", "run"), when="@0.1.3:")
    depends_on("r-dplyr", type=("build", "run"), when="@0.1.5:")
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
