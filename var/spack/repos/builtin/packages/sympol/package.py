# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
from spack.pkg.builtin.boost import Boost


class Sympol(CMakePackage):
    """SymPol is a C++ tool to work with symmetric polyhedra"""
    homepage = "http://www.math.uni-rostock.de/~rehn/software/sympol.html"
    url      = "http://www.math.uni-rostock.de/~rehn/software/sympol-0.1.8.tar.gz"

    version('0.1.8', sha256='8f4c013fa563e696fc8c27c408fd1f3d47783639815e8141e3a99826f1f3d54f')

    depends_on("cmake@2.6:", type="build")

    depends_on("bliss")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("gmp")
    depends_on("lrslib")

    patch("lrs_mp_close.patch")
