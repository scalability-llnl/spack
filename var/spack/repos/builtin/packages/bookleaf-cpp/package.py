# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BookleafCpp(CMakePackage):
    """BookLeaf is a 2D unstructured hydrodynamics mini-app."""

    homepage = "https://github.com/UK-MAC/BookLeaf_Cpp"
    url = "https://github.com/UK-MAC/BookLeaf_Cpp/archive/v2.0.tar.gz"
    git = "https://github.com/UK-MAC/BookLeaf_Cpp.git"

    license("GPL-3.0-or-later")

    version("develop", branch="develop")

    version("2.0.2", sha256="787ade5045415d71d9bad55fe9f93598f3a0548d13e2ff80e752cc99f62fe6d3")
    version("2.0.1", sha256="1286f916f59d1f3bf325041854e8c203894e293c5e26d5b19b9362ee02082983")
    version("2.0", sha256="3c14344c31385bec9e089f9babf815566c4fcf98a47822f663afa2cefb0e90e1")

    depends_on("cxx", type="build")  # generated

    variant("typhon", default=True, description="Use Typhon")
    variant("parmetis", default=False, description="Use ParMETIS")
    variant("silo", default=False, description="Use Silo")
    variant("caliper", default=False, description="Use Caliper")

    depends_on("caliper", when="+caliper")
    depends_on("parmetis", when="+parmetis")
    depends_on("silo", when="+silo")
    depends_on("typhon", when="+typhon")
    depends_on("mpi", when="+typhon")
    depends_on("yaml-cpp@0.6.0:")

    def cmake_args(self):
        spec = self.spec
        cmake_args = []

        if spec.satisfies("+typhon"):
            cmake_args.append("-DENABLE_TYPHON=ON")

        if spec.satisfies("+parmetis"):
            cmake_args.append("-DENABLE_PARMETIS=ON")

        if spec.satisfies("+silo"):
            cmake_args.append("-DENABLE_SILO=ON")

        if spec.satisfies("+caliper"):
            cmake_args.append("-DENABLE_CALIPER=ON")

        return cmake_args
