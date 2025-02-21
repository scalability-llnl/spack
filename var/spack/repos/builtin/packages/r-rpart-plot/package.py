# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRpartPlot(RPackage):
    """Plot 'rpart' Models: An Enhanced Version of 'plot.rpart'.

    Plot 'rpart' models. Extends plot.rpart() and text.rpart() in the 'rpart'
    package."""

    cran = "rpart.plot"

    version("3.1.2", sha256="3dca2a5d1a8e5eb5129fd6efce9c5f6b2fa241bfb65f2a8823a8db89f4b422b2")
    version("3.1.1", sha256="30736240058df21a96d10912a091d938f821d521a3bc4efb9aa4ef6fb233024d")
    version("3.1.0", sha256="2aaba0c0cabbc17aca9085248b0ad74ee7ff2b8f729e020e84b3917de174c15e")
    version("3.0.9", sha256="1150f5e9899b3b31b17160617cd99c3ad340c8361aeb229264a7a3a3a28015a4")
    version("3.0.7", sha256="04e7fcadfa907507b74529c3ecfae4a0c782badf55e87d9c62dbd9a536ea9144")
    version("3.0.6", sha256="1c584290c8f58ded5c3f0638790a0da63408eca3ecd5d5c4d8c46954de9f4b02")
    version("2.1.0", sha256="17686da1883f97cb8f44be0d9cb915b366a3cb7313cd131b96497ab09f727436")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@3.0.7:")
    depends_on("r-rpart@4.1-10:", type=("build", "run"))
    depends_on("r-rpart@4.1-15:", type=("build", "run"), when="@3.0.9:")
