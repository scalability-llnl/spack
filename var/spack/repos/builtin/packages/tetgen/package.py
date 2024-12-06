# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import glob

from spack.package import *


class Tetgen(Package):
    """TetGen is a program and library that can be used to generate
    tetrahedral meshes for given 3D polyhedral domains. TetGen
    generates exact constrained Delaunay tetrahedralizations,
    boundary conforming Delaunay meshes, and Voronoi paritions.
    """

    homepage = "https://wias-berlin.de/software/tetgen/"

    license("AGPL-3.0-only")

    version(
        "1.6.0",
        sha256="87b5e61ebd3a471fc4f2cdd7124c2b11dd6639f4feb1f941a5d2f5110d05ce39",
        url="http://www.tetgen.org/1.5/src/tetgen1.6.0.tar.gz",
    )
    version(
        "1.5.1",
        sha256="e46a4434a3e7c00044c8f4f167e18b6f4a85be7d22838c8f948ce8cc8c01b850",
        url="http://www.tetgen.org/1.5/src/tetgen1.5.1.tar.gz",
        preferred=True,
    )
    version(
        "1.5.0",
        sha256="4d114861d5ef2063afd06ef38885ec46822e90e7b4ea38c864f76493451f9cf3",
        url="http://www.tetgen.org/1.5/src/tetgen1.5.0.tar.gz",
    )
    version(
        "1.4.3",
        sha256="952711bb06b7f64fd855eb24c33f08e3faf40bdd54764de10bbe5ed5b0dce034",
        url="http://www.tetgen.org/files/tetgen1.4.3.tar.gz",
    )

    depends_on("cxx", type="build")  # generated

    variant("pic", default=True, description="Builds the library in pic mode.")
    variant("debug", default=False, description="Builds the library in debug mode.")
    variant(
        "except",
        default=False,
        description="Replaces asserts with exceptions for better C++ compatibility.",
        when="@:1.5.0",
    )

    patch("tetgen-1.5.0-free.patch", when="@1.5.0")

    def patch(self):
        cflags = "-g -O0" if "+debug" in self.spec else "-g0 -O3"
        cflags = cflags + " -fPIC" if "+pic" in self.spec else cflags
        predcflags = "-fPIC" if "+pic" in self.spec else ""

        mff = FileFilter("makefile")
        mff.filter(r"^(C(XX)?FLAGS\s*=)(.*)$", r"\1 {0}".format(cflags))
        mff.filter(r"^(PREDC(XX)?FLAGS\s*=.*)$", r"\1 {0}".format(predcflags))

        if "+except" in self.spec:
            hff = FileFilter("tetgen.h")
            hff.filter(r"(\b)(throw)(\b)(.*);", r"\1assert_throw(false);")
            hff.filter(
                r"^(#define\s*tetgenH\s*)$",
                r"\1{0}".format(
                    """\n
#include <stdexcept>

inline void assert_throw(bool assertion)
{
  if(!assertion)
    throw std::runtime_error("Tetgen encountered a problem (assert failed)!");
}\n"""
                ),
            )

            sff = FileFilter(*(glob.glob("*.cxx")))
            sff.filter(r"(\b)(assert)(\b)", r"\1assert_throw\3")

    def install(self, spec, prefix):
        make("tetgen", "tetlib")

        mkdirp(prefix.bin)
        install("tetgen", prefix.bin)

        mkdirp(prefix.include)
        install("tetgen.h", prefix.include)

        mkdirp(prefix.lib)
        install("libtet.a", prefix.lib)
