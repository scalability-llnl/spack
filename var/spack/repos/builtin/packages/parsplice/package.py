# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Parsplice(CMakePackage):
    """ParSplice code implements the Parallel Trajectory Splicing algorithm"""

    homepage = "https://gitlab.com/exaalt/parsplice"
    url = (
        "https://gitlab.com/api/v4/projects/exaalt%2Fparsplice/repository/archive.tar.gz?sha=v1.1"
    )
    git = "https://gitlab.com/exaalt/parsplice.git"

    tags = ["ecp", "ecp-apps"]

    license("Unlicense")

    version("develop", branch="master")
    version("multisplice", branch="multisplice")
    version("1.1", sha256="a011c4d14f66e7cdbc151cc74b5d40dfeae19ceea033ef48185d8f3b1bc2f86b")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1:", type="build")
    depends_on("berkeley-db")
    depends_on("nauty")
    depends_on("boost cxxstd=11")
    depends_on("mpi")
    depends_on("eigen@3:")
    depends_on("lammps+lib@20170901:")
    depends_on("lammps+lib+exceptions", when="@multisplice")

    def cmake_args(self):
        spec = self.spec
        if spec.satisfies("@multisplice"):
            options = []
        else:
            options = ["-DBUILD_SHARED_LIBS=ON", "-DBoost_NO_BOOST_CMAKE=ON"]

        return options
