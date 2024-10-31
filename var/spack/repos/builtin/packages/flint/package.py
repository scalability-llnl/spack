# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flint(AutotoolsPackage):
    """FLINT (Fast Library for Number Theory)."""

    homepage = "https://flintlib.org"
    url = "https://flintlib.org/flint-3.1.2.tar.gz"
    git = "https://github.com/flintlib/flint.git"
    list_url = "https://flintlib.org/downloads.html"
    list_depth = 0

    license("LGPL-2.1-or-later")

    version("main", branch="main")
    version("3.1.2", sha256="fdb3a431a37464834acff3bdc145f4fe8d0f951dd5327c4c6f93f4cbac5c2700")
    version("3.0.1", sha256="7b311a00503a863881eb8177dbeb84322f29399f3d7d72f3b1a4c9ba1d5794b4")
    version("2.5.2", sha256="cbf1fe0034533c53c5c41761017065f85207a1b770483e98b2392315f6575e87")
    version("2.4.5", sha256="e489354df00f0d84976ccdd0477028693977c87ccd14f3924a89f848bb0e01e3")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Overlap in functionality between gmp and mpir
    # All other dependencies must also be built with
    # one or the other
    # variant('mpir', default=False,
    #         description='Compile with the MPIR library')

    depends_on("gmp")  # mpir is a drop-in replacement for this
    depends_on("mpfr")  # Could also be built against mpir

    def configure_args(self):
        spec = self.spec
        return [f"--with-gmp={spec['gmp'].prefix}", f"--with-mpfr={spec['mpfr'].prefix}"]
