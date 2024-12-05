# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRbgl(RPackage):
    """An interface to the BOOST graph library.

    A fairly extensive and comprehensive interface to the graph algorithms
    contained in the BOOST library."""

    bioc = "RBGL"

    license("BSL-1.0")

    version("1.76.0", commit="18b7cc5f002435aa83e8b693e7bf269fc0b096a5")
    version("1.74.0", commit="e698db897b719992a8c0747138735c0e7d9dfb21")
    version("1.72.0", commit="a86f3102f2795e1ffb530bb061247e3a42ca22f7")
    version("1.70.0", commit="9cfd5fdad4f1f438ff748317f32e822aede8921b")
    version("1.66.0", commit="bf0c111dbc231de6d3423c28e115b54fb010e1ea")
    version("1.60.0", commit="ef24c17c411659b8f030602bd9781c534d6ec93b")
    version("1.58.2", commit="086ad0c6bab7be29311b6ae14fd39df7a21331a6")
    version("1.56.0", commit="a1fa9d89c6a3401892c5dd1493df6a14031f0912")
    version("1.54.0", commit="e9c743d380e83c155495cb8732102f01f213c905")
    version("1.52.0", commit="93e8fcfafec8f1cd5638fe30dc0f9506d15b49c0")

    depends_on("cxx", type="build")  # generated

    depends_on("r-graph", type=("build", "run"))
    depends_on("r-bh", type=("build", "run"), when="@1.60.0:")
