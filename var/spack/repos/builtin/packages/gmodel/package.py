# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gmodel(CMakePackage):
    """Gmsh model generation library

    Gmodel is a C++11 library that implements a minimal CAD kernel based
    on the .geo format used by the Gmsh mesh generation code, and is
    designed to make it easier for users to quickly construct CAD models
    for Gmsh.
    """

    homepage = "https://github.com/ibaned/gmodel"
    url = "https://github.com/ibaned/gmodel/archive/v2.1.0.tar.gz"

    license("BSD-2-Clause-FreeBSD")

    version("2.1.0", sha256="80df0c6dc413a9ffa0f0e7b65118b05b643ba3e1bfcac28fb91d2d3ad017fda0")

    depends_on("cxx", type="build")  # generated

    # fix error [-Werror,-Wzero-as-null-pointer-constant]
    # fix error [-Werror,-Wunused-template]
    # Ref: https://github.com/ibaned/gmodel/commit/6b81ec190cf2ce9a6554a99cb6d759b023393cdd
    patch("fix_gmodel.cpp.patch")
