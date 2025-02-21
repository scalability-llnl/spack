# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# See the Spack documentation for more information on packaging.

from spack.package import *


class RRobust(RPackage):
    """Port of the S+ Robust Library.

    Methods for robust statistics, a state of the art in the early 2000s,
    notably for robust regression and robust multivariate analysis."""

    cran = "robust"

    license("GPL-3.0-or-later")

    version("0.7-5", sha256="a3c02a9c9101b966907cb52b3193c4ef51864928ad99c3351edf5390532c1acc")
    version("0.7-1", sha256="efaac70c6399b2787938e23ea89039b4a6043e76601bd794ba0ddda1edee65df")
    version("0.7-0", sha256="5e1aac30e185e416c22445663704f39433af9fdb48452185f2c9beb3528084b9")
    version("0.6-1", sha256="496fd225f6bc6f734e338308f18475125aaf691b39e25308bddb284d3106117d")
    version("0.5-0.0", sha256="82f0b50028938966f807a4c4da5c345a3a64ccafd9a31c64a22cda852ed345cf")
    version("0.4-18.1", sha256="de31901882873ef89748bb6863caf55734431df5b3eb3c6663ed17ee2e4a4077")
    version("0.4-18", sha256="e4196f01bb3b0d768759d4411d524238b627eb8dc213d84cb30014e75480f8ac")

    depends_on("r-fit-models", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-robustbase", type=("build", "run"))
    depends_on("r-rrcov", type=("build", "run"))
