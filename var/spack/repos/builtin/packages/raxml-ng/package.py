# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RaxmlNg(CMakePackage):
    """RAxML-NG is a phylogenetic tree inference tool which uses
    maximum-likelihood (ML) optimality criterion.

    Its search heuristic is based on iteratively performing a series
    of Subtree Pruning and Regrafting (SPR) moves,
    which allows to quickly navigate to the best-known ML tree.
    RAxML-NG is a successor of RAxML (Stamatakis 2014) and leverages
    the highly optimized likelihood computation implemented in libpll
    (Flouri et al. 2014)."""

    homepage = "https://github.com/amkozlov/raxml-ng/wiki"
    url = "https://github.com/amkozlov/raxml-ng/archive/1.0.1.tar.gz"
    git = "https://github.com/amkozlov/raxml-ng.git"

    license("AGPL-3.0-only")

    version("1.1.0", submodules=True)
    version("1.0.2", submodules=True)
    version("1.0.1", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="Use MPI")

    depends_on("bison")
    depends_on("flex")
    depends_on("gmp")
    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        return [self.define_from_variant("USE_MPI", "mpi")]
