# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.boost import Boost


class Sympol(CMakePackage):
    """SymPol is a C++ tool to work with symmetric polyhedra"""

    homepage = "https://www.math.uni-rostock.de/~rehn/software/sympol.html"
    url = "https://www.math.uni-rostock.de/~rehn/software/sympol-0.1.8.tar.gz"

    license("GPL-2.0-only")

    version("0.1.8", sha256="8f4c013fa563e696fc8c27c408fd1f3d47783639815e8141e3a99826f1f3d54f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.6:", type="build")

    depends_on("bliss")
    depends_on("boost+math+program_options+test")
    depends_on(Boost.with_default_variants)
    depends_on("gmp")
    depends_on("lrslib")

    patch("lrs_mp_close.patch")
