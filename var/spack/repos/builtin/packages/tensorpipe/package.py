# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tensorpipe(CMakePackage):
    """A tensor-aware point-to-point communication primitive for machine learning."""

    homepage = "https://github.com/pytorch/tensorpipe"
    git = "https://github.com/pytorch/tensorpipe.git"

    license("BSD-3-Clause")

    version("master", branch="master", submodules=True)
    version(
        "2021-05-13", commit="05e4c890d4bd5f8ac9a4ba8f3c21e2eba3f66eda", submodules=True
    )  # py-torch@1.9
    version(
        "2021-03-04", commit="369e855ea82fc71f45cfab277863b86747202c92", submodules=True
    )  # py-torch@1.8.1
    version(
        "2021-02-09", commit="05467ba9bc164f06722986b615c4495901747c58", submodules=True
    )  # py-torch@1.8.0
    version(
        "2020-09-28", commit="95ff9319161fcdb3c674d2bb63fac3e94095b343", submodules=True
    )  # py-torch@1.7
    version(
        "2020-06-26", commit="3b8089c9c6717038cff44b70b881d0ad6c93e679", submodules=True
    )  # py-torch@1.6

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    generator("ninja")
    depends_on("cmake@3.5:", type="build")
    depends_on("libuv@1.26:")
