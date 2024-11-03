# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Parmmg(CMakePackage):
    """ParMMG is a parallel remesher based on MMG"""

    homepage = "https://www.mmgtools.org"
    url = "https://github.com/MmgTools/ParMmg/archive/refs/tags/v1.3.0.tar.gz"
    git = "https://github.com/MmgTools/ParMmg.git"

    maintainers("corentin-dev")

    license("LGPL-3.0-or-later")

    version("master", branch="master")
    version("1.5.0", sha256="0baec7914e49a26bdbb849ab64dcd92147eff79ac02ef3b2599cb05104901a7a")
    version("1.4.0", sha256="d8053bce9e1cd66077ad8cb86a5a874f47d0d0d2216e4eee4b98990355a0ea7f")
    version("1.3.0", sha256="d43b73a73b62545b5a31bbe25562f69c9e63ad8a6d416bd459781203e37427cf")
    version("1.2.0", sha256="99729cc292dcb59c87e3f25d4cabf5a64841e83b624d383e1fd3fb7f960df672")
    version("1.1.0", sha256="a5904f1f56b7809ab9ec2f6118b03a082ec2b5564355a73c74fc55426cc69600")
    version("1.0.0", sha256="614feb815ff6cdfc9bced30e8105994f0bf3a812243619d3349203ec1851cf6d")

    patch("parmmg_cmake_patch.diff")

    variant("vtk", default=False, description="Build with VTK support")
    variant("shared", default=True, description="Build shared libraries")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    
    depends_on("mmg@5.8: +private")
    depends_on("metis")
    depends_on("vtk", when="+vtk")
    depends_on("mpi")

    variant("pic", default=True, description="Build with position independent code")

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("DOWNLOAD_MMG", False),
            self.define("MMG_DIR", self.spec["mmg"].prefix),
            self.define("DOWNLOAD_METIS", False),
            self.define("METIS_DIR", self.spec["metis"].prefix),
            self.define("MMG_INCLUDE_DIRS", self.spec["mmg"].headers.directories),
            self.define_from_variant("USE_VTK", "vtk"),
        ]

        return args
