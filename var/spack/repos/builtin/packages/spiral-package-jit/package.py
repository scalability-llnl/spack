# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SpiralPackageJit(Package):
    """This is the SPIRAL package for Just-In-Time (JIT) or Real-Time
    Compilation (RTC)."""

    homepage = "https://spiralgen.com"
    url = "https://github.com/spiral-software/spiral-package-jit/archive/refs/tags/1.1.0.tar.gz"
    git = "https://github.com/spiral-software/spiral-package-jit.git"

    maintainers("spiralgen")
    # Although this package 'extends("spiral-software")' don't declare it as
    # such.  If this package is required spiral-software should be installed
    # with the +jit variant active

    license("BSD-2-Clause-FreeBSD")

    version("develop", branch="develop")
    version("main", branch="main")
    version("1.1.0", sha256="64cebf31b7a02fdcb3992a581c2fef67576f92bf893eaf88cd5ed1b1d853d550")
    version("1.0.3", sha256="97ff0d7d46ed4e53b1971ca279a30b27f0d9b328c70585d4cc0c56dfe6701894")
    version("1.0.2", sha256="d7fac0493ac406a8b1874491223c3a9a1c6727ea1aa39de7ef4694c59aac9d26")
    version("1.0.1", sha256="acf22db04e705276f06642d7f2ebf161f6c347f93bb1bdd6e3ddcfc4b7be5707")

    # JIT package is an extension for Spiral (spec: spiral-software).

    def install(self, spec, prefix):
        spiral_pkgs = join_path(prefix, "namespaces", "packages", "jit")
        install_tree(".", spiral_pkgs)
