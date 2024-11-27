# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gbl(CMakePackage):
    """General Broken Lines: Advanced track fitting library"""

    homepage = "https://www.desy.de/~kleinwrt/GBL/doc/cpp/html/"
    git = "https://gitlab.desy.de/claus.kleinwort/general-broken-lines.git"

    tags = ["hep"]

    version("V02-04-01", commit="1061b643c6656fbf7ceba579997eb43f0a9e9d3c")
    version("V02-01-03", commit="8acaade19c20e9ef23d1244a555fead6ef149c33")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("root", default=True, description="Support ROOT for user I/O")
    depends_on("eigen", type=("build", "link"))
    depends_on("root", type=("build", "link"), when="+root")

    root_cmakelists_dir = "cpp"

    def cmake_args(self):
        eigen_inc = self.spec["eigen"].prefix.include.eigen3
        args = [
            self.define("EIGEN3_INCLUDE_DIR", eigen_inc),
            self.define_from_variant("SUPPORT_ROOT", "root"),
        ]
        return args
