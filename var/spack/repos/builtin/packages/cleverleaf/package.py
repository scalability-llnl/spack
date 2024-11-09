# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Cleverleaf(CMakePackage):
    """CleverLeaf is a hydrodynamics mini-app that extends CloverLeaf with
    Adaptive Mesh Refinement using the SAMRAI toolkit from Lawrence
    Livermore National Laboratory. The primary goal of CleverLeaf is
    to evaluate the application of AMR to the Lagrangian-Eulerian
    hydrodynamics scheme used by CloverLeaf.
    """

    homepage = "https://uk-mac.github.io/CleverLeaf/"
    git = "https://github.com/UK-MAC/CleverLeaf_ref.git"

    license("LGPL-3.0-or-later")

    version("develop", branch="develop")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("samrai@3.8.0:")
    depends_on("hdf5+mpi")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("cmake@3.1:", type="build")

    # The Fujitsu compiler requires the '--linkfortran'
    # option to combine C++ and Fortran programs.
    patch("fujitsu_add_link_flags.patch", when="%fj")

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%intel") and name in ["cppflags", "cxxflags"]:
            flags.append(self.compiler.cxx11_flag)

        return (None, None, flags)
