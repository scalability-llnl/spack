# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Paintor(MakefilePackage):
    """Probabilistic Annotation integrator. Fast, integrative fine mapping with functional
    data"""

    homepage = "https://github.com/gkichaev/PAINTOR_V3.0"
    url = "https://github.com/gkichaev/PAINTOR_V3.0/archive/refs/tags/3.0.tar.gz"

    version("3.0", sha256="cc39d3c334cc6d787e4f04847192c9d0185025a2ca46910bd38901b6679d198f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("nlopt")
    depends_on("eigen")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("CC = g\\+\\+", f"CC = {spack_cxx}")
        makefile.filter(
            r"(.*)-I/\$\(curr\)/eigen/Eigen(.*)",
            r"\1-I{}/eigen3/Eigen\2".format(spec["eigen"].prefix.include),
        )
        makefile.filter(r"(.*)-L/\$\{curr}/lib(.*)", r"\1-L{}\2".format(spec["nlopt"].prefix.lib))
        makefile.filter(
            r"(.*)-I/\${curr}/include(.*)", r"\1-I{}\2".format(spec["nlopt"].prefix.include)
        )

    @run_after("install")
    def mv_binary(self):
        mkdirp(self.prefix.bin)
        with working_dir(self.build_directory):
            install("PAINTOR", self.prefix.bin)
