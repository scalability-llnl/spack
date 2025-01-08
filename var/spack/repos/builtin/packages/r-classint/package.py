# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RClassint(RPackage):
    """Choose Univariate Class Intervals.

    Selected commonly used methods for choosing univariate class intervals for
    mapping or other graphics purposes."""

    cran = "classInt"

    version("0.4-10", sha256="c3561eafbc493ac02840191d4f1e4d2ef437ca8eb20f41fc5eca28f00ee42b8b")
    version("0.4-9", sha256="5b11af7d08f8793c7b47ee7c68b8e371cb23027165d30abddbd8b2abcc20e1c3")
    version("0.4-8", sha256="6ae9617f5b71bbecfa204a4f36b5972808bafd060d87a4a5bac17f3ad2ca59b3")
    version("0.4-3", sha256="9ede7a2a7a6b6c114919a3315a884fb592e33b037a50a4fe45cbd4fe2fc434ac")
    version("0.4-1", sha256="39c63f8e37b379033d73d57929b5b8ea41b0023626cc1cec648d66bade5d0103")
    version("0.3-3", sha256="a93e685ef9c40d5977bb91d7116505a25303b229897a20544722a94ea1365f30")
    version("0.3-1", sha256="e2e6f857b544dfecb482b99346aa3ecfdc27b4d401c3537ee8fbaf91caca92b9")
    version("0.1-24", sha256="f3dc9084450ea3da07e1ea5eeb097fd2fedc7e29e5d7794b418bcb438c4fcfa2")

    depends_on("r@2.2:", type=("build", "run"))
    depends_on("r-e1071", type=("build", "run"))
    depends_on("r-class", type=("build", "run"))
    depends_on("r-kernsmooth", type=("build", "run"))
