# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Talass(CMakePackage):
    """TALASS: Topological Analysis of Large-Scale Simulations
    This package compiles the talass tool chain thar implements
    various topological algorithms to analyze large scale data.
    The package is organized hierarchical FileFormat < Statistics
    < StreamingTopology and any of the subsets can be build stand-
    alone."""

    homepage = "http://www.cedmav.org/research/topology/72-talass.html"
    git = "https://bitbucket.org/cedmav/talass.git"

    maintainers("lpottier")

    version("process-statistics", branch="process-statistics")
    version("2018-10-29", commit="5d459c0dd89e733fa301391908a5b79fe2850ad7")

    depends_on("cxx", type="build")  # generated

    # The default precision and index space sizes
    variant(
        "precision",
        default="32",
        values=("32", "64"),
        description="Precision of the function values",
    )
    variant(
        "global",
        default="32",
        values=("16", "32", "64"),
        description="Number of bits used for the global index space",
    )
    variant(
        "local",
        default="32",
        values=("16", "32", "64"),
        description="Number of bits used for the local index space",
    )

    root_cmakelists_dir = "StreamingTopology"

    def cmake_args(self):
        variants = self.spec.variants

        args = []

        if int(variants["local"].value) > int(variants["global"].value):
            msg = (
                "The global index space (%d bits) must be at least as "
                "large as the local index space (% bits)"
            )
            raise InstallError(msg % (variants["global"].value, variants["local"].value))

        if variants["precision"].value == "32":
            args.append("-DFUNCTION_TYPE=float")
        elif variants["precision"].value == "64":
            args.append("-DFUNCTION_TYPE=double")

        # Set global index space
        args.append("-DGLOBAL_INDEX_TYPE=uint{0}_t".format(variants["global"].value))

        # Set local index space
        args.append("-DLOCAL_INDEX_TYPE=uint{0}_t".format(variants["local"].value))

        # Deal with the PROJECT_INSTALL_PREFIX to enable Talass super builds
        args.append("-DPROJECT_INSTALL_PREFIX=%s" % self.prefix)

        return args
