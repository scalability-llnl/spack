# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLobstr(RPackage):
    """Visualize R Data Structures with Trees.

    A set of tools for inspecting and understanding R data structures inspired
    by str(). Includes ast() for visualizing abstract syntax trees, ref() for
    showing shared references, cst() for showing call stack trees, and
    obj_size() for computing object sizes."""

    cran = "lobstr"

    license("MIT")

    version("1.1.2", sha256="9bc533ed7e8f816097a03acfbca33308c9940ba26d02674f4ba06311cf3a1718")
    version("1.1.1", sha256="b8c9ce00095bd4f304b4883ef71da24572022f0632a18c3e1ba317814e70716e")
    version("1.0.1", sha256="25fb288f73dbaf680ebbf27a50da338868c55d788501118fd33748854c5104fb")
    version("1.0.0", sha256="9d24de1519c51b3bac79066a1abf623b939e884ba5b3005110bb9c2016954b3d")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.2:", type=("build", "run"), when="@1.1.1:")
    depends_on("r-crayon", type=("build", "run"))
    depends_on("r-cpp11@0.4.2:", type=("build", "run"), when="@1.1.2:")
    depends_on("r-prettyunits", type=("build", "run"), when="@1.1.2:")
    depends_on("r-rlang@0.3.0:", type=("build", "run"))
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@1.1.2:")

    depends_on("r-rcpp", type=("build", "run"), when="@:1.1.1")
