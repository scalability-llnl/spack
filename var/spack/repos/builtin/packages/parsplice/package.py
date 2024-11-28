# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
from spack.pkg.builtin.boost import Boost


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

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
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
