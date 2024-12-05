# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCaret(RPackage):
    """Classification and Regression Training.

    Misc functions for training and plotting classification and regression
    models."""

    cran = "caret"

    license("GPL-2.0-or-later")

    version("6.0-94", sha256="2715e83ca260bb739cd926a55b0d2da1e3f6308b17b56862466e738d930d29a8")
    version("6.0-93", sha256="4c156b88879d390436a54779ea19ffbae3f476533d83caaf30400d76130c4a07")
    version("6.0-92", sha256="1d814a2a921a23ad8b9a7da6f788e6abc06f5668b3918bd440d4355bc4b81511")
    version("6.0-90", sha256="e851a4ed7d939c665e57e3551a5464b09fe4285e7c951236efdd890b0da866bc")
    version("6.0-86", sha256="da4a1c7c3fbf645c5b02871e563a77404622b83623f0d1c5dc1425de7aa4ce37")
    version("6.0-84", sha256="a1831c086a9c71b469f7405649ba04517683cdf229e119c005189cf57244090d")
    version("6.0-83", sha256="9bde5e4da1f0b690bfe06c2439c0136504e851a8d360bf56b644f171fe20dcef")
    version("6.0-73", sha256="90a0a4a10f1a3b37502cb0ed7d8830063d059a548faabb9cc5d8d34736c7eacb")
    version("6.0-70", sha256="21c5bdf7cf07bece38729465366564d8ca104c2466ee9fd800ca1fd88eb82f38")

    depends_on("c", type="build")  # generated

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@3.2.0:", type=("build", "run"), when="@6.0-82:")
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-lattice@0.20:", type=("build", "run"))
    depends_on("r-e1071", type=("build", "run"), when="@6.0-90:")
    depends_on("r-foreach", type=("build", "run"))
    depends_on("r-modelmetrics@1.1.0:", type=("build", "run"))
    depends_on("r-modelmetrics@1.2.2.2:", type=("build", "run"), when="@6.0-86:")
    depends_on("r-nlme", type=("build", "run"))
    depends_on("r-plyr", type=("build", "run"))
    depends_on("r-proc", type=("build", "run"), when="@6.0-86:")
    depends_on("r-recipes@0.1.4:", type=("build", "run"), when="@6.0-83:")
    depends_on("r-recipes@0.1.10:", type=("build", "run"), when="@6.0-86:")
    depends_on("r-reshape2", type=("build", "run"))
    depends_on("r-withr@2.0.0:", type=("build", "run"), when="@6.0-83:")

    depends_on("r-car", type=("build", "run"), when="@:6.0-73")
