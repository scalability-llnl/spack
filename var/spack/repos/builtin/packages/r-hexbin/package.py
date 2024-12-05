# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RHexbin(RPackage):
    """Hexagonal Binning Routines.

    Binning and plotting functions for hexagonal bins. Now uses and relies on
    grid graphics and formal (S4) classes and methods."""

    cran = "hexbin"

    license("GPL-2.0-only")

    version("1.28.3", sha256="0eb33511c1a4ff29dda8b89fee420ea7041033f981c7f16484c9f504d749de5f")
    version("1.28.2", sha256="6241f8d3a6c6be2c1c693c3ddb99554bc103e3c6cf602d0c2787c0ce6fd1702d")
    version("1.27.3", sha256="7ea422a76542c2fc2840df601af1b7803aa96df4fee6d51dec456ac36940c191")
    version("1.27.2", sha256="46d47b1efef75d6f126af686a4dd614228b60418b9a5bde9e9e5d11200a0ee52")
    version("1.27.1", sha256="075935a3ae2d90e44aca6ebbd368dc6f7e59d322e36e0e0932dedbf01330ad08")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("r@2.0.1:", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
