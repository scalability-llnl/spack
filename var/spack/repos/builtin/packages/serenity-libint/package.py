# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SerenityLibint(CMakePackage):
    """Serenity fork of libint, which is difficult to reproduce from libint itself"""

    url = "https://www.uni-muenster.de/Chemie.oc/THCLAB/libint/libint-2.7.0-beta.6.tgz"

    license("LGPL-3.0-or-later")

    version(
        "2.7.0-beta.6", sha256="53af60c7be74374b2a2d893b3d2d37fa6a3078a72d98067bf71ba4ede4e807df"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("boost")
    depends_on("eigen@3:")  # Probably overdepending?
    depends_on("gmp+cxx")

    def cmake_args(self):
        args = [self.define("BUILD_SHARED_LIBS", True)]
        return args
