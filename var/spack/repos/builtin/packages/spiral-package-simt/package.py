# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpiralPackageSimt(Package):
    """This is the SPIRAL package for SIMT:  SIMT, single instruction multiple
    threads, is used to generate code for GPUs and multi-threading aplications."""

    homepage = "https://spiralgen.com"
    url = "https://github.com/spiral-software/spiral-package-simt/archive/refs/tags/1.1.0.tar.gz"
    git = "https://github.com/spiral-software/spiral-package-simt.git"

    maintainers("spiralgen")
    # Although this package 'extends("spiral-software")' don't declare it as
    # such.  If this package is required spiral-software should be installed
    # with the +simt variant active

    license("BSD-2-Clause-FreeBSD")

    version("develop", branch="develop")
    version("main", branch="main")
    version("1.1.0", sha256="4d6a5e586889b9e000968c99f3068ba86a12cc389665c6deadc4734117ef7a95")
    version("1.0.0", sha256="888ca01aa8fd5df80d6ae1bd64eb1b1e70240b6a36bc3437eb48f5a4b59c2d07")

    # SIMT package is an extension for Spiral (spec: spiral-software).

    def install(self, spec, prefix):
        spiral_pkgs = join_path(prefix, "namespaces", "packages", "simt")
        install_tree(".", spiral_pkgs)
