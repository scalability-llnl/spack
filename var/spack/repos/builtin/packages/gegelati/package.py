# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install gegelati
#
# You can edit this file again by typing:
#
#     spack edit gegelati
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Gegelati(CMakePackage):
    """Class to add the a TPG library(gegelati) into Spack"""

    homepage = "https://github.com/gegelati/gegelati"
    url = "https://github.com/gegelati/gegelati/archive/refs/tags/v1.2.0.tar.gz"

    # notify when the package is updated.
    maintainers = ["lucascarvalhoroncoroni"]

    version("1.2.0", sha256="039997c7d6cb394f910f6c40620165b32094e0c85c170be01eb74b55488a1d4c")

    depends_on("sdl2")
    depends_on("doxygen")

    def cmake_args(self):
        args = []
        return args
