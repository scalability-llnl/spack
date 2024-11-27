# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flap(CMakePackage):
    """Fortran command Line Arguments Parser"""

    homepage = "https://github.com/szaghi/FLAP"
    url = "https://github.com/szaghi/FLAP.git"
    git = "https://github.com/szaghi/FLAP.git"

    maintainers("fluidnumerics-joe")

    license("GPL-3.0-only")

    version("master", branch="master", submodules=True)

    depends_on("fortran", type="build")  # generated

    def flag_handler(self, name, flags):
        if name in ["cflags", "cxxflags", "cppflags"]:
            return (None, flags, None)
        elif name == "fflags":
            flags.append("-cpp")
        return (flags, None, None)
