# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Liblbfgs(AutotoolsPackage):
    """libLBFGS is a C port of the implementation of Limited-memory
    Broyden-Fletcher-Goldfarb-Shanno (L-BFGS) method written by Jorge Nocedal.

    The L-BFGS method solves the unconstrainted minimization problem:
        minimize F(x), x = (x1, x2, ..., xN),
    only if the objective function F(x) and its gradient G(x) are computable."""

    homepage = "https://www.chokkan.org/software/liblbfgs/"
    url = "https://github.com/downloads/chokkan/liblbfgs/liblbfgs-1.10.tar.gz"
    git = "https://github.com/chokkan/liblbfgs.git"

    maintainers("RemiLacroix-IDRIS")

    license("MIT")

    version("master", branch="master")
    version("1.10", sha256="4158ab7402b573e5c69d5f6b03c973047a91e16ca5737d3347e3af9c906868cf")

    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")
    depends_on("m4", type="build", when="@master")
