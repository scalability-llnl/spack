# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lcc(CMakePackage):
    """Los Alamos Crystal Cut (LCC) is a simple crystal builder. It is an easy-to-use
    and easy-to-develop code to make crystal solid/shape and slabs from a crystal
    lattice. Provided you have a ‘.pdb‘ file containing your lattice basis you can
    create a solid or slab from command line."""

    homepage = "https://github.com/lanl/LCC.git"
    url = "https://github.com/lanl/LCC/archive/refs/tags/v1.0.1.tar.gz"
    git = "https://github.com/lanl/LCC.git"

    maintainers("cnegre")

    license("BSD-3-Clause")

    version("main", branch="main", preferred=True)
    version("1.0.1", sha256="fa13364dcdf3b1f8d80fc768f0e7ad3849f8d98091fb96926100a6764f836020")
    version("1.0.0", sha256="750ce09e809a4e85ae3219fd537dc84a923fe3d3683b26b5d915eccfd1f0120c")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=False, description="Build shared libs")

    depends_on("cmake@3.10:", type="build")
    depends_on("bml")
    depends_on("qmd-progress")

    root_cmakelists_dir = "src"

    def cmake_args(self):
        args = [
            "-DCMAKE_Fortran_FLAGS=-ffree-line-length-none",
            "-DCMAKE_Fortran_FLAGS=-g -fopenmp",
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]
        return args
