# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcppprogress(RPackage):
    """An Interruptible Progress Bar with OpenMP Support for C++ in R Packages.

    Allows to display a progress bar in the R console for long running
    computations taking place in c++ code, and support for interrupting those
    computations even in multithreaded code, typically using OpenMP."""

    cran = "RcppProgress"

    version("0.4.2", sha256="b1624b21b7aeb1dafb30f092b2a4bef4c3504efd2d6b00b2cdf55dc9df194b48")
    version("0.4.1", sha256="11764105922f763d4c75c502599ec7dcc2fd629a029964caf53f98b41d0c607a")
    version("0.4", sha256="706e14360dbc5976db05c2ac6692c3279c0f8c95e72bf9d4becd9e1348025e3e")
    version("0.3", sha256="3de5dc47cc2f9e839f92355c463289531e8c13806e54c7438f63c7c34378261d")
    version("0.2.1", sha256="cf121d34766344d05dea77895cd2e48a977ebb28ccf7af14bb46c3744c4a50b5")
    version("0.2", sha256="ca32624739058f1b5aab18b09dc4c613ecfd18a3ace39f3b97790232db829481")
    version("0.1", sha256="04f71d3391b7dfab997afadf7ffdd87b88037f7fbc751bea544ad2a65e2872bf")

    depends_on("cxx", type="build")  # generated

    depends_on("r-rcpp@0.9.4:", type=("build", "run"), when="@:0.4.0")
