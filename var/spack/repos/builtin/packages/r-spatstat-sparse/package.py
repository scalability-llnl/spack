# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatstatSparse(RPackage):
    """Sparse Three-Dimensional Arrays and Linear Algebra Utilities.

    Defines sparse three-dimensional arrays and supports standard operations on
    them. The package also includes utility functions for matrix calculations
    that are common in statistics, such as quadratic forms."""

    cran = "spatstat.sparse"

    version("3.1-0", sha256="63be5dc5818339b878a14a39815dab730b28029d51bac5233e88f5e2464bbbe9")
    version("3.0-1", sha256="2c1cf0ddad366aa4230bd03241a1ef87ed635f53a6943fc4a6c2d371626d0d1c")
    version("3.0-0", sha256="99be0a3c7592760fdf1668dc0811f75ed91c400390d1ecc3d5e643255f501ad2")
    version("2.1-1", sha256="9a35ad69715b767b3ae60b02dce05ccf108fcccdf95bbc8f7d02557bcbde7303")
    version("2.1-0", sha256="0019214418668cba9f01ee5901ed7f4dba9cfee5ff62d5c7e1c914adfbea0e91")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"))
    depends_on("r-tensor", type=("build", "run"))
    depends_on("r-spatstat-utils@2.1-0:", type=("build", "run"))
    depends_on("r-spatstat-utils@3.0-0:", type=("build", "run"), when="@3.0-0:")
    depends_on("r-spatstat-utils@3.0-2:", type=("build", "run"), when="@3.0-1:")
    depends_on("r-spatstat-utils@3.0-5:", type=("build", "run"), when="@3.1-0:")
