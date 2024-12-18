# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.build_systems import makefile
from spack.package import *


class Fpocket(MakefilePackage):
    """The fpocket suite of programs is a very fast open source
    protein pocket detection algorithm based on Voronoi tessellation."""

    homepage = "https://github.com/Discngine/fpocket"
    url = "https://github.com/Discngine/fpocket/archive/refs/tags/4.1.tar.gz"

    license("MIT")

    version("4.2", sha256="8aea4ccdf4243606110c8f6978b13dd90f9cae092660eca4c6970206011de4aa")
    version("4.1", sha256="1a2af2d3f2df42de67301996db3b93c7eaff0375f866443c0468dcf4b1750688")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("netcdf-c")
    depends_on("netcdf-cxx")
    depends_on("qhull")


class MakefileBuilder(makefile.MakefileBuilder):
    def setup_build_environment(self, env):
        if self.pkg.compiler.name == "gcc":
            env.set("CXX", "g++")

    def edit(self, pkg, spec, prefix):
        mkdirp(prefix.lib)
        makefile = FileFilter("makefile")
        makefile.filter("BINDIR .*", f"BINDIR = {prefix}/bin")
        makefile.filter("MANDIR .*", f"MANDIR = {prefix}/man/man8")
        makefile.filter("LIBDIR .*", f"LIBDIR = {prefix}/lib")
