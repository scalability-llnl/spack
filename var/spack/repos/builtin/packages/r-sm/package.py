# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSm(RPackage):
    """Smoothing Methods for Nonparametric Regression and Density Estimation.

    This is software linked to the book 'Applied Smoothing Techniques for Data
    Analysis - The Kernel Approach with S-Plus Illustrations' Oxford University
    Press."""

    cran = "sm"

    license("GPL-2.0-or-later")

    version("2.2-6.0", sha256="27a6e3291a572c3d30f25982902ccde5299230061e5dc1a38fb52aaac2561d61")
    version("2.2-5.7.1", sha256="ea0cc32eb14f6c18beba0bede66ed37bc5341bd3f76c1a7ae56d7254693e1457")
    version("2.2-5.7", sha256="2607a2cafc68d7e99005daf99e36f4a66eaf569ebb6b7500e962642cf58be80f")
    version("2.2-5.6", sha256="b890cd7ebe8ed711ab4a3792c204c4ecbe9e6ca1fd5bbc3925eba5833a839c30")
    version("2.2-5.5", sha256="43e212a14c364b98b10018b56fe0a619ccffe4bde1294e6c45b3eafe7caf82e7")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@3.1.0:", type=("build", "run"))
