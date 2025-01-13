# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAer(RPackage):
    """Applied Econometrics with R.

    Functions, data sets, examples, demos, and vignettes for the book Christian
    Kleiber and Achim Zeileis (2008), Applied Econometrics with R,
    Springer-Verlag, New York.  ISBN 978-0-387-77316-2."""

    cran = "AER"

    version("1.2-12", sha256="55c7b0f17ecd0dc6e1c54ab09b40e89676f44658eaad444c818133fae8d1ea86")
    version("1.2-10", sha256="650a5fb54a8addf8c86f1e0f88f4fac5349731bc5bf34762a991022140eedbdc")
    version("1.2-9", sha256="3b79390b14766419fc1e8912689bc462d4beb01aff9dad26d628aed69d04540d")
    version("1.2-7", sha256="3aee5c606313710c2dca6c1e9b2c20a145aa33f2a3ecc5cfcec66c8e91838a93")
    version("1.2-6", sha256="653c3a2d253819e0ce8c2cf12cff2ab222bf3d19dbf382b7c4b4c3d762469474")
    version("1.2-5", sha256="ef0cf14ff9d3de2b97e5855243426cc918808eb1011f0e2253b3b00043927a62")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-car@2.0-19:", type=("build", "run"))
    depends_on("r-lmtest", type=("build", "run"))
    depends_on("r-sandwich@2.4-0:", type=("build", "run"))
    depends_on("r-survival@2.37-5:", type=("build", "run"))
    depends_on("r-zoo", type=("build", "run"))
    depends_on("r-formula@0.2-0:", type=("build", "run"))
