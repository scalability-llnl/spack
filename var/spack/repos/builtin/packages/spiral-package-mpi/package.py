# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpiralPackageMpi(Package):
    """This is the SPIRAL package for MPI."""

    homepage = "https://spiralgen.com"
    url = "https://github.com/spiral-software/spiral-package-mpi/archive/refs/tags/1.1.0.tar.gz"
    git = "https://github.com/spiral-software/spiral-package-mpi.git"

    maintainers("spiralgen")
    # Although this package 'extends("spiral-software")' don't declare it as
    # such.  If this package is required spiral-software should be installed
    # with the +mpi variant active

    license("BSD-2-Clause-FreeBSD")

    version("develop", branch="develop")
    version("main", branch="main")
    version("1.1.0", sha256="baf3c9dac7fee330e4bb4adbd24cc7e55f27fc27417644c0b216124f9052f1f5")
    version("1.0.0", sha256="64896a82aacce9cc8abe88b921e09ba7a5fceb8262e490f60a7088583c2c2151")

    # MPI package is an extension for Spiral (spec: spiral-software).

    def install(self, spec, prefix):
        spiral_pkgs = join_path(prefix, "namespaces", "packages", "mpi")
        install_tree(".", spiral_pkgs)
