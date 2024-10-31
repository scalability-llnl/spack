# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Odgi(CMakePackage):
    """Optimized dynamic genome/graph implementation.
    Odgi provides an efficient and succinct dynamic DNA sequence graph model, as
    well as a host of algorithms that allow the use of such graphs in
    bioinformatic analyses.
    """

    homepage = "https://github.com/pangenome/odgi"
    git = "https://github.com/pangenome/odgi.git"

    # notify when the package is updated.
    maintainers("tbhaxor", "EbiArnie")

    # <<< Versions list starts here
    version("0.8.3", commit="34f006f31c3f6b35a1eb8d58a4edb1c458583de3", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    # >>> Versions list ends here

    # compilation problem with ninja
    generator("make", default="make")

    # the range is required to successfully build the program
    requires("%gcc", msg="Package odgi depends on the gcc C++ compiler")
    conflicts(
        "%gcc@:9.2,13:", msg="Unsupported compiler version. Recommended range is 9.3 -> 12.x"
    )

    # <<< Dependencies list starts here
    depends_on("python")
    depends_on("py-pybind11")
    depends_on("sdsl-lite")
    depends_on("libdivsufsort")
    depends_on("jemalloc")
    # >>> Dependencies list ends here

    def cmake_args(self):
        return ["-DCMAKE_CXX_STANDARD_REQUIRED:BOOL=ON"]
