# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Sfcgal(CMakePackage):
    """
    SFCGAL is a C++ wrapper library around CGAL with the aim of supporting
    ISO 19107:2013 and OGC Simple Features Access 1.2 for 3D operations. SFCGAL
    provides standard compliant geometry types and operations, that can be
    accessed from its C or C++ APIs.
    """

    homepage = "http://www.sfcgal.org/"
    url      = "https://github.com/Oslandia/SFCGAL/archive/v1.3.7.tar.gz"

    version('1.3.7', sha256='30ea1af26cb2f572c628aae08dd1953d80a69d15e1cac225390904d91fce031b')

    # Ref: http://oslandia.github.io/SFCGAL/installation.html
    depends_on('cgal@4.3: +core')
    depends_on('boost@1.54.0:')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('mpfr@2.2.1:')
    depends_on('gmp@4.2:')

    def cmake_args(self):
        # It seems viewer is discontinued as of v1.3.0
        # https://github.com/Oslandia/SFCGAL/releases/tag/v1.3.0
        # Also, see https://github.com/Oslandia/SFCGAL-viewer
        return ['-DSFCGAL_BUILD_VIEWER=OFF']
