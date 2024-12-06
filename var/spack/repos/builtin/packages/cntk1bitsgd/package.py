# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import listdir

from spack.package import *


class Cntk1bitsgd(Package):
    """CNTK1bitSGD is the header-only
    1-bit stochastic gradient descent (1bit-SGD) library for
    the Computational Network Toolkit (CNTK)."""

    homepage = "https://github.com/CNTK-components/CNTK1bitSGD"
    git = "https://github.com/CNTK-components/CNTK1bitSGD.git"

    version("master")
    version("c8b77d", commit="c8b77d6e325a4786547b27624890276c1483aed1")

    def install(self, spec, prefix):
        mkdirp(prefix.include)
        for file in listdir("."):
            if file.endswith(".h"):
                install(file, prefix.include)
