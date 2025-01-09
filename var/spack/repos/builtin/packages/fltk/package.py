# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fltk(Package):
    """FLTK (pronounced "fulltick") is a cross-platform C++ GUI toolkit for
    UNIX/Linux (X11), Microsoft Windows, and MacOS X. FLTK provides
    modern GUI functionality without the bloat and supports 3D
    graphics via OpenGL and its built-in GLUT emulation.

    FLTK is designed to be small and modular enough to be statically
    linked, but works fine as a shared library. FLTK also includes an
    excellent UI builder called FLUID that can be used to create
    applications in minutes.

    """

    homepage = "https://www.fltk.org/"
    url = "https://fltk.org/pub/fltk/1.3.3/fltk-1.3.3-source.tar.gz"
    git = "https://github.com/fltk/fltk.git"

    version("master", branch="master")
    version("1.3.7", sha256="5d2ccb7ad94e595d3d97509c7a931554e059dd970b7b29e6fd84cb70fd5491c6")
    version("1.3.3", sha256="f8398d98d7221d40e77bc7b19e761adaf2f1ef8bb0c30eceb7beb4f2273d0d97")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libx11")

    patch("font.patch", when="@1.3.3")

    # https://github.com/fltk/fltk/commits/master/src/Fl_Tree_Item.cxx
    #  -Fix return value test, as pointed out by Albrecht.
    patch("fix_compare_val.patch", when="@:1.3.3")
    # https://github.com/fltk/fltk/commits/master/test/menubar.cxx
    # -Allow compilation with -std=c++11
    # -Add missing cast (part of patch for STR #2813).
    patch("type_cast.patch", when="@:1.3.3")

    variant("shared", default=True, description="Enables the build of shared libraries")

    variant("gl", default=True, description="Enables opengl support")

    variant("xft", default=False, description="Enables Anti-Aliased Fonts")

    # variant dependencies
    depends_on("gl", when="+gl")

    depends_on("libxft", when="+xft")

    def install(self, spec, prefix):
        options = [
            "--prefix=%s" % prefix,
            "--enable-localjpeg",
            "--enable-localpng",
            "--enable-localzlib",
        ]

        if spec.satisfies("+shared"):
            options.append("--enable-shared")

        if spec.satisfies("+xft"):
            # https://www.fltk.org/articles.php?L374+I0+TFAQ+P1+Q
            options.append("--enable-xft")
        else:
            options.append("--disable-xft")

        if spec.satisfies("~gl"):
            options.append("--disable-gl")

        # FLTK needs to be built in-source
        configure(*options)
        make()
        make("install")

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies("%nvhpc"):
            filter_file(
                'OPTIM="-Wall -Wunused -Wno-format-y2k $OPTIM"',
                'OPTIM="-Wall $OPTIM"',
                "configure",
                string=True,
            )
            filter_file('OPTIM="-Os $OPTIM"', 'OPTIM="-O2 $OPTIM"', "configure", string=True)
            filter_file(
                'CXXFLAGS="$CXXFLAGS -fvisibility=hidden"',
                'CXXFLAGS="$CXXFLAGS"',
                "configure",
                string=True,
            )
            filter_file(
                'OPTIM="$OPTIM -fvisibility=hidden"', 'OPTIM="$OPTIM"', "configure", string=True
            )
