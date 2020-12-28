# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sympol(CMakePackage):
    """SymPol is a C++ tool to work with symmetric polyhedra"""
    homepage = "http://www.math.uni-rostock.de/~rehn/software/sympol.html"
    url      = "http://www.math.uni-rostock.de/~rehn/software/sympol-0.1.8.tar.gz"

    version('0.1.8', sha256='8f4c013fa563e696fc8c27c408fd1f3d47783639815e8141e3a99826f1f3d54f')

    depends_on("cmake@2.6:", type="build")

    depends_on("bliss")
    depends_on("boost")
    depends_on("gmp")
    depends_on("lrslib")

    patch("lrs_mp_close.patch")
